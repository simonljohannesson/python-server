INSERT INTO app_user        (username, email)
VALUES                      ('bonk', 'bonk@bonk.bonk');
INSERT INTO user_password   (user_id, password_hash, password_salt)
VALUES                      (1,
                             'b''\x92\xf1\x17}\x9f2\xfe\xa6\xb44\xb9\x15\xf1o2\x18}#\xe6\xc8\x84\xf4$\x08\xd8.\xc1\xe8BR\x00\xdd''',
                             'b''e}\x16@\xff\xb8\xd2Jryu\x9b\xb1\x80\xe7\tQ\xb9e<\xe1\xeb\x1f\xf8\xc49\xe7\xa6W+`\xa7''' );
-- VALUES                      (1,
--                              'monkey123',
--                              'hash');

with new_user as (
    INSERT INTO app_user (username, email)
    VALUES ('user2', '2@bonk.bonk')
    returning user_id
)
INSERT INTO user_password   (user_id, password_hash, password_salt)
VALUES                      ((select user_id from new_user),
                              'monkey123',
                              'hash');
