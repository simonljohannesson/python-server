"""
This module handles database interaction.

TODO: More nuanced error handling
TODO: Delete debug config
TODO: Rethink class designs
"""
import psycopg2

authenticator_connection_config = {
    "dbname" : "routine",
    "user" : "password_hash_authenticator",
    "password" : "developer",
    "host" : "172.17.0.2",
    "port" : "5432"
}
app_user_manager_connection_config = {
    "dbname" : "routine",
    "user" : "app_user_manager",
    "password" : "developer",
    "host" : "172.17.0.2",
    "port" : "5432"
}


class DatabaseConnectionError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class UserNotInDatabaseError(Exception):
    pass


def open_db_connection(config):
    """
    Opens a connection to the database with the user that performs
    password hash authentication, used in authenticator objects.

    The parameter config should have the structure shown below:

    {
    "dbname" :      <placeholder>,
    "user" :        <placeholder>,
    "password" :    <placeholder>,
    "host" :        <placeholder>,
    "port" :        <placeholder>
    }

    :param config: a dictionary with the information needed to
    set up the database connection.
    :raises DatabaseConnectionError
    """
    try:
        return psycopg2.connect(
            dbname=config["dbname"],
            user=config["user"],
            password=config["password"],
            host=config["host"],
            port=config["port"])
    except (psycopg2.Error, psycopg2.Warning) as error:
        print("SHOULD LOG! (TODO)")  # TODO: log error
        raise DatabaseConnectionError("Could not connect to the database.")


class DatabaseHandler(object):
    """
    Class that handles database connections and queries.

    The parameter user_dict should be a dictionary containing
    database user configurations as per below:

    {
    "dbname" :      <placeholder>,
    "user" :        <placeholder>,
    "password" :    <placeholder>,
    "host" :        <placeholder>,
    "port" :        <placeholder>
    }

    TODO: Required users in user_dict

    :param config_dict: a dictionary with the information needed to
    set up the database connection.
    """
    def __init__(self, user_dict, debug=False):
        if debug:
            self._database_users = {
                "authenticator": authenticator_connection_config,
                "app_user_manager": app_user_manager_connection_config
            }
        else:
            self._config = user_dict

    def add_user(self, username, email, password_hash, password_salt):
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
        connection = open_db_connection(self._database_users["app_user_manager"])
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute( sql, (username, email, password_hash, password_salt))
                    connection.commit()
        finally:
            connection.close()

    def authenticate(self, username: str, password_hash: str) -> bool:
        """
        Opens a connection to the configured database and authenticates
        a password hash and username.

        Uses the database user authenticator.

        :param username:
        :param password_hash:
        :return: boolean
        :raises UserNotInDatabaseError
        """
        connection = open_db_connection(self._database_users["authenticator"])
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

    def get_password_salt(self, username: str) -> str:
        """
        Opens a connection to the configured database and gets the password
        salt associated to a user.

        Uses the database user authenticator.

        :param username:
        :raises UserNotInDatabaseError
        """
        connection = open_db_connection(self._database_users["authenticator"])
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
