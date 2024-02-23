CREATE SCHEMA staging;
CREATE SCHEMA gold;

-- STAGE TABLE CREATION
CREATE TABLE staging.stg_users (
    user_id INT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(150),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE staging.stg_comments (
    comment_id INT,
    blog_id INT,
    user_id INT,
    content TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE staging.stg_blog_tags (
    tag_id INT,
    blog_id INT
);

CREATE TABLE staging.stg_tags (
    tag_id INT,
    name VARCHAR(50),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE staging.stg_blogs (
    blog_id INT,
    user_id INT,
    title VARCHAR(150),
    content TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE staging.stg_favorites (
    favorite_id INT,
    blog_id INT,
    user_id INT,
    favorite_date DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE staging.stg_opinions (
    opinion_id INT,
    blog_id INT,
    user_id INT,
    opinion TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- GOLD TABLE CREATION
CREATE TABLE gold.tag_lookup (
    tag_id INT PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE gold.blogs (
    blog_id INT PRIMARY KEY,
    tag_ids INT ARRAY,
    title VARCHAR(150),
    content TEXT
);

CREATE TABLE gold.users (
    user_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(150)
);

CREATE TABLE gold.comments (
    comment_id INT PRIMARY KEY,
    content TEXT
);

CREATE TABLE gold.favorites (
    favorite_id INT PRIMARY KEY,
    favorite_date DATE
);

CREATE TABLE gold.opinions (
    opinion_id INT PRIMARY KEY,
    opinion BOOLEAN
);

CREATE TABLE gold.blog_activity (
    blog_activity_id SERIAL,
    blog_id INT,
    user_id INT,
    comment_id INT,
    favorite_id INT,
    opinion_id INT,
    CONSTRAINT fk_blog_id
        FOREIGN KEY (blog_id)
            REFERENCES gold.blogs(blog_id),
    CONSTRAINT fk_user_id
        FOREIGN KEY (user_id)
            REFERENCES gold.users(user_id),
    CONSTRAINT fk_comment_id
        FOREIGN KEY (comment_id)
            REFERENCES gold.comments(comment_id),
    CONSTRAINT fk_favorite_id
        FOREIGN KEY (favorite_id)
            REFERENCES gold.favorites(favorite_id),
    CONSTRAINT fk_opinion_id
        FOREIGN KEY (opinion_id)
            REFERENCES gold.opinions(opinion_id)
);
