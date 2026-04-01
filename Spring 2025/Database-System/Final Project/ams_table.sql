-- CS4400: Introduction to Database Systems (Spring 2025)
-- Phase II: Create Table & Insert Statements [v0] Monday, February 3, 2025 @ 17:00 EST

-- Team __
-- Siwan Yang (syang723)
-- Eujin Jeon (ejeon9)
-- Jinseo Lee (jlee4223)
-- Team Member Name (GT username)

-- Directions:
-- Please follow all instructions for Phase II as listed on Canvas.
-- Fill in the team number and names and GT usernames for all members above.
-- Create Table statements must be manually written, not taken from an SQL Dump file.
-- This file must run without error for credit.

/* This is a standard preamble for most of our scripts.  The intent is to establish
a consistent environment for the database behavior. */
set global transaction isolation level serializable;
set global SQL_MODE = 'ANSI,TRADITIONAL';
set names utf8mb4;
set SQL_SAFE_UPDATES = 0;

set @thisDatabase = 'airline_management';
drop database if exists airline_management;
create database if not exists airline_management;
use airline_management;

-- Define the database structures
/* You must enter your tables definitions, along with your primary, unique and foreign key
declarations, and data insertion statements here.  You may sequence them in any order that
works for you.  When executed, your statements must create a functional database that contains
all of the data, and supports as many of the constraints as reasonably possible. */
CREATE TABLE Airline (
	airlineID varchar(30) not null,
    revenue decimal(5),
    check (revenue >= 0),
    primary key (airlineID)
);

CREATE TABLE Location (
	locID varchar(10) not null,
    primary key (locID)
);

CREATE TABLE Airport (
	airportID char(3) not null,
    airport_name varchar(50) not null,
    city varchar(30) not null,
    state varchar(30) not null,
    country_code char(3) not null,
    locID varchar(10),
    foreign key (locID) references Location(locID) on update restrict on delete restrict,
    primary key (airportID)
);

CREATE TABLE Leg (
	legID varchar(7) not null,
    distance decimal(5,0) not null,
    arriveID char(3),
    departID char(3),
    foreign key(arriveID) references Airport(airportID) on update restrict on delete set null,
    foreign key(departID) references Airport(airportID) on update restrict on delete set null,
    primary key(legID)
);

CREATE TABLE Route (
	routeID varchar(30) not null,
    primary key(routeID)
);

CREATE TABLE Airplane (
    tail_num varchar(8) not null,
    airlineID varchar(30) not null,
    speed decimal(4,0) not null,
    seat_cap int not null,
    locID varchar(10),
    primary key(tail_num, airlineID),
    foreign key(airlineID) references Airline(airlineID) on update restrict on delete cascade,
    foreign key(locID) references Location(locID) on update restrict on delete restrict
);

CREATE TABLE Flight (
	flightID varchar(10) not null,
    cost decimal(5,2) not null,
    tail_num varchar(8) not null,
    airlineID varchar(30) not null,
    routeID varchar(30) not null,
    progress int not null,
    status ENUM('in_flight', 'on_ground') not null,
    next_time time not null,
    primary key(flightID),
    foreign key(tail_num, airlineID) references Airplane(tail_num, airlineID) on update restrict on delete restrict,
    foreign key(routeID) references Route(routeID) on update cascade on delete restrict
);

CREATE TABLE Boeing (
   tail_num varchar(8) not null,
   airlineID varchar(30) not null,
   maintained boolean,
   model decimal(3,0),
   primary key(tail_num, airlineID),
   foreign key(tail_num, airlineID) references Airplane(tail_num, airlineID) on update cascade on delete restrict
);

CREATE TABLE Airbus (
   tail_num varchar(8) not null,
   airlineID varchar(30) not null,
   variant boolean,
   primary key(tail_num, airlineID),
   foreign key(tail_num, airlineID) references Airplane(tail_num, airlineID) on update cascade on delete restrict
);

CREATE TABLE Person (
   personID varchar(5) not null,
   fname varchar(30) not null,
   lname varchar(30) not null,
   locID varchar(10) not null,
   primary key(personID),
   foreign key(locID) references Location(locID) on update cascade on delete restrict
);

CREATE TABLE Pilot (
   taxID varchar(20),
   personID varchar(5) not null,
   experience float(3,0),
   flightID varchar(10) not null, 
   primary key(taxID),
   foreign key(personId) references Person(personID) on update cascade on delete restrict,
   foreign key(flightID) references Flight(flightID) on update cascade on delete restrict
);

CREATE TABLE Passenger (
	personID varchar(5) not null,
    miles decimal(5,0),
    check(miles >= 0),
    funds decimal(5,0),
    check (funds >= 0),
    primary key(personID),
    foreign key(personID) references Person(personID) on update cascade on delete restrict
);

