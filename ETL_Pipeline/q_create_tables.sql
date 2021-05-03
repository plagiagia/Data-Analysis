CREATE TABLE IF NOT EXISTS postal_codes (
    PostalCodeID SERIAL CONSTRAINT post_pk PRIMARY KEY,
    PostalCode VARCHAR (10));
	
CREATE TABLE IF NOT EXISTS categories (
    CategoryID SERIAL CONSTRAINT category_pk PRIMARY KEY,
    Category VARCHAR (50));
	
CREATE TABLE IF NOT EXISTS restaurants_info (
    id VARCHAR CONSTRAINT restaurant_pk PRIMARY KEY,
    RestaurantName VARCHAR (50),
    Reviews INT CONSTRAINT positive_reviews CHECK (reviews > 0),
    Rating DECIMAL (2, 1) CONSTRAINT positive_rating CHECK (rating > 0),
    RestaurantPhone VARCHAR(20),
    RestaurantAddress VARCHAR(50),
    RestaurantLatitude DECIMAL (8, 6),
    RestaurantLongitude DECIMAL (8, 6),
    RestaurantDistance DECIMAL (7, 3) CONSTRAINT positive_distance CHECK (RestaurantDistance > 0),
    PostalCodeID INT,
    FOREIGN KEY (PostalCodeID) REFERENCES postal_codes (PostalCodeID) ON DELETE CASCADE
    );
	
CREATE TABLE IF NOT EXISTS rest_cats (
    RestaurantID VARCHAR,
    CategoryID INT,
    FOREIGN KEY (RestaurantID) REFERENCES restaurants_info (id) ON DELETE CASCADE,
    FOREIGN KEY (CategoryID) REFERENCES categories (CategoryID) ON DELETE CASCADE
);