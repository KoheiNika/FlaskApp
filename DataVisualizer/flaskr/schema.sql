DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

-- 同じ名前のやつくらいいるやろwww
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  username TEXT NOT NULL, -- TEXT's length doesn't limitation, so can't have unique index.
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
)
