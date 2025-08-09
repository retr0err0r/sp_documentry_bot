import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
from config import DATABASE_URL
from utils.logger import add_log

engine = create_engine(DATABASE_URL)
get_session = sessionmaker(autoflush=True, bind=engine)
Base = declarative_base()


def init_db():
    if not database_exists(engine.url):
        create_database(engine.url)
    db_url = DATABASE_URL.rsplit("/", 1)[0] + "/postgres"
    database_name = DATABASE_URL.split("/")[-1]
    conn = psycopg2.connect(db_url)
    try:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [database_name])
            if not cursor.fetchone():
                cursor.execute(sql.SQL("CREATE DATABASE{}").format(sql.Identifier(database_name)))
    except Exception as e:
        add_log(f"Error in init_db: {e}")
    finally:
        conn.close()
    Base.metadata.create_all(engine)
