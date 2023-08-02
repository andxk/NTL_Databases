-- Задание 2 --

-- Название и продолжительность самого длительного трека --

SELECT name, len FROM track
ORDER BY len DESC
LIMIT 1;



-- Название треков, продолжительность которых не менее 3,5 минут --

SELECT name FROM track
WHERE len >= '00:03:30';



-- Названия сборников, вышедших в период с 2018 по 2020 год включительно --

SELECT name, coll_year FROM collection
WHERE coll_year BETWEEN 2018 AND 2020;



-- Исполнители, чьё имя состоит из одного слова --

SELECT name FROM singer 
WHERE name NOT LIKE ('% %');



-- Название треков, которые содержат слово «мой» или «my».

SELECT name FROM track
WHERE lower(name) LIKE '%my%';  



-- Задание 3 --

-- Количество исполнителей в каждом жанре

SELECT genre_id, (SELECT name FROM genre WHERE genre_id = genre.id), COUNT(*) FROM genre_singer
GROUP BY genre_id
ORDER BY genre_id;



-- Количество треков, вошедших в альбомы 2019–2020 годов.

SELECT count(*) FROM track t
WHERE (SELECT album_year FROM album a WHERE t.album_id = a.id) BETWEEN 2018 AND 2020;



-- Средняя продолжительность треков по каждому альбому --
SELECT (SELECT name FROM album a WHERE a.id = album_id), AVG(len) FROM track
GROUP BY album_id
ORDER BY album_id;



-- Все исполнители, которые не выпустили альбомы в 2020 году --

SELECT name FROM singer s
WHERE s.id NOT IN 
	(SELECT singer_id FROM album_singer
	 WHERE album_id IN (SELECT id FROM album WHERE album_year=2020)
	 );
			
		

-- Названия сборников, в которых присутствует конкретный исполнитель (выберите его сами).

SELECT name FROM collection c WHERE id IN 	
	(SELECT collection_id FROM collection_track WHERE track_id IN 
		(SELECT id FROM track WHERE album_id IN 
			(SELECT album_id FROM album_singer WHERE singer_id IN 
				(SELECT id FROM singer WHERE name = 'Beyonce')
			)
		)
	)
ORDER BY c.id;




 
-- Задание 4 --

-- Названия альбомов, в которых присутствуют исполнители более чем одного жанра.

SELECT name FROM album a 
WHERE a.id IN (SELECT album_id FROM album_singer WHERE singer_id IN 
	(SELECT singer_id FROM genre_singer GROUP BY singer_id HAVING count(*) > 1)
);



-- Наименования треков, которые не входят в сборники.

SELECT name FROM track t 
WHERE t.id NOT IN (SELECT track_id FROM collection_track);



-- Исполнитель или исполнители, написавшие самый короткий по продолжительности трек, — теоретически таких треков может быть несколько.

SELECT name FROM singer s
WHERE s.id IN (SELECT singer_id FROM album_singer WHERE album_id IN 
	(SELECT album_id FROM track WHERE len = (SELECT min(len) FROM track)));



-- Названия альбомов, содержащих наименьшее количество треков.

SELECT name FROM album a 
WHERE a.id IN 
	(SELECT album_id FROM track
    GROUP BY album_id 
	HAVING count(*) =  
		(SELECT min(count) FROM 
			(SELECT count(id) FROM track GROUP BY album_id ) AS tba)
	);






