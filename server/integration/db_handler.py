"""
This module handles database interaction.

Design decision:
    Each method in DatabaseHandler has a database user hardcoded into
    it in order to match the minimum permissions needed for each task.
    The reason that it is hardcoded in the class is because integration
    would have knowledge of the internals of the database but say
    controller would not. Even if the controller can initiate a class
    object instance it cannot know which database user to use.
TODO: More nuanced error handling
TODO: Consider database roles and how to organize them
"""
import psycopg2
from server.config import config

_PASSWORD_AUTH = "password_hash_authenticator"
_USER_MANAGER = "app_user_manager"


class DatabaseConnectionError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class UserNotInDatabaseError(Exception):
    pass


def _open_db_connection(dbname, user, password, host, port):
    """
    Opens a connection to the database with the user that performs
    password hash authentication, used in authenticator objects.

    :param user:
    :param port:
    :param host:
    :param password:
    :param dbname:
    :raises DatabaseConnectionError
    """
    try:
        return psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port)
    except (psycopg2.Error, psycopg2.Warning) as error:
        print("SHOULD LOG! (TODO)")  # TODO: log error
        raise DatabaseConnectionError("Could not connect to the database.")


class DatabaseHandler:
    """
    Class that handles database connections and queries.

    """
    @classmethod
    def add_user(cls, username, email, password_hash, password_salt):
        """
        Adds a user to the database.

        :param username:
        :param email:
        :param password_hash:
        :param password_salt:
        :return:
        """
        sql = """
                with new_user as (
                    INSERT INTO app_user (username, email)
                    VALUES
                    (
                        %s,
                        %s
                    )
                    returning user_id
                )
                INSERT INTO user_password
                    (user_id, password_hash, password_salt)
                VALUES
                (   (select user_id from new_user),
                    %s,
                    %s
                );
                """
        connection = _open_db_connection(dbname=config.get("DATABASE_NAME"),
                                         user=_USER_MANAGER,
                                         password=config.get("APP_USER_MANAGER_PASSWORD"),
                                         host=config.get("DATABASE_HOST_IP"),
                                         port=config.get("DATABASE_HOST_PORT"))
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql, (username, email, password_hash, password_salt))
                    connection.commit()
        finally:
            connection.close()

    @classmethod
    def authenticate(cls, username: str, password_hash: str) -> bool:
        """
        Opens a connection to the configured database and authenticates
        a password hash and username.

        Uses the database user authenticator.

        :param username:
        :param password_hash:
        :return: boolean
        :raises UserNotInDatabaseError
        """
        connection = _open_db_connection(dbname=config.get("DATABASE_NAME"),
                                         user=_PASSWORD_AUTH,
                                         password=config.get("PASSWORD_HASH_AUTHENTICATOR_PASSWORD"),
                                         host=config.get("DATABASE_HOST_IP"),
                                         port=config.get("DATABASE_HOST_PORT"))
        try:
            with connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                        password_hash=%s AS match 
                        FROM app_user_password_view 
                        WHERE username=%s 
                        """,
                        (password_hash, username,))
                    result = cursor.fetchall()
                    if len(result) == 0:
                        raise UserNotInDatabaseError()
                    else:
                        return True if result[0][0] else False
        finally:
            connection.close()

    @classmethod
    def get_password_salt(cls, username: str) -> str:
        """
        Opens a connection to the configured database and gets the password
        salt associated to a user.

        Uses the database user authenticator.

        :param username:
        :raises UserNotInDatabaseError
        """
        connection = _open_db_connection(dbname=config.get("DATABASE_NAME"),
                                         user=_PASSWORD_AUTH,
                                         password=config.get("PASSWORD_HASH_AUTHENTICATOR_PASSWORD"),
                                         host=config.get("DATABASE_HOST_IP"),
                                         port=config.get("DATABASE_HOST_PORT"))
        try:
            with connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 
                        password_salt
                        FROM app_user_password_view 
                        WHERE username=%s
                        LIMIT 1
                        """,
                        (username,))
                    result = cursor.fetchall()
                    if len(result) == 0:
                        raise UserNotInDatabaseError()
                    else:
                        return result[0][0]
        finally:
            connection.close()
