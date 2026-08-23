-- Схема базы данных мини-сайта «Список задач» (глава 22 книги «Python с нуля»).
-- Применяется через init_db() в app.py — см. раздел 22.29 сайта.

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1))
);
