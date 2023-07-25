CREATE TABLE IF NOT EXISTS genre (
	id SERIAL PRIMARY KEY,
	name VARCHAR(30) UNIQUE NOT NULL
);


CREATE TABLE IF NOT EXISTS singer (
	id SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS album (
	id SERIAL PRIMARY KEY,
	name VARCHAR(60) NOT NULL,
	album_year int NOT NULL CHECK (album_year > 1900)
);


CREATE TABLE IF NOT EXISTS track (
	id SERIAL PRIMARY KEY,
	name VARCHAR(60) NOT NULL,
	--len int	NOT NULL,
	len TIME NOT NULL CHECK (len > '00:00:59') CHECK (len < '01:00:00'),
	album_id SERIAL REFERENCES album(id)
);


CREATE TABLE IF NOT EXISTS collection (
	id SERIAL PRIMARY KEY,
	name VARCHAR(60) NOT NULL,
	coll_year int NOT NULL CHECK (coll_year > 1900)
);



CREATE TABLE IF NOT EXISTS collection_track (
	id SERIAL PRIMARY KEY,
    collection_id SERIAL NOT NULL REFERENCES collection(id),
    track_id SERIAL NOT NULL REFERENCES track(id)
);


CREATE TABLE IF NOT EXISTS album_singer (
	id SERIAL PRIMARY KEY,
    singer_id SERIAL NOT NULL REFERENCES singer(id),
    album_id SERIAL NOT NULL REFERENCES album(id)
);


CREATE TABLE IF NOT EXISTS genre_singer (
	id SERIAL PRIMARY KEY,
    singer_id SERIAL NOT NULL REFERENCES singer(id),
    genre_id SERIAL NOT NULL REFERENCES genre(id)
);