CREATE TABLE License (
   pilotID varchar(5) not null,
   license_types enum('airbus', 'boeing', 'general'),
   primary key(pilotID, license_types),
   foreign key(pilotID) references Person(personID) on update cascade on delete restrict
);

CREATE TABLE Vacation (
   passengerID varchar(5) not null,
   destination char(3),
   sequence int,
   primary key(destination, sequence, passengerID),
   foreign key(passengerID) references Person(personID) on update cascade on delete cascade
);

CREATE TABLE Contains (
   routeID varchar(30) not null,
   legID varchar(7) not null,
   sequence int not null,
   primary key(routeID, legID, sequence),
   foreign key(routeID) references Route(routeID) on update cascade on delete restrict,
   foreign key(legID) references Leg(legID) on update cascade on delete cascade
);

INSERT INTO Airline (airlineID, revenue) VALUES ('Delta', 53000);
INSERT INTO Airline (airlineID, revenue) VALUES ('United', 48000);
INSERT INTO Airline (airlineID, revenue) VALUES ('British Airways', 24000);
INSERT INTO Airline (airlineID, revenue) VALUES ('Lufthansa', 35000);
INSERT INTO Airline (airlineID, revenue) VALUES ('Air_France', 29000);
INSERT INTO Airline (airlineID, revenue) VALUES ('KLM', 29000);
INSERT INTO Airline (airlineID, revenue) VALUES ('Ryanair', 10000);
INSERT INTO Airline (airlineID, revenue) VALUES ('Japan Airlines', 9000);
INSERT INTO Airline (airlineID, revenue) VALUES ('China Southern Airlines', 14000);
INSERT INTO Airline (airlineID, revenue) VALUES ('Korean Air Lines', 10000);
INSERT INTO Airline (airlineID, revenue) VALUES ('American', 52000);

INSERT INTO Location (locID) VALUES ('port_1');
INSERT INTO Location (locID) VALUES ('port_2');
INSERT INTO Location (locID) VALUES ('port_3');
INSERT INTO Location (locID) VALUES ('port_4');
INSERT INTO Location (locID) VALUES ('port_6');
INSERT INTO Location (locID) VALUES ('port_7');
INSERT INTO Location (locID) VALUES ('port_10');
INSERT INTO Location (locID) VALUES ('port_11');
INSERT INTO Location (locID) VALUES ('port_12');
INSERT INTO Location (locID) VALUES ('port_13');
INSERT INTO Location (locID) VALUES ('port_14');
INSERT INTO Location (locID) VALUES ('port_15');
INSERT INTO Location (locID) VALUES ('port_16');
INSERT INTO Location (locID) VALUES ('port_17');
INSERT INTO Location (locID) VALUES ('port_18');
INSERT INTO Location (locID) VALUES ('port_20');
INSERT INTO Location (locID) VALUES ('port_21');
INSERT INTO Location (locID) VALUES ('port_22');
INSERT INTO Location (locID) VALUES ('port_23');
INSERT INTO Location (locID) VALUES ('port_24');
INSERT INTO Location (locID) VALUES ('port_25');
INSERT INTO Location (locID) VALUES ('plane_1');
INSERT INTO Location (locID) VALUES ('plane_2');
INSERT INTO Location (locID) VALUES ('plane_3');
INSERT INTO Location (locID) VALUES ('plane_4');
INSERT INTO Location (locID) VALUES ('plane_5');
INSERT INTO Location (locID) VALUES ('plane_6');
INSERT INTO Location (locID) VALUES ('plane_7');
INSERT INTO Location (locID) VALUES ('plane_8');
INSERT INTO Location (locID) VALUES ('plane_10');
INSERT INTO Location (locID) VALUES ('plane_13');
INSERT INTO Location (locID) VALUES ('plane_18');
INSERT INTO Location (locID) VALUES ('plane_20');

