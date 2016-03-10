import sys, csv
#testttt change and lalala and hello and pp
sqlString = "SELECT count(*) FROM  (SELECT houseid,personid,sum(vmt_mile)FROM dayv2pub"
" WHERE vmt_mile>0 GROUP BY houseid,personid UNION SELECT houseid,personid,sum(trpmiles)"
" FROM dayv2pub WHERE trpmiles>0 AND trptrans>7 GROUP BY houseid,personid) AS testtttt"

#execute that SQLSTRING and return the value
for i in range(5,105, 5):
	i = str(i)
	sqlString = "SELECT count(*) FROM (SELECT houseid,personid,sum(vmt_mile) FROM dayv2pub"
	" WHERE vmt_mile>0 GROUP BY houseid,personid HAVING sum(vmt_mile)<"
	sqlString+= i
	sqlString+= " UNION SELECT houseid,personid,sum(trpmiles) FROM dayv2pub WHERE"
	" trpmiles>0 AND trptrans>7 GROUP BY houseid,personid HAVING sum(trpmiles)<"
	sqlString+= i + "AS lalala;"
	#execute the strng here and then evaluate it and then divide by total people and print
for i in range(5,105, 5):
	i = str(i)
	sqlString = "SELECT dist/fuel as fuel_economy FROM(SELECT sum(trpmiles/epatmpg) as fuel,"
	" sum(trpmiles) as dist FROM (SELECT houseid,vehid,epatmpg,trpmiles FROM dayv2pub NATURAL"
	" JOIN vehv2pub WHERE trpmiles>0 AND trpmiles<"
	sqlString += i
	sqlString += " AND vehid>=1 GROUP BY dayv2pub.vehid,dayv2pub.houseid,vehv2pub.epatmpg,"
	"dayv2pub.trpmiles) AS hi) AS hello;"
	#execute the file and then use and print
for i in range(200803, 200813, 1):
	i = str(i)
	sqlString = "SELECT 117538000/count(DISTINCT houseid)*sum(.000000008887*30*trpmiles/epatmpg)"
	" AS gallons FROM (SELECT dayv2pub.houseid, trpmiles, epatmpg FROM vehv2pub,dayv2pub WHERE"
	" vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND dayv2pub.trpmiles>0"
	" AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate="
	sqlString += i + " ) AS pp;"
	#execute this and store it as variable home
	sql2 = "SELECT value FROM eia_co2_transportation_2014 WHERE YYYYMM = "
	sql2 += i + " ORDER BY value DESC LIMIT 1;"
	#execute this and store it as total
	#print home/total
for i in range(200901, 200905, 1):
	i = str(i)
	sqlString = "SELECT 117538000/count(DISTINCT houseid)*sum(.000000008887*30*trpmiles/epatmpg)"
	" AS gallons FROM (SELECT dayv2pub.houseid, trpmiles, epatmpg FROM vehv2pub,dayv2pub WHERE"
	" vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND dayv2pub.trpmiles>0"
	" AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate="
	sqlString += i + " ) AS pp;"
	#execute this and store it as variable home
	sql2 = "SELECT value FROM eia_co2_transportation_2014 WHERE YYYYMM = "
	sql2 += i + " ORDER BY value DESC LIMIT 1;"
	#execute this and store it as total
	#print home/total
