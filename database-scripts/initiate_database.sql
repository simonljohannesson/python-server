CREATE TABLE permission (
 permission_id SERIAL PRIMARY KEY,
 Relation VARCHAR(200) NOT NULL,
 Action VARCHAR(200) NOT NULL
);


CREATE TABLE app_user (
 user_id SERIAL PRIMARY KEY,
 username VARCHAR(300) UNIQUE,
 email VARCHAR(300)
);


CREATE TABLE user_credentials_view (
);


CREATE TABLE user_information (
);


CREATE TABLE UserNameViewMaterializedIndexOnUser (
);


CREATE TABLE user_password (
 user_id INT         REFERENCES app_user (user_id) ON DELETE CASCADE,
 password_hash VARCHAR(1000) NOT NULL,
 password_salt VARCHAR(200) NOT NULL,
 PRIMARY KEY (user_id)
);


CREATE TABLE user_permission (
 user_id INT                    REFERENCES app_user (user_id) ON DELETE CASCADE,
 permission_id INT ,
 PRIMARY KEY(user_id, permission_id)
);

CREATE TABLE user_token (
 user_id SERIAL                 REFERENCES app_user (user_id) ON DELETE CASCADE,
 token VARCHAR(1000) NOT NULL,
 expires TIMESTAMP WITH TIME ZONE,
 PRIMARY KEY (user_id)
);


CREATE VIEW app_user_password_view as
select
    username, 
    password_hash, 
    password_salt 
from app_user natural join user_password;