INSERT INTO Airport VALUES ('ATL', 'Atlanta Hartsfield_Jackson International', 'Atlanta', 'Georgia', 'USA' ,'port_1');
INSERT INTO Airport VALUES ('DXB', 'Dubai International', 'Dubai', 'Al Garhoud', 'UAE' ,'port_2');
INSERT INTO Airport VALUES ('HND', 'Tokyo International Haneda', 'Ota City', 'Tokyo', 'JPN' ,'port_3');
INSERT INTO Airport VALUES ('LHR', 'London Heathrow', 'London', 'England', 'GBR' ,'port_4');
INSERT INTO Airport VALUES ('IST', 'Istanbul International', 'Arnavutkoy', 'Istanbul', 'TUR' ,NULL);
INSERT INTO Airport VALUES ('DFW', 'Dallas_Fort Worth International', 'Dallas', 'Texas', 'USA' ,'port_6');
INSERT INTO Airport VALUES ('CAN', 'Guangzhou International', 'Guangzhou', 'Guangdong', 'CHN' ,'port_7');
INSERT INTO Airport VALUES ('DEN', 'Denver International', 'Denver', 'Colorado', 'USA' ,NULL);
INSERT INTO Airport VALUES ('LAX', 'Los Angeles International', 'Los Angeles', 'California', 'USA' ,NULL);
INSERT INTO Airport VALUES ('ORD', 'O_Hare International', 'Chicago', 'Illinois', 'USA' ,'port_10');
INSERT INTO Airport VALUES ('AMS', 'Amsterdam Schipol International', 'Amsterdam', 'Haarlemmermeer', 'NLD' ,'port_11');
INSERT INTO Airport VALUES ('CDG', 'Paris Charles de Gaulle', 'Roissy_en_France', 'Paris', 'FRA' ,'port_12');
INSERT INTO Airport VALUES ('FRA', 'Frankfurt International', 'Frankfurt', 'Frankfurt_Rhine_Main', 'DEU' ,'port_13');
INSERT INTO Airport VALUES ('MAD', 'Madrid Adolfo Suarez_Barajas', 'Madrid', 'Barajas', 'ESP' ,'port_14');
INSERT INTO Airport VALUES ('BCN', 'Barcelona International', 'Barcelona', 'Catalonia', 'ESP' ,'port_15');
INSERT INTO Airport VALUES ('FCO', 'Rome Fiumicino', 'Fiumicino', 'Lazio', 'ITA' ,'port_16');
INSERT INTO Airport VALUES ('LGW', 'London Gatwick', 'London', 'England', 'GBR' ,'port_17');
INSERT INTO Airport VALUES ('MUC', 'Munich International', 'Munich', 'Bavaria', 'DEU' ,'port_18');
INSERT INTO Airport VALUES ('MDW', 'Chicago Midway International', 'Chicago', 'Illinois', 'USA' ,NULL);
INSERT INTO Airport VALUES ('IAH', 'George Bush Intercontinental', 'Houston', 'Texas', 'USA' ,'port_20');
INSERT INTO Airport VALUES ('HOU', 'William P_Hobby International', 'Houston', 'Texas', 'USA' ,'port_21');
INSERT INTO Airport VALUES ('NRT', 'Narita International', 'Narita', 'Chiba', 'JPN' ,'port_22');
INSERT INTO Airport VALUES ('BER', 'Berlin Brandenburg Willy Brandt International', 'Berlin', 'Schonefeld', 'DEU' ,'port_23');
INSERT INTO Airport VALUES ('ICN', 'Incheon International Airport', 'Seoul', 'Jung_gu', 'KOR' ,'port_24');
INSERT INTO Airport VALUES ('PVG', 'Shanghai Pudong International Airport', 'Shanghai', 'Pudong', 'CHN' ,'port_25');

INSERT INTO Route VALUES ('americas_hub_exchange');
INSERT INTO Route VALUES ('americas_one');
INSERT INTO Route VALUES ('americas_three');
INSERT INTO Route VALUES ('americas_two');
INSERT INTO Route VALUES ('big_europe_loop');
INSERT INTO Route VALUES ('euro_north');
INSERT INTO Route VALUES ('euro_south');
INSERT INTO Route VALUES ('germany_local');
INSERT INTO Route VALUES ('pacific_rim_tour');
INSERT INTO Route VALUES ('south_euro_loop');
INSERT INTO Route VALUES ('texas_local');
INSERT INTO Route VALUES ('korea_direct');

