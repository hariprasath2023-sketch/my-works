import mysql.connector
import csv


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="mycustomer"
)
def executeSql():
    mycursor=mydb.cursor()
    CreatesalesDetail="create table sales(sales_id int,productname varchar(255),amount int);"
    CreateCustomerDetail="create table person(person_id int,name varchar(255),purchase_amt varchar(255));"
    # mycursor.execute(CreateCustomerDetail)
    # mycursor.execute(CreatesalesDetail)
    insertsalesValues = "INSERT INTO sales (sales_id, productname, amount) VALUES (%s, %s, %s)"
    val=[(1, 'mobile', 30000),(2, 'laptop', 40000),(3,'ipad',35000)]
    insertCustomerValues = "INSERT INTO person (person_id, name, purchase_amt) VALUES (%s, %s, %s)"
    val1=[(1, 'hari', 400000),(2, 'mugesh', 42000),(3,'logesh',45000)]
    mycursor.executemany(insertCustomerValues,val)
    # mycursor.execute(val)
    # mycursor.execute(val1)
    mycursor.executemany(insertsalesValues,val1)
    mydb.commit()
  
  
    sql="Select * From person"
    sql1="Select * From sales"
    # sql2="update  person set purchase=10000 where purchase=40000"
    # mycursor.execute(sql)
    # myresult=mycursor.fetchall()
    mycursor.execute(sql)
    myresult=mycursor.fetchall()
    with open("execute.csv",'w',newline='') as file:
        writer=csv.writer(file)
        for x in myresult:
            writer.writerow(x)

executeSql()




