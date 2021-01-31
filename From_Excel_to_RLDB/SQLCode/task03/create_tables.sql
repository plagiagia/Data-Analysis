-- Category Tables
CREATE TABLE categories
(
    CategoryID int NOT NULL IDENTITY(1,1),
    CategoryName VARCHAR(100),
    PRIMARY KEY(CategoryID)
)

CREATE TABLE sub_categories
(
    SubCategoryID int NOT NULL IDENTITY(1,1),
    SubCategoryName VARCHAR(100),
    CategoryID int,
    PRIMARY KEY(SubCategoryID),
    FOREIGN KEY(CategoryID) REFERENCES categories(CategoryID)
)

--Product Tables
CREATE TABLE manufactureres
(
    ManufacturerID int NOT NULL IDENTITY(1,1),
    Manufacturer VARCHAR(150),
    PRIMARY KEY(ManufacturerID)
)

CREATE TABLE products
(
    ProductID int NOT NULL IDENTITY(1,1),
    ProductName VARCHAR(1000),
    ManufacturerID int,
    SubCategoryID int,
    PRIMARY KEY(ProductID),
    FOREIGN KEY(ManufacturerID) REFERENCES manufactureres(ManufacturerID),
    FOREIGN KEY(SubCategoryID) REFERENCES sub_categories(SubCategoryID)
)

-- GEO Tables
CREATE TABLE countries
(
    CountryID int NOT NULL IDENTITY(1,1),
    CountryName VARCHAR(50),
    PRIMARY KEY(CountryID)
)

CREATE TABLE regions
(
    RegionID int NOT NULL IDENTITY(1,1),
    RegionName VARCHAR(50),
    CountyID int,
    PRIMARY KEY(RegionID),
    FOREIGN KEY(CountyID) REFERENCES countries(CountryID)
)

CREATE TABLE states
(
    StateID int NOT NULL IDENTITY(1,1),
    StateName VARCHAR(50),
    RegionID int,
    PRIMARY KEY(StateID),
    FOREIGN KEY(RegionID) REFERENCES regions(RegionID)
)

CREATE TABLE cities
(
    CityID int NOT NULL IDENTITY(1,1),
    CityName VARCHAR(50),
    StateID int,
    PRIMARY KEY(CityID),
    FOREIGN KEY(StateID) REFERENCES states(StateID)
)

CREATE TABLE postal_codes
(
    PostalCodeID int NOT NULL IDENTITY(1,1),
    PostalCode VARCHAR(50),
    CityID int,
    PRIMARY KEY(PostalCodeID),
    FOREIGN KEY(CityID) REFERENCES cities(CityID)
)

-- Customer Table
CREATE TABLE customers
(
    CustomerID int NOT NULL IDENTITY(1,1),
    CustomerName VARCHAR(50) NOT NULL,
    PostalCodeID int,
    PRIMARY KEY(CustomerID),
    FOREIGN KEY(PostalCodeID) REFERENCES postal_codes(PostalCodeID)
)


-- Order Tables
CREATE TABLE order_events
(
    EventID varchar(50) NOT NULL,
    OrderDate date,
    ShipDate date,
    CustomerID int,
    PRIMARY KEY(EventID),
    FOREIGN KEY(CustomerID) REFERENCES customers(CustomerID)
)

CREATE TABLE orders
(
    OrderID int NOT NULL IDENTITY(1,1),
    EventID VARCHAR(50),
    ProductID int,
    Quantity int,
    Sales float,
    Discount float,
    Profit float,
    PRIMARY KEY(OrderID),
    FOREIGN KEY(EventID) REFERENCES order_events(EventID),
    FOREIGN KEY(ProductID) REFERENCES products(ProductID)
)
