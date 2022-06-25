

-- 每天注册用户
SELECT DATE_FORMAT(create_time, "%Y-%m-%d" ) AS time, COUNT(*) AS total FROM t_user GROUP BY DATE_FORMAT(create_time, "%Y-%m-%d") ORDER BY create_time DESC

-- 每天下单用户
SELECT DATE_FORMAT(create_time, "%Y-%m-%d" ) AS time, COUNT(*) AS total FROM t_order GROUP BY DATE_FORMAT(create_time, "%Y-%m-%d") ORDER BY create_time DESC;

SELECT DATE_FORMAT(create_time, "%Y-%m-%d" ) AS time, COUNT(*) AS total FROM t_collection_stock_use GROUP BY DATE_FORMAT(create_time, "%Y-%m-%d") ORDER BY create_time DESC;




DELETE FROM t_collection_stock_use WHERE  create_time BETWEEN '2022-06-22 15:52:03' AND '2022-06-22 16:33:00'; -- 删除库存使用记录

DELETE FROM t_order_item WHERE  create_time BETWEEN '2022-06-22 15:40:00' AND '2022-06-22 15:52:00'; -- 删除订单明细表

DELETE FROM t_order WHERE  create_time BETWEEN '2022-06-22 15:40:00' AND '2022-06-22 15:52:00';   -- 删除订单表

DELETE FROM t_user WHERE  create_time BETWEEN '2022-06-23 13:38:00' AND '2022-06-23 13:59:00';   -- 删除user表

SELECT COUNT(*) as 订单数 from t_order;SELECT COUNT(*) as 订单明细数 from t_order_item;SELECT COUNT(*) as 库存使用数 from t_collection_stock_use; -- 查询订单表相关记录




CALL updateCert("2022-06-23")    -- 新增当日的用户实名状态



