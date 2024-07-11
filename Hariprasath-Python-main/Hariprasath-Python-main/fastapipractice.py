import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="mycustomer"
)
mycursor=mydb.cursor(dictionary=True)
def add(tablename,columnname):
    try:
        sql_query=f"Alter table {tablename} Add {columnname}"
        mycursor.execute(sql_query)
        mydb.commit()
    except Exception as e:
        print(e)    
def Delete(tablename,columnname):
    try:
        sql_query=f"Alter table {tablename} Drop column {columnname}"
        mycursor.execute(sql_query)    
        mydb.commit()
    except Exception as e:
        print(e)    
def update(tablename,columnname,new_value,condition_value,condition_column):
    try:
        sql_query = f"UPDATE `{tablename}` SET `{columnname}` = %s WHERE `{condition_column}` = %s"
        mycursor.execute(sql_query, (new_value, condition_value))
        mydb.commit()
    except Exception as e:
        print(e)
      
def filter(tablename,columname,conditions):
      sql_query = f"SELECT {columname} FROM {tablename} WHERE {conditions}"     
      mycursor.execute(sql_query)
      result = mycursor.fetchall()
      for row in result:
                print(row) 
                
def sortbyAsc(tablename,columname): 
    sql_query = f"SELECT {columname} FROM {tablename} ORDER BY {columname} ASC"      
    mycursor.execute(sql_query)
    result = mycursor.fetchall()
    for row in result:
                print(row)             
    print(result)
def sortbydesc(tablename,columname): 
    sql_query = f"SELECT {columname} FROM {tablename} ORDER BY {columname} DESC"   
    mycursor.execute(sql_query)
    result = mycursor.fetchall()
    for row in result:
                print(row)             
    print(result)    
# filter('items', '*', "name LIKE '%m%'")              
sortbyAsc('person','name')

  
# update('person',"purchase_amt",50000,1,"person_id")