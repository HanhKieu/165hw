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
		SELECT count(*) FROM  

		(SELECT houseid,personid,sum(vmt_mile)
		FROM dayv2pub
		WHERE vmt_mile>0 GROUP BY houseid,personid 
		UNION 
		SELECT houseid,personid,sum(trpmiles)
		FROM dayv2pub WHERE trpmiles>0 GROUP BY houseid,personid) AS t
	"""
	curr.execute(sqlString)
	total = curr.fetchone()[0]
	#print(total)
	for i in range(5,105,5):
		#print("for range %d:" % i)
		sqlString = """
		SELECT count(*) FROM 

		(SELECT houseid,personid,sum(vmt_mile)
 		FROM dayv2pub
		WHERE vmt_mile>0 GROUP BY houseid,personid HAVING sum(vmt_mile) < %d
		UNION 
		SELECT houseid,personid,sum(trpmiles) FROM dayv2pub 
		WHERE
		trpmiles>0  GROUP BY houseid,personid HAVING sum(trpmiles)< %d) as l
		""" % (i,i)
		curr.execute(sqlString)
		subAnswer = curr.fetchone()[0]
		answer = float(subAnswer) / float(total) * 100

		#print("%d %.3f " % (i, answer))
		print("Percent is : %.3f" % answer)

def problem3b(curr):
	print "QUESTION 3b"
	for i in range(5,105,5):
		sqlString = """
		SELECT dist/fuel as fuel_economy FROM(SELECT sum(trpmiles/epatmpg) as fuel,
		sum(trpmiles) as dist FROM (SELECT houseid,vehid,epatmpg,trpmiles FROM dayv2pub NATURAL
		JOIN vehv2pub WHERE trpmiles>0 AND trpmiles<%d AND vehid>=1 GROUP BY dayv2pub.vehid,dayv2pub.houseid,vehv2pub.epatmpg,
		dayv2pub.trpmiles) AS var1) AS var2
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
			AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d ) AS pvar;
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
			AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d ) AS pvar;
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


def problem3d_helper(i,monthFrom,monthTo,actualMonth,curr):
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
		SELECT sum(( %f *(trpmiles*11.03)/(epatmpg*1.0))) AS electric 
		FROM vehv2pub,dayv2pub 
		WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0
		AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d
		AND trpmiles<=%d;""" % (ratio, j, i)
		#created a lessthan veriable from the result of this

		curr.execute(sql)
		lessthan = float(curr.fetchone()[0])

		sql = """
		SELECT sum(.008887*%d*(trpmiles-%d)/epatmpg) AS electric 
		FROM vehv2pub,dayv2pub 
		WHERE vehv2pub.houseid=dayv2pub.houseid AND
		vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND
		dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND trpmiles>%d;
		""" % (month,i,j,i)
		#store the result and save this as submorethan

		curr.execute(sql)
		submorethan = float(curr.fetchone()[0])

		sql = """
		SELECT sum(.008887*%d*trpmiles/epatmpg) AS electric 
		FROM vehv2pub,dayv2pub
		WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND
		trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND trpmiles>%d;
		""" % (month, j,i)

		curr.execute(sql)
		comorethan = float(curr.fetchone()[0])
		#result store comorethan

		sql = """
		SELECT sum((%f*(%d*11.03)/(epatmpg*1.0))) AS electric 
		FROM vehv2pub,dayv2pub 
		WHERE vehv2pub.houseid=dayv2pub.houseid AND
		vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND
		dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d AND trpmiles>%d;""" % (ratio, i, j, i)

		curr.execute(sql)
		newele= float(curr.fetchone()[0])

		sql = """
		SELECT sum(.008887*%d*trpmiles/epatmpg) AS electric 
		FROM vehv2pub,dayv2pub
		WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND
		trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=%d;
		""" % (month,j )
		#store result as cototal


		curr.execute(sql)
		cototal = float(curr.fetchone()[0])

		answer = lessthan + (comorethan - submorethan + newele)
		change = (answer - cototal)/cototal

		print("For hybrids with electric range of %d in month %d of year 2008, the change CO2 emissions was: %.3f" %(i, j - actualMonth, change))

def problem3d(curr):
	print "QUESTION 3D"
	for i in range(20,80,20):
		problem3d_helper(i,200803,200813,200800,curr)
		problem3d_helper(i,200901, 200905,200900,curr)

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
	elif(problemName.lower() == "all"):
		problem3a()
		problem3b()
		problem3c()
		problem3d()
	conn.commit()
	conn.close()
	print("--- %s seconds ---" % (time.time() - start_time))


main()