for i in range(20,80,20):
	i = str(i)
	for j in range(200803, 200813, 1): #
		j = str(j)
		sql = "SELECT (SELECT value FROM eia_co2_electric_2014 WHERE yyyymm="
		sql += j
		sql += " ORDER BY value DESC LIMIT 1)/(SELECT value FROM eia_mkwh_2014 WHERE yyyymm="
		sql += j
		sql += " ORDER BY value DESC LIMIT 1);"
		#result and store as ratio
		ratio = "1.1"
		sql += "SELECT sum(("
		sql += ratio
		sql += "*(trpmiles*11.03)/(epatmpg*1.0))) AS eelec FROM vehv2pub,dayv2pub WHERE"
		" vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0"
		" AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate="
		sql += j + " AND trpmiles<=" + i + ";"
		#created a lessthan veriable from the result of this

		lessthan = "1.1"
		sql = "SELECT sum(.008887*30*(trpmiles-" + i + ")/epatmpg) AS eelec FROM"
		" vehv2pub,dayv2pub WHERE vehv2pub.houseid=dayv2pub.houseid AND"
		" vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND"
		" dayv2pub.vehid>0 AND dayv2pub.tdaydate="
		sql += j + " AND trpmiles>" + i + ";"
		#store the result and save this as submorethan
		submorethan = "1.1"
		sql = "SELECT sum(.008887*30*trpmiles/epatmpg) AS eelec FROM vehv2pub,dayv2pub"
		" WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND"
		" trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=" + j

		sql += " AND trpmiles>" + i + ";"
		#result store comorethan
		comorethan = "1.1"
		sql = "SELECT sum((" + ratio + "*(" + i + "*11.03)/(epatmpg*1.0))) AS"
		" eelec FROM vehv2pub,dayv2pub WHERE vehv2pub.houseid=dayv2pub.houseid AND"
		" vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND"
		" dayv2pub.vehid>0 AND dayv2pub.tdaydate="
		sql += j + " AND trpmiles>" + i + ";"
		#result stored in newele
		newele = "1.1"

		sql = "SELECT sum(.008887*30*trpmiles/epatmpg) AS eelec FROM vehv2pub,dayv2pub"
		" WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND"
		" trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate="
		sql += j + ";"
		#store result as cototal
		#answer = lessthan + (comorethan - submorethan + newele)
		#change = (answer - cototal)/cototal

	for j in range(200901, 200905, 1):
		j = str(j)
		sql = "SELECT (SELECT value FROM eia_co2_electric_2014 WHERE yyyymm="
		sql += j
		sql += " ORDER BY value DESC LIMIT 1)/(SELECT value FROM eia_mkwh_2014 WHERE yyyymm="
		sql += j
		sql += " ORDER BY value DESC LIMIT 1);"
		#result and store as ratio
		ratio = "1.1"
		sql += "SELECT sum(("
		sql += ratio
		sql += "*(trpmiles*11.03)/(epatmpg*1.0))) AS eelec FROM vehv2pub,dayv2pub WHERE"
		" vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0"
		" AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate="
		sql += j + " AND trpmiles<=" + i + ";"
		#created a lessthan veriable from the result of this

		lessthan = "1.1"
		sql = "SELECT sum(.008887*30*(trpmiles-" + i + ")/epatmpg) AS eelec FROM"
		" vehv2pub,dayv2pub WHERE vehv2pub.houseid=dayv2pub.houseid AND"
		" vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND"
		" dayv2pub.vehid>0 AND dayv2pub.tdaydate="
		sql += j + " AND trpmiles>" + i + ";"
		#store the result and save this as submorethan
		submorethan = "1.1"
		sql = "SELECT sum(.008887*30*trpmiles/epatmpg) AS eelec FROM vehv2pub,dayv2pub"
		" WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND"
		" trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate=" + j

		sql += " AND trpmiles>" + i + ";"
		#result store comorethan
		comorethan = "1.1"
		sql = "SELECT sum((" + ratio + "*(" + i + "*11.03)/(epatmpg*1.0))) AS"
		" eelec FROM vehv2pub,dayv2pub WHERE vehv2pub.houseid=dayv2pub.houseid AND"
		" vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND"
		" dayv2pub.vehid>0 AND dayv2pub.tdaydate="
		sql += j + " AND trpmiles>" + i + ";"
		#result stored in newele
		newele = "1.1"

		sql = "SELECT sum(.008887*30*trpmiles/epatmpg) AS eelec FROM vehv2pub,dayv2pub"
		" WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND"
		" trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate="
		sql += j + ";"
		#store result as cototal
		#answer = lessthan + (comorethan - submorethan + newele)
		#change = (answer - cototal)/cototal

for i in range(20,80,20):
	i = str(i)
	j = 200001
	while(j <= 201407):
		if (j % 100 == 13):
			j = j -12 + 100
		else:
			j += 1
			j = str(j)
			sql = "SELECT (SELECT value FROM eia_co2_electric_2014 WHERE yyyymm=" + j
			sql += " ORDER BY value DESC LIMIT 1)/(SELECT value FROM eia_mkwh_2014 WHERE yyyymm=" + j
			sql += " ORDER BY value DESC LIMIT 1);"
			#result execute store it as ratio
			ratio = "1.1"

			sql = "SELECT sum((" + ratio + "*(trpmiles*11.03)/(epatmpg*1.0))) AS eelec"
			" ROM vehv2pub,dayv2pub WHERE vehv2pub.houseid=dayv2pub.houseid AND"
			" vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND"
			" dayv2pub.vehid>0 AND dayv2pub.tdaydate=" + j
			sql += " AND trpmiles<=" + i + ";"
			#result lessthan

			sql = "SELECT sum(.008887*30*(trpmiles-" + i + ")/epatmpg) AS eelec FROM"
			" vehv2pub,dayv2pub WHERE vehv2pub.houseid=dayv2pub.houseid AND"
			" vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND"
			" dayv2pub.vehid>0 AND dayv2pub.tdaydate=" + j + " AND trpmiles>" + i + ";"
			#result submorethan

			sql = "SELECT sum(.008887*30*trpmiles/epatmpg) AS eelec FROM vehv2pub,dayv2pub"
			" WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND"
			" trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate="
			sql += j + " AND trpmiles>" + i + ";"
			#result comorethan

			sql = "SELECT sum((" + ratio + "*(" + i + "*11.03)/(epatmpg*1.0))) AS eelec"
			" FROM vehv2pub,dayv2pub WHERE vehv2pub.houseid=dayv2pub.houseid AND"
			" vehv2pub.vehid=dayv2pub.vehid AND trpmiles>0 AND vehv2pub.vehid>0 AND"
			" dayv2pub.vehid>0 AND dayv2pub.tdaydate=" + j + " AND trpmiles>" + i + ";"
			#result newele

			sql = "SELECT sum(.008887*30*trpmiles/epatmpg) AS eelec FROM vehv2pub,dayv2pub"
			" WHERE vehv2pub.houseid=dayv2pub.houseid AND vehv2pub.vehid=dayv2pub.vehid AND"
			" trpmiles>0 AND vehv2pub.vehid>0 AND dayv2pub.vehid>0 AND dayv2pub.tdaydate="
			sql += j + ";"
			#result in cototal

			#answer = lessthan + (comorthan - submorethan + newele)
			#change = (answer-cototal)/cototal

