-- use finalproject;

-- SELECT n_id, image_url 
-- FROM nft
-- LIMIT 10;

-- SELECT n_id, salePrice
-- FROM historicalSales
-- LIMIT 20;

-- SELECT traitname
-- FROM traits;

-- The cheapest NFT that owner 420 has purchased 
-- join across three tables 
-- SELECT n_id, MIN(salePrice)
-- FROM historicalSales
-- INNER JOIN nft USING (n_id)
-- INNER JOIN owners USING (o_id)
-- WHERE o_id = 420
-- GROUP BY n_id;



-- View 
-- join across three tables 
-- CREATE VIEW BIGBANG
-- AS 
-- SELECT historicalSales.salePrice, nft.n_id, owners.username
-- FROM historicalSales
-- INNER JOIN nft USING (n_id)
-- INNER JOIN owners USING (o_id); 

-- Create new record (example)
 -- INSERT INTO BIGBANG VALUES (101, 7000, %s);

-- DELETE (example)
-- DELETE FROM BIGBANG
-- WHERE username = ''; 

-- UPDATE (example)
 -- UPDATE BIGBANG
 -- SET username = %s
 -- WHERE username = %s; 


-- delimiter $$
-- CREATE PROCEDURE sold_within_timeframe( -- Input trait names
-- 	IN date_begin DATE,
--     IN date_end DATE, 
--     OUT nft_between_dates INT)
-- BEGIN
-- 	SELECT n_id
--     INTO nft_between_dates
--     FROM historicalSales
--     WHERE saleDate BETWEEN date_begin AND date_end;
-- END $$

-- delimiter $$
-- CREATE PROCEDURE getPrice(
-- 	IN NFT INT, 
--     OUT NFT_price INT)
-- BEGIN 
-- 	SELECT NFT_price 
--     INTO price
--     FROM currentValue 
--     WHERE n_id = NFT;
-- END $$

-- CALL getPrice(21, @NFT_price);


-- SELECT p2, n_id, MIN(price), traitname
-- FROM currentValue 
-- INNER JOIN nft USING (n_id)
-- GROUP BY p2, n_id
-- HAVING p2 > 0;


-- delimiter $$
-- CREATE PROCEDURE sp( -- Input trait names
-- 	IN in_trait1 VARCHAR(50), 	
--     IN in_trait2 VARCHAR(50), 	
--     IN in_trait3 VARCHAR(50), 	
--     IN in_trait4 VARCHAR(50), 	
--     IN in_trait5 VARCHAR(50), 	
--     IN in_trait6 VARCHAR(50), 	
--     IN in_trait7 VARCHAR(50), 	
--     IN in_trait8 VARCHAR(50), 	
--     IN in_trait9 VARCHAR(50), 
--     OUT out_NFT INT
-- 	)
-- BEGIN
-- 	SELECT n_id
--     INTO out_NFT
--     FROM nft
--     WHERE (
--     
--     IF(in_trait1 != '', -- Check if user is specifying trait
--     p1 = (
-- 		SELECT t_subid -- Select trait sub id which will equal the trait id in nft
--         FROM traits
--         WHERE traitname = in_trait1
--         AND t_id = 1
-- 	),
-- 		TRUE) -- input = *, so dont care if nft has trait, return true
--     )
--     
-- 	AND 
--     
--     IF(in_trait2 != '',
--     p2 = (
--  		SELECT t_subid
--         FROM traits
--         WHERE traitname = in_trait2
--         AND t_id = 2
--  	),
-- 		TRUE)
--         
--     AND 
--     
--     IF(in_trait3 != '',
--     p3 = (
-- 		SELECT t_subid
--         FROM traits
--         WHERE traitname = in_trait3
--         AND t_id = 3
-- 	),
-- 		TRUE)
--         
--     AND 
--     
--     IF(in_trait4 != '',
--     p4 = (
-- 		SELECT t_subid
--         FROM traits
--         WHERE traitname = in_trait4
--         AND t_id = 4
-- 	),
-- 		TRUE)
--         
-- 	AND 
--     
--     IF(in_trait5 != '',
--     p5 = (
-- 		SELECT t_subid
--         FROM traits
--         WHERE traitname = in_trait5
--         AND t_id = 5
-- 	),
-- 		TRUE) 
--         
-- 	AND 
--     
--     IF(in_trait6 != '',
--     p6 = (
-- 		SELECT t_subid
--         FROM traits
--         WHERE traitname = in_trait6
--         AND t_id = 6
-- 	),
-- 		TRUE) 
--         
-- 	AND 
--     
--     IF(in_trait7 != '',
--     p7 = (
-- 		SELECT t_subid
--         FROM traits
--         WHERE traitname = in_trait7
--         AND t_id = 7
-- 	),
-- 		TRUE) 
--         
-- 	AND 
--     
--     IF(in_trait8 != '',
--     p8 = (
-- 		SELECT t_subid
--         FROM traits
--         WHERE traitname = in_trait8
--         AND t_id = 8
-- 	),
-- 		TRUE) 
--         
-- 	AND 
--     
--     IF(in_trait9 != '',
--     p9 = (
-- 		SELECT t_subid
--         FROM traits
--         WHERE traitname = in_trait9
--         AND t_id = 9
-- 	),
-- 		TRUE)
-- 	LIMIT 1; 
-- 	 
-- END$$

-- DROP PROCEDURE sp;



-- CALL sp('Dark','Gremplin Blue','Blonde Pigtails','White & Red Goggles','','','','','', @out_NFT);
-- CALL sp('','','','','','','','','', @out_NFT);
-- SELECT @out_NFT;

-- SELECT t_subid, traitname
-- FROM traits
-- WHERE t_id = 2
-- ORDER BY t_subid;

-- SELECT username
-- FROM usernameView
-- WHERE username LIKE 'y%';

-- DELETE FROM usernameView WHERE username = 'yuppie';

-- SELECT IS_UPDATABLE
-- FROM INFORMATION_SCHEMA.VIEWS
-- WHERE TABLE_NAME = 'usernameView';


-- SET SQL_SAFE_UPDATES = 0;

-- INSERT INTO usernameView VALUES (101, 7000, 'Aviv Zohman');

-- The cheapest NFT that owner 420 has purchased 
-- join across three tables 

-- delimiter $$
-- CREATE PROCEDURE bone(
--     IN in_ownerID INT, 
--     OUT totalToadz INT
-- )
-- BEGIN 
-- 	SELECT COUNT(n_id)
--     INTO totalToadz
-- 	FROM owners
-- 	INNER JOIN nft USING (o_id)
-- 	INNER JOIN currentValue USING (n_id)
-- 	WHERE o_id = in_ownerID
-- 	GROUP BY username;
-- END$$

-- DROP PROCEDURE bone;



-- CALL bone(33, @totalToadz); 
-- SELECT @totalToadz;

-- INSERT INTO usernameView VALUES (101, 7000, 'Jeff Wang');

-- CREATE INDEX property ON traits(traitname);


-- SELECT n_id, COUNT(p2) AS `value_occurrence` 
-- FROM nft
-- GROUP BY n_id
-- ORDER BY `value_occurrence` DESC
-- LIMIT 20;

-- SELECT username 
-- FROM usernameView
-- WHERE username = 'Updated Rao';








