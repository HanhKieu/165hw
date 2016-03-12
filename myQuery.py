import csv 
import os, sys
import psycopg2
from tableUtilities import intChecker, floatChecker, charChecker
import time


def monthDays(x):
	if (x == 2):
		return (28)
	elif (x in [1, 3, 5, 7, 8, 10, 12]):
		return (31)
	else:
		return (30)


def problem3a(curr):
	print "QUESTION 3a"
	sqlString ="""
		SELECT count(*), tdaydate FROM  

		(SELECT houseid,personid,sum(vmt_mile), tdaydate
		FROM dayv2pub
		WHERE vmt_mile>0 GROUP BY houseid,personid, tdaydate 
		UNION 
		SELECT houseid,personid,sum(trpmiles), tdaydate
		FROM dayv2pub WHERE trpmiles>0  GROUP BY houseid,personid, tdaydate) AS t GROUP BY tdaydate 
	"""
	curr.execute(sqlString)
	total = curr.fetchall()
	stotal = 0
	wtotal = 0
	currentY = 0
	currentM = 0
	weight = 0
	amountforM = 0
	for row in total:
		amountforM = int(row[0])
		stotal += amountforM

		currentY = int(row[1])
		if currentY < 200900:
			currentM = currentY - 200800
		else:
			currentM = currentY - 200900

		weight = monthDays(currentM)
		wtotal += weight * amountforM
	# print("Total is: " + str(stotal) + " WTotal is: " + str(wtotal) + " Total times 30: " + str(stotal * 30))

	for i in range(5,105,5):
		#print("for range %d:" % i)
		sqlString = """
		SELECT count(*), tdaydate FROM 

		(SELECT houseid,personid,sum(vmt_mile), tdaydate
 		FROM dayv2pub
		WHERE vmt_mile>0 GROUP BY houseid,personid, tdaydate HAVING sum(vmt_mile) < %d
		UNION 
		SELECT houseid,personid,sum(trpmiles), tdaydate FROM dayv2pub 
		WHERE
		trpmiles>0  GROUP BY houseid,personid, tdaydate HAVING sum(trpmiles)< %d) as l GROUP BY tdaydate
		""" % (i,i)

		curr.execute(sqlString)
		total = curr.fetchall()
		stotal = 0
		wttotal = 0
		currentY = 0
		currentM = 0
		weight = 0
		amountforM = 0
		for row in total:
			amountforM = int(row[0])
			stotal += amountforM

			currentY = int(row[1])
			if currentY < 200900:
				currentM = currentY - 200800
			else:
				currentM = currentY - 200900

			weight = monthDays(currentM)
			wttotal += weight * amountforM
		# print("Total is: " + str(stotal) + " WTTotal is: " + str(wttotal) + " Total times 30: " + str(stotal * 30))

		answer = float(wttotal) / float(wtotal) * 100

		#print("%d %.3f " % (i, answer))
		print("Percent when miles are less than " + str(i) + " is: %.3f" % answer)

def problem3b(curr):
	print "QUESTION 3b"
	for i in range(5,105,5):
		sqlString = """
		SELECT dist/fuel as fuel_economy 
		FROM(
			SELECT sum(trpmiles/epatmpg) as fuel, sum(trpmiles) as dist 
			FROM (
				SELECT houseid,vehid,epatmpg,trpmiles 
				FROM dayv2pub NATURAL JOIN vehv2pub WHERE drvr_flg = '01' AND trpmiles>0 AND trpmiles<%d AND vehid>=1 GROUP BY dayv2pub.vehid,dayv2pub.houseid,vehv2pub.epatmpg,
		dayv2pub.trpmiles) AS hi) AS hello
		""" % i
		curr.execute(sqlString)
		answer = curr.fetchone()[0]
		print("Average Fuel Economy for < %.d miles %.3f" % (i, answer))

