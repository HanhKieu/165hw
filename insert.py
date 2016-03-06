#!/usr/bin/python
import os, sys
from tableUtilities import intChecker, floatChecker, charChecker

def insertTable(filePath, filename):
	with open(filePath, 'r') as myFile:
		myFile.readline() # skip a line
		sqlString = "INSERT INTO " + filename
		sqlString += " VALUES\n"
		i = 0
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

			if i == 5:
				if(charChecker(valList[-1])): # account for last value 
					sqlString += "'" + valList[-1].strip() + "'" + ");" + "\n"
				else:
					sqlString += valList[-1].strip() + ");" + "\n"
				break
			else:
				if(charChecker(valList[-1])): # account for last value 
					sqlString += "'" + valList[-1].strip() + "'" + ")," + "\n"
				else:
					sqlString += valList[-1].strip() + ")," + "\n"
			i+=1
		print(sqlString)
directory = "../CSVFILES"
fileList = []
for filename in os.listdir(directory):
    if filename[-3:] == "CSV":
        fileList.append(filename)

for filename in fileList:
	insertTable(os.path.join(directory, filename), filename.split(".")[0])