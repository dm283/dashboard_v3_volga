import sys, os, configparser
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

BASE_DIR = Path(__file__).resolve().parent.parent
config = configparser.ConfigParser()
config_file = BASE_DIR / 'config.ini'
if os.path.exists(config_file): config.read(config_file, encoding='utf-8')
else: print("error! config file doesn't exist"); sys.exit()

SQLALCHEMY_DATABASE_URL = config['db']['sqlalchemy_database_url'].replace('pwd', quote_plus(config['db']['pwd']))

engine = create_engine(SQLALCHEMY_DATABASE_URL, )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
