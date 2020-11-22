/* Welcome to the SQL mini project. You will carry out this project partly in
the PHPMyAdmin interface, and partly in Jupyter via a Python connection.

This is Tier 2 of the case study, which means that there'll be less guidance for you about how to setup
your local SQLite connection in PART 2 of the case study. This will make the case study more challenging for you: 
you might need to do some digging, aand revise the Working with Relational Databases in Python chapter in the previous resource.

Otherwise, the questions in the case study are exactly the same as with Tier 1. 

PART 1: PHPMyAdmin
You will complete questions 1-9 below in the PHPMyAdmin interface. 
Log in by pasting the following URL into your browser, and
using the following Username and Password:

URL: https://sql.springboard.com/
Username: student
Password: learn_sql@springboard

The data you need is in the "country_club" database. This database
contains 3 tables:
    i) the "Bookings" table,
    ii) the "Facilities" table, and
    iii) the "Members" table.

In this case study, you'll be asked a series of questions. You can
solve them using the platform, but for the final deliverable,
paste the code for each solution into this script, and upload it
to your GitHub.

Before starting with the questions, feel free to take your time,
exploring the data, and getting acquainted with the 3 tables. */


/* QUESTIONS 
/* Q1: Some of the facilities charge a fee to members, but some do not.
Write a SQL query to produce a list of the names of the facilities that do. */

/* A1: SELECT name, membercost FROM `Facilities` WHERE membercost > 0 */




/* Q2: How many facilities do not charge a fee to members? */

/* A2: SELECT COUNT(*) FROM `Facilities` WHERE membercost = 0 */




/* Q3: Write an SQL query to show a list of facilities that charge a fee to members,
where the fee is less than 20% of the facility's monthly maintenance cost.
Return the facid, facility name, member cost, and monthly maintenance of the
facilities in question. */


/* A3:
SELECT facid, name, membercost, monthlymaintenance, (membercost / monthlymaintenance) as feeperc 
FROM `Facilities`
WHERE membercost / monthlymaintenance < 0.20
*/


/* A3 w/o feeperc:
SELECT facid, name, membercost, monthlymaintenance
FROM `Facilities`
WHERE membercost / monthlymaintenance < 0.20
*/





/* Q4: Write an SQL query to retrieve the details of facilities with ID 1 and 5.
Try writing the query without using the OR operator. */

/* A4:
SELECT *
FROM `Facilities`
WHERE name LIKE '%2'
*/

/* A4 alternative:
SELECT *
FROM `Facilities` AS f
WHERE f.facid IN 
	(SELECT (CASE WHEN f.facid = 1 THEN f.facid
     WHEN f.facid = 5 THEN f.facid
     ELSE NULL END) AS subquery)
*/


/* extra */
/* wrong A4:
SELECT *
FROM `Facilities`
WHERE facid =1
OR facid =5
*/




/* Q5: Produce a list of facilities, with each labelled as
'cheap' or 'expensive', depending on if their monthly maintenance cost is
more than $100. Return the name and monthly maintenance of the facilities
in question. */

/* A5: 
SELECT name, monthlymaintenance,
(CASE WHEN monthlymaintenance < 100
THEN 'cheap'
ELSE 'expensive'
END) AS monthlymaintenancedescription
FROM `Facilities`
*/




/* Q6: You'd like to get the first and last name of the last member(s)
who signed up. Try not to use the LIMIT clause for your solution. */
*/




/* A6:
SELECT firstname,
	surname,
	joindate
FROM `Members`
WHERE joindate IN
(SELECT MAX(joindate) as maxjoindate FROM `Members`)
*/

/* lesser A6:
SELECT firstname, surname, joindate FROM `Members` ORDER BY joindate DESC LIMIT 0, 1
*/


/* wrong A6:
SELECT firstname, surname FROM `Members`
*/

/* wrong A6:
SELECT firstname, surname FROM `Members` WHERE joindate IS NOT NULL
*/

/* does not work A6:
SELECT firstname,
    surname,
    joindate
FROM `Members`
WHERE joindate IN MAX(joindate)
*/



/* Q7: Produce a list of all members who have used a tennis court.
Include in your output the name of the court, and the name of the member
formatted as a single column. Ensure no duplicate data, and order by
the member name. */

/* A7:
SELECT DISTINCT f.name, concat(surname, ' ',firstname) as membername FROM `Bookings` as b
LEFT JOIN `Facilities`as f
ON  b.facid = f.facid
LEFT JOIN `Members` as m
ON m.memid = b.memid
WHERE name = 'Tennis Court 1' OR name = 'Tennis Court 2'
ORDER BY membername
*/