INSERT INTO Leg VALUES ('leg_4', 600, 'ORD', 'ATL');
INSERT INTO Leg VALUES ('leg_2', 3900, 'AMS', 'ATL');
INSERT INTO Leg VALUES ('leg_1', 400, 'BER', 'AMS');
INSERT INTO Leg VALUES ('leg_31', 3700, 'CDG', 'ORD');
INSERT INTO Leg VALUES ('leg_14', 400, 'MUC', 'CDG');
INSERT INTO Leg VALUES ('leg_3', 3700, 'LHR', 'ATL');
INSERT INTO Leg VALUES ('leg_22', 600, 'BER', 'LHR');
INSERT INTO Leg VALUES ('leg_23', 500, 'MUC', 'LHR');
INSERT INTO Leg VALUES ('leg_29', 400, 'FCO', 'MUC');
INSERT INTO Leg VALUES ('leg_16', 800, 'MAD', 'FCO');
INSERT INTO Leg VALUES ('leg_25', 600, 'CDG', 'MAD');
INSERT INTO Leg VALUES ('leg_13', 200, 'LHR', 'CDG');
INSERT INTO Leg VALUES ('leg_24', 300, 'BCN', 'MAD');
INSERT INTO Leg VALUES ('leg_5', 500, 'CDG', 'BCN');
INSERT INTO Leg VALUES ('leg_27', 300, 'BER', 'MUC');
INSERT INTO Leg VALUES ('leg_8', 600, 'LGW', 'BER');
INSERT INTO Leg VALUES ('leg_21', 600, 'BER', 'LGW');
INSERT INTO Leg VALUES ('leg_9', 300, 'MUC', 'BER');
INSERT INTO Leg VALUES ('leg_28', 400, 'CDG', 'MUC');
INSERT INTO Leg VALUES ('leg_11', 500, 'BCN', 'CDG');
INSERT INTO Leg VALUES ('leg_6', 300, 'MAD', 'BCN');
INSERT INTO Leg VALUES ('leg_26', 800, 'FCO', 'MAD');
INSERT INTO Leg VALUES ('leg_30', 200, 'FRA', 'MUC');
INSERT INTO Leg VALUES ('leg_17', 300, 'BER', 'FRA');
INSERT INTO Leg VALUES ('leg_7', 4700, 'CAN', 'BER');
INSERT INTO Leg VALUES ('leg_10', 1600, 'HND', 'CAN');
INSERT INTO Leg VALUES ('leg_18', 100, 'NRT', 'HND');
INSERT INTO Leg VALUES ('leg_12', 600, 'FCO', 'CDG');
INSERT INTO Leg VALUES ('leg_15', 200, 'IAH', 'DFW');
INSERT INTO Leg VALUES ('leg_20', 100, 'HOU', 'IAH');
INSERT INTO Leg VALUES ('leg_19', 300, 'DFW', 'HOU');
INSERT INTO Leg VALUES ('leg_32', 6800, 'ICN', 'DFW');

INSERT INTO Airplane VALUES ('n106js', 'Delta', 800, 4, 'plane_1');
INSERT INTO Airplane VALUES ('n110jn', 'Delta', 800, 5, 'plane_3');
INSERT INTO Airplane VALUES ('n127js', 'Delta', 600, 4, NULL);
INSERT INTO Airplane VALUES ('n330ss', 'United', 800, 4, NULL);
INSERT INTO Airplane VALUES ('n380sd', 'United', 400, 5, 'plane_5');
INSERT INTO Airplane VALUES ('n616lt', 'British Airways', 600, 7, 'plane_6');
INSERT INTO Airplane VALUES ('n517ly', 'British Airways', 600, 4, 'plane_7');
INSERT INTO Airplane VALUES ('n620la', 'Lufthansa', 800, 4, 'plane_8');
INSERT INTO Airplane VALUES ('n401fj', 'Lufthansa', 300, 4, NULL);
INSERT INTO Airplane VALUES ('n653fk', 'Lufthansa', 600, 6, 'plane_10');
INSERT INTO Airplane VALUES ('n118fm', 'Air_France', 400, 4, NULL);
INSERT INTO Airplane VALUES ('n815pw', 'Air_France', 400, 3, NULL);
INSERT INTO Airplane VALUES ('n161fk', 'KLM', 600, 4, 'plane_13');
INSERT INTO Airplane VALUES ('n337as', 'KLM', 400, 5, NULL);
INSERT INTO Airplane VALUES ('n256ap', 'KLM', 300, 4, NULL);
INSERT INTO Airplane VALUES ('n156sq', 'Ryanair', 600, 8, NULL);
INSERT INTO Airplane VALUES ('n451fi', 'Ryanair', 600, 5, NULL);
INSERT INTO Airplane VALUES ('n341eb', 'Ryanair', 400, 4, 'plane_18');
INSERT INTO Airplane VALUES ('n353kz', 'Ryanair', 400, 4, NULL);
INSERT INTO Airplane VALUES ('n305fv', 'Japan Airlines', 400, 6, 'plane_20');
INSERT INTO Airplane VALUES ('n443wu', 'Japan Airlines', 800, 4, NULL);
INSERT INTO Airplane VALUES ('n454gq', 'China Southern Airlines', 400, 3, NULL);
INSERT INTO Airplane VALUES ('n249yk', 'China Southern Airlines', 400, 4, NULL);
INSERT INTO Airplane VALUES ('n180co', 'Korean Air Lines', 600, 5, 'plane_4');
INSERT INTO Airplane VALUES ('n448cs', 'American', 400, 4, NULL);
INSERT INTO Airplane VALUES ('n225sb', 'American', 800, 8, NULL);
INSERT INTO Airplane VALUES ('n553qn', 'American', 800, 5, 'plane_2');

