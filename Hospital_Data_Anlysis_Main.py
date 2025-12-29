import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Connect to MySQL database
def create_connection():
    connection = mysql.connector.connect(
        host="localhost",      # MySQL host, change if necessary
        user="root",  # Your MySQL username
        password="Indian123#",  # Your MySQL password
        database="hospital"  # The database you want to use
    )
    return connection

# Step 2: Fetch data from MySQL
def fetch_data():
    connection = create_connection()
    
    add_data()
    
    query = "SELECT * FROM hospital_data"  # Replace with your actual SQL query
    data = pd.read_sql(query, connection)
    connection.close()
    return data


def add_data():
    connection = create_connection()
    cursor = connection.cursor()

    stmt = """
        INSERT INTO hospital_data
        (Hospital_code, Hospital_type_code, City_Code_Hospital, Hospital_region_code, Available_EXTRA_Room,
         Type_of_Admission, Severity_of_Illness, Visitors_with_Patient, Age, Admission_Deposit, Stay)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # List of data to insert
    insert_values = [
        ('003', 'd', 103, 'Y2', 1, 'Emergency', 'Extreme', 1, '31-40', 16017, '0-10'),
        ('001', 'a', 101, 'Y2', 1, 'Trauma', 'Extreme', 3, '21-30', 6641, '11-20'),
        ('002', 'b', 101, 'Y2', 0, 'Trauma', 'Moderate', 1, '11-20', 6257, '11-20'),
        ('005', 'd', 103, 'Y2', 0, 'Emergency', 'Minor', 2, '51-60', 5942, '21-30'),
        ('001', 'd', 103, 'X1', 0, 'Trauma', 'Minor', 3, '11-20', 19916, '11-20')
    ]

    # Execute insert for each row
    for values in insert_values:
        cursor.execute(stmt, values)

    connection.commit()  # Save changes
    cursor.close()
    connection.close()
    print("Data inserted successfully.")
# Step 3: Data Analysis - You can perform various analyses here
def analyze_data(data):
    # Descriptive statistics
    print("Descriptive statistics:\n", data.describe())

    # Missing data
    print("\nMissing data:\n", data.isnull().sum())

    # Convert categorical columns to numeric codes
    categorical_cols = ['Hospital_code', 'Hospital_type_code', 'Hospital_region_code',
                        'Type_of_Admission', 'Severity_of_Illness', 'Age', 'Stay']
    for col in categorical_cols:
        if col in data.columns:
            data[col + "_num"] = data[col].astype('category').cat.codes

    # Compute correlation on numeric columns only
    numeric_data = data.select_dtypes(include='number')
    print("\nCorrelation matrix:\n", numeric_data.corr())

# Step 4: Data Visualization - Use Seaborn and Matplotlib for plotting
def visualize_data(data):
  # Histogram example for numeric column
    if 'Visitors_with_Patient' in data.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(data['Visitors_with_Patient'], kde=True)
        plt.title("Distribution of Visitors_with_Patient")
        plt.xlabel('Visitors_with_Patient')
        plt.ylabel('Frequency')
        plt.savefig("Visitors_with_Patient.png")  # image 1             
        plt.show()

     # Correlation heatmap (numeric columns only)
    numeric_data = data.select_dtypes(include='number')
    plt.figure(figsize=(12, 8))
    sns.heatmap(numeric_data.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Heatmap")
    plt.savefig("correlation_heatmap.png")  # Image 2
    plt.show()

        
# Main execution
if __name__ == "__main__":
    # Fetch data from MySQL
    data = fetch_data()

    # Perform analysis
    analyze_data(data)

    # Visualize data
    visualize_data(data)