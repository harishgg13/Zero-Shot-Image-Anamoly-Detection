import streamlit as st
import pymysql
import math
import pandas as pd

con=pymysql.connect(
    host="localhost",        # your DB host
    user="root",             # your username
    password="12345678",
    database="production"
)
cursor = con.cursor()
# --------------------------------------------------------------------------------------------------------------------
def info(table_name):
    total_check=f"select count(*) from {table_name};"
    cursor.execute(total_check)
    p = cursor.fetchone()[0]

    total_good=f"select count(*) from {table_name} where result = 1;"
    cursor.execute(total_good)
    q = cursor.fetchone()[0]

    total_defective=f"select count(*) from {table_name} where result = 0;"
    cursor.execute(total_defective)
    r = cursor.fetchone()[0]

    a = q
    b = r
    c = p
    g = math.gcd(a, b)
    ratio = (a // g, b // g)
    production_prob=f"{ratio[0]} : {ratio[1]}"

    last_check=f"select max(time) from {table_name};"
    cursor.execute(last_check)
    time = cursor.fetchone()[0]

    percent=(a/c)*100
    if percent > 90:
        machine_status= "Excellent"
    elif percent > 75:
        machine_status= "Good"
    elif percent > 60:
        machine_status= "Moderate"
    elif percent > 40:
        machine_status= "Poor"
    else:
        machine_status= "Critical"

    return p,q,r,production_prob,time,machine_status,percent

# --------------------------------------------------------------------------------------------------------------------

def History(table_name,input):
    a=pd.read_sql(sql=f"select * from {table_name} order by time desc limit {input};",con=con)
    return a

# --------------------------------------------------------------------------------------------------------------------

def health(days,table_name):
    query = f"""SELECT (sum(result)/count(result))*100
FROM {table_name}
WHERE time >= NOW() - INTERVAL {days} DAY;"""
    cursor.execute(query)
    health = cursor.fetchone()[0]
    return health
    
# --------------------------------------------------------------------------------------------------------------------
if st.session_state.page == "Machine Status":
    machine=st.selectbox("Select the Machine",["Hazelnut", "Tooth Brush"])
    option=st.radio("Select one option",["Machine Information","Latest History","Machine Health"],horizontal=True)
    if machine == "Hazelnut":
        if option == "Machine Information":
            TC,TG,TD,PP,LC,MS,percent=info("hazelnut") #,PP,LC,MS
            st.markdown(f"""<h3>
                        Machine Name : Hazel Nut </br>
                        Total Check : {TC} </br>
                        Total Good : {TG} </br>
                        Total Defective : {TD} </br>
                        Prodcution Probability (Good:Defective): {PP} </br>
                        Last Check : {LC} </br>
                        Machine Status : {MS} </br>
                        Overall Good Production : {percent}
                        </h3>
                        """,unsafe_allow_html=True)
            
        elif option == "Latest History":
            input=st.text_input("Enter the Entries","10")
            result=History("hazelnut",input)
            st.dataframe(result, hide_index=True)

        else:
            input=st.text_input("Enter the No.of Days","10")
            result=health(int(input),"hazelnut")
            st.markdown(f"""<h3>
                        Health of Hazelnut Machine in the interval of last {input} days is {result} %
                        """,unsafe_allow_html=True)


    if machine == "Tooth Brush":
        if option == "Machine Information":
            TC,TG,TD,PP,LC,MS,percent=info("toothbrush") #,PP,LC,MS
            st.markdown(f"""<h3>
                        Machine Name : Tooth Brush </br>
                        Total Check : {TC} </br>
                        Total Good : {TG} </br>
                        Total Defective : {TD} </br>
                        Prodcution Probability (Good:Defective): {PP} </br>
                        Last Check : {LC} </br>
                        Machine Status : {MS} </br>
                        Overall Good Production : {percent}
                        </h3>
                        """,unsafe_allow_html=True)
        elif option == "Latest History":
            input=st.text_input("Enter the Entries","10")
            result=History("toothbrush",input)
            st.dataframe(result, hide_index=True)

        else:
            input=st.text_input("Enter the No.of Days","10")
            result=health(int(input),"toothbrush")
            st.markdown(f"""<h3>
                        Health of ToothBrush Machine in the interval of last {input} days is {result} %
                        """,unsafe_allow_html=True)
# --------------------------------------------------------------------------------------------------------------------

    