INSERT INTO Flight VALUES ('dl_10', 200, 'n106js', 'Delta', 'americas_one', 1, 'in_flight', '08:00:00');
INSERT INTO Flight VALUES ('un_38', 200, 'n380sd', 'United', 'americas_three', 2, 'in_flight', '14:30:00');
INSERT INTO Flight VALUES ('ba_61', 200, 'n616lt', 'British Airways', 'americas_two', 0, 'on_ground', '09:30:00');
INSERT INTO Flight VALUES ('lf_20', 300, 'n620la', 'Lufthansa', 'euro_north', 3, 'in_flight', '11:00:00');
INSERT INTO Flight VALUES ('km_16', 400, 'n161fk', 'KLM', 'euro_south', 6, 'in_flight', '14:00:00');
INSERT INTO Flight VALUES ('ba_51', 100, 'n517ly', 'British Airways', 'big_europe_loop', 0, 'on_ground', '11:30:00');
INSERT INTO Flight VALUES ('ja_35', 300, 'n305fv', 'Japan Airlines', 'pacific_rim_tour', 1, 'in_flight', '09:30:00');
INSERT INTO Flight VALUES ('ry_34', 100, 'n341eb', 'Ryanair', 'germany_local', 0, 'on_ground', '15:00:00');
INSERT INTO Flight VALUES ('aa_12', 150, 'n553qn', 'American', 'americas_hub_exchange', 1, 'on_ground', '12:15:00');
INSERT INTO Flight VALUES ('dl_42', 220, 'n110jn', 'Delta', 'texas_local', 0, 'on_ground', '13:45:00');
INSERT INTO Flight VALUES ('ke_64', 500, 'n180co', 'Korean Air Lines', 'korea_direct', 0, 'on_ground', '16:00:00');
INSERT INTO Flight VALUES ('lf_67', 900, 'n653fk', 'Lufthansa', 'euro_north', 6, 'on_ground', '21:23:00');

INSERT INTO Boeing VALUES ('n118fm', 'Air_France', FALSE, 777);
INSERT INTO Boeing VALUES ('n256ap', 'KLM', FALSE, 737);
INSERT INTO Boeing VALUES ('n341eb', 'Ryanair', TRUE, 737);
INSERT INTO Boeing VALUES ('n353kz', 'Ryanair', TRUE, 737);
INSERT INTO Boeing VALUES ('n249yk', 'China Southern Airlines', FALSE, 787);
INSERT INTO Boeing VALUES ('n448cs', 'American', TRUE, 787);

INSERT INTO Airbus VALUES ('n106js', 'Delta', FALSE);
INSERT INTO Airbus VALUES ('n110jn', 'Delta', FALSE);
INSERT INTO Airbus VALUES ('n127js', 'Delta', TRUE);
INSERT INTO Airbus VALUES ('n330ss', 'United', FALSE);
INSERT INTO Airbus VALUES ('n380sd', 'United', FALSE);
INSERT INTO Airbus VALUES ('n616lt', 'British Airways', FALSE);
INSERT INTO Airbus VALUES ('n517ly', 'British Airways', FALSE);
INSERT INTO Airbus VALUES ('n620la', 'Lufthansa', TRUE);
INSERT INTO Airbus VALUES ('n653fk', 'Lufthansa', FALSE);
INSERT INTO Airbus VALUES ('n815pw', 'Air_France', FALSE);
INSERT INTO Airbus VALUES ('n161fk', 'KLM', TRUE);
INSERT INTO Airbus VALUES ('n337as', 'KLM', FALSE);
INSERT INTO Airbus VALUES ('n156sq', 'Ryanair', FALSE);
INSERT INTO Airbus VALUES ('n451fi', 'Ryanair', TRUE);
INSERT INTO Airbus VALUES ('n305fv', 'Japan Airlines', FALSE);
INSERT INTO Airbus VALUES ('n443wu', 'Japan Airlines', TRUE);
INSERT INTO Airbus VALUES ('n180co', 'Korean Air Lines', FALSE);
INSERT INTO Airbus VALUES ('n225sb', 'American', FALSE);
INSERT INTO Airbus VALUES ('n553qn', 'American', FALSE);

