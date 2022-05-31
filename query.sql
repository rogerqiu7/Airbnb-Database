-- creates the airbnb database
CREATE DATABASE airbnb;

-- use table data import wizard to import apartments.csv to airbnb database
-- apartments table with about 3500 rows now exists

-- inspect the apartments table, view first 10 rows
SELECT * FROM apartments LIMIT 10;

-- add primary key id to apartments table and remove the old rental_id column
ALTER TABLE apartments
ADD id INT PRIMARY KEY AUTO_INCREMENT,
DROP COLUMN rental_id;

-- each row now has a unique id that is its primary key
SELECT * FROM apartments LIMIT 5;

-- drop columns that we do not need:
-- we do not care about the floor, building age, roofdeck, doorman, patio, dishwasher or gym
ALTER TABLE apartments
DROP COLUMN floor,
DROP COLUMN building_age_yrs,
DROP COLUMN has_roofdeck,
DROP COLUMN has_doorman,
DROP COLUMN has_patio,
DROP COLUMN has_gym,
DROP COLUMN has_dishwasher;

-- we now just have the columns we need
SELECT * FROM apartments LIMIT 5;

-- we only want apartments that are 10 minutes or less to the subway 
-- has no fee, has washer and dryer, has an elevator and is in manhattan 

DELETE FROM apartments WHERE min_to_subway > 10;
DELETE FROM apartments WHERE no_fee = 0;
DELETE FROM apartments WHERE has_washer_dryer = 0;
DELETE FROM apartments WHERE has_elevator = 0;
DELETE FROM apartments WHERE borough != "Manhattan";

-- we now just have the apartments we would like to consider
SELECT * FROM apartments;

-- now we export this dataset into a csv file for our Python machine learning analysis and visualization. 

-- we have completed the analysis, we now have 5 owners who have just purchased 7 apartments

-- we now create the owners table with primary key id's, first and last name, and apartments that they own.
CREATE TABLE owners (
    id INT PRIMARY KEY AUTO_INCREMENT,
    firstname TEXT,
    lastname TEXT,
    apartment_id INT,
    FOREIGN KEY (apartment_id) REFERENCES apartments(id)
);

-- lets view this newly created owners table
SELECT * FROM owners;

-- lets add our owner information to this table
INSERT INTO owners (firstname, lastname, apartment_id)
VALUES
('Lebron', 'James', 2838),
('Lebron', 'James', 47),
('Elon', 'Musk', 1761),
('Tom', 'Cruise', 582),
('Selena', 'Gomez', 3240),
('Selena', 'Gomez', 3078),
('Roger', 'Qiu', 2142);

-- lets view our owners now and their property ids
SELECT * FROM owners;

-- lets join the owners table to the apartments table so we can see in detail the apartments that these owners have.
-- left join so we keep all rows on our left table which is owners
SELECT * FROM owners 
LEFT JOIN apartments
ON owners.apartment_id = apartments.id;

-- lets now create a guests table for airbnb users to come in a book
CREATE TABLE guests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    firstname TEXT,
    lastname TEXT
);

-- lets view the guest table
SELECT * FROM guests;

-- lets add our 3 new guests in
INSERT INTO guests (email, firstname, lastname)
VALUES 
('tswift@sql.com','Taylor','Swift'),
('jbezos@sql.com','Jeff','Bezos'),
('kwest@sql.com','Kanye','West');

-- lets see our guests now
SELECT * FROM guests;

-- finally lets create our bookings table so we can link guests to apartments and owner that they book
CREATE TABLE bookings (
id INT PRIMARY KEY AUTO_INCREMENT,
guest_id INT NOT NULL,
apartment_id INT NOT NULL,
owner_id INT NOT NULL,
check_in DATETIME,
FOREIGN KEY (guest_id) REFERENCES guests(id),
FOREIGN KEY (apartment_id) REFERENCES apartments(id),
FOREIGN KEY (owner_id) REFERENCES owners(id)
);

-- lets see look at our newly created table
SELECT * FROM bookings;

-- now we fill our table to show which guests booked which rooms and at what time, and who the owner is
INSERT INTO bookings (guest_id, apartment_id,owner_id, check_in)
VALUES 
(1,2838,1,'2022-07-01 15:10:10'),
(2,2142,7,'2022-08-02 03:10:10'),
(3,1761,3,'2022-09-03 11:10:10');

-- lets see look at our bookings
SELECT * FROM bookings;

-- lets join our guests with our apartments now
-- we only want to see apartments that are booked so we use inner join
SELECT * FROM owners
INNER JOIN bookings 
ON owners.apartment_id = bookings.apartment_id;

-- we can finally see our owners, the guests and their checkin time using the bookings table