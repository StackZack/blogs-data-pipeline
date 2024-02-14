CREATE SCHEMA staging;
CREATE SCHEMA gold;

-- STAGE TABLE CREATION
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

-- GOLD TABLE CREATION
CREATE TABLE gold.tag_lookup (
    tag_id INT,
    name VARCHAR(50)
);

CREATE TABLE gold.blogs (
    blog_id INT,
    tag_ids INT ARRAY,
    title VARCHAR(150),
    content TEXT
);

CREATE TABLE gold.users (
    user_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(150)
);

CREATE TABLE gold.comment (
    comment_id INT,
    content TEXT
);

CREATE TABLE gold.favorites (
    favorite_id INT,
    favorite_date DATE
);

CREATE TABLE gold.opinions (
    opinion_id INT,
    opinion BOOLEAN
);

CREATE TABLE gold.blog_activity (
    blog_activity_id INT,
    blog_id INT,
    user_id INT,
    comment_id INT,
    favorite_id INT,
    opinion_id INT,
    tag_id INT
);
