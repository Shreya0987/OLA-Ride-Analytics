import sqlite3
import pandas as pd

# Load cleaned CSV
df = pd.read_csv(r"c:\Users\Shreya Ghosal\Downloads\ola_cleaned.csv")

# Connect to SQLite DB (it will create file if not exists)
conn = sqlite3.connect("ola_ola_project.db")
cursor = conn.cursor()

# Write the cleaned CSV to a table called 'rides'
df.to_sql("rides", conn, if_exists="replace", index=False)

print("Database created and CSV loaded into 'rides' table")

# Query 1: All successful bookings
query1 = "SELECT * FROM rides WHERE booking_status = 'completed';"
df1 = pd.read_sql(query1, conn)
df1['booking_status'] = df['booking_status'].str.lower().str.strip()
print("Query1 rows:", len(df1))

# Query 2: Average ride distance per vehicle type
query2 = """
SELECT vehicle_type,
       AVG(ride_distance) AS avg_distance_km,
       COUNT(*) AS total_rides
FROM rides
WHERE ride_distance IS NOT NULL
GROUP BY vehicle_type
ORDER BY avg_distance_km DESC;
"""
df2 = pd.read_sql(query2, conn)
print("Query2 Average ride distance per vehicle type:", df2)

# Query 3: Total number of cancelled rides by customers
query3 = "SELECT SUM(canceled_rides_by_customer) AS total_cancelled_by_customers FROM rides;"
df3 = pd.read_sql(query3, conn)
print("Query 3: Total number of cancelled rides by customers", df3)

# Query 4: Top 5 customers by number of rides
query4 = """
SELECT customer_id,
       COUNT(*) AS total_rides
FROM rides
GROUP BY customer_id
ORDER BY total_rides DESC
LIMIT 5;
"""
df4 = pd.read_sql(query4, conn)
print("Query 4: Top 5 customers by number of rides",df4)

# Query 5: Rides cancelled by drivers due to personal/car issues
query5 = """
SELECT incomplete_rides_reason AS cancellation_reason,
       SUM(canceled_rides_by_driver) AS total_cancelled
FROM rides
WHERE canceled_rides_by_driver > 0
  AND incomplete_rides_reason IN ('personal','car-related')
GROUP BY incomplete_rides_reason;
"""
df5 = pd.read_sql(query5, conn)
print("Query 5: Rides cancelled by drivers due to personal/car issues", df5)

# Query 6: Max and Min driver ratings for Prime Sedan
query6 = """
SELECT MAX(driver_ratings) AS max_rating,
       MIN(driver_ratings) AS min_rating
FROM rides
WHERE vehicle_type = 'prime sedan'
  AND driver_ratings IS NOT NULL;
"""
df6 = pd.read_sql(query6, conn)
print("Query 6: Max and Min driver ratings for Prime Sedan",df6)

# Query 7: Rides paid using UPI
query7 = "SELECT * FROM rides WHERE LOWER(payment_method) = 'upi';"
df7 = pd.read_sql(query7, conn)
print("Query7 rows:", len(df7))

# Query 8: Average customer rating per vehicle type
query8 = """
SELECT vehicle_type,
       AVG(customer_rating) AS avg_customer_rating,
       COUNT(*) AS rated_count
FROM rides
WHERE customer_rating IS NOT NULL
GROUP BY vehicle_type
ORDER BY avg_customer_rating DESC;
"""
df8 = pd.read_sql(query8, conn)
print("Query 8: Average customer rating per vehicle type",df8)

# Query 9: Total booking value of completed rides
query9 = "SELECT SUM(booking_value) AS total_booking_value FROM rides WHERE booking_status = 'completed';"
df9 = pd.read_sql(query9, conn)
print("Query 9: Total booking value of completed rides", df9)

# Query 10: List incomplete rides with reason
query10 = """
SELECT booking_id, customer_id, booking_status, incomplete_rides, incomplete_rides_reason
FROM rides
WHERE incomplete_rides = 1;
"""
df10 = pd.read_sql(query10, conn)
print("Query 10: List incomplete rides with reason",df10.head())