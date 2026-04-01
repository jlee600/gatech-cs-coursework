-- CS4400: Introduction to Database Systems: Monday, March 3, 2025
-- Simple Airline Management System Course Project Mechanics [TEMPLATE] (v0)
-- Views, Functions & Stored Procedures

/* This is a standard preamble for most of our scripts.  The intent is to establish
a consistent environment for the database behavior. */
set global transaction isolation level serializable;
set global SQL_MODE = 'ANSI,TRADITIONAL';
set names utf8mb4;
set SQL_SAFE_UPDATES = 0;

set @thisDatabase = 'flight_tracking';
use flight_tracking;
-- -----------------------------------------------------------------------------
-- stored procedures and views
-- -----------------------------------------------------------------------------
/* Standard Procedure: If one or more of the necessary conditions for a procedure to
be executed is false, then simply have the procedure halt execution without changing
the database state. Do NOT display any error messages, etc. */

-- [_] supporting functions, views and stored procedures
-- -----------------------------------------------------------------------------
/* Helpful library capabilities to simplify the implementation of the required
views and procedures. */
-- -----------------------------------------------------------------------------
drop function if exists leg_time;
delimiter //
create function leg_time (ip_distance integer, ip_speed integer)
	returns time reads sql data
begin
	declare total_time decimal(10,2);
    declare hours, minutes integer default 0;
    set total_time = ip_distance / ip_speed;
    set hours = truncate(total_time, 0);
    set minutes = truncate((total_time - hours) * 60, 0);
    return maketime(hours, minutes, 0);
end //
delimiter ;

-- [1] add_airplane()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new airplane.  A new airplane must be sponsored
by an existing airline, and must have a unique tail number for that airline.
username.  An airplane must also have a non-zero seat capacity and speed. An airplane
might also have other factors depending on it's type, like the model and the engine.  
Finally, an airplane must have a new and database-wide unique location
since it will be used to carry passengers. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_airplane;
delimiter //
create procedure add_airplane (in ip_airlineID varchar(50), in ip_tail_num varchar(50),
	in ip_seat_capacity integer, in ip_speed integer, in ip_locationID varchar(50),
    in ip_plane_type varchar(100), in ip_maintenanced boolean, in ip_model varchar(50),
    in ip_neo boolean)
sp_main: begin

	-- Ensure that the plane type is valid: Boeing, Airbus, or neither
    if ip_plane_type not like 'boeing' and ip_plane_type not like 'airbus' and ip_plane_type is not null then leave sp_main; end if;
    -- Ensure that the type-specific attributes are accurate for the type
    if ip_plane_type like 'boeing' and (ip_maintenanced is null or ip_model is null) then leave sp_main;
    elseif ip_plane_type like 'airbus' and ip_neo is null then leave sp_main; end if;
    -- Ensure that the airplane and location values are new and unique
    if ip_tail_num in (select tail_num from airplane) then leave sp_main; end if;
    if ip_locationID in (select locationID from location) then leave sp_main; 
    else insert into location values (ip_locationID);
    end if;
    -- Add airplane and location into respective tables
    if ip_seat_capacity <= 0 or ip_speed <= 0 then leave sp_main; end if;
    insert into airplane values (ip_airlineID, ip_tail_num, ip_seat_capacity, ip_speed, ip_locationID, ip_plane_type, ip_maintenanced, ip_model, ip_neo);

end //
delimiter ;

-- [2] add_airport()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new airport.  A new airport must have a unique
identifier along with a new and database-wide unique location if it will be used
to support airplane takeoffs and landings.  An airport may have a longer, more
descriptive name.  An airport must also have a city, state, and country designation. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_airport;
delimiter //
create procedure add_airport (in ip_airportID char(3), in ip_airport_name varchar(200),
    in ip_city varchar(100), in ip_state varchar(100), in ip_country char(3), in ip_locationID varchar(50))
sp_main: begin

	-- Ensure that the airport and location values are new and unique
    if ip_airportID in (select airportID from airport) then leave sp_main; end if;
    if ip_locationID in (select locationID from location) then leave sp_main; 
    else insert into location values (ip_locationID);
    end if;
    -- Add airport and location into respective tables
    if ip_city is null or ip_state is null or ip_country is null then leave sp_main; end if;
    insert into airport values (ip_airportID, ip_airport_name, ip_city, ip_state, ip_country, ip_locationID);

end //
delimiter ;