def problem3c(curr):
	print "QUESTION 3c"
	for i in range(200803, 200813):
		sqlString = """
		SELECT 117538000/count(DISTINCT houseid)*sum(.000000008887*%d*trpmiles/epatmpg) AS gallons 
		FROM (
			SELECT dayv2pub.houseid, trpmiles, epatmpg 
			FROM vehv2pub,dayv2pub 
			WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND dayv2pub.trpmiles>0
			AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND drvr_flg = '01') AS pp;
		""" % (monthDays(i - 200800), i)

		curr.execute(sqlString)
		home = float(curr.fetchone()[0])
		sqlString = "SELECT value FROM eia_co2_transportation_2015 WHERE YYYYMM = %d ORDER BY value DESC LIMIT 1;" % i
		curr.execute(sqlString)
		total = float(curr.fetchone()[0])
		#execute this and store it as total
		print("For the month %d in 2008, household vehicle CO2 emissions were: %.3f" % (i - 200800, home / total * 100))
		# print("Home was: " + str(home) + "and Total was: " + str(total))

		#print home/total
	for i in range(200901, 200905):
		sqlString = """
		SELECT 117538000/count(DISTINCT houseid)*sum(.000000008887*%d*trpmiles/epatmpg) AS gallons
		FROM (
			SELECT dayv2pub.houseid, trpmiles, epatmpg FROM vehv2pub,dayv2pub 
			WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND dayv2pub.trpmiles>0
			AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND drvr_flg = '01') AS pp;
			""" % (monthDays(i - 200900), i)
		#execute this and store it as variable home

		curr.execute(sqlString)
		home = float(curr.fetchone()[0])

		sqlString = "SELECT value FROM eia_co2_transportation_2015 WHERE YYYYMM = %d ORDER BY value DESC LIMIT 1;" % i
		#execute this and store it as total
		#print home/total
		curr.execute(sqlString)
		total = float(curr.fetchone()[0])

		print("For the month %d in 2009, household vehicle CO2 emissions were: %.3f" % (i - 200800, home / total * 100))


def problem3d_helper(i,monthFrom,monthTo,actualMonth,curr,year):
	for j in range(monthFrom, monthTo): 
		month = monthDays(j - actualMonth)
		sql = """
			SELECT 
			(
			SELECT value 
			FROM eia_co2_electricity_2015 
			WHERE yyyymm=%d
			ORDER BY value DESC LIMIT 1) / 
			(SELECT value FROM eia_mkwh_2015 WHERE yyyymm=%d
			ORDER BY value DESC LIMIT 1);
		""" % (j,j)

		curr.execute(sql)
		ratio = float(curr.fetchone()[0])


		sql = """
		SELECT sum(( %f *(trpmiles*11.03)/(epatmpg*1.0))) AS eelec 
		FROM vehv2pub,dayv2pub 
		WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0
		AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND drvr_flg = '01'
		AND trpmiles<=%d;""" % (ratio, j, i)
		#created a lessthan veriable from the result of this

		curr.execute(sql)
		lessthan = float(curr.fetchone()[0])

		sql = """
		SELECT sum(.008887*%d*(trpmiles-%d)/epatmpg) AS eelec 
		FROM vehv2pub,dayv2pub 
		WHERE vehv2pub.houseid=dayv2pub.houseid AND
		vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND
		dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND trpmiles>%d AND drvr_flg = '01';
		""" % (month,i,j,i)
		#store the result and save this as submorethan

		curr.execute(sql)
		submorethan = float(curr.fetchone()[0])

		sql = """
		SELECT sum(.008887*%d*trpmiles/epatmpg) AS eelec 
		FROM vehv2pub,dayv2pub
		WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND
		trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND trpmiles>%d AND drvr_flg = '01';
		""" % (month, j,i)

		curr.execute(sql)
		comorethan = float(curr.fetchone()[0])
		#result store comorethan

		sql = """
		SELECT sum((%f*(%d*11.03)/(epatmpg*1.0))) AS eelec 
		FROM vehv2pub,dayv2pub 
		WHERE vehv2pub.houseid=dayv2pub.houseid AND
		vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND
		dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND trpmiles>%d AND drvr_flg = '01';""" % (ratio, i, j, i)

		curr.execute(sql)
		newele= float(curr.fetchone()[0])

		sql = """
		SELECT sum(.008887*%d*trpmiles/epatmpg) AS eelec 
		FROM vehv2pub,dayv2pub
		WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND
		trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND drvr_flg = '01';
		""" % (month,j )
		#store result as cototal


		curr.execute(sql)
		cototal = float(curr.fetchone()[0])

		answer = lessthan + (comorethan - submorethan + newele)
		change = (answer - cototal)/cototal

		print("For hybrids with electric range of %d in month %d of year %s, the change CO2 emissions was: %.3f" %(i, j - actualMonth, year, change))


