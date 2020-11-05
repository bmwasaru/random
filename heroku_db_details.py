import os


if os.environ.get('CLEARDB_DATABASE_URL'):
    db_url = os.environ['CLEARDB_DATABASE_URL']
    mysql_database = db_url.split('/')[3]
    mysql_user = db_url.split('//')[1].split(':')[0]
    mysql_password = db_url.split('@')[0].split(':')[2]
    mysql_host = db_url.split('@')[1].split('/')[0]
else:
    mysql_database = ""
    mysql_user = ""
    mysql_password = ""
    mysql_host = "localhost"
