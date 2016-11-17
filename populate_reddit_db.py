import csv
import os
import random
import sys
import sqlite3

DB_NAME = 'reddit_data.db'
schema_file = 'reddit-table-schema.sql'
DATA_PATH = 'reddit-top-2.5-million/data'

db_is_new = not os.path.exists(DB_NAME)

conn = sqlite3.connect(DB_NAME)

if db_is_new:
    print "Creating schema"
    with open(schema_file, 'rt') as f:
        schema = f.read()
    conn.executescript(schema)
    conn.commit()
    print "Schmea created"

print "Going to insert entries now"

c = conn.cursor()

files = [f for f in os.listdir(DATA_PATH) if os.path.isfile(os.path.join(DATA_PATH, f))]

insert_tmpl = "INSERT INTO reddit_posts (subreddit, created_utc, score, domain, "\
              "id, title, author, ups, downs, num_comments, permalink, selftext, "\
              "over_18, is_self, random_number) "\
              "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

total_files = len(files)
for file_index, csv_file in enumerate(files):
    subreddit, ext = os.path.splitext(csv_file)
    if ext.lower() != '.csv':
        continue

    # Inserting the subreddit title in subreddit table
    c.execute("INSERT INTO subreddits (subreddit) VALUES (?)", (subreddit, ))

    f = open(os.path.join(DATA_PATH, csv_file))
    reader = csv.DictReader(f)

    for row_index, row in enumerate(reader):
        sys.stdout.write("\rSubreddit: %d / %d, Post: %d" % (file_index+1,
                                                             total_files,
                                                             row_index+1))
        sys.stdout.flush()
        row['subreddit'] = subreddit
        try:
            row['is_self'] = int(eval(row['is_self']))
            row['over_18'] = int(eval(row['over_18']))
        except:
            row['is_self'] = None
            row['over_18']= None

        row['random_number'] = random.randint(1, 100)
        vals_tup = (row['subreddit'], row['created_utc'], row['score'], row['domain'],
                    row['id'], row['title'], row['author'], row['ups'], row['downs'],
                    row['num_comments'],
                    row['permalink'], row['selftext'], row['over_18'], row['is_self'],
                    row['random_number'])
        unicode_vals_tup = tuple(map(lambda x: x.decode('utf-8') if isinstance(x, str) else x, vals_tup))
        c.execute(insert_tmpl, unicode_vals_tup)
    f.close()

conn.commit()
conn.close()
