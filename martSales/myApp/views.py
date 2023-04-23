from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
import mysql.connector as ms

def make_connection():
    mydb = ms.connect(
        host= "localhost",
        user= "root",
        password= "Vilas@343",
        database= "mart_sales"
    )
    return mydb

def base(request):
    return render(request, "base.html")

def home(request):
    return render(request, 'home.html')

def Analysis(request):
    return render(request, "Analysis.html")

def log_out(request):
    return redirect("/")

username = ''
password = ''
def login_action(request):
    global username, password

    db_user = ''
    db_pass = ''
    mydb = make_connection()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT*FROM login")
    login_cred = mycursor.fetchall()
     
    ds = request.POST
    for key, value in ds.items():
        if key == 'username':
            username = value
        if key == 'password':
            password = value

    for x in login_cred:
        db_user = x[0]
        db_pass = x[1]
        if db_user == username and db_pass == password:
            return redirect('/home/')
    
    messages.info(request, 'INVALID CREDENTIALS !!!!')
    return redirect('/')

def Excel_to_db(excel):
    my_con = make_connection()
    my_cursor = my_con.cursor()
    # print(my_con)
    my_cursor.execute("CREATE TABLE db1(Products VARCHAR(100), Total INT)")
    names = excel['Products']
    sales = excel["Total"] 

    for i in range(0, 50):
        # print(names[i])
        # print(sales[i])
        n = names[i]
        s = sales[i].item()
        # print(type(n))
        # print(type(s))

        sql = "INSERT INTO db1 (Products, Total) VALUES (%s, %s)"
        # print(sql)
        # val = ("Chips", 100) 
        val = (n, s) 
        # print(sql, val)
        my_cursor.execute(sql, val)
        my_con.commit()

    sum_query = "SELECT Products, SUM(Total) AS TotalPrice from db1 GROUP BY Products"
    my_cursor.execute(sum_query)
    ans = my_cursor.fetchall()
    for i in ans:
        print(i[1])
    # print(ans)
    my_con.close()


def upload_file(request):
    if request.method == "POST":
        file = request.FILES["myFile"]
        excel = pd.read_excel(file)
        sumition = Excel_to_db(excel)
        # print(excel.head())
        # arr = excel["sum2"]
        # sumition = sum(arr)
        # print(sumition)
        return render(request, "Analysis.html", {"something": True, "sum": sumition})
    return render(request, 'home.html')
        


