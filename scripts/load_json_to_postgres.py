import os
import json
import time
import psycopg2
from psycopg2.extras import Json
from psycopg2 import OperationalError

DB_HOST = os.getenv('POSTGRES_HOST', 'db')
DB_PORT = os.getenv('POSTGRES_PORT', 5432)
DB_NAME = os.getenv('POSTGRES_DB', 'telegram_data_db')
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'postgres')

DATA_DIR = 'data/raw'  # Directory where JSON files are stored

def wait_for_db(host, port, user, password, dbname, retries=10, delay=5):
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password,
            )
            conn.close()
            print("✅ Database is ready.")
            return
        except OperationalError as e:
            print(f"⏳ Waiting for database... ({i + 1}/{retries}) - {str(e)}")
            time.sleep(delay)
    raise Exception("❌ Database not reachable after several retries.")

def load_files_to_db():
    wait_for_db(DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME)

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_telegram_messages (
            id SERIAL PRIMARY KEY,
            source_file TEXT,
            message JSONB
        );
    """)
    conn.commit()

    # Load each JSON file into the table
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            path = os.path.join(DATA_DIR, filename)
            with open(path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print(f"⚠️ Skipping invalid JSON file: {filename}")
                    continue

            for message in data:
                cursor.execute(
                    "INSERT INTO raw_telegram_messages (source_file, message) VALUES (%s, %s)",
                    (filename, Json(message))
                )

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ All JSON files loaded into raw_telegram_messages.")

if __name__ == '__main__':
    load_files_to_db()
