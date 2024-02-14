CREATE SCHEMA staging;
CREATE SCHEMA gold;

CREATE TABLE staging.stg_users (
    user_id TEXT,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE staging.stg_comments (
    comment_id TEXT,
    blog_id TEXT,
    user_id TEXT,
    content TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE staging.stg_blog_tags (
    tag_id TEXT,
    blog_id TEXT
);

CREATE TABLE staging.stg_tags (
    tag_id TEXT,
    name TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE staging.stg_blogs (
    blog_id TEXT,
    user_id TEXT,
    title TEXT,
    content TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE staging.stg_favorites (
    favorite_id TEXT,
    blog_id TEXT,
    user_id TEXT,
    favorite_date TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE staging.stg_opinions (
    opinion_id TEXT,
    blog_id TEXT,
    user_id TEXT,
    opinion TEXT,
    created_at TEXT,
    updated_at TEXT
);
