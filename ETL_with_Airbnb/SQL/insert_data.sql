-- ============================================================================
-- ISNERT DATA INTO TABLES
-- AUTHOR: D.GIANNOULIS
-- DATA: 2019-10-01
-- ============================================================================

-- FILL HOSTS
INSERT INTO Hosts
	(id, host_since)
SELECT HostId, HostSince
FROM RAW_table
GROUP BY HostId, HostSince
ORDER BY HostSince;

-- FILL NEIGHBOURHOODS
INSERT INTO Neighbourhoods
	(neighbourhood)
(SELECT FullNeighbourhood
FROM RAW_table
GROUP BY FullNeighbourhood);

-- FILL PROPERTY TYPE
INSERT INTO PropertyTypes
	(property_type)
SELECT PropertyType
FROM RAW_table
GROUP BY PropertyType;

-- FILL ROOM TYPES
INSERT INTO RoomTypes
	(room_type)
SELECT RoomType
FROM RAW_table
GROUP BY RoomType;

-- FILL POSTCODES
INSERT INTO PostCodes
	(post_code, neighbourhood_id)
SELECT Zipcode, Neighbourhoods.id
FROM RAW_table
	INNER JOIN Neighbourhoods
	ON RAW_table.FullNeighbourhood = Neighbourhoods.neighbourhood
GROUP BY Zipcode, Neighbourhoods.id;

-- FILL PROPERTIES
INSERT INTO Properties
	(host__id, postCode_id, propertyType_id, roomType_id, property_name, num_beds, price, num_reviews, review_score)
SELECT Hosts.id, PostCodes.id, PropertyTypes.id, RoomTypes.id, PropertyName, Beds, Price, NumberOfReviews, ScoresRating
FROM RAW_table
	INNER JOIN Hosts
	ON Hosts.id = RAW_table.HostId
	INNER JOIN Neighbourhoods
	ON Neighbourhoods.neighbourhood = RAW_table.FullNeighbourhood
	INNER JOIN PostCodes
	ON PostCodes.neighbourhood_id = Neighbourhoods.id AND PostCodes.post_code = RAW_table.Zipcode
	INNER JOIN PropertyTypes
	ON PropertyTypes.property_type = RAW_table.PropertyType
	INNER JOIN RoomTypes
	ON RoomTypes.room_type = RAW_table.RoomType
ORDER BY 1;
