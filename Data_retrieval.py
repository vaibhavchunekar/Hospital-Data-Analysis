import mysql.connector
import pandas as pd

# Step 1: Connect to MySQL
def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Indian123#",
        database="hospital"
    )
    return connection

# Step 2: Fetch data
def fetch_data():
    connection = create_connection()
    query = "SELECT * FROM hospital_data"  # Replace with your table name
    data = pd.read_sql(query, connection)
    connection.close()
    return data

# Step 3: Save to CSV
data = fetch_data()
data.to_csv(r"C:\Users\chune\Desktop\Medical_Project\hospital_data.csv", index=False)  # Save CSV in project folder
print("Data exported successfully!")