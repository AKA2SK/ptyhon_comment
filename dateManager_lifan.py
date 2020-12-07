# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import pandas as pd
import pymysql
import logging

TxtImgPath = "file" + "\\forbiddenWords.txt"
# ExcelImgPath = "file" + '\\123.xlsx'

conn = pymysql.connect(host='rm-uf66nmbkyl58d9tda8o.mysql.rds.aliyuncs.com', port=3306, user='lifan',
                       passwd='#cC20200916mM*', db='ql-cartoon')
cur = conn.cursor()
# sql = 'SELECT * FROM c_cartoon WHERE gender = 0 and isdelete = 0'
sql = "UPDATE c_comment SET isdelete = 1 WHERE ("

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logging.basicConfig(filename="execution_lifan.log", level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


# def dateOperation_excel():
#     df = pd.read_excel(ExcelImgPath, sheet_name=0, header=None, keep_default_na=False)
#
#     # 获取最大行，最大列
#     rows = df.shape[0]
#     cols = df.columns.size
#
#     # 遍历逐行逐列
#     for iRow in range(rows):
#         for iCol in range(cols):
#             if df.iloc[iRow, iCol] != '' and df.iloc[iRow, iCol] is not None:
#                 print(df.iloc[iRow, iCol])

def dateOperation_txt(sql):
    df = pd.read_csv(TxtImgPath, sep=',', header=None, keep_default_na=False)
    rows = df.shape[0]
    cols = df.columns.size
    sql1 = ''

    for iRow in range(rows):
        for iCol in range(cols):
            if df.iloc[iRow, iCol] != '' and df.iloc[iRow, iCol] is not None:
                sql1 += " content like '%s' or" % ('%' + df.iloc[iRow, iCol] + '%')
    try:
        sql1 = sql1[0:-3]
        sql = sql + sql1 + ") AND isdelete = 0"
        logging.info("狸番评论禁词清理开始")
        logging.info("sql执行语句 %s", sql)
        update = cur.execute(sql)
        logging.info('修改后受影响的行数为：%s', update)
        conn.commit()
        logging.info("sql执行成功")
    except:
        logging.error("sql执行失败")
        conn.rollback()
    finally:
        logging.info("狸番评论禁词清理结束")


def dateOperation(sql):
    sql1 = "content regexp '[^0-9]' = 0 or content regexp '[^[:punct:]\ \（\）\《\》\——\；\，\。\“\”\<\>\！\ ]' = 0 or " \
           "content regexp '[^a-zA-Z]' = 0 or (content regexp '[一-龥]' = 1 and length(REPLACE(content,' ','')) = 3)"

    try:
        sql = sql + sql1 + ") AND isdelete = 0"
        logging.info("狸番垃圾评论清理开始")
        logging.info("sql执行语句 %s", sql)
        update = cur.execute(sql)
        logging.info('修改后受影响的行数为：%s', update)
        cur.close()
        conn.commit()
        logging.info("sql执行成功")
    except:
        logging.error("sql执行失败")
        conn.rollback()
    finally:
        logging.info("狸番垃圾评论清理结束")
        conn.close()

# if __name__ == '__main__':
#     dateOperation_txt(sql)
#     dateOperation(sql)