-- [3] add_person()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new person.  A new person must reference a unique
identifier along with a database-wide unique location used to determine where the
person is currently located: either at an airport, or on an airplane, at any given
time.  A person must have a first name, and might also have a last name.

A person can hold a pilot role or a passenger role (exclusively).  As a pilot,
a person must have a tax identifier to receive pay, and an experience level.  As a
passenger, a person will have some amount of frequent flyer miles, along with a
certain amount of funds needed to purchase tickets for flights. */
-- -----------------------------------------------------------------------------
drop procedure if exists add_person;
delimiter //
create procedure add_person (in ip_personID varchar(50), in ip_first_name varchar(100),
    in ip_last_name varchar(100), in ip_locationID varchar(50), in ip_taxID varchar(50),
    in ip_experience integer, in ip_miles integer, in ip_funds integer)
sp_main: begin

	-- Ensure that the location is valid
    if ip_locationID not in (select locationID from location) then leave sp_main; end if;
    -- Ensure that the persion ID is unique
    if ip_personID in (select personID from person) or ip_first_name is null then leave sp_main; end if;
    -- Ensure that the person is a pilot or passenger
    -- Add them to the person table as well as the table of their respective role
	insert into person values (ip_personID, ip_first_name, ip_last_name, ip_locationID);
	if ip_taxID is null then 
		insert into passenger (personID, miles, funds) values (ip_personID, ip_miles, ip_funds);
	else
		insert into pilot (personID, taxID, experience) values (ip_personID, ip_taxID, ip_experience);
	end if;
    
end //
delimiter ;

-- [4] grant_or_revoke_pilot_license()
-- -----------------------------------------------------------------------------
/* This stored procedure inverts the status of a pilot license.  If the license
doesn't exist, it must be created; and, if it aready exists, then it must be removed. */
-- -----------------------------------------------------------------------------
drop procedure if exists grant_or_revoke_pilot_license;
delimiter //
create procedure grant_or_revoke_pilot_license (in ip_personID varchar(50), in ip_license varchar(100))
sp_main: begin

	-- Ensure that the person is a valid pilot
    if ip_personID not in (select personID from pilot) then leave sp_main; end if; 
    -- If license exists, delete it, otherwise add the license
    if ip_personID in (select personID from pilot_licenses where personID = ip_personID and license = ip_license) then
		delete from pilot_licenses where personID = ip_personID and license = ip_license;
	else
		insert into pilot_licenses values (ip_personID, ip_license);
	end if; 

end //
delimiter ;

-- [5] offer_flight()
-- -----------------------------------------------------------------------------
/* This stored procedure creates a new flight.  The flight can be defined before
an airplane has been assigned for support, but it must have a valid route.  And
the airplane, if designated, must not be in use by another flight.  The flight
can be started at any valid location along the route except for the final stop,
and it will begin on the ground.  You must also include when the flight will
takeoff along with its cost. */
-- -----------------------------------------------------------------------------
drop procedure if exists offer_flight;
delimiter //
create procedure offer_flight (in ip_flightID varchar(50), in ip_routeID varchar(50),
    in ip_support_airline varchar(50), in ip_support_tail varchar(50), in ip_progress integer,
    in ip_next_time time, in ip_cost integer)
sp_main: begin

	declare route_len int;
	-- Ensure that the airplane exists
    if ip_support_tail not in (select tail_num from airplane) and ip_support_tail is not null then leave sp_main; end if;
    -- Ensure that the route exists
    if ip_routeID not in (select routeID from route) then leave sp_main; end if; 
    -- Ensure that the progress is less than the length of the route
    select count(*) into route_len from route_path where routeID = ip_routeID;
	if ip_progress >= route_len then leave sp_main; end if; 
    -- Create the flight with the airplane starting in on the ground
	if ip_flightID in (select flightID from flight) or ip_flightID is null then leave sp_main; end if; 
    insert into flight values (ip_flightID, ip_routeID, ip_support_airline, ip_support_tail, ip_progress, 'on_ground', ip_next_time, ip_cost);
    
end //
delimiter ;

