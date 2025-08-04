import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DATABASE_URL
from utils.logger import add_log

engine = create_engine(DATABASE_URL)
get_session = sessionmaker(autoflush=True, bind=engine)
Base = declarative_base()


def init_db():
    create_database_if_not_exists(DATABASE_URL)
    Base.metadata.create_all(engine)


def create_database_if_not_exists(database_url):
    database_name = database_url.split("/")[-1]
    db_url = database_url.rsplit("/", 1)[0] + "/postgres"
    conn = psycopg2.connect(db_url)
    try:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [database_name])
            if not cursor.fetchone():
                cursor.execute(sql.SQL("CREATE DATABASE{}").format(sql.Identifier(database_name)))
    except psycopg2.Error as e:
        add_log(e)
    finally:
        conn.close()