INSERT INTO Person VALUES ('p1', 'Jeanne', 'Nelson', 'port_1');
INSERT INTO Person VALUES ('p2', 'Roxanne', 'Byrd', 'port_1');
INSERT INTO Person VALUES ('p11', 'Sandra', 'Cruz', 'port_3');
INSERT INTO Person VALUES ('p13', 'Bryant', 'Figueroa', 'port_3');
INSERT INTO Person VALUES ('p14', 'Dana', 'Perry', 'port_3');
INSERT INTO Person VALUES ('p15', 'Matt', 'Hunt', 'port_10');
INSERT INTO Person VALUES ('p16', 'Edna', 'Brown', 'port_10');
INSERT INTO Person VALUES ('p12', 'Dan', 'Ball', 'port_3');
INSERT INTO Person VALUES ('p17', 'Ruby', 'Burgess', 'plane_3');
INSERT INTO Person VALUES ('p18', 'Esther', 'Pittman', 'plane_10');
INSERT INTO Person VALUES ('p19', 'Doug', 'Fowler', 'port_17');
INSERT INTO Person VALUES ('p8', 'Bennie', 'Palmer', 'port_2');
INSERT INTO Person VALUES ('p20', 'Thomas', 'Olson', 'port_17');
INSERT INTO Person VALUES ('p21', 'Mona', 'Harrison', 'plane_1');
INSERT INTO Person VALUES ('p22', 'Arlene', 'Massey', 'plane_1');
INSERT INTO Person VALUES ('p23', 'Judith', 'Patrick', 'plane_1');
INSERT INTO Person VALUES ('p24', 'Reginald', 'Rhodes', 'plane_5');
INSERT INTO Person VALUES ('p25', 'Vincent', 'Garcia', 'plane_5');
INSERT INTO Person VALUES ('p26', 'Cheryl', 'Moore', 'plane_5');
INSERT INTO Person VALUES ('p27', 'Michael', 'Rivera', 'plane_8');
INSERT INTO Person VALUES ('p28', 'Luther', 'Matthews', 'plane_8');
INSERT INTO Person VALUES ('p29', 'Moses', 'Parks', 'plane_13');
INSERT INTO Person VALUES ('p3', 'Tanya', 'Nguyen', 'port_1');
INSERT INTO Person VALUES ('p30', 'Ora', 'Steele', 'plane_13');
INSERT INTO Person VALUES ('p31', 'Antonio', 'Flores', 'plane_13');
INSERT INTO Person VALUES ('p32', 'Glenn', 'Ross', 'plane_13');
INSERT INTO Person VALUES ('p33', 'Irma', 'Thomas', 'plane_20');
INSERT INTO Person VALUES ('p34', 'Ann', 'Maldonado', 'plane_20');
INSERT INTO Person VALUES ('p35', 'Jeffrey', 'Cruz', 'port_12');
INSERT INTO Person VALUES ('p36', 'Sonya', 'Price', 'port_12');
INSERT INTO Person VALUES ('p37', 'Tracy', 'Hale', 'port_12');
INSERT INTO Person VALUES ('p38', 'Albert', 'Simmons', 'port_14');
INSERT INTO Person VALUES ('p39', 'Karen', 'Terry', 'port_15');
INSERT INTO Person VALUES ('p4', 'Kendra', 'Jacobs', 'port_1');
INSERT INTO Person VALUES ('p40', 'Glen', 'Kelley', 'port_20');
INSERT INTO Person VALUES ('p41', 'Brooke', 'Little', 'port_3');
INSERT INTO Person VALUES ('p42', 'Daryl', 'Nguyen', 'port_4');
INSERT INTO Person VALUES ('p43', 'Judy', 'Willis', 'port_14');
INSERT INTO Person VALUES ('p44', 'Marco', 'Klein', 'port_15');
INSERT INTO Person VALUES ('p45', 'Angelica', 'Hampton', 'port_16');
INSERT INTO Person VALUES ('p5', 'Jeff', 'Burton', 'port_1');
INSERT INTO Person VALUES ('p6', 'Randal', 'Parks', 'port_1');
INSERT INTO Person VALUES ('p10', 'Lawrence', 'Morgan', 'port_3');
INSERT INTO Person VALUES ('p7', 'Sonya', 'Owens', 'port_2');
INSERT INTO Person VALUES ('p9', 'Marlene', 'Warner', 'port_3');
INSERT INTO Person VALUES ('p46', 'Janice', 'White', 'plane_10');

