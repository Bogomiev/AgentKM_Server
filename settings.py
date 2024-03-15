import pathlib

from utils.configuration.configs import Config

ROOT_DIR = pathlib.Path(__file__).parent.absolute()

config = Config(root_dir=ROOT_DIR).get_config_storage()

API_PREFIX = "/api"

SECRET_KEY = config.get('SECRET_KEY')

PROJECT_NAME = config.get('PROJECT_NAME')

TIME_ZONE = config.get('TIME_ZONE')

POSTGRES_DB_HOST = config.get('POSTGRES_DB_HOST')
POSTGRES_DB_PORT = config.get('POSTGRES_DB_PORT')
POSTGRES_DB_USERNAME = config.get('POSTGRES_DB_USERNAME')
POSTGRES_DB_PASSWORD = config.get('POSTGRES_DB_PASSWORD')
POSTGRES_DB_NAME = config.get('POSTGRES_DB_NAME')
