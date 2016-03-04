import sys, csv

with open("DAYV2PUB.CSV", "r") as myFile:
    myTempList = (myFile.readline()).split(",")
    secondLine = myFile.readline()
    myList = []
    for element in myTempList:
        myList.append(element.strip())
    print(secondLine)