from dotenv import load_dotenv
import os

load_dotenv()


# FIX: If this was a real application we would probably check some sort of
# environmentsettings to make sure we're not running dev values in production,
# e.g. not inlcude .env in the docker image etc.
def __read_config():
    db_url = os.getenv('RATES_SERVER_DB_URL')
    db_user = os.getenv('RATES_SERVER_DB_USER')
    db_password = os.getenv('RATES_SERVER_DB_PW')
    db_connection_string = f'postgresql://{str(db_user)}:{db_password}@{db_url}'

    return {
        'db_connection_string': db_connection_string,
    }


config = __read_config()