INSERT INTO Pilot VALUES ('330-12-6907', 'p1', 31, 'dl_10');
INSERT INTO Pilot VALUES ('842-88-1257', 'p2', 9, 'dl_10');
INSERT INTO Pilot VALUES ('369-22-9505', 'p11', 22, 'km_16');
INSERT INTO Pilot VALUES ('513-40-4168', 'p13', 24, 'km_16');
INSERT INTO Pilot VALUES ('454-71-7847', 'p14', 13, 'km_16');
INSERT INTO Pilot VALUES ('153-47-8101', 'p15', 30, 'ja_35');
INSERT INTO Pilot VALUES ('598-47-5172', 'p16', 28, 'ja_35');
INSERT INTO Pilot VALUES ('680-92-5329', 'p12', 24, 'ry_34');
INSERT INTO Pilot VALUES ('865-71-6800', 'p17', 36, 'dl_42');
INSERT INTO Pilot VALUES ('250-86-2784', 'p18', 23, 'lf_20');
INSERT INTO Pilot VALUES ('701-38-2179', 'p8', 12, 'ry_34');
INSERT INTO Pilot VALUES ('750-24-7616', 'p3', 11, 'un_38');
INSERT INTO Pilot VALUES ('776-21-8098', 'p4', 24, 'un_38');
INSERT INTO Pilot VALUES ('933-93-2165', 'p5', 27, 'ba_61');
INSERT INTO Pilot VALUES ('707-84-4555', 'p6', 38, 'ba_61');
INSERT INTO Pilot VALUES ('769-60-1266', 'p10', 15, 'lf_20');
INSERT INTO Pilot VALUES ('450-25-5617', 'p7', 13, 'lf_20');
INSERT INTO Pilot VALUES ('936-44-6941', 'p9', 13, 'lf_20');

INSERT INTO Passenger VALUES ('p21', 771, 700);
INSERT INTO Passenger VALUES ('p22', 374, 200);
INSERT INTO Passenger VALUES ('p23', 414, 400);
INSERT INTO Passenger VALUES ('p24', 292, 500);
INSERT INTO Passenger VALUES ('p25', 390, 300);
INSERT INTO Passenger VALUES ('p26', 302, 600);
INSERT INTO Passenger VALUES ('p27', 470, 400);
INSERT INTO Passenger VALUES ('p28', 208, 400);
INSERT INTO Passenger VALUES ('p29', 292, 700);
INSERT INTO Passenger VALUES ('p30', 686, 500);
INSERT INTO Passenger VALUES ('p31', 547, 400);
INSERT INTO Passenger VALUES ('p32', 257, 500);
INSERT INTO Passenger VALUES ('p33', 564, 600);
INSERT INTO Passenger VALUES ('p34', 211, 200);
INSERT INTO Passenger VALUES ('p35', 233, 500);
INSERT INTO Passenger VALUES ('p36', 293, 400);
INSERT INTO Passenger VALUES ('p37', 552, 700);
INSERT INTO Passenger VALUES ('p38', 812, 700);
INSERT INTO Passenger VALUES ('p39', 541, 400);
INSERT INTO Passenger VALUES ('p40', 441, 700);
INSERT INTO Passenger VALUES ('p41', 875, 300);
INSERT INTO Passenger VALUES ('p42', 691, 500);
INSERT INTO Passenger VALUES ('p43', 572, 300);
INSERT INTO Passenger VALUES ('p44', 572, 500);
INSERT INTO Passenger VALUES ('p45', 663, 500);
INSERT INTO Passenger VALUES ('p46', 690, 5000);

INSERT INTO License VALUES ('p1', 'airbus');
INSERT INTO License VALUES ('p2', 'airbus');
INSERT INTO License VALUES ('p2', 'boeing');
INSERT INTO License VALUES ('p11', 'airbus');
INSERT INTO License VALUES ('p11', 'boeing');
INSERT INTO License VALUES ('p13', 'airbus');
INSERT INTO License VALUES ('p14', 'airbus');
INSERT INTO License VALUES ('p15', 'airbus');
INSERT INTO License VALUES ('p15', 'boeing');
INSERT INTO License VALUES ('p15', 'general');
INSERT INTO License VALUES ('p16', 'airbus');
INSERT INTO License VALUES ('p12', 'boeing');
INSERT INTO License VALUES ('p17', 'airbus');
INSERT INTO License VALUES ('p17', 'boeing');
INSERT INTO License VALUES ('p18', 'airbus');
INSERT INTO License VALUES ('p3', 'airbus');
INSERT INTO License VALUES ('p4', 'airbus');
INSERT INTO License VALUES ('p4', 'boeing');
INSERT INTO License VALUES ('p5', 'airbus');
INSERT INTO License VALUES ('p6', 'airbus');
INSERT INTO License VALUES ('p6', 'boeing');
INSERT INTO License VALUES ('p10', 'airbus');
INSERT INTO License VALUES ('p7', 'airbus');
INSERT INTO License VALUES ('p9', 'airbus');
INSERT INTO License VALUES ('p9', 'boeing');
INSERT INTO License VALUES ('p9', 'general');

