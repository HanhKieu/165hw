import csv 
import os, sys
import psycopg2
from tableUtilities import intChecker, floatChecker, charChecker
import time


def sqlEndingAppend(element, colonOrComma):
	if(charChecker(element)): # account for last value 
		return "'" + element.strip() + "'" + ")" + colonOrComma + "\n"
	else:
		return element.strip() + ")" + colonOrComma + "\n"

def sqlElementAppend(element):
	if element == "Not Available":
		return"NULL,"
	elif(charChecker(element)):
		return "'" + element + "'" + ","
	else:
		return element + ", "

def insertTable(filePath, filename, curr):
	# ----- Opens Files and Prep to Loop-----
	i = 0
	j = 0
	myFile = open(filePath, 'r')
	csvFile = csv.reader(myFile, delimiter = ",")
	rowCount = sum(1 for row in csvFile)
	myFile.seek(0) 
	sqlString = '' 
	next(csvFile) #skips first line
	sqlString = "INSERT INTO " + filename
	sqlString += " VALUES\n"
	# ----- end Opens Files and Prep to Loop-----
	# ----- loops through each row in CSVFILE -----
	for row in csvFile:
		i+=1;
		j+=1;
		#------ begins appending elements to form a row -------#
		sqlString += "("
		for element in row[:-1]: #everythign except the last value
			sqlString += sqlElementAppend(element)
		lastElement = row[-1]

		if j == (rowCount -1):
			sqlString += sqlEndingAppend(lastElement, ";")
			#print(sqlString)
			curr.execute(sqlString)
			break
		elif i == 1000:
			sqlString += sqlEndingAppend(lastElement, ";")
			#print(sqlString)
			curr.execute(sqlString)
			sqlString = ""
			sqlString = "INSERT INTO " + filename
			sqlString += " VALUES\n"
			i = 0
		else:
			sqlString += sqlEndingAppend(lastElement, ",")


	return sqlString
		#------ end begins appending elements to form a row------






def main():
	start_time = time.time()
	USER = os.environ['USER']
	HOST = os.path.join('home',USER,'postgres')
	conn = psycopg2.connect(database="postgres", user=USER)
	curr = conn.cursor()
	try:
	    directory = sys.argv[1]
	except:
	    print("Please enter in the directory of CSV files")
	    return -1

	fileList = []
	for filename in os.listdir(directory):
	    if filename[-3:] == "CSV":
	        fileList.append(filename)



	#insertTable(os.path.join(directory, 'DAYV2PUB.CSV'), 'DAYV2PUB', curr)
	#insertTable(os.path.join(directory, 'HHV2PUB.CSV'), 'HHV2PUB', curr)
	#insertTable(os.path.join(directory, 'VEHV2PUB.CSV'), 'VEHV2PUB', curr)
	#insertTable(os.path.join(directory, 'PERV2PUB.CSV'), 'PERV2PUB', curr)
	conn.commit()
	conn.close()
	print("--- %s seconds ---" % (time.time() - start_time))
main()