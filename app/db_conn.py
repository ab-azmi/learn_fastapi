import psycopg2
from psycopg2.extras import RealDictCursor

try:
    connection = psycopg2.connect("dbname=fastapi user=postgres password=1sampai9 port=5432", cursor_factory=RealDictCursor)
    cursor = connection.cursor()
    print('Connected to the database')
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
