FROM mysql

LABEL maintainer "Antonio Ortega <antonio.ortega@kuleuven.vib.be>"

RUN printf "\ninnodb_buffer_pool_size = 128M\ninnodb_log_file_size = 32M\ninnodb_log_buffer_size = 50M\ninnodb_flush_log_at_trx_commit = 1\ninnodb_lock_wait_timeout = 50\ninnodb_file_per_table=1\n" >> /etc/mysql/my.cnf

