-- Наполнение таблиц музыкального сайта --

INSERT INTO genre ("name") VALUES ('Rock');
INSERT INTO genre ("name") VALUES ('Pop');
INSERT INTO genre ("name") VALUES ('R&B');


INSERT INTO singer VALUES (1, 'Madonna');
INSERT INTO singer VALUES (2, 'Patrick Leonard');
INSERT INTO singer VALUES (3, 'Michael Jackson');
INSERT INTO singer VALUES (4, 'Beyonce');

INSERT INTO genre_singer (singer_id, genre_id) VALUES (1, 1); 
INSERT INTO genre_singer (singer_id, genre_id) VALUES (1, 2);
INSERT INTO genre_singer (singer_id, genre_id) VALUES (2, 1); 
INSERT INTO genre_singer (singer_id, genre_id) VALUES (3, 1); 
INSERT INTO genre_singer (singer_id, genre_id) VALUES (3, 3);
INSERT INTO genre_singer (singer_id, genre_id) VALUES (4, 3);

--SELECT * FROM singer;

-- album 1 --
INSERT INTO album (id, name, album_year) VALUES (1, 'Like a Prayer', 1989);

INSERT INTO album_singer (singer_id, album_id) VALUES (1, 1);
INSERT INTO album_singer (singer_id, album_id) VALUES (2, 1);

INSERT INTO track (name, len, album_id)
VALUES ('My Love Song', '00:04:52', 1);

INSERT INTO track (name, len, album_id)
VALUES ('Cherish', '00:05:03', 1);

INSERT INTO track (name, len, album_id)
VALUES ('Act of Contrition', '00:02:19', 1);

-- album 2 --
INSERT INTO album (id, name, album_year) VALUES (2, 'Madame X', 2020);

INSERT INTO album_singer (singer_id, album_id) VALUES (1, 2);

INSERT INTO track (name, len, album_id) VALUES ('Crave', '00:03:21', 2);
INSERT INTO track (name, len, album_id) VALUES ('Crazy', '00:04:02', 2);

-----


-- album 3 -- Michael Jackson --
INSERT INTO album (id, name, album_year) VALUES (3, 'Off the Wall', 1979);

INSERT INTO album_singer (singer_id, album_id) VALUES (3, 3);

INSERT INTO track (name, len, album_id) VALUES ('Rock with You', '00:03:39', 3);
INSERT INTO track (name, len, album_id) VALUES ('Girlfriend', '00:03:04', 3);


-- album 4 -- Beyonce --
INSERT INTO album (id, name, album_year) VALUES (4, 'B day', 2006);
INSERT INTO album_singer (singer_id, album_id) VALUES (4, 4);

INSERT INTO track (name, len, album_id) VALUES ('Deja Vu', '00:04:00', 4);
INSERT INTO track (name, len, album_id) VALUES ('My Kitty Kat', '00:03:55', 4);
INSERT INTO track (name, len, album_id) VALUES ('Suga Mama', '00:03:25', 4);


-- Collectioons --
--SELECT * FROM track t; 
--SELECT * FROM collection c; 

INSERT INTO collection ("name", coll_year) VALUES ('Rock Collection 15', 2015);
INSERT INTO collection ("name", coll_year) VALUES ('Collection 18', 2018);
INSERT INTO collection ("name", coll_year) VALUES ('Super Collection 20', 2020);
INSERT INTO collection ("name", coll_year) VALUES ('Best Collection 22', 2022);

INSERT INTO collection_track (collection_id, track_id) VALUES (1, 1);
INSERT INTO collection_track (collection_id, track_id) VALUES (1, 3);
INSERT INTO collection_track (collection_id, track_id) VALUES (1, 6);

INSERT INTO collection_track (collection_id, track_id) VALUES (2, 2);
INSERT INTO collection_track (collection_id, track_id) VALUES (2, 7);
INSERT INTO collection_track (collection_id, track_id) VALUES (2, 9);

INSERT INTO collection_track (collection_id, track_id) VALUES (3, 4);
INSERT INTO collection_track (collection_id, track_id) VALUES (3, 1);
INSERT INTO collection_track (collection_id, track_id) VALUES (3, 8);

INSERT INTO collection_track (collection_id, track_id) VALUES (4, 3);
INSERT INTO collection_track (collection_id, track_id) VALUES (4, 4);
INSERT INTO collection_track (collection_id, track_id) VALUES (4, 5);



