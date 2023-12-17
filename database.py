import csv
import psycopg2
from psycopg2.extras import execute_values
from decouple import config

ids = set()
lots_queries = []
view_queries = []

connect = psycopg2.connect(
    dbname=config('DB_NAME'),
    user=config('DB_USER'),
    password=config('DB_PASS'),
    host=config('DB_HOST'),
    port=config('DB_PORT'),
    sslmode='require'
)
cursor = connect.cursor()
connect.autocommit = True
with open('huge_clear_events.csv', 'r', newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    for datas in csvreader:
        try:
            profile_id, event_time, lot_id, lot_name, lot_city, lot_category_id, seller_id, lot_price_start = datas

            if seller_id[-2:] == '.0':
                seller_id = seller_id[:-2]

            if profile_id == '':
                profile_id = None
            else:
                ids.add(profile_id)
            ids.add(seller_id)

            lots_queries.append((lot_id, lot_name, lot_city, int(lot_price_start), seller_id))
            view_queries.append((event_time, lot_id, profile_id))

        except Exception as _ex:
            pass


print(f'Parsing is done')

execute_values(cursor, 'INSERT INTO users (id) VALUES %s ON CONFLICT (id) DO NOTHING', [(profile_id,) for profile_id in ids])
print('Query 1 is complete')
execute_values(cursor, 'INSERT INTO lots (id, name, city, "priceStart", "sellerId") VALUES %s ON CONFLICT DO NOTHING', lots_queries)
print('Query 2 is complete')
execute_values(cursor, 'INSERT INTO views ("viewedAt", "lotId", "userId") VALUES %s ON CONFLICT DO NOTHING', view_queries)
print('Query 3 is complete')

cursor.close()
connect.commit()
connect.close()
