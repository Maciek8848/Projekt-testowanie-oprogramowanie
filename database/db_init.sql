PRAGMA foreign_keys = ON;

CREATE TABLE user (
    id       INTEGER PRIMARY KEY,
    login    TEXT UNIQUE,
    password TEXT,
    name     TEXT
);

CREATE TABLE paper (
    id       INTEGER PRIMARY KEY,
    content  TEXT,
    id_autor INTEGER,
    FOREIGN KEY(id_autor) REFERENCES user(id)
);

CREATE TABLE review (
    id       INTEGER PRIMARY KEY,
    content  TEXT,
    id_autor INTEGER,
    id_paper INTEGER,
    FOREIGN KEY(id_autor) REFERENCES user(id),
    FOREIGN KEY(id_paper) REFERENCES paper(id)
);

CREATE TRIGGER delete_user
AFTER DELETE ON user
FOR EACH ROW
BEGIN
    DELETE FROM paper  WHERE id_autor = OLD.id;
    DELETE FROM review WHERE id_autor = OLD.id;
END;

CREATE TRIGGER delete_paper
AFTER DELETE ON paper
FOR EACH ROW
BEGIN
    DELETE FROM review WHERE id_paper = OLD.id;
END;