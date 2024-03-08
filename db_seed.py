import sqlite3
import json

try:
    # Establish connection to the SQLite database
    conn = sqlite3.connect('property_listings.db')
    cursor = conn.cursor()

    # Read property data from JSON file
    with open('property_data.json', 'r') as file:
        property_data = json.load(file)

    # Create a property table if it doesn't exist
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS properties (
                       id INTEGER PRIMARY KEY,
                   Reference_ID TEXT,
                   Verification TEXT,
                   Property_Type_1 TEXT,
                   Property_Type_2 TEXT,
                   Property_Status TEXT,
                   Title TEXT,
                   Description TEXT,
                   Location TEXT,
                    Sub_Location TEXT,
                   Bedrooms TEXT,
                   Bathrooms TEXT,
                   Price FLOAT,
                  
                   Map TEXT,
                   Publish_Date DATE,
                   Area TEXT,
                   Agent_Name TEXT,
                   Agency_Name TEXT ,
                   Amenities TEXT , 
                   Listed_By TEXT ,
                   Furnishing TEXT ,
                   PERMIT_Number INTEGER ,
                   BRN_Number INTEGER ,
                   Source_Link TEXT ,
                   Source_Website TEXT ,
                   Agent_Picture TEXT 
 



                      
                   )
    """)
    
    
    # Create a viewings table if it doesn't exist
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS viewings (
                       id INTEGER PRIMARY KEY,
                       location TEXT,
                       viewing_date TEXT
                   )
    """)

    # Insert the property data into the database
    for prop in property_data:
        reference_id = prop['Reference ID']
        verification = prop['Verification']
        property_type_1 = prop['Property Type 1']
        property_type_2 = prop['Property Type 2']
        property_status = prop['Property Status']
        title = prop['Title']
        description = prop['Description']   
        location = prop['Location']
        Sub_Location=prop['Sub Location']
        bedrooms = prop['No of Bedroom']
        bathrooms = prop['No of Bathroom']
        price = prop['Price']
        map = prop['Map']
        Publish_Date = prop['Publish Date']
        Area = prop['Area']
        Agent_Name = prop['Agent Name']
        Agency_Name = prop['Agency Name']
        Amenities = prop['Amenities']
        Listed_By = prop['Listed By']
        Furnishing = prop['Furnishing']
        PERMIT_Number = prop['PERMIT Number']
        BRN_Number = prop['BRN Number']
        Source_Link = prop['Source Link']
        Source_Website = prop['Source Website']
        Agent_Picture = prop['Agent Picture']

        cursor.execute("INSERT INTO properties (Reference_ID, Verification, Property_Type_1, Property_Type_2, Property_Status, Title, Description, Location, Sub_Location, Bedrooms, Bathrooms, Price, Map, Publish_Date, Area, Agent_Name, Agency_Name, Amenities, Listed_By, Furnishing, PERMIT_Number, BRN_Number, Source_Link, Source_Website,Agent_Picture) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(reference_id, verification, property_type_1, property_type_2, property_status, title, description,location, Sub_Location, bedrooms, bathrooms, price, map, Publish_Date, Area, Agent_Name, Agency_Name, Amenities, Listed_By, Furnishing, PERMIT_Number, BRN_Number, Source_Link, Source_Website,Agent_Picture))
                     
                   


       
    # Commit the changes
    conn.commit()

except sqlite3.Error as e:
    print("SQLite error:", e)

except json.JSONDecodeError as e:
    print("JSON decode error:", e)

finally:
    # Close the connection in a finally block
    if conn:
        conn.close()
