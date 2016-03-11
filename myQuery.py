import csv 
import os, sys
import psycopg2
from tableUtilities import intChecker, floatChecker, charChecker
import time

def problem1a(curr):
	for i in range(5,105,5):
		print("LESS THAN %d" % i) 
		sqlString = """
			select round ((select count(trpmiles)
			from dayv2pub 
			WHERE trpmiles < %d AND trpmiles >= 0) / (select count(trpmiles) from dayv2pub)
			) as percentage
			from dayv2pub
			group by percentage

			""" % i
		curr.execute(sqlString)
		answer = curr.fetchone()
		print(answer[0])

def problem2a(curr):
	print("PROBLEM 2A")

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
	if(problemName == "1a"):
		problem1a(curr)
	if(problemName == "2a"):
		problem2a(curr)

	conn.commit()
	conn.close()
	print("--- %s seconds ---" % (time.time() - start_time))


main()