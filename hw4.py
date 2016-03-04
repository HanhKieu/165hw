import sys, csv
import os

def intChecker(inputString):
    if inputString.startswith('-') and inputString[1:].isdigit():
        return True
    elif inputString.isdigit():
        return True
    return False

def floatChecker(inputString):
    try:
        myValue = float(inputString)
    except ValueError:
        return False
    if myValue.is_integer():
        return False
    else:
        return True


def createTable(directory):
    with open(directory, "r") as myFile:
        myTempList = (myFile.readline()).split(",")
        secondLine = (myFile.readline().split(","))

        myList = []
        typesList = []
        for element in myTempList:
            myList.append(element.strip())
        for element in secondLine:
            if intChecker(element):
                typesList.append("INTEGER")
            elif floatChecker(element):
                typesList.append("FLOAT")
            else:
                typesList.append("VARCHAR(30)")

        sqlString = "CREATE TABLE DAYV2PUB(" + "\n"
        for attribute, type in zip(myList[:-1], typesList[:-1]):
            sqlString += "\t" + attribute + " " + type + "," + "\n"
        sqlString += "\t" + myList[-1] + " " + typesList[-1] + "\n"
        sqlString += ");"
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

    for file in fileList:
        print(createTable(os.path.join(directory, file)))


        # CREATE TABLE
main()