/* alternative A7:
SELECT DISTINCT f.name, concat(surname, ' ',firstname) as membername FROM `Bookings` as b
LEFT JOIN `Facilities`as f
ON  b.facid = f.facid
LEFT JOIN `Members` as m
ON m.memid = b.memid
WHERE name LIKE 'Tennis Court%'
ORDER BY membername
*/




/* Q8: Produce a list of bookings on the day of 2012-09-14 which
will cost the member (or guest) more than $30. Remember that guests have
different costs to members (the listed costs are per half-hour 'slot'), and
the guest user's ID is always 0. Include in your output the name of the
facility, the name of the member formatted as a single column, and the cost.
Order by descending cost, and do not use any subqueries. */

/* A8:
SELECT f.name as facilityname,
	concat(m.firstname, ' ', m.surname) as membername,
	(CASE WHEN m.memid != 0 THEN f.membercost * slots
	ELSE f.guestcost * slots END) AS cost
FROM `Bookings` as b
LEFT JOIN `Members` as m
ON m.memid = b.memid
LEFT JOIN `Facilities` as f
ON b.facid = f.facid
WHERE DATE(starttime) = '2012-09-14'
AND (m.memid = 0
AND guestcost * slots > 30)
OR (m.memid != 0 AND membercost * slots > 30)
ORDER BY cost DESC
*/




/* Q9: This time, produce the same result as in Q8, but using a subquery. */

/*
SELECT ff.name as facilityname,
	concat(mm.firstname, ' ', mm.surname) as membername,
	(CASE WHEN mm.memid != 0 THEN ff.membercost * slots
	ELSE ff.guestcost * slots END) AS cost
FROM `Bookings` as b
LEFT JOIN (SELECT m.memid, m.firstname, m.surname FROM `Members` as m) as mm
ON mm.memid = b.memid
LEFT JOIN (SELECT f.facid, f.name, f.membercost, f.guestcost FROM `Facilities` as f) as ff
ON b.facid = ff.facid
WHERE DATE(starttime) = '2012-09-14'
AND (mm.memid = 0
AND guestcost * slots > 30)
OR (mm.memid != 0 AND membercost * slots > 30)
ORDER BY cost DESC
*/










/* PART 2: SQLite

Export the country club data from PHPMyAdmin, and connect to a local SQLite instance from Jupyter notebook 
for the following questions.  

QUESTIONS:
/* Q10: Produce a list of facilities with a total revenue less than 1000.
The output of facility name and total revenue, sorted by revenue. Remember
that there's a different cost for guests and members! */


/*
"""
SELECT *
FROM (SELECT f.name as facilityname,
    SUM((CASE WHEN m.memid != 0 THEN f.membercost * slots
	ELSE f.guestcost * slots END)) AS totalrevenue
FROM `Bookings` as b
LEFT JOIN `Members` as m
ON m.memid = b.memid
LEFT JOIN `Facilities` as f
ON b.facid = f.facid
GROUP BY facilityname
ORDER BY totalrevenue DESC) as subquery
WHERE subquery.totalrevenue < 1000"""
*/



/* Q11: Produce a report of members and who recommended them in alphabetic surname,firstname order */

/*
"""
SELECT DISTINCT (m.surname || ',' || m.firstname) as membername
FROM Members as m
INNER JOIN 
(SELECT DISTINCT CAST(m.recommendedby AS UNSIGNED) as recommendedby
FROM Members as m
where m.recommendedby IS NOT NULL
AND m.recommendedby != '') as subquery
ON subquery.recommendedby = m.memid
ORDER BY membername"""
*/


/*
"""
SELECT DISTINCT (m.surname || ',' || m.firstname) as membername
FROM Members as m
INNER JOIN 
(SELECT DISTINCT CAST(m.recommendedby AS UNSIGNED) as recommendedby
FROM Members as m
where m.recommendedby != '') as subquery
ON subquery.recommendedby = m.memid
ORDER BY membername"""
*/








/* Q12: Find the facilities with their usage by member, but not guests */


/*
"""
SELECT m.memid,
    m.firstname || ' ' || m.surname as membername,
    SUM(b.slots)
FROM Members as m
LEFT JOIN Bookings as b
ON m.memid = b.memid
LEFT JOIN Facilities as f
ON f.facid = b.facid
WHERE m.memid != 0
GROUP BY m.memid"""
*/




/* Q13: Find the facilities usage by month, but not guests */


/*
"""
SELECT strftime('%m', bb.starttime) as month,
    ff.name,
    SUM(bb.slots) as totalslots
FROM (SELECT m.memid FROM `Members` as m WHERE m.memid != 0) as mm
LEFT JOIN (SELECT b.facid, b.memid, b.starttime, b.slots FROM `Bookings` as b) as bb
ON mm.memid = bb.memid
LEFT JOIN (SELECT f.facid, f.name FROM `Facilities` as f) as ff
ON ff.facid = bb.facid
GROUP BY ff.name, month"""

*/




