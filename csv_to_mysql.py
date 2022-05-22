import pymysql
import csv
import config

conn = pymysql.connect(
                        host=config.db['host'],
                        user=config.db['user'],
                        password=config.db['password'],
                        db=config.db['database'],
                        charset='utf8'
                    )


curs = conn.cursor()

sql = "insert into company (company_ko, company_en, company_ja, tag_ko, tag_en, tag_ja) values (%s, %s, %s, %s, %s, %s)"
f = open('wanted_temp_data.csv', 'r', encoding='utf-8')

rd = csv.reader(f)

for line in rd:
    print(line)
    curs.execute(sql, (line[0],line[1],line[2],line[3],line[4],line[5]))

conn.commit()
conn.close()
f.close()