#!/usr/bin/env python3

# Log Analysis Project
#Udacity Full-Stack Nanodegree project

# importing Postgresql library
import psycopg2

# import datetime.date module for
# problem 3
from datetime import date




# Global database name
DBNAME = 'news'

def execute_Query(query):
try:
#Create a new database session and return a new connection object.
db = psycopg2.connect('dbname=' + DBNAME)
#A control structure that enables traversal over the records in database;
c = db.cursor()
#standard procedures of this kind of the program;
c.execute(query)
#cursor object, loop the cursor and process each row individually.
rows = c.fetchall()
db.close()
return rows
except BaseException:
Print("Unable to connect to database")



# Problem 1: What are the most popular three articles of all time?
def find_top_three_articles():
	query = """SELECT articles.title, COUNT (*) as views FROM 
	articles JOIN log ON articles.slug = SUBSTRING(path, 10) 
	GROUP BY path, articles.title 
	ORDER BY views  desc LIMIT 3;"""
	top_three_articles = execute_Query(query)
	#Display header and results for Problem 1
	print('1. Top Three Articles by views')
	for i in top_three_articles:
		print('    ' + i[0] + ' ---- ' + str(i[1]) + ' views')
	print(' ') # Display line break


# Problem 2: Who are the most popular article authors of all time?
#The percent sign means zero, one or multiple.
ques_2 = 'Who are the most popular article authors of all time?'
def popular_authors_all_time():
	query = """SELECT authors.name, COUNT (*) as views 
	FROM articles INNER JOIN authors 
	ON articles.author = authors.id INNER JOIN log 
	ON concat('/article/', articles.slug) = log.path where
    log.status like '%200%' group by authors.name order by views desc
        """
	author_popularity = execute_Query(query)
	#display header and results for problem 2
	print('2. Most Popular article authors of all time')
	for i in author_popularity:
		print('    ' + i[0] + ' ---- ' + str(i[1]) + ' views')
	print(' ') #display line break


# Problem 3. On which days did more than 1% of requests lead to errors?
def high_error_rate_days():
    query = """ select * from (
        select a.day,
        round(cast((100*b.hits) as numeric) / cast(a/hits as numeric), 2)
        as errp from
        (select data(time) as day, count(*) as hits from log group by day)
        as a
        inner join
        (select date(time) as day, count(*) as hits from log where status
        like '%404%' group by day) as b
        on a.day = b.day)
        as t where errp > 1.0;
        """


if __name__ == '__main__':
	print (" ")
    find_top_three_articles()
	popular_authors_all_time()
	high_error_rate_days()
