-- password_hash_authenticator, used to authenticate passwords
CREATE USER password_hash_authenticator WITH PASSWORD 'developer';
GRANT SELECT ON app_user_password_view TO password_hash_authenticator;

-- app_user_manager, used to add users to the application database
CREATE USER app_user_manager WITH PASSWORD 'developer';
GRANT CONNECT        ON DATABASE routine            TO app_user_manager;
GRANT USAGE          ON SCHEMA public                  TO app_user_manager;  -- if you revoked from PUBLIC
GRANT SELECT, UPDATE, insert ON app_user, user_password      TO app_user_manager;  -- DELETE, INSERT?
GRANT USAGE          ON ALL SEQUENCES IN SCHEMA public TO app_user_manager;  -- if you also granted INSERT

