import sys, csv
import os, sys
import psycopg2

USER = os.environ['USER']
HOST = os.path.join('home',USER,'postgres')
conn = psycopg2.connect(database="postgres", user=USER)
curr = conn.cursor()

key = int(sys.argv[1])
#key 1111 means all answers, first is 3a
#testttt change and lalala and hello and pp
def monthDays(x):
	if (x == 2):
		return (28)
	elif (x == 1 or x == 3 or x==5 or x== 7 or x==8 or x==10 or x==12):
		return (31)
	else:
		return (30)

#Q3a--------------------------------------------------------------------------------------
if (key - 999 > 0):
	print "\nQUESTION 3a\n"
	sqlString = "SELECT count(*) FROM  (SELECT houseid,personid,sum(vmt_mile)FROM dayv2pub" \
	" WHERE vmt_mile>0 GROUP BY houseid,personid UNION SELECT houseid,personid,sum(trpmiles)" \
	" FROM dayv2pub WHERE trpmiles>0 AND trptrans>7 GROUP BY houseid,personid) AS t"
	curr.execute(sqlString)
	row = curr.fetchall()
	for rows in row:
	    total = int(rows[0])
	print("Total:")
	print(total)
	#execute that SQLSTRING and return the value
	for i in range(5,105, 5):
		num = i
		i = str(i)
		sqlString = "SELECT count(*) FROM (SELECT houseid,personid,sum(vmt_mile) FROM dayv2pub"\
		" WHERE vmt_mile>0 GROUP BY houseid,personid HAVING sum(vmt_mile)<"
		sqlString+= i
		sqlString+= " UNION SELECT houseid,personid,sum(trpmiles) FROM dayv2pub WHERE"\
		" trpmiles>0 AND trptrans>7 GROUP BY houseid,personid HAVING sum(trpmiles)<"
		sqlString+= i + ") AS l;"


		curr.execute(sqlString)
		row = curr.fetchall()
		for rows in row:
			numP = int(rows[0])

		print ("For < " + i + " miles, there are " + str(numP) + " people which is " + str(float(numP)/float(total)) + " of the total.")


#Q3b--------------------------------------------------------------------------------------

if (key % 1000 > 99):
	print "\nQUESTION 3b\n"
	for i in range(5,105, 5):
		num = i
		i = str(i)
		sqlString = "SELECT dist/fuel as fuel_economy FROM(SELECT sum(trpmiles/epatmpg) as fuel,"\
		" sum(trpmiles) as dist FROM (SELECT houseid,vehid,epatmpg,trpmiles FROM dayv2pub NATURAL"\
		" JOIN vehv2pub WHERE trpmiles>0 AND trpmiles<"
		sqlString += i
		sqlString += " AND vehid>=1 GROUP BY dayv2pub.vehid,dayv2pub.houseid,vehv2pub.epatmpg,"\
		"dayv2pub.trpmiles) AS hi) AS hello;"
		#execute the file and then use and print
		curr.execute(sqlString)
		row = curr.fetchall()
		for rows in row:
			   numP = float(rows[0])
		print("Average Fuel Economy for < " + i + " miles : " + str(numP))

