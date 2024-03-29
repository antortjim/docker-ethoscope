from threading import Thread
import urllib.request, urllib.error, urllib.parse
import os
import datetime
import json
import time
import logging
import traceback
from functools import wraps
import socket
from zeroconf import ServiceBrowser, Zeroconf


class ScanException(Exception):
    pass


def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry
    """
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)
        return f_retry
    return deco_retry


class Sensor(Thread):
    """
    """
    def __init__(self, ip, refresh_period = 5, port = 80, results_dir = ""):

        self._ip = ip
        self._port = port
        self._data_url = "http://%s:%i/" % (ip, port)
        self._id_url = "http://%s:%i/id" % (ip, port)
        self._post_url = "http://%s:%i/set" % (ip, port)

        self._info = {"status": "offline"}
        self._id = ""
        self._reset_info()

        self._is_online = True
        self._skip_scanning = False
        self._refresh_period = refresh_period
        self._update_info()
        super(Sensor,self).__init__()


    def run(self):
        '''
        while the device is active (i.e. online and communicating)
        interrogates periodically on the status and info
        '''
        
        last_refresh = 0
        while self._is_online:
            time.sleep(.2)
            if time.time() - last_refresh > self._refresh_period:

                if not self._skip_scanning:
                    self._update_info()
                else:
                    self._reset_info()
                last_refresh = time.time()

    def _update_id(self):
        """
        """
        if self._skip_scanning:
            raise ScanException("Not scanning this ip (%s)." % self._ip)

        old_id = self._id
        resp = self._get_json(self._id_url)
        self._id = resp['id']
        if self._id != old_id:
            if old_id:
                logging.warning("Device id changed at %s. %s ===> %s" % (self._ip, old_id, self._id))
            self._reset_info()

        self._info["ip"] = self._ip
        self._id = resp['id']

    def set(self, data):
        """
        Set remote variables 
        data is a dict
        set key to value
        Value can be char[20]
        """
        args = urllib.parse.urlencode(data).encode("utf-8")
        self._get_json(self._post_url, 3, args)

    @retry(ScanException, tries=3, delay=1, backoff=1)
    def _get_json(self, url,timeout=5, post_data=None):

        try:
            req = urllib.request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})
            f = urllib.request.urlopen(req, timeout=timeout)
            message = f.read()
            if not message:
                # logging.error("URL error whist scanning url: %s. No message back." % self._id_url)
                raise ScanException("No message back")
            try:
                resp = json.loads(message)
                return resp
            except ValueError:
                # logging.error("Could not parse response from %s as JSON object" % self._id_url)
                raise ScanException("Could not parse Json object")
        
        except urllib.error.HTTPError as e:
            raise ScanException("Error" + str(e.code))
            #return e
        
        except urllib.error.URLError as e:
            raise ScanException("Error" + str(e.reason))
            #return e
        
        except Exception as e:
            raise ScanException("Unexpected error" + str(e))

    def _reset_info(self):
        '''
        This is called whenever the device goes offline
        '''
        self._info['status'] = "offline"
        self._info['ip'] = "offline"

    def _update_info(self):
        '''
        '''
        try:
            self._update_id()
        except ScanException:
            self._reset_info()
            return
        
        try:
            resp = self._get_json(self._data_url)
            self._info.update(resp)
            self._info['status'] = 'online'
        except ScanException:
            pass

    def ip(self):
        return self._ip
        
    def id(self):
        return self._id
        
    def info(self):
        return self._info

class Device(Thread):
    _ethoscope_db_credentials = {"user": "ethoscope",
                                "passwd": "ethoscope",
                                "db":"ethoscope_db"}

    _remote_pages = {
            'id' : "id",
            'videofiles' :  "data/listfiles/video",
            'stream' : "stream.mjpg",
            'user_options' : "user_options",
            'log' : "data/log",
            'static' : "static",
            'controls' : "controls",
            'machine_info' : "machine",
            'update' : "update"
            }
    
    _allowed_instructions_status = { "stream": ["stopped"],
                                     "start": ["stopped"],
                                     "start_record": ["stopped"],
                                     "stop": ["streaming", "running", "recording"],
                                     "poweroff": ["stopped"],
                                     "reboot" : ["stopped"],
                                     "offline": []}

    def __init__(self, ip, refresh_period = 2, port = 9000, results_dir = "/ethoscope_data/results"):
        '''
        Initialises the info gathering and controlling activity of a Device by the node
        The server will interrogate the status of the device with frequency of refresh_period
        '''
        
        self._results_dir = results_dir
        self._ip = ip
        self._port = port
        self._id_url = "http://%s:%i/%s" % (ip, port, self._remote_pages['id'])

        self._info = {"status": "offline"}
        self._id = ""
        self._reset_info()

        self._is_online = True
        self._skip_scanning = False
        self._refresh_period = refresh_period
        
        self._update_info()
        super(Device,self).__init__()

    def run(self):
        '''
        while the device is active (i.e. online and communicating)
        interrogates periodically on the status and info
        '''
        
        last_refresh = 0
        while self._is_online:
            time.sleep(.2)
            if time.time() - last_refresh > self._refresh_period:

                if not self._skip_scanning:
                    self._update_info()
                else:
                    self._reset_info()
                last_refresh = time.time()

    def send_instruction(self,instruction,post_data):
        post_url = "http://%s:%i/%s/%s/%s" % (self._ip, self._port, self._remote_pages['controls'], self._id, instruction)
        self._check_instructions_status(instruction)

        # we do not expect any data back when device is powered off.
        if instruction == "poweroff" or instruction == "reboot":
            try:
                self._get_json(post_url, 3, post_data)
            except ScanException:
                pass

        else:
            self._get_json(post_url, 3, post_data)
            
        self._update_info()
        
    def send_settings(self, post_data):
        post_url = "http://%s:%i/%s/%s" % (self._ip, self._port, self._remote_pages['update'], self._id)
        self._get_json(post_url, 3, post_data)
        self._update_info()

    def _check_instructions_status(self, instruction):
        self._update_info()
        status = self._info["status"]

        try:
            allowed_inst = self._allowed_instructions_status[instruction]
        except KeyError:
            raise KeyError("Instruction %s is not allowed" % instruction)

        if status not in allowed_inst:
            raise Exception("You cannot send the instruction '%s' to a device in status %s" %(instruction, status))

    def ip(self):
        return self._ip
        
    def id(self):
        return self._id
        
    def info(self):
        return self._info

    def machine_info(self):
        '''
        Retrieves private machine info from the ethoscope
        This is used to check if the ethoscope is a new installation
        '''
        machine_info_url = "http://%s:%i/%s/%s" % (self._ip, self._port, self._remote_pages['machine_info'], self._id)
        out = self._get_json(machine_info_url)
        return out
        

    def skip_scanning(self, value):
        self._skip_scanning = value

    def videofiles(self):
        '''
        Return a list of file videos available on the ethoscope or virtuascope
        '''
        videofiles_url = "http://%s:%i/%s/%s" % (self._ip, self._port, self._remote_page['videofiles'], self._id)
        out = self._get_json(videofiles_url)
        return out

    def relay_stream(self):
        '''
        The node uses this function to relay the stream of images from the device to the node client
        '''
        stream_url = "http://%s:%i/%s" % (self._ip, 8008, self._remote_pages['stream'])
        #stream_url = "http://217.7.233.140:80/cgi-bin/faststream.jpg?stream=full&fps=0"

        req = urllib.request.Request(stream_url)
        stream = urllib.request.urlopen(req, timeout=5)
        bytes = b''
        while True:
            bytes += stream.read(1024)
            a = bytes.find(b'\xff\xd8') #frame starting 
            b = bytes.find(b'\xff\xd9') #frame ending
            if a != -1 and b != -1:
                frame = bytes[a:b+2]
                bytes = bytes[b+2:]
                yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def user_options(self):
        user_options_url= "http://%s:%i/%s/%s" % (self._ip, self._port, self._remote_pages['user_options'], self._id)
        out = self._get_json(user_options_url)
        return out

    def get_log(self):
        log_url = "http://%s:%i/%s/%s" % (self._ip, self._port, self._remote_pages['log'], self._id)
        out = self._get_json(log_url)
        return out

    def last_image(self):
        """
        Collects the last drawn image fromt the device
        TODO: on the device side, this should not rely on an actuale image file but be fished from memory
        """
        # we return none if the device is not in a stoppable status (e.g. running, recording)
        if self._info["status"] not in self._allowed_instructions_status["stop"]:
            return None
        try:
            img_path = self._info["last_drawn_img"]
        except KeyError:
            raise KeyError("Cannot find last image for device %s" % self._id)

        img_url = "http://%s:%i/%s/%s" % (self._ip, self._port, self._remote_pages['static'], img_path)
        try:
            return urllib.request.urlopen(img_url,timeout=5)
        except  urllib.error.HTTPError:
            logging.error("Could not get image for ip = %s (id = %s)" % (self._ip, self._id))
            raise Exception("Could not get image for ip = %s (id = %s)" % (self._ip, self._id))

    def dbg_img(self):
        try:
            img_path = self._info["dbg_img"]
        except KeyError:
            raise KeyError("Cannot find dbg img path for device %s" % self._id)

        img_url = "http://%s:%i/%s/%s" % (self._ip, self._port, self._remote_pages['static'], img_path)
        try:
            file_like = urllib.request.urlopen(img_url)
            return file_like
        except Exception as e:
            logging.warning(traceback.format_exc())

    @retry(ScanException, tries=3, delay=1, backoff=1)
    def _get_json(self, url,timeout=5, post_data=None):

        try:
            req = urllib.request.Request(url, data=post_data, headers={'Content-Type': 'application/json'})            
            f = urllib.request.urlopen(req, timeout=timeout)
            message = f.read()
            if not message:
                # logging.error("URL error whist scanning url: %s. No message back." % self._id_url)
                raise ScanException("No message back")
            try:
                resp = json.loads(message)
                return resp
            except ValueError:
                # logging.error("Could not parse response from %s as JSON object" % self._id_url)
                raise ScanException("Could not parse Json object")
        
        except urllib.error.HTTPError as e:
            raise ScanException("Error" + str(e.code))
            #return e
        
        except urllib.error.URLError as e:
            raise ScanException("Error" + str(e.reason))
            #return e
        
        except Exception as e:
            raise ScanException("Unexpected error" + str(e))

        

    def _update_id(self):
        """
        """
        if self._skip_scanning:
            raise ScanException("Not scanning this ip (%s)." % self._ip)

        old_id = self._id
        resp = self._get_json(self._id_url)
        self._id = resp['id']
        if self._id != old_id:
            if old_id:
                logging.warning("Device id changed at %s. %s ===> %s" % (self._ip, old_id, self._id))
            self._reset_info()

        self._info["ip"] = self._ip
        self._id = resp['id']


    def _reset_info(self):
        '''
        This is called whenever the device goes offline
        '''
        self._info['status'] = "offline"
        self._info['ip'] = "offline"

    def _update_info(self):
        '''
        '''
        try:
            self._update_id()
        except ScanException:
            self._reset_info()
            return
        
        try:
            data_url = "http://%s:%i/data/%s" % (self._ip, self._port, self._id)
            resp = self._get_json(data_url)
            self._info.update(resp)
            resp = self._make_backup_path()
            self._info.update(resp)
        except ScanException:
            pass


    def _make_backup_path(self,  timeout=30):
        try:
            import mysql.connector
            device_id = self._info["id"]
            device_name = self._info["name"]
            com = "SELECT value from METADATA WHERE field = 'date_time'"

            docker_container = os.environ.get("DOCKER_CONTAINER", False)
            if docker_container:
                ip = "mysqld"
            else:
                ip = self._ip

            mysql_db = mysql.connector.connect(host = ip,
                                               connect_timeout=timeout,
                                               **self._ethoscope_db_credentials,
                                               buffered=True)
            cur = mysql_db.cursor()
            cur.execute(com)
            query = [c for c in cur]
            timestamp = float(query[0][0])
            mysql_db.close()
            date_time = datetime.datetime.fromtimestamp(timestamp)
            formatted_time = date_time.strftime('%Y-%m-%d_%H-%M-%S')
            file_name = "%s_%s.db" % (formatted_time, device_id)
            output_db_file = os.path.join(self._results_dir,
                                          device_id,
                                          device_name,
                                          formatted_time,
                                          file_name
                                          )

        except Exception as e:
            logging.error("Could not generate backup path for device. Probably a MySQL issue")
            logging.error(traceback.format_exc())
            return {"backup_path": "None"}

        return {"backup_path": output_db_file}

    def stop(self):
        self._is_online = False


class DeviceScanner(object):
    """
    Uses zeroconf (aka Bonjour, aka Avahi etc) to passively listen for ethoscope devices registering themselves on the network.
    From: https://github.com/jstasiak/python-zeroconf
    """
    #avahi requires .local but some routers may have .lan
    #TODO: check if this is going to be a problem
    
    _suffix = ".local" 
    _service_type = "_ethoscope._tcp.local." 
    
    def __init__(self, device_refresh_period = 5, results_dir="/ethoscope_data/results", deviceClass=Device):
        # Zero-configuration networking (zeroconf) is a set of technologies that automatically
        # creates a usable computer network based on the Internet Protocol Suite (TCP/IP)
        # when computers or network peripherals are interconnected.
        # Zeroconf automates several processes, including listening for new devices :)

        self._zeroconf = Zeroconf()
        self.devices = []
        self.device_refresh_period = device_refresh_period
        self.results_dir = results_dir
        self._Device = deviceClass
        
    def start(self):
        # Use self as the listener class because I have add_service and remove_service methods
        self.browser = ServiceBrowser(self._zeroconf, self._service_type, self)
        
    def stop(self):
        self._zeroconf.close()

    def _get_last_backup_time(self, device):
        try:
            backup_path = device.info()["backup_path"]
            time_since_backup = time.time() - os.path.getmtime(backup_path)
            return time_since_backup
        except OSError:
            return
        except KeyError:
            return
        except Exception as e:
            logging.error(traceback.format_exc())
            return
        
    def get_all_devices_info(self):
        '''
        '''
        out = {}
        for device in self.devices:
            out[device.id()] = device.info()
            out[device.id()]["time_since_backup"] = self._get_last_backup_time(device)
        return out
        
    def get_device(self, id):
        for device in self.devices:
            if device.id()==id:
                return device
        # Not found, so produce an error
        raise KeyError("No such device: %s" % id)
        
    def add(self, name, url):
        """
        Manually add a device to the list
        """
        device = self._Device(url, self.device_refresh_period, results_dir = self.results_dir )
        device.zeroconf_name = name
        device.start()
        logging.info("New device manually added with name = %s, id = %s at URL = %s" % (name, device.id(), url))
        self.devices.append(device)
        
    def add_service(self, zeroconf, type, name):
        """
        Method required to be a Zeroconf listener. Called by Zeroconf when a "_ethoscope._tcp" service
        is registered on the network. Don't call directly.
        
        sample values:
        type = '_ethoscope._tcp.local.'
        name = 'ETHOSCOPE000._ethoscope._tcp.local.'
        """

        
        try:
            info = zeroconf.get_service_info(type, name)
            # Note that I don't trust the address given in the info. When registering, the
            # service doesn't know which interface it will be accessed by and hence which IP
            # address to use (src/scripts/device_server.py puts gibberish in this field for
            # this reason).
            # Query the IP address just using the services hostname and zeroconf.

            if info:
                #ip = socket.inet_ntoa(info.address)
                ip = socket.inet_ntoa(info.addresses[0])
                
                device = self._Device(ip, self.device_refresh_period, results_dir = self.results_dir )
                device.zeroconf_name = name
                device.start()
                logging.info("New device detected with id = %s at IP = %s" % (device.id(), ip))
                self.devices.append(device)
        
        except Exception as error:
            logging.error("Exception trying to add zeroconf service '"+name+"' of type '"+type+"': "+str(error))
            
    def remove_service(self, zeroconf, type, name):
        """
        Method required to be a Zeroconf listener. Called by Zeroconf when a "_ethoscope._tcp" service
        unregisters itself. Don't call directly.
        """
        for device in self.devices:
            if device.zeroconf_name == name:
                logging.info("Device with id = %s has gone down" % device.id())
                #we do not remove devices from the list when they go down so that keep a record of them in the node
                #self.devices.remove(device)
                return

class SensorScanner(DeviceScanner):
    """
    Scans the network for avahi announced sensors
    """
    _suffix = ".local" 
    _service_type = "_sensor._tcp.local." 
    
    def __init__(self, device_refresh_period = 60, deviceClass=Sensor):
        self._zeroconf = Zeroconf()
        self.devices = []
        self.device_refresh_period = device_refresh_period
        self._Device = deviceClass
        self.results_dir = ""
        super(SensorScanner, self).__init__(device_refresh_period=self.device_refresh_period, deviceClass=self._Device)
        
    def start(self):
        # Use self as the listener class because I have add_service and remove_service methods
        self.browser = ServiceBrowser(self._zeroconf, self._service_type, self)
        
    def stop(self):
        self._zeroconf.close()


