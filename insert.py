#!/usr/bin/python
import os, sys
import psycopg2
from tableUtilities import intChecker, floatChecker, charChecker
USER = os.environ['USER']
HOST = os.path.join('home',USER,'postgres')
conn = psycopg2.connect(database="postgres", user=USER)
curr = conn.cursor()
def insertTable(filePath, filename):
	with open(filePath, 'r') as myFile:
		sqlString = ""
		myFile.readline() # skip a line
		sqlString = "INSERT INTO " + filename
		sqlString += " VALUES\n"
		i = 0
		j = 0
		myFileCopy = open(filePath, 'r')
		length = len(myFileCopy.readlines())
		lines = myFileCopy.readlines()
		for line in myFile.readlines(): # reads starting from second line
			sqlString += "("
			valList = line.split(",")
			for val in valList[:-1]:
				if val == "Not Available":
					sqlString += "NULL,"
				elif(charChecker(val)):
					sqlString += "'" + val + "'" + ","
				else:
					sqlString += val + ", "
			if j == (length - 1):
				if(charChecker(valList[-1])): # account for last value 
					sqlString += "'" + valList[-1].strip() + "'" + ");" + "\n"
				else:
					sqlString += valList[-1].strip() + ");" + "\n"
				#print(sqlString)
				#print(sqlString)
				print()
				curr.execute(sqlString)
				conn.commit()
				break
			elif i == 1000:
				if(charChecker(valList[-1])): # account for last value 
					sqlString += "'" + valList[-1].strip() + "'" + ");" + "\n"
				else:
					sqlString += valList[-1].strip() + ");" + "\n"
				curr.execute(sqlString)
				conn.commit()
				#print(sqlString)
				sqlString = ""
				sqlString = "INSERT INTO " + filename
				sqlString += " VALUES\n"
				i = 0 #reset
			else:
				if(charChecker(valList[-1])): # account for last value 
					sqlString += "'" + valList[-1].strip() + "'" + ");" + "\n"
				else:
					sqlString += valList[-1].strip() + ");" + "\n"

			i+=1
			j+=1
		return sqlString

def main():
	try:
	    directory = sys.argv[1]
	except:
	    print("Please enter in the directory of CSV files")
	    return -1

	fileList = []
	for filename in os.listdir(directory):
	    if filename[-3:] == "CSV":
	        fileList.append(filename)
	#j = 0
	# for filename in fileList:
	# 	#print(insertTable(os.path.join(directory, filename), filename.split(".")[0]))
	# 	#print(j)
	# 	insertTable(os.path.join(directory, filename), filename.split(".")[0])
	# 	print("Banana")


	# insertTable(os.path.join(directory, 'DAYV2PUB.CSV'), 'DAYV2PUB')
	insertTable(os.path.join(directory, 'HHV2PUB.CSV'), 'HHV2PUB')
	# insertTable(os.path.join(directory, 'VEHV2PUB.CSV'), 'VEHV2PUB')
	# insertTable(os.path.join(directory, 'PERV2PUB.CSV'), 'PERV2PUB')
		#j+=1
	conn.commit()

	conn.close()

main()