def problem5a_helper(i,monthFrom,monthTo,actualMonth,curr, year):
	for j in range(monthFrom, monthTo): 
		month = monthDays(j - actualMonth)
		sql = """
			SELECT 
			(
			SELECT value 
			FROM eia_co2_electricity_2015 
			WHERE yyyymm=%d
			ORDER BY value DESC LIMIT 1) / 
			(SELECT value FROM eia_mkwh_2015 WHERE yyyymm=%d
			ORDER BY value DESC LIMIT 1);
		""" % (j,j)

		curr.execute(sql)
		ratio = float(curr.fetchone()[0])


		sql = """
		SELECT sum(( %f *(trpmiles*11.03)/(epatmpg*1.0))) AS eelec 
		FROM vehv2pub,dayv2pub 
		WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0
		AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND drvr_flg = '01'
		AND trpmiles<=%d;""" % (ratio, j, i)
		#If its less than then , its electric vehicle. CO2 Equivalent values

		curr.execute(sql)
		electricVehicle = float(curr.fetchone()[0])

		sql = """
		SELECT sum(.008887*%d*(trpmiles)/epatmpg) AS eelec 
		FROM vehv2pub,dayv2pub 
		WHERE vehv2pub.houseid=dayv2pub.houseid AND
		vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND
		dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND trpmiles>%d AND drvr_flg = '01';
		""" % (month,j,i)
		#If its greater than, then its conventional
		curr.execute(sql)
		try:
			conventional = float(curr.fetchone()[0])
		except:
			conventional = float(0)
		#result store comorethan



		sql = """
		SELECT sum(.008887*%d*trpmiles/epatmpg) AS eelec 
		FROM vehv2pub,dayv2pub
		WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND
		trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND drvr_flg = '01';
		""" % (month,j )
		#store result as cototal


		curr.execute(sql)
		cototal = float(curr.fetchone()[0])

		answer = conventional + electricVehicle
		change = (answer - cototal)/cototal

		print("Change of CO2 emissions for Electric and conventional cars range of %d in month %d of year %s, the change CO2 emissions was: %.3f" %(i, j - actualMonth, year, change))

def problem3d(curr):
	print "QUESTION 3D"
	for i in range(20,80,20):
		problem3d_helper(i,200803,200813,200800,curr,"2008")
		problem3d_helper(i,200901, 200905,200900,curr,"2009")

def problem5a(curr):
	print "QUESTION 5a"
	for i in [84, 107,208, 270]:
		problem5a_helper(i,200803,200813,200800,curr,"2008")
		problem5a_helper(i,200901, 200905,200900,curr,"2009")

