
SELECT title, name, price, date_sale FROM
(SELECT * FROM 
	(SELECT *, s.id AS stid FROM stock s 
	JOIN book b 
	ON s.id_book = b.id 
	WHERE b.id IN (SELECT id FROM book WHERE id_pub = 1)
	) AS st
	JOIN shop sh
	ON sh.id = st.id_shop
) AS sbs
JOIN sale sa
ON sa.id_stock = stid;
