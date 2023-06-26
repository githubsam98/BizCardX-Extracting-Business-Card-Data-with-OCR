import streamlit as st
import pandas as pd
import easyocr
import mysql.connector
from mysql.connector import Error
import cv2
import numpy as np

#Connection for mysql
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sharma123@",
    database="bizcard"
)
#creating a CURSOR for mysql query
mycursor = mydb.cursor()

#create the table to store details of businesscard
mycursor.execute("CREATE TABLE IF NOT EXISTS bus (id INT AUTO_INCREMENT PRIMARY KEY , name VARCHAR(255),job VARCHAR(255),address VARCHAR(255),postcode VARCHAR(255),phone VARCHAR(255),email VARCHAR(255),website VARCHAR(255),company_name VARCHAR(255)) ")

#Read the card details using easyocr
reader = easyocr.Reader(['en'])

#streamlit setup
st.title(':blue[Get **Frustrated** by kepping your cards in a wallet]:imp:')
st.subheader(':grey[Here is solution   !!]')

#Upload file widgets
Upload_files = st.file_uploader(":white[Upload your Business Card Here]",type=["jpg","jpeg","png"])

#sidebar
menu = ['Add','View','Update',"Delete"]
choice = st.sidebar.selectbox("Select the Option ",menu)

if choice == 'Add':
    if Upload_files is not None :
        image = cv2.imdecode(np.fromstring(Upload_files.read(), np.uint8),1)
        #Display the uploaded image
        st.image(image,caption = 'uploaded Business card image ', use_column_width=True)
        #Create a Button
        if st.button('Extract Information'):
            read = reader.readtext(image,detail = 0)
            text = '\n'.join(read)

            #insert the information into sql database
            sql = "INSERT INTO bus(name,job_title,address,postcode,phone,email,website,company_name) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (read[0],read[1],read[2],read[3],read[4],read[5],read[6],read[7])
            mycursor.execute(sql,val)
            mydb.commit()
            #Display success message
            st.success("Business Card information Successfully added to Database")

    elif choice == 'view':
        #Display the stored card information
        mycursor.execute("SELECT * FROM bus")
        result = mycursor.fetchall()
        df= pd.DataFrame(result,columns= ['id','name','job_title','address','postcode','phone','email','website','company_name'])
        st.write(df)