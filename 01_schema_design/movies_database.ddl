CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work(
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.person(
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.person_film_work(
    id uuid PRIMARY KEY,
    FOREIGN KEY(person_id)
        REFERENCES content.person(person_id),
    FOREIGN KEY(film_work_id)
        REFERENCES content.film_work(film_work_id),
    role TEXT NOT NULL,
    created TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre(
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre_film_work(
    id uuid PRIMARY KEY,
    FOREIGN KEY(genre_id)
        REFERENCES content.genre(genre_id),
    FOREIGN KEY(film_work_id)
        REFERENCES content.genre(film_work_id),
    created TIMESTAMP WITH TIME ZONE
);

CREATE UNIQUE INDEX film_work_person_idx
    ON content.person_film_work (film_work_id, person_id, role);

CREATE UNIQUE INDEX film_work_idx
    ON content.film_work (title, creation_date);
