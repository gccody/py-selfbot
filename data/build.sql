CREATE TABLE IF NOT EXISTS users (
    id text PRIMARY KEY,
    whitelisted NUMBER(0),
    CONSTRAINT ck_users_whitelisted CHECK (whitelisted in (1,0))
)