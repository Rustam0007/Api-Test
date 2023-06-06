import pytest
from psycopg2 import connect
from sshtunnel import SSHTunnelForwarder
from config.DB_config import HOSTNAME, USER, HOST, DATABASE, PASSWORD, PORT, SSH


@pytest.fixture(scope='session')
def db_connection():
    hostname = HOSTNAME
    username = USER
    password = SSH
    remote_bind_address = HOST

    with SSHTunnelForwarder(
            (hostname, 22),
            ssh_username=username,
            ssh_password=password,
            remote_bind_address=(remote_bind_address, 5432),
            local_bind_address=(HOST, 5440)) as tunnel:
        tunnel.start()
        params = {
            'database': DATABASE,
            'user': USER,
            'password': PASSWORD,
            'host': HOST,
            'port': PORT
        }
        conn = connect(**params)

        yield conn
        conn.close()
        tunnel.close()


@pytest.fixture(scope="session")
def db_cursor(db_connection):
    # Создание курсора для выполнения SQL-запросов
    cursor = db_connection.cursor()
    yield cursor
    cursor.close()


@pytest.fixture(scope="function")
def select_value(db_cursor):
    def _select_value(column, table, critery, criteryValue, secondCritery=None, secondCriteryValue=None,
                      thirdCritery=None, thirdCriteryValue=None, fourthCritery=None, fourthCriteryValue=None):
        getRequest = f"SELECT {column} from {table} where {critery} = %s"
        if secondCritery is None:
            db_cursor.execute(f"{getRequest};", [criteryValue])
        elif thirdCritery is None:
            db_cursor.execute(f"{getRequest} AND {secondCritery} = %s;", [criteryValue, secondCriteryValue])
        elif fourthCritery is None:
            db_cursor.execute(f"{getRequest} AND {secondCritery} = %s AND {thirdCritery} = %s;", [criteryValue, secondCriteryValue, thirdCriteryValue])
        elif fourthCritery is not None:
            db_cursor.execute(f"{getRequest} AND {secondCritery} = %s AND {thirdCritery} = %s AND {fourthCritery} = %s;", [criteryValue, secondCriteryValue, thirdCriteryValue, fourthCriteryValue])
        return db_cursor.fetchone()[0]
    return _select_value


@pytest.fixture(scope="function")
def existing_in_db(db_cursor):
    def _existing_in_db(table, critery, criteryValue):
        getRequest = f"SELECT EXISTS (SELECT 1 FROM {table} WHERE {critery} = %s)"
        db_cursor.execute(f"{getRequest};", [criteryValue])
        exist = db_cursor.fetchone()[0]
        return exist
    return _existing_in_db


@pytest.fixture(scope="function")
def update_value(db_cursor, db_connection):
    def _update_value(table, column, changeColumnValue, critery, criteryValue):
        getRequest = f"UPDATE {table} SET {column} = %s where {critery} = %s;"
        db_cursor.execute(getRequest, [changeColumnValue, criteryValue])
        db_connection.commit()

    return _update_value


@pytest.fixture(scope="function")
def remove_value(db_cursor, db_connection):
    def _remove_value(table, criteryColumn, columnValue):
        getRequest = f"DELETE FROM {table} WHERE {criteryColumn} = %s;"
        db_cursor.execute(getRequest, [columnValue])
        db_connection.commit()

    return _remove_value