#Q3c-------------------------------------------------------------------------------------
if (key % 100 > 9):
	print "\nQUESTION 3c\n"
	for i in range(200803, 200813, 1):
		num = i
		i = str(i)
		month = monthDays(num - 200800)
		sqlString = "SELECT 117538000/count(DISTINCT houseid)*sum(.000000008887*"+str(month)+"*trpmiles/epatmpg)"\
		" AS gallons FROM (SELECT dayv2pub.houseid, trpmiles, epatmpg FROM vehv2pub,dayv2pub WHERE"\
		" vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND dayv2pub.trpmiles>0"\
		" AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate="
		sqlString += i + " ) AS pp;"

		curr.execute(sqlString)
		row = curr.fetchall()
		for rows in row:
			   home = float(rows[0])

		sql2 = "SELECT value FROM eia_co2_transportation_2015 WHERE YYYYMM = "
		sql2 += i + " ORDER BY value DESC LIMIT 1;"
		curr.execute(sql2)
		row = curr.fetchall()
		for rows in row:
			   total = float(rows[0])
		#execute this and store it as total
		print("For the month " + str(num - 200800) + " in 2008, household vehicle CO2 emissions were: "+ str(home/total))
		# print("Home was: " + str(home) + "and Total was: " + str(total))

		#print home/total
	for i in range(200901, 200905, 1):
		num = i
		i = str(i)
		month = monthDays(num - 200900)
		sqlString = "SELECT 117538000/count(DISTINCT houseid)*sum(.000000008887*"+str(month)+"*trpmiles/epatmpg)"\
		" AS gallons FROM (SELECT dayv2pub.houseid, trpmiles, epatmpg FROM vehv2pub,dayv2pub WHERE"\
		" vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND dayv2pub.trpmiles>0"\
		" AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate="
		sqlString += i + " ) AS pp;"
		#execute this and store it as variable home

		curr.execute(sqlString)
		row = curr.fetchall()
		for rows in row:
			home = float(rows[0])

		sql2 = "SELECT value FROM eia_co2_transportation_2015 WHERE YYYYMM = "
		sql2 += i + " ORDER BY value DESC LIMIT 1;"
		#execute this and store it as total
		#print home/total
		curr.execute(sql2)
		row = curr.fetchall()
		for rows in row:
			   total = float(rows[0])
		#execute this and store it as total

		print("For the month " + str(num - 200900) + " in 2009, household vehicle CO2 emissions were: "+ str(home/total))

