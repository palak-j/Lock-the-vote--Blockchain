import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="MySQL@18",
  database="votingdata"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM users")

voters_list = mycursor.fetchall()

  
mycursor.execute("SELECT * FROM candidates")

candidates_list = mycursor.fetchall()

candidates =[]      #Candidates list
voters =[]           #Voters list
passwords ={}
for x in range(0,len(voters_list)):
    voters.append(voters_list[x][0])
    passwords[voters_list[x][0]]= voters_list[x][1]
    
for y in range(0,len(candidates_list)):
    candidates.append(candidates_list[y][0])
