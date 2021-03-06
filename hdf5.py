#!/usr/bin/python
import h5py
import numpy as np
import csv 
import os, sys
import psycopg2
from tableUtilities import intChecker, floatChecker, charChecker
import time



# def createTable(directory, filename):
#     with open(directory, "r") as myFile:
#         myTempList = (myFile.readline()).split(",")
#         secondLine = (myFile.readline().split(","))

#         myList = []
#         typesList = []
#         for element in myTempList:
#             myList.append(element.strip())
#         for element in secondLine:
#             if intChecker(element):
#                 typesList.append("INTEGER")
#             elif floatChecker(element):
#                 typesList.append("FLOAT")
#             else:
#                 typesList.append("VARCHAR(30)")

#         sqlString = "CREATE TABLE " + filename + "(" + "\n"
#         for attribute, type in zip(myList[:-1], typesList[:-1]):
#             sqlString += "\t" + attribute + " " + type + "," + "\n"
#         sqlString += "\t" + myList[-1] + " " + typesList[-1] + "\n"
#         sqlString += ");"
#         return sqlString

# def printTable(directory, filename):
#     with open(directory, "r") as myFile:
#         for line in myFile:
#             print(line)
def main():
	USER = os.environ['USER']
	HOST = os.path.join('home',USER,'postgres')
	conn = psycopg2.connect(database="postgres", user=USER)
	curr = conn.cursor()
    # try:
    #     directory = sys.argv[1]
    # except:
    #     print("Please enter in the directory of CSV files")
    #     return -1

    # fileList = []
    # for filename in os.listdir(directory):
    #     if filename[-3:].lower() == "csv":
    #         fileList.append(filename)

    # #this creates our initial table before we make any manual edits
    # for filename in fileList:
    # #     #curr.execute(createTable(os.path.join(directory, filename), filename.split(".")[0]))
    #     print(createTable(os.path.join(directory, filename), filename.split(".")[0]))

    # sqlTable = open("nhtsTables", "r")
    # curr.execute(sqlTable.read())
    # sqlTable2 = open("eiaTables", "r")
    # curr.execute(sqlTable2.read())

        # CREATE TABLE



	hdf5_path = "/home/cjnitta/ecs165a/HW4Data.mat"
	sqlString = ""
	hf = h5py.File(hdf5_path,'r')
	data = hf.get('DAYV2PUB')
	np_data = np.array(data)
	# for element in np_data:
	# 	print(element)
	for key in hf.keys():
		print(key)
	conn.commit()
	conn.close()



main()




