import psycopg2

def create_connection():
    return psycopg2.connect(
        database='RehatSejenak',
        user='postgres',
        password='Okt@vian2510.',
        host='localhost',
        port=5432
    )