SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));

USE littmental;

-- count the times of being bestsellers and create new table
CREATE TABLE IF NOT EXISTS clean_bestsellers AS
	SELECT *, count(*) AS times FROM bestsellers
	GROUP BY title_id;

DROP TABLE bestsellers;
RENAME TABLE clean_bestsellers TO bestsellers;

-- join the reviews table with title_id and create new table
CREATE TABLE IF NOT EXISTS new_reviews AS
	SELECT bt.title_id, r.*
	FROM reviews AS r
	JOIN books_title AS bt
	ON r.title = bt.title
	GROUP BY r.title
	ORDER BY bt.title_id;
DROP TABLE reviews;
RENAME TABLE new_reviews TO reviews;

-- join the book_info table with title_id and create new table
CREATE TABLE IF NOT EXISTS new_book_info AS
	SELECT bt.title_id, b.*
	FROM book_info AS b
	JOIN books_title AS bt
	ON b.title = bt.title
	GROUP BY b.title
	ORDER BY bt.title_id;
DROP TABLE book_info;
RENAME TABLE new_book_info TO book_info;

-- in book_info, check if the book is bestsellers
DROP VIEW IF EXISTS clean_book_info;
CREATE VIEW clean_book_info AS
	SELECT b.*, COUNT(DISTINCT bs.title) AS is_bestseller
	FROM book_info AS b
	LEFT JOIN bestsellers AS bs ON b.title = bs.title
	GROUP BY b.title
	ORDER BY b.year, b.votes desc;


-- add primary key and foreign key for each table
ALTER TABLE bestsellers
ADD PRIMARY KEY (title_id);

ALTER TABLE book_info
ADD PRIMARY KEY (title_id);

ALTER TABLE lists_bestsellers
ADD PRIMARY KEY (list_id);

ALTER TABLE books_title
ADD PRIMARY KEY (title_id);

ALTER TABLE reviews
ADD PRIMARY KEY (title_id);

ALTER TABLE bestsellers
ADD FOREIGN KEY (list_id) REFERENCES lists_bestsellers(list_id);

ALTER TABLE bestsellers
ADD FOREIGN KEY (title_id) REFERENCES books_title(title_id);

ALTER TABLE book_info
ADD FOREIGN KEY (title_id) REFERENCES books_title(title_id);

ALTER TABLE book_info
ADD FOREIGN KEY (title_id) REFERENCES reviews(title_id);