-- [6] flight_landing()
-- -----------------------------------------------------------------------------
/* This stored procedure updates the state for a flight landing at the next airport
along it's route.  The time for the flight should be moved one hour into the future
to allow for the flight to be checked, refueled, restocked, etc. for the next leg
of travel.  Also, the pilots of the flight should receive increased experience, and
the passengers should have their frequent flyer miles updated. */
-- -----------------------------------------------------------------------------
drop procedure if exists flight_landing;
delimiter //
create procedure flight_landing (in ip_flightID varchar(50))
sp_main: begin
	
    declare curr_dist int;
    declare curr_routeID varchar(50);
    declare curr_tailNum varchar(50);
    declare curr_status varchar(100);
    declare curr_progress int; 
	select routeid, support_tail, airplane_status, progress into curr_routeID, curr_tailNum, curr_status, curr_progress from flight where flightid = ip_flightid;
	-- Ensure that the flight exists
    if ip_flightID not in (select flightID from flight) then leave sp_main; end if; 
    -- Ensure that the flight is in the air
    if curr_status not like 'in%' then leave sp_main; end if;
    -- Increment the pilot's experience by 1
    update pilot set experience = experience + 1 where commanding_flight = ip_flightID;
    -- Increment the frequent flyer miles of all passengers on the plane
    select l.distance into curr_dist from route_path rp join leg l on rp.legid = l.legid where rp.routeid = curr_routeid and rp.sequence = curr_progress;
    update passenger p join (select psg.personid as pid from passenger psg join person p on psg.personid = p.personid join airplane a on p.locationid = a.locationid where a.tail_num = curr_tailnum) as d on p.personid = d.pid
	set p.miles = p.miles + curr_dist;
    -- Update the status of the flight and increment the next time to 1 hour later
		-- Hint: use addtime()
	update flight set airplane_status = 'on_ground', next_time = ADDTIME(next_time, '01:00:00') where flightID = ip_flightID;

end //
delimiter ;


-- [7] flight_takeoff()
-- -----------------------------------------------------------------------------
/* This stored procedure updates the state for a flight taking off from its current
airport towards the next airport along it's route.  The time for the next leg of
the flight must be calculated based on the distance and the speed of the airplane.
And we must also ensure that Airbus and general planes have at least one pilot
assigned, while Boeing must have a minimum of two pilots. If the flight cannot take
off because of a pilot shortage, then the flight must be delayed for 30 minutes. */
-- -----------------------------------------------------------------------------
drop procedure if exists flight_takeoff;
delimiter //
create procedure flight_takeoff (in ip_flightID varchar(50))
sp_main: begin
	
    declare leg_count int; 
    declare curr_plane varchar(100);
    declare pilot_count int; 
    declare flight_time time; 
    declare curr_speed int;
    declare curr_dist int;
	declare curr_routeID varchar(50);
    declare curr_tailNum varchar(50);
    declare curr_status varchar(100);
    declare curr_progress int; 
	select routeid, support_tail, airplane_status, progress into curr_routeID, curr_tailNum, curr_status, curr_progress from flight where flightID = ip_flightID;
	-- Ensure that the flight exists
    if ip_flightID not in (select flightID from flight) then leave sp_main; end if;
    -- Ensure that the flight is on the ground
	if curr_status not like 'on%' then leave sp_main; end if;
    -- Ensure that the flight has another leg to fly
	select count(*) into leg_count from route_path where routeid = curr_routeid;
    if leg_count <= 1 then leave sp_main; end if;
    -- Ensure that there are enough pilots (1 for Airbus and general, 2 for Boeing)
		-- If there are not enough, move next time to 30 minutes later
	select plane_type into curr_plane from airplane where tail_num = curr_tailNum;
	select count(*) into pilot_count from pilot where commanding_flight = ip_flightID;
    if (curr_plane like 'airbus' and pilot_count < 1) or (curr_plane like 'boeing' and pilot_count < 2) then
		update flight set nextime = ADDTIME(next_time, '00:30:00') where flightID = ip_flightID; leave sp_main;
	end if; 
	-- Increment the progress and set the status to in flight
    update flight set progress = progress + 1, airplane_status = 'in_flight' where flightID = ip_flightID;
    -- Calculate the flight time using the speed of airplane and distance of leg
    select l.distance into curr_dist from route_path rp join leg l on rp.legid = l.legid where rp.routeid = curr_routeid and rp.sequence = curr_progress + 1;
    select speed into curr_speed from airplane where tail_num = curr_tailNum; 
    set flight_time = leg_time(curr_dist, curr_speed);
    -- Update the next time using the flight time
    update flight set next_time = ADDTIME(next_time, flight_time) where flightID = ip_flightID; 
	
end //
delimiter ;

