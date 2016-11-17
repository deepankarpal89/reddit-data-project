BEGIN;
CREATE TABLE reddit_posts(
       pk_id    INTEGER PRIMARY KEY autoincrement NOT NULL,
       subreddit   CHAR(256) NOT NULL,
       created_utc INTEGER   NOT NULL,
       score INTEGER   NOT NULL,
       domain TEXT NOT NULL,
       id     CHAR(20) NOT NULL,
       title TEXT NOT NULL,
       author CHAR(50) NOT NULL,
       ups INTEGER NOT NULL,
       downs INTEGER NOT NULL,
       num_comments INTEGER NOT NULL,
       permalink TEXT NOT NULL,
       selftext TEXT NOT NULL,
       over_18 INTEGER NULL,
       is_self INTEGER NULL,
       random_number INTEGER NULL
);

CREATE INDEX reddit_posts_subreddit_index ON reddit_posts (subreddit);
CREATE INDEX reddit_posts_id_index ON reddit_posts (id);

CREATE TABLE subreddits(
       pk_id INTEGER PRIMARY KEY autoincrement NOT NULL,
       subreddit CHAR(256) NOT NULL
);

CREATE INDEX subreddits_subreddit_index ON subreddits (subreddit);
COMMIT;
