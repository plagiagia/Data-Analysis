-- PRINT ALL DATA IN RAW TABLE
SELECT *
FROM raw_table;

-- DROP TABLES
DROP TABLE IF EXISTS restaurants_info;
DROP TABLE IF EXISTS postal_codes;
DROP TABLE IF EXISTS city;
DROP TABLE IF EXISTS categories;


-- CREATE TABLE FOR CITY
CREATE TABLE IF NOT EXISTS city
(
    CityID SERIAL
        CONSTRAINT city_pk PRIMARY KEY,
    City   VARCHAR(20)
);

-- FILL THE CITY
INSERT INTO city (City)
SELECT DISTINCT restaurant_location_city
FROM raw_table;

-- CREATE TABLE FOR POSTAL CODES
CREATE TABLE IF NOT EXISTS postal_codes
(
    PostalCodeID SERIAL
        CONSTRAINT post_pk PRIMARY KEY,
    PostalCode   VARCHAR(10),
    CityId       INT,
    CONSTRAINT postal_city_fk FOREIGN KEY (CityId) REFERENCES city (CityId) ON DELETE CASCADE ON UPDATE CASCADE
);


-- FILL TABLE POSTAL CODES
INSERT INTO postal_codes (PostalCode, CityId)
SELECT raw_table.restaurant_location_zip_code,
       city.cityid
FROM raw_table
         INNER JOIN
     city ON city.city = raw_table.restaurant_location_city
GROUP BY raw_table.restaurant_location_zip_code,
         city.cityid;

-- CREATE TABLE FOR CATEGORIES
CREATE TABLE IF NOT EXISTS categories
(
    CategoryID SERIAL
        CONSTRAINT category_pk PRIMARY KEY,
    Category   VARCHAR(50)
);

-- FILL IN THE CATEGORIES
INSERT INTO categories(Category)
SELECT DISTINCT category_alias
FROM raw_table;


-- CREATE TABLE FOR RESTAURANT INFORMATION
CREATE TABLE IF NOT EXISTS restaurants_info
(
    id                  VARCHAR
        CONSTRAINT restaurant_pk PRIMARY KEY,
    RestaurantName      VARCHAR(50),
    Reviews             INT
        CONSTRAINT positive_reviews CHECK (reviews > 0),
    Rating              DECIMAL(2, 1)
        CONSTRAINT positive_rating CHECK (rating > 0),
    Price               varchar(5),
    RestaurantPhone     VARCHAR(20),
    RestaurantAddress   VARCHAR(50),
    RestaurantLatitude  DECIMAL(8, 6),
    RestaurantLongitude DECIMAL(8, 6),
    RestaurantDistance  DECIMAL(7, 3)
        CONSTRAINT positive_distance CHECK (RestaurantDistance > 0),
    PostalCodeID        INT,
    CONSTRAINT postal_code_restaurant_fk FOREIGN KEY (PostalCodeID) REFERENCES postal_codes (PostalCodeID) ON DELETE CASCADE ON UPDATE CASCADE
);

-- FILL TABLE FOR RESTAURANT INFO
INSERT INTO restaurants_info
SELECT t1.id,
       t1.name,
       t1.reviews,
       t1.rating,
       t1.price,
       t1.phone,
       t1.address,
       t1.lat,
       t1.lon,
       t1.distance,
       t1.post_id
FROM (Select restaurant_id                         AS id,
             restaurant_name                       AS name,
             Avg(Distinct restaurant_review_count) AS reviews,
             Avg(Distinct restaurant_rating)       AS rating,
             restaurant_price                      AS price,
             restaurant_phone                      AS phone,
             restaurant_location_address1          AS address,
             restaurant_coordinates_latitude       AS lat,
             restaurant_coordinates_longitude      AS lon,
             restaurant_distance                   AS distance,
             postal_codes.postalcodeid             AS post_id
      From raw_table
               Inner Join
           postal_codes On postal_codes.postalcode = restaurant_location_zip_code
      Group By restaurant_id,
               restaurant_name,
               restaurant_price,
               restaurant_phone,
               restaurant_location_address1,
               restaurant_coordinates_latitude,
               restaurant_coordinates_longitude,
               restaurant_distance,
               postal_codes.postalcodeid) AS t1;

-- CREATE TABLE FOR CATEGORIES AND RESTAURANTS
CREATE TABLE IF NOT EXISTS restaurants_with_categories
(
    RestaurantID VARCHAR,
    CategoryID   INT,
    CONSTRAINT restaurant_id_fk FOREIGN KEY (RestaurantID) REFERENCES restaurants_info (id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT category_id FOREIGN KEY (CategoryID) REFERENCES categories (CategoryID) ON DELETE CASCADE ON UPDATE CASCADE

);

-- FILL TABLE WITH RESTAURANTS AND CATEGORIES
INSERT INTO restaurants_with_categories(RestaurantID, CategoryID)
SELECT
    restaurants_info.id,
    categories.CategoryID
From
    restaurants_info Inner Join
    raw_table On raw_table.restaurant_id = restaurants_info.id Inner Join
    categories On raw_table.category_alias = categories.category