-- [8] passengers_board()
-- -----------------------------------------------------------------------------
/* This stored procedure updates the state for passengers getting on a flight at
its current airport.  The passengers must be at the same airport as the flight,
and the flight must be heading towards that passenger's desired destination.
Also, each passenger must have enough funds to cover the flight.  Finally, there
must be enough seats to accommodate all boarding passengers. */
-- -----------------------------------------------------------------------------
drop procedure if exists passengers_board;
delimiter //
create procedure passengers_board (in ip_flightID varchar(50))
sp_main: begin
	
    declare leg_count int;
    declare on_board int;
    declare curr_loc varchar(50);
    declare curr_dest char(3);
    declare psg_eligible int;
    
	declare curr_routeID varchar(50);
    declare curr_airline varchar(50);
    declare curr_tailNum varchar(50);
    declare curr_status varchar(100);
    declare curr_progress int; 
    declare curr_cost int;
	-- Ensure the flight exists
    if ip_flightID not in (select flightID from flight) then select 'invalid flight'; leave sp_main; end if;
    -- Assign values to the variables
	select routeid, support_airline, support_tail, airplane_status, progress, cost into curr_routeID, curr_airline, curr_tailNum, curr_status, curr_progress, curr_cost from flight where flightID = ip_flightID;
	-- Ensure that the flight is on the ground
    if curr_status not like 'on%' then select 'flight in the air'; leave sp_main; end if; 
	-- Ensure that the flight has further legs to be flown
    select count(*) into leg_count from route_path where routeID = curr_routeID;
    if curr_progress >= leg_count then select 'Not enough left'; leave sp_main; end if;
	-- Determine the number of passengers already on the flight
    select count(*) into on_board from passenger psg join person p on psg.personID = p.personID 
    where p.locationID = (select locationID from airplane where airlineID = curr_airline and tail_num = curr_tailNum);
	-- Use the following to check:
		-- The airport the airplane is currently located at & destination of the current flight
        select a.locationID, l.arrival into curr_loc, curr_dest from flight f join route_path rp on f.routeID = rp.routeID and rp.sequence = curr_progress + 1 join leg l on rp.legID = l.legID join airport a on l.departure = a.airportID 
        where f.flightID = ip_flightID and f.support_airline = curr_airline;
		-- The passengers are located at that airport
		-- The passenger's immediate next destination matches that of the flight
		-- The passenger has enough funds to afford the flight
	-- Count the number of passengers eligible to board the flight
	select count(*) into psg_eligible from person p join passenger_vacations pv on p.personID = pv.personID join passenger psg on p.personID = psg.personID
	where p.locationID = curr_loc and pv.sequence = 1 and pv.airportID = curr_dest and psg.funds >= curr_cost;
    -- Check if there enough seats for all the passengers
    if psg_eligible + on_board > (select seat_capacity from airplane where tail_num = curr_tailNum and airlineID = curr_airline) then select 'Airline overbooking'; leave sp_main; end if;
    -- If not, do not add board any passengers
	-- If there are, board them and deduct their fund
    -- update location of the passenger

	update passenger psg join (
		select p.personID as pid from person p join passenger psg on p.personID = psg.personID join passenger_vacations pv on p.personID = pv.personID 
        where p.locationID = curr_loc and pv.sequence = 1 and pv.airportID = curr_dest and psg.funds >= curr_cost) as sub on psg.personID = sub.pid
	set psg.funds = psg.funds - curr_cost;
    
    update person p join (
       select p.personID as pid from person p join passenger_vacations pv on p.personID = pv.personID join passenger pa on p.personID = pa.personID
       where p.locationID = curr_loc and pv.sequence = 1 and pv.airportID = curr_dest
    ) as d on p.personID = d.pid
    set p.locationID = (select locationID from airplane where tail_num = curr_tailNum and airlineID = curr_airline);
    
	update airline set revenue = revenue + (psg_eligible * curr_cost) where airlineID = curr_airline;

end //
delimiter ;

-- [9] passengers_disembark()
-- -----------------------------------------------------------------------------
/* This stored procedure updates the state for passengers getting off of a flight
at its current airport.  The passengers must be on that flight, and the flight must
be located at the destination airport as referenced by the ticket. */
-- -----------------------------------------------------------------------------