def problem5b_helper(curr, i):
	time = 1
	while(time < 12):
		month = monthDays(i)
		if (time>= 3):
			j = 200800 + time
		else:
			j = 200900 + time


			sql = """
			SELECT 
			(
			SELECT value 
			FROM eia_co2_electricity_2015 
			WHERE yyyymm=%d
			ORDER BY value DESC LIMIT 1) / 
			(SELECT value FROM eia_mkwh_2015 WHERE yyyymm=%d
			ORDER BY value DESC LIMIT 1);
			""" % (time + 201400,time + 201400)

		curr.execute(sql)
		ratio = float(curr.fetchone()[0])


		sql = """
		SELECT sum(( %f *(trpmiles*11.03)/(epatmpg*1.0))) AS eelec 
		FROM vehv2pub,dayv2pub 
		WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND 
		trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND trpmiles<=%d AND drvr_flg = '01';
		""" % (ratio, j, i)
		#created a lessthan veriable from the result of this

		curr.execute(sql)
		lessthan = float(curr.fetchone()[0])

		sql = """
		SELECT sum(.008887*%d*trpmiles/epatmpg) AS eelec 
		FROM vehv2pub,dayv2pub
		WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND
		trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND trpmiles>%d AND drvr_flg = '01';
		""" % (month, j,i)

		curr.execute(sql)
		try:
			comorethan = float(curr.fetchone()[0])
		except:
			comorethan = float(0)
		#result store comorethan


		sql = """
		SELECT sum(.008887*%d*trpmiles/epatmpg) AS eelec 
		FROM vehv2pub,dayv2pub
		WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND
		trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND drvr_flg = '01';
		""" % (month,j )
		#store result as cototal
		curr.execute(sql)
		cototal = float(curr.fetchone()[0])

		if time in [3, 4]:
			j += 100

			sql = """
			SELECT 
			(
			SELECT value 
			FROM eia_co2_electricity_2015 
			WHERE yyyymm=%d
			ORDER BY value DESC LIMIT 1) / 
			(SELECT value FROM eia_mkwh_2015 WHERE yyyymm=%d
			ORDER BY value DESC LIMIT 1);
			""" % (time + 201400,time + 201400)

			curr.execute(sql)
			ratio = float(curr.fetchone()[0])


			sql = """
			SELECT sum(( %f *(trpmiles*11.03)/(epatmpg*1.0))) AS eelec 
			FROM vehv2pub,dayv2pub 
			WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND 
			trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND trpmiles<=%d AND drvr_flg = '01';
			""" % (ratio, j, i)
			#created a lessthan veriable from the result of this

			curr.execute(sql)
			lessthan += float(curr.fetchone()[0])

			sql = """
			SELECT sum(.008887*%d*trpmiles/epatmpg) AS eelec 
			FROM vehv2pub,dayv2pub
			WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND
			trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND trpmiles>%d AND drvr_flg = '01';
			""" % (month, j,i)

			curr.execute(sql)
			comorethan += float(curr.fetchone()[0])
			#result store comorethan


			sql = """
			SELECT sum(.008887*%d*trpmiles/epatmpg) AS eelec 
			FROM vehv2pub,dayv2pub
			WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND
			trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND drvr_flg = '01';
			""" % (month,j )
			#store result as cototal
			curr.execute(sql)
			cototal += float(curr.fetchone()[0])


		answer = lessthan + (comorethan)
		change = (answer - cototal)/cototal


		print("For hybrids with electric range of %d in month %d of year 2014, the change CO2 emissions was: %.3f" %(i, time,  change))
		time += 1

def problem5b(curr):
	print "QUESTION 5b"
	for i in [84, 107,208, 270]:
		problem5b_helper(curr, i)

def main():
	start_time = time.time()
	USER = os.environ['USER']
	HOST = os.path.join('home',USER,'postgres')
	conn = psycopg2.connect(database="postgres", user=USER)
	curr = conn.cursor()
	try:
		problemName = sys.argv[1]
	except:
		print("Please enter the problem name")
		return -1
	if(problemName == "3a"):
		problem3a(curr)
	elif(problemName == "3b"):
		problem3b(curr)
	elif(problemName == "3c"):
		problem3c(curr)
	elif(problemName == "3d"):
		problem3d(curr)
	elif(problemName == "5a"):
		problem5a(curr)
	elif(problemName == "5b"):
		problem5b(curr)
	elif(problemName.lower() == "all"):
		problem3a(curr)
		problem3b(curr)
		problem3c(curr)
		problem3d(curr)
		problem5a(curr)
	conn.commit()
	conn.close()
	print("--- %s seconds ---" % (time.time() - start_time))


main()