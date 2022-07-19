CREATE table IF NOT EXISTS posts(
    id integer PRIMARY KEY AUTOINCREMENT,
    author TEXT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);