drop procedure if exists passengers_disembark;
delimiter //
create procedure passengers_disembark (in ip_flightID varchar(50))
sp_main: begin

	declare curr_arrival_airportid char(3);
    declare curr_airport_locationid varchar(50);
    declare curr_plane_locationid varchar(50);
    declare curr_airlineid varchar(50);
    declare curr_tailnum varchar(50);

    select l.arrival
    into curr_arrival_airportid
    from flight f
    join route_path rp on f.routeid = rp.routeid and rp.sequence = f.progress
    join leg l on rp.legid = l.legid
    where f.flightid = ip_flightid and f.airplane_status = 'on_ground';

    if curr_arrival_airportid is null then leave sp_main; end if;

    select locationid
    into curr_airport_locationid
    from airport
    where airportid = curr_arrival_airportid;

    if curr_airport_locationid is null then leave sp_main; end if;

    select support_airline, support_tail
    into curr_airlineid, curr_tailnum
    from flight
    where flightid = ip_flightid;

    if curr_airlineid is null or curr_tailnum is null then leave sp_main; end if;

    select locationid
    into curr_plane_locationid
    from airplane
    where airlineid = curr_airlineid and tail_num = curr_tailnum;

    if curr_plane_locationid is null then leave sp_main; end if;

    update person p
    join passenger_vacations pv on p.personid = pv.personid
    join (
        select personid, min(sequence) as min_seq
        from passenger_vacations
        group by personid
    ) next_stop on pv.personid = next_stop.personid and pv.sequence = next_stop.min_seq
    set p.locationid = curr_airport_locationid
    where p.locationid = curr_plane_locationid
      and pv.airportid = curr_arrival_airportid;

end //
delimiter ;

-- [10] assign_pilot()
-- -----------------------------------------------------------------------------
/* This stored procedure assigns a pilot as part of the flight crew for a given
flight.  The pilot being assigned must have a license for that type of airplane,
and must be at the same location as the flight.  Also, a pilot can only support
one flight (i.e. one airplane) at a time.  The pilot must be assigned to the flight
and have their location updated for the appropriate airplane. */
-- -----------------------------------------------------------------------------
drop procedure if exists assign_pilot;
delimiter //
create procedure assign_pilot (in ip_flightID varchar(50), ip_personID varchar(50))
sp_main: begin

	declare plane_model varchar(100);
    declare curr_loc varchar(50);
	-- Ensure the flight exists
    if not exists (select 1 from flight where flightID = ip_flightID) then leave sp_main; end if;
    
    -- Ensure that the flight is on the ground
    if (select airplane_status from flight where flightID = ip_flightID) != 'on_ground' then leave sp_main; end if;
    
    -- Ensure that the flight has further legs to be flown
    if (select max(sequence) from route_path where routeID = (select routeID from flight where flightID = ip_flightID)) 
    = (select progress from flight where flightID = ip_flightID) then leave sp_main; end if;
    
    -- Ensure that the pilot exists and is not already assigned
    if not exists (select 1 from pilot where personID = ip_personID) then leave sp_main; end if;
    if (select commanding_flight from pilot where personID = ip_personID) is not null then leave sp_main; end if;
    
        -- Ensure that the pilot has the appropriate license
    select plane_type into plane_model from airplane where tail_num = (select support_tail from flight where flightID = ip_flightID);
    if plane_model not in (select license from pilot_licenses where personID = ip_personID) then leave sp_main; end if;
    
    -- Ensure the pilot is located at the airport of the plane that is supporting the flight
    select locationID into curr_loc from airport where airportID = (select departure from leg where legID = 
    (select legID from route_path where routeID = (select routeID from flight where flightID = ip_flightID) 
    and sequence = (select progress + 1 from flight where flightID = ip_flightID)));
    
    if (select locationID from person where personID = ip_personID) != curr_loc then leave sp_main; end if;
    
    -- Assign the pilot to the flight and update their location to be on the plane
    update pilot
		set commanding_flight = ip_flightID
        where personID = ip_personID;
    
    update person
		set locationID = (select locationID from airplane 
		where tail_num = (select support_tail from flight where flightID = ip_flightID))
        where personID = ip_personID;
end //
delimiter ;