#Q3d----------------------------------------------------------------------------------------
if (key % 10 > 0):
	print "\nQUESTION 3d\n"
	for i in range(20,80,20):
		numi = i
		i = str(i)

		for j in range(200803, 200813, 1): #
			numj = j
			j = str(j)
			month = monthDays(numj - 200800)
			sql = "SELECT (SELECT value FROM eia_co2_electricity_2015 WHERE yyyymm="
			sql += j
			sql += " ORDER BY value DESC LIMIT 1)/(SELECT value FROM eia_mkwh_2015 WHERE yyyymm="
			sql += j
			sql += " ORDER BY value DESC LIMIT 1);"
			#result and store as ratio

			curr.execute(sql)
			row = curr.fetchall()
			for rows in row:
				ratioF = float(rows[0])

			ratio = str(ratioF)
			sql += "SELECT sum(("
			sql += ratio
			sql += "*(trpmiles*11.03)/(epatmpg*1.0))) AS eelec FROM vehv2pub,dayv2pub WHERE"\
			" vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0"\
			" AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate="
			sql += j + " AND trpmiles<=" + i + ";"
			#created a lessthan veriable from the result of this

			curr.execute(sql)
			row = curr.fetchall()
			for rows in row:
				lessthanF = float(rows[0])

			lessthan = str(lessthanF)

			sql = "SELECT sum(.008887*"+str(month)+"*(trpmiles-" + i + ")/epatmpg) AS eelec FROM"\
			" vehv2pub,dayv2pub WHERE vehv2pub.houseid=dayv2pub.houseid AND"\
			" vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND"\
			" dayv2pub.vehid>0 AND dayv2pub.tdaydate="
			sql += j + " AND trpmiles>" + i + ";"
			#store the result and save this as submorethan

			curr.execute(sql)
			row = curr.fetchall()
			for rows in row:
				submorethanF = float(rows[0])

			submorethan = str(submorethanF)

			sql = "SELECT sum(.008887*"+str(month)+"*trpmiles/epatmpg) AS eelec FROM vehv2pub,dayv2pub"\
			" WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND"\
			" trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=" + j

			sql += " AND trpmiles>" + i + ";"

			curr.execute(sql)
			row = curr.fetchall()
			for rows in row:
				comorethanF = float(rows[0])
			#result store comorethan
			comorethan = str(comorethanF)

			sql = "SELECT sum((" + ratio + "*(" + i + "*11.03)/(epatmpg*1.0))) AS"\
			" eelec FROM vehv2pub,dayv2pub WHERE vehv2pub.houseid=dayv2pub.houseid AND"\
			" vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND"\
			" dayv2pub.vehid>0 AND dayv2pub.tdaydate="
			sql += j + " AND trpmiles>" + i + ";"
			#result stored in newele


			curr.execute(sql)
			row = curr.fetchall()
			for rows in row:
				neweleF = float(rows[0])
			newele = str(neweleF)

			sql = "SELECT sum(.008887*"+str(month)+"*trpmiles/epatmpg) AS eelec FROM vehv2pub,dayv2pub"\
			" WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND"\
			" trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate="
			sql += j + ";"
			#store result as cototal


			curr.execute(sql)
			row = curr.fetchall()
			for rows in row:
				cototal = float(rows[0])

			answer = lessthanF + (comorethanF - submorethanF + neweleF)
			change = (answer - cototal)/cototal

			print("For hybrids with electric range of " + i + " in month " + str(numj - 200800) + " of year 2008, the change CO2 emissions was: " + str(change))

		for j in range(200901, 200905, 1):
			numj = j
			j = str(j)
			month = monthDays(numj - 200900)
			sql = "SELECT (SELECT value FROM eia_co2_electricity_2015 WHERE yyyymm="
			sql += j
			sql += " ORDER BY value DESC LIMIT 1)/(SELECT value FROM eia_mkwh_2015 WHERE yyyymm="
			sql += j
			sql += " ORDER BY value DESC LIMIT 1);"
			#result and store as ratio

			curr.execute(sql)
			row = curr.fetchall()
			for rows in row:
				ratio = float(rows[0])

			sql += "SELECT sum(("
			sql += str(ratio)
			sql += "*(trpmiles*11.03)/(epatmpg*1.0))) AS eelec FROM vehv2pub,dayv2pub WHERE"\
			" vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0"\
			" AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate="
			sql += j + " AND trpmiles<=" + i + ";"
			#created a lessthan veriable from the result of this

			curr.execute(sql)
			row = curr.fetchall()
			for rows in row:
				lessthanF = float(rows[0])

			lessthan = str(lessthanF)

			sql = "SELECT sum(.008887*"+str(month)+"*(trpmiles-" + i + ")/epatmpg) AS eelec FROM"\
			" vehv2pub,dayv2pub WHERE vehv2pub.houseid=dayv2pub.houseid AND"\
			" vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND"\
			" dayv2pub.vehid>0 AND dayv2pub.tdaydate="
			sql += j + " AND trpmiles>" + i + ";"
			#store the result and save this as submorethan

			curr.execute(sql)
			row = curr.fetchall()
			for rows in row:
				submorethanF = float(rows[0])

			submorethan = str(submorethanF)

			sql = "SELECT sum(.008887*"+str(month)+"*trpmiles/epatmpg) AS eelec FROM vehv2pub,dayv2pub"\
			" WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND"\
			" trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=" + j

			sql += " AND trpmiles>" + i + ";"
			#result store comorethan

			curr.execute(sql)
			row = curr.fetchall()
			for rows in row:
				comorethanF = float(rows[0])

			comorethan = str(comorethanF)

			sql = "SELECT sum((" + str(ratio) + "*(" + i + "*11.03)/(epatmpg*1.0))) AS"\
			" eelec FROM vehv2pub,dayv2pub WHERE vehv2pub.houseid=dayv2pub.houseid AND"\
			" vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND"\
			" dayv2pub.vehid>0 AND dayv2pub.tdaydate="
			sql += j + " AND trpmiles>" + i + ";"
			#result stored in newele

			curr.execute(sql)
			row = curr.fetchall()
			for rows in row:
				neweleF = float(rows[0])
			newele = str(neweleF)

			sql = "SELECT sum(.008887*"+str(month)+"*trpmiles/epatmpg) AS eelec FROM vehv2pub,dayv2pub"\
			" WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND"\
			" trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate="
			sql += j + ";"
			#store result as cototal
			#answer = lessthan + (comorethan - submorethan + newele)
			#change = (answer - cototal)/cototal
			curr.execute(sql)
			row = curr.fetchall()
			for rows in row:
				cototal = float(rows[0])

			answer = lessthanF + (comorethanF - submorethanF + neweleF)
			change = (answer - cototal)/cototal

			print("For hybrids with electric range of " + i + " in month " + str(numj - 200900) + " of year 2009, the change in CO2 emissions was: " + str(change))
