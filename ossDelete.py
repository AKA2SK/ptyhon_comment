# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import pandas as pd
import pymysql
import logging
import datetime
import time

# import redis

# TxtImgPath = 'file' + '\forbiddenWords.txt'
# ExcelImgPath = "file" + '\\123.xlsx'

# conn = pymysql.connect(host='sh-cdb-lh38qm1u.sql.tencentcdb.com', port=61799, user='shike', passwd='FWAF5324WEF#',
#                        db='cartoon')

conn = pymysql.connect(host='sh-cdb-ko1n9fya.sql.tencentcdb.com', port=61767, user='shike', passwd='FWAF5324WEF#',
                       db='cartoon3_pre')
cur = conn.cursor()
# pool = redis.ConnectionPool(host='localhost', port=6379, password="", db=6)
# r = redis.Redis(connection_pool=pool)
# sql = 'SELECT * FROM c_cartoon WHERE gender = 0 and isdelete = 0'

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename="oss_delete.log", level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def dateOperation_oss_delete():
    sql = "select uid from cps_history where create_time >= %s group by uid" % (t)

    try:
        logging.info("vip添加开始")
        logging.info("查询数据库内用户的阅读记录 %s", sql)
        cur.execute(sql)
        result = cur.fetchall()
        logging.info("用户信息 %s", result)
        if result:
            for it in result:
                logging.info("查询是否已经赠送会员 %s", sql1)
                cur.execute(sql1, it)
                result2 = cur.fetchall()
                if result2:
                    logging.info("用户%s已赠送", it)
                else:
                    print(it)
                    logging.info("更新cps_customer内的会员天数 %s", sql3)
                    cur.execute(sql3, it)
                    logging.info("查询cps_member_pay是否存在信息 %s", sql5)
                    cur.execute(sql5, it)
                    result3 = cur.fetchall()
                    if result3:
                        logging.info("cps_member_pay已存在该用户信息")
                        logging.info("更新cps_member_pay内的会员信息 %s", sql4)
                        cur.execute(sql4, it)
                        logging.info("标识已赠送会员 %s", sql2)
                        val = (it, 1)
                        cur.execute(sql2, val)
                        logging.info("执行redis")
                        # r.delete("laravel:cartoon:member_pay:%s" % (it))
                    else:
                        logging.info("cps_member_pay没数据")
        else:
            logging.info("无数据执行")
        conn.commit()
        logging.info("sql执行成功")
    except (Exception) as Argument:
        logging.error("sql执行失败%s" % Argument)
        conn.rollback()
    finally:
        logging.info("vip添加结束")
        cur.close()
        conn.close()


# def dateOperation(sql):
#     sql1 = "content regexp '[^0-9]' = 0 or content regexp '[^[:punct:]\ \（\）\《\》\——\；\，\。\“\”\<\>\！\ ]' = 0 or " \
#            "content regexp '[^a-zA-Z]' = 0 or (content regexp '[一-龥]' = 1 and length(REPLACE(content,' ','')) = 3)"
#
#     try:
#         sql = sql + sql1 + ") AND delete_flag = 0"
#         logging.info("猫爪垃圾评论清理开始")
#         logging.info("sql执行语句 %s",sql)
#         update = cur.execute(sql)
#         logging.info('修改后受影响的行数为：%s', update)
#         cur.close()
#         conn.commit()
#         logging.info("sql执行成功")
#     except:
#         logging.error("sql执行失败")
#         conn.rollback()
#     finally:
#         logging.info("猫爪垃圾评论清理结束")
#         conn.close()
if __name__ == '__main__':
    dateOperation_oss_delete()
    # dateOperation(sql)