-- [11] recycle_crew()
-- -----------------------------------------------------------------------------
/* This stored procedure releases the assignments for a given flight crew.  The
flight must have ended, and all passengers must have disembarked. */
-- -----------------------------------------------------------------------------
drop procedure if exists recycle_crew;
delimiter //
create procedure recycle_crew (in ip_flightID varchar(50))
sp_main: begin

    declare curr_routeid varchar(50);
    declare curr_progress int;
    declare curr_max_seq int;
    declare curr_plane_loc varchar(50);
    declare curr_arrival_port char(3);

    -- check: flight must be on the ground
    if (select airplane_status from flight where flightid = ip_flightid) != 'on_ground' then
        leave sp_main;
    end if;

    -- get flight route and progress info
    select routeid, progress into curr_routeid, curr_progress
    from flight
    where flightid = ip_flightid;

    -- check: no remaining route legs
    select max(sequence) into curr_max_seq
    from route_path
    where routeid = curr_routeid;

    if curr_progress != curr_max_seq then
        leave sp_main;
    end if;

    -- get plane's current location
    select a.locationid into curr_plane_loc
    from airplane a
    join flight f on f.support_tail = a.tail_num and f.flightid = ip_flightid;

    -- check: all passengers have disembarked (none at plane location)
    if exists (
        select 1
        from person p
        join passenger pa on pa.personid = p.personid
        where p.locationid = curr_plane_loc
    ) then
        leave sp_main;
    end if;

    -- get final leg's arrival airport
    select l.arrival into curr_arrival_port
    from route_path rp
    join leg l on l.legid = rp.legid
    where rp.routeid = curr_routeid and rp.sequence = curr_max_seq;

    -- move pilots to that airport
    update person
    set locationid = (
        select locationid from airport where airportid = curr_arrival_port
    )
    where personid in (
        select personid from pilot where commanding_flight = ip_flightid
    );

    -- unassign pilots
    update pilot
    set commanding_flight = null
    where commanding_flight = ip_flightid;
end //
delimiter ;

-- [12] retire_flight()
-- -----------------------------------------------------------------------------
/* This stored procedure removes a flight that has ended from the system.  The
flight must be on the ground, and either be at the start its route, or at the
end of its route.  And the flight must be empty - no pilots or passengers. */
-- -----------------------------------------------------------------------------
drop procedure if exists retire_flight;
delimiter //
create procedure retire_flight (in ip_flightID varchar(50))
sp_main: begin
	declare route_id varchar(50);
    declare flight_status varchar(100);
    declare progress_value int;
    declare max_sequence int;
    declare plane_location varchar(50);
    declare onboard_count int;

    -- get status, route, progress
    select routeid, airplane_status, progress
    into route_id, flight_status, progress_value
    from flight
    where flightid = ip_flightid;

    -- ensure the flight is on the ground
    if flight_status != 'on_ground' then leave sp_main; end if;

    -- ensure it's at either the beginning or end of the route
    select max(sequence) into max_sequence
    from route_path
    where routeid = route_id;

    if progress_value != 0 and progress_value != max_sequence then leave sp_main; end if;

    -- get airplane's location
    select locationid into plane_location
    from airplane
    where (airlineid, tail_num) = (
        select support_airline, support_tail
        from flight
        where flightid = ip_flightid
    );

    -- check if any people are still onboard
    select count(*) into onboard_count
    from person
    where locationid = plane_location;

    if onboard_count > 0 then
        leave sp_main;
    end if;

    -- delete the flight
    delete from flight where flightid = ip_flightid;

end //
delimiter ;

-- [13] simulation_cycle()
-- -----------------------------------------------------------------------------
/* This stored procedure executes the next step in the simulation cycle.  The flight
with the smallest next time in chronological order must be identified and selected.
If multiple flights have the same time, then flights that are landing should be
preferred over flights that are taking off.  Similarly, flights with the lowest
identifier in alphabetical order should also be preferred.

If an airplane is in flight and waiting to land, then the flight should be allowed
to land, passengers allowed to disembark, and the time advanced by one hour until
the next takeoff to allow for preparations.

If an airplane is on the ground and waiting to takeoff, then the passengers should
be allowed to board, and the time should be advanced to represent when the airplane
will land at its next location based on the leg distance and airplane speed.

If an airplane is on the ground and has reached the end of its route, then the
flight crew should be recycled to allow rest, and the flight itself should be
retired from the system. */
-- -----------------------------------------------------------------------------
drop procedure if exists simulation_cycle;
delimiter //
create procedure simulation_cycle ()
sp_main: begin

    declare curr_flightid varchar(50);
    declare curr_status varchar(100);
    declare curr_progress int;
    declare curr_max_seq int;
    declare curr_routeid varchar(50);

    select flightid
    into curr_flightid
    
    from flight
    order by next_time asc,
             case when airplane_status = 'in_flight' then 0 else 1 end,
             flightid asc
    limit 1;

    if curr_flightid is null then
        leave sp_main;
    end if;

    select airplane_status, progress, routeid
    into curr_status, curr_progress, curr_routeid
    from flight
    where flightid = curr_flightid;

    if curr_status = 'in_flight' then
        call flight_landing(curr_flightid);
        call passengers_disembark(curr_flightid);

        select max(sequence) into curr_max_seq from route_path where routeid = curr_routeid;
        if curr_progress + 1 = curr_max_seq then
            call recycle_crew(curr_flightid);
            call retire_flight(curr_flightid);
        end if;

    elseif curr_status = 'on_ground' then
        call passengers_board(curr_flightid);
        call flight_takeoff(curr_flightid);
    end if;

