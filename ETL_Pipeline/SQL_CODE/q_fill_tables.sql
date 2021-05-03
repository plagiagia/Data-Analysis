insert into postal_codes (PostalCode) (
		SELECT distinct(restaurant_location_zip_code)
		from public."RAW_TABLE"
	);
	
SELECT * FROM postal_codes;

insert into categories (Category)
SELECT distinct(category_title)
from public."RAW_TABLE"
order by category_title;

SELECT *
FROM categories;
insert into public.restaurants_ifo
select t1.id,
	t1.name,
	t1.reviews,
	t1.rating,
	t1.price,
	t1.phone,
	t1.address,
	t1.lat,
	t1.lon,
	t1.distance,
	PostalCodeID
from (
		SELECT DISTINCT(restaurant_id),
			restaurant_id as id,
			restaurant_name as name,
			restaurant_review_count as reviews,
			restaurant_rating as rating,
			restaurant_price as price,
			restaurant_phone as phone,
			restaurant_location_address1 as address,
			restaurant_coordinates_latitude as lat,
			restaurant_coordinates_longitude as lon,
			restaurant_distance as distance,
			restaurant_location_zip_code
		from public."RAW_TABLE"
	) as t1
	inner join postal_codes on t1.restaurant_location_zip_code = postal_codes.PostalCode;

SELECT * FROM restaurants_ifo;


insert into rest_cats
select id, CategoryID
from public."RAW_TABLE"
	left join public.restaurants_info  on public."RAW_TABLE".restaurant_id = public.restaurants_info.id
	inner join categories on public."RAW_TABLE".category_title = categories.Category;



SELECT *
FROM rest_cats;

ALTER TABLE  public.rest_cats
ADD CONSTRAINT id_fk 
FOREIGN KEY (restaurantid)
REFERENCES public.restaurants_info (id) ON DELETE CASCADE;

ALTER TABLE  public.rest_cats
ADD CONSTRAINT category_fk 
FOREIGN KEY (categoryid)
REFERENCES categories (CategoryID) ON DELETE CASCADE;
