-- A collection of queries to execute different actions

-- CREATE DATABASE
CREATE DATABASE yelp_restaurants;

-- DROP TABLES
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS postal_codes;
DROP TABLE IF EXISTS categories;

-- CREATE TABLES

-- GEO TABLE
CREATE TABLE IF NOT EXISTS postal_codes (
  postal_code_id SERIAL CONSTRAINT post_key PRIMARY KEY,
  postal_code VARCHAR (10)
);

-- CATEGORIES TABLE
CREATE TABLE IF NOT EXISTS categories (
  category_id SERIAL CONSTRAINT category_key PRIMARY KEY,
  category VARCHAR (50)
);

-- RASTAURANT TABLE
CREATE TABLE IF NOT EXISTS restaurant (
  id VARCHAR CONSTRAINT restaurant_pk PRIMARY KEY,
  restaurant_name VARCHAR (100),
  reviews INT CHECK (reviews > 0),
  rating DECIMAL (2, 1),
  coordinates_latitude DECIMAL (8, 6),
  coordinates_longitude DECIMAL (8, 6),
  postal_code_id INT,
  category_id INT,
  FOREIGN KEY (postal_code_id) REFERENCES postal_codes (postal_code_id),
  FOREIGN KEY (category_id) REFERENCES categories (category_id)
);