INSERT INTO Vacation VALUES ('p21', 'AMS', '0');
INSERT INTO Vacation VALUES ('p22', 'AMS', '0');
INSERT INTO Vacation VALUES ('p23', 'BER', '0');
INSERT INTO Vacation VALUES ('p24', 'MUC', '0');
INSERT INTO Vacation VALUES ('p24', 'CDG', '1');
INSERT INTO Vacation VALUES ('p25', 'MUC', '0');
INSERT INTO Vacation VALUES ('p26', 'MUC', '0');
INSERT INTO Vacation VALUES ('p27', 'BER', '0');
INSERT INTO Vacation VALUES ('p28', 'LGW', '0');
INSERT INTO Vacation VALUES ('p29', 'FCO', '0');
INSERT INTO Vacation VALUES ('p29', 'LHR', '1');
INSERT INTO Vacation VALUES ('p30', 'FCO', '0');
INSERT INTO Vacation VALUES ('p30', 'MAD', '1');
INSERT INTO Vacation VALUES ('p31', 'FCO', '0');
INSERT INTO Vacation VALUES ('p32', 'FCO', '0');
INSERT INTO Vacation VALUES ('p33', 'CAN', '0');
INSERT INTO Vacation VALUES ('p34', 'HND', '0');
INSERT INTO Vacation VALUES ('p35', 'LGW', '0');
INSERT INTO Vacation VALUES ('p36', 'FCO', '0');
INSERT INTO Vacation VALUES ('p37', 'FCO', '0');
INSERT INTO Vacation VALUES ('p37', 'LGW', '1');
INSERT INTO Vacation VALUES ('p37', 'CDG', '2');
INSERT INTO Vacation VALUES ('p38', 'MUC', '0');
INSERT INTO Vacation VALUES ('p39', 'MUC', '0');
INSERT INTO Vacation VALUES ('p40', 'HND', '0');
INSERT INTO Vacation VALUES ('p46', 'LGW', '0');

INSERT INTO Contains VALUES ('americas_hub_exchange', 'leg_4', '0');
INSERT INTO Contains VALUES ('americas_one', 'leg_2', '0');
INSERT INTO Contains VALUES ('americas_one', 'leg_1', '1');
INSERT INTO Contains VALUES ('americas_three', 'leg_31', '0');
INSERT INTO Contains VALUES ('americas_three', 'leg_14', '1');
INSERT INTO Contains VALUES ('americas_two', 'leg_3', '0');
INSERT INTO Contains VALUES ('americas_two', 'leg_22', '1');
INSERT INTO Contains VALUES ('big_europe_loop', 'leg_23', '0');
INSERT INTO Contains VALUES ('big_europe_loop', 'leg_29', '1');
INSERT INTO Contains VALUES ('big_europe_loop', 'leg_16', '2');
INSERT INTO Contains VALUES ('big_europe_loop', 'leg_25', '3');
INSERT INTO Contains VALUES ('big_europe_loop', 'leg_13', '4');
INSERT INTO Contains VALUES ('euro_north', 'leg_16', '0');
INSERT INTO Contains VALUES ('euro_north', 'leg_24', '1');
INSERT INTO Contains VALUES ('euro_north', 'leg_5', '2');
INSERT INTO Contains VALUES ('euro_north', 'leg_14', '3');
INSERT INTO Contains VALUES ('euro_north', 'leg_27', '4');
INSERT INTO Contains VALUES ('euro_north', 'leg_8', '5');
INSERT INTO Contains VALUES ('euro_south', 'leg_21', '0');
INSERT INTO Contains VALUES ('euro_south', 'leg_9', '1');
INSERT INTO Contains VALUES ('euro_south', 'leg_28', '2');
INSERT INTO Contains VALUES ('euro_south', 'leg_11', '3');
INSERT INTO Contains VALUES ('euro_south', 'leg_6', '4');
INSERT INTO Contains VALUES ('euro_south', 'leg_26', '5');
INSERT INTO Contains VALUES ('germany_local', 'leg_9', '0');
INSERT INTO Contains VALUES ('germany_local', 'leg_30', '1');
INSERT INTO Contains VALUES ('germany_local', 'leg_17', '2');
INSERT INTO Contains VALUES ('pacific_rim_tour', 'leg_7', '0');
INSERT INTO Contains VALUES ('pacific_rim_tour', 'leg_10', '1');
INSERT INTO Contains VALUES ('pacific_rim_tour', 'leg_18', '2');
INSERT INTO Contains VALUES ('south_euro_loop', 'leg_16', '0');
INSERT INTO Contains VALUES ('south_euro_loop', 'leg_24', '1');
INSERT INTO Contains VALUES ('south_euro_loop', 'leg_5', '2');
INSERT INTO Contains VALUES ('south_euro_loop', 'leg_12', '3');
INSERT INTO Contains VALUES ('texas_local', 'leg_15', '0');
INSERT INTO Contains VALUES ('texas_local', 'leg_20', '1');
INSERT INTO Contains VALUES ('texas_local', 'leg_19', '2');
INSERT INTO Contains VALUES ('korea_direct', 'leg_32', '0');