end //
delimiter ;

-- [14] flights_in_the_air()
-- -----------------------------------------------------------------------------
/* This view describes where flights that are currently airborne are located. 
We need to display what airports these flights are departing from, what airports 
they are arriving at, the number of flights that are flying between the 
departure and arrival airport, the list of those flights (ordered by their 
flight IDs), the earliest and latest arrival times for the destinations and the 
list of planes (by their respective flight IDs) flying these flights. */
-- -----------------------------------------------------------------------------
create or replace view flights_in_the_air (departing_from, arriving_at, num_flights,
	flight_list, earliest_arrival, latest_arrival, airplane_list) as
select 
	departure as departing_from,
    arrival as arriving_at,
    COUNT(*) as num_flights,
    GROUP_CONCAT(flightID order by flightID separator ',') as flight_list,
    MIN(next_time) as earliest_arrival,
    MAX(next_time) as latest_arrival,
    GROUP_CONCAT(locationID order by flightID separator ',') as airplane_list
from leg natural join route_path rp natural join flight f join airplane a on f.support_tail = a.tail_num
where airplane_status = 'in_flight' and sequence = progress
group by departure, arrival;

-- [15] flights_on_the_ground()
-- ------------------------------------------------------------------------------
/* This view describes where flights that are currently on the ground are 
located. We need to display what airports these flights are departing from, how 
many flights are departing from each airport, the list of flights departing from 
each airport (ordered by their flight IDs), the earliest and latest arrival time 
amongst all of these flights at each airport, and the list of planes (by their 
respective flight IDs) that are departing from each airport.*/
-- ------------------------------------------------------------------------------
create or replace view flights_on_the_ground (departing_from, num_flights,
	flight_list, earliest_arrival, latest_arrival, airplane_list) as 
(select arrival as departing_from, count(*) as num_flights,
	GROUP_CONCAT(flightID order by flightID separator ',') as flight_list,
	MIN(next_time) as earliest_arrival,
    MAX(next_time) as latest_arrival,
    GROUP_CONCAT(locationID order by flightID separator ',') as airplane_list
from flight f 
join route_path rp on f.routeID = rp.routeID
join leg l on l.legID = rp.legID
join airplane a on f.support_tail = a.tail_num
where airplane_status = 'on_ground' and (sequence - progress = 0)
group by departure, arrival)

union

(select 
	departure as departing_from,
    COUNT(*) as num_flights,
    GROUP_CONCAT(flightID order by flightID separator ',') as flight_list,
    MIN(next_time) as earliest_arrival,
    MAX(next_time) as latest_arrival,
    GROUP_CONCAT(locationID order by flightID separator ',') as airplane_list
from leg natural join route_path rp natural join flight f join airplane a on f.support_tail = a.tail_num
where airplane_status = 'on_ground' and (sequence = 1 and progress = 0)
group by departure, arrival);

-- [16] people_in_the_air()
-- -----------------------------------------------------------------------------
/* This view describes where people who are currently airborne are located. We 
need to display what airports these people are departing from, what airports 
they are arriving at, the list of planes (by the location id) flying these 
people, the list of flights these people are on (by flight ID), the earliest 
and latest arrival times of these people, the number of these people that are 
pilots, the number of these people that are passengers, the total number of 
people on the airplane, and the list of these people by their person id. */
-- -----------------------------------------------------------------------------
create or replace view people_in_the_air (departing_from, arriving_at, num_airplanes,
	airplane_list, flight_list, earliest_arrival, latest_arrival, num_pilots,
	num_passengers, joint_pilots_passengers, person_list) as
    
    select l.departure as departing_from, l.arrival as arriving_at, 
    COUNT(distinct apn.tail_num) as num_airplanes,
    GROUP_CONCAT(distinct apn.locationID order by apn.locationID separator ',') as airplane_list,
	GROUP_CONCAT(distinct f.flightID order by f.flightID separator ',') as flight_list,
    MIN(f.next_time) AS earliest_arrival,
	MAX(f.next_time) AS latest_arrival,
    SUM(case when pt.commanding_flight is not null then 1 else 0 end) as num_pilots,
	SUM(case when pr.miles is not null then 1 else 0 end) as num_passengers,
	COUNT(distinct p.personID) as joint_pilots_passengers,
    GROUP_CONCAT(distinct p.personID order by p.personID separator ',') as person_list
    
	from flight f
	join route_path rp on f.routeID = rp.routeID and f.progress = rp.sequence
	join leg l on rp.legID = l.legID
	join airplane apn on f.support_tail = apn.tail_num
	left join person p on apn.locationID = p.locationID
	left join pilot pt on p.personID = pt.personID
	left join passenger pr on p.personID = pr.personID
    
    where f.airplane_status = 'in_flight'
    group by l.departure, l.arrival;


