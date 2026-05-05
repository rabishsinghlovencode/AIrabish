

import pymysql
import csv

filename = "empinfo.csv"

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="YOUR_DB_NAME",
    charset="utf8mb4"
)

cur = conn.cursor()

sql = """
INSERT INTO empinfo
(`age`,`workclass`,`fnlwgt`,`education`,`educational-num`,`marital-status`,
 `occupation`,`relationship`,`race`,`gender`,`capital-gain`,`capital-loss`,
 `hours-per-week`,`native-country`,`income`)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

obj = open(filename, "r", newline="", encoding="utf-8")
reader = csv.reader(obj)

next(reader)  # skip header row

for line in reader:
    line = [x.strip() for x in line]  # remove spaces after commas
    cur.execute(sql, line)

conn.commit()

obj.close()
cur.close()
conn.close()

print("✅ All records inserted.")
