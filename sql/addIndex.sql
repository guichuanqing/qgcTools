SELECT count(*) FROM `t_order`

    #查看进程id，然后用kill id杀掉进程 
    show processlist; 
    SELECT * FROM information_schema.PROCESSLIST;
     #查询正在执行的进程 
    SELECT * FROM information_schema.PROCESSLIST where length(info) >0 ; 
    #查询是否锁表 
    show OPEN TABLES where In_use > 0; 
    #查看被锁住的 
    SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKs;  #5.6
		SELECT * FROM performance_schema.data_locks;  #8
    #等待锁定 
    SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCK_WAITS;  #5.6
		SELECT * FROM performance_schema.data_lock_waits;  #8
    #杀掉锁表进程 
    kill 进程号 
		
		#查看kill死锁命令
SELECT trx_state,trx_started,trx_mysql_thread_id,trx_query,trx_operation_state,CONCAT('kill ',trx_mysql_thread_id,' ;') FROM information_schema.INNODB_TRX order by 4 ;


show tables from information_schema;   -- 查询mysql所有配置与状态信息 添加权限：GRANT PROCESS ON *.* TO 'deme3'@'localhost';  flush privileges;
show tables from PERFORMANCE_SCHEMA;   -- 查询mysql运行时的资源消耗 添加权限：GRANT ALL PRIVILEGES ON *.* TO 'deme3'@'%';  flush privileges;

SELECT * FROM information_schema.INNODB_TRX;  -- 查询正在执行的事务



alter table t_user add unique index index_name(phone);   -- 添加唯一索引
alter table t_user add unique index uniq_email(email);   -- 添加唯一索引


ALTER TABLE t_user RENAME INDEX index_name TO uniq_phone; -- 重名索引

show index FROM t_collection   -- 显示索引
show binary logs;  -- 显示归档日志
show variables like '%connection%'; -- 查看连接数配置
show variables like '%tmp%';  -- 查看临时表配置
select User,authentication_string,Host from mysql.user;  -- 查看用户权限