-- [17] people_on_the_ground()
-- -----------------------------------------------------------------------------
/* This view describes where people who are currently on the ground and in an 
airport are located. We need to display what airports these people are departing 
from by airport id, location id, and airport name, the city and state of these 
airports, the number of these people that are pilots, the number of these people 
that are passengers, the total number people at the airport, and the list of 
these people by their person id. */
-- -----------------------------------------------------------------------------
create or replace view people_on_the_ground (departing_from, airport, airport_name,
	city, state, country, num_pilots, num_passengers, joint_pilots_passengers, person_list) as
	select apt.airportID as departing_from, apt.locationID as airport, 
    apt.airport_name, apt.city, apt.state, apt.country,
	  SUM(case when pt.taxID is not null then 1 else 0 end) as num_pilots,
	  SUM(case when ps.miles is not null then 1 else 0 end) as num_passengers,
	  COUNT(distinct p.personID) as joint_pilots_passengers,
	  GROUP_CONCAT(distinct p.personID order by p.personID separator ',') as person_list
	from person p
	left join pilot pt on p.personID = pt.personID
	left join passenger ps on p.personID = ps.personID
	join airport apt on p.locationID = apt.locationID
	where p.locationID like 'port_%'
	group by apt.airportID, apt.locationID, apt.airport_name, apt.city, apt.state, apt.country;

-- [18] route_summary()
-- -----------------------------------------------------------------------------
/* This view will give a summary of every route. This will include the routeID, 
the number of legs per route, the legs of the route in sequence, the total 
distance of the route, the number of flights on this route, the flightIDs of 
those flights by flight ID, and the sequence of airports visited by the route. */
-- -----------------------------------------------------------------------------
create or replace view route_summary (route, num_legs, leg_sequence, route_length,
	num_flights, flight_list, airport_sequence) as
	select rp.routeID as route, COUNT(*) as num_legs, GROUP_CONCAT(rp.legID order by rp.sequence separator ',') AS leg_sequence,
	  SUM(l.distance) AS route_length,
      (
        select COUNT(*) 
	    from flight f 
		where f.routeID = rp.routeID
	  ) as num_flights,
	  (
		select GROUP_CONCAT(distinct f.flightID order by f.flightID separator ',')
		from flight f 
		where f.routeID = rp.routeID
	  ) as flight_list,
	  GROUP_CONCAT(CONCAT(l.departure, '->', l.arrival) order by rp.sequence separator ',') as airport_sequence
	from route_path rp
	join leg l on rp.legID = l.legID
	group by rp.routeID;

-- [19] alternative_airports()
-- -----------------------------------------------------------------------------
/* This view displays airports that share the same city and state. It should 
specify the city, state, the number of airports shared, and the lists of the 
airport codes and airport names that are shared both by airport ID. */
-- -----------------------------------------------------------------------------

create or replace view alternative_airports (city, state, country, num_airports,
	airport_code_list, airport_name_list) as
	select ac.city, ac.state, ac.country, ac.num_airports, ac.airport_code_list, an.airport_name_list
		from (
		  select city,state, MAX(country) AS country, COUNT(*) AS num_airports, GROUP_CONCAT(airportID ORDER BY airportID SEPARATOR ',') AS airport_code_list
		  from airport
		  group by city, state
		  having COUNT(*) > 1
		) ac
		join (
		  select city, state, GROUP_CONCAT(airport_name ORDER BY airportID SEPARATOR ',') AS airport_name_list
		  from airport
		  group by city, state
		  having COUNT(*) > 1
		) an
		on ac.city = an.city and ac.state = an.state;
