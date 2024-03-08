
import sqlite3
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionSearchProperty(Action):

    def name(self) -> Text:
        return "action_search_property"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Fetching slot values
        location = tracker.get_slot("location")
        bedrooms = tracker.get_slot("bedrooms")
        bathrooms = tracker.get_slot("bathrooms")
        price = tracker.get_slot("price")
        amenities= tracker.get_slot("amenities")
        area = tracker.get_slot("area")
        property_type = tracker.get_slot("property_type")
          # Printing slot values
        print(f"Location: {location}")
        print(f"Bedrooms: {bedrooms}")
        print(f"Bathrooms: {bathrooms}")
        print(f"Price: {price}")
        print(f"amenities: {amenities}")
        print(f"area: {area}")
        print(f"property_type: {property_type}")

        # Handling empty slots
        if location is None:
            location = ''
        if bedrooms is None:
            bedrooms = ''
        if bathrooms is None:
            bathrooms = ''
        if price is None:
            price = ''
        if amenities is None:
            amenities = ''
        if area is None:
            area = ''
        if property_type is None:
            property_type = ''

        # Establish connection to the sqlite database
        conn = sqlite3.connect("property_listings.db")
        cursor = conn.cursor()
        
        # Build the SQL query based on user criteria
        query = "SELECT * FROM properties WHERE 1=1"
        params = {}

        # Searching based on single slot
        if location and not any([bedrooms, bathrooms, price,area,property_type,amenities]):
            query += " AND Location LIKE :location"
            params['location'] = f"%{location.strip()}%"
        if price and not any([location, bedrooms, bathrooms, area, property_type, amenities]):
            query += " AND (price LIKE :price OR price < :less_than_price)"
            params['price'] = f"%{price.strip()}%"
            params['less_than_price'] = price.strip()
        elif bedrooms and not any([location, bathrooms, price,area,property_type,amenities]):
            query += " AND bedrooms LIKE :bedrooms"
            params['bedrooms'] = f"%{bedrooms.strip()}%"
        elif bathrooms and not any([location, bedrooms, price,area,property_type,amenities]):
            query += " AND bathrooms LIKE :bathrooms"
            params['bathrooms'] = f"%{bathrooms.strip()}%"
        elif amenities and not any([location, bedrooms, bathrooms, price,area,property_type]):
            query += " AND Amenities LIKE :amenities "
            params['amenities'] = f"%{amenities.strip()}%"
        elif area and not any([location, bedrooms, bathrooms, price, amenities]):
            query += " AND Area LIKE :area "
            params['area'] = f"%{area.strip()}%"
        elif property_type and not any([location, bedrooms, bathrooms, price, amenities, area]):
            query += " AND (Property_Type_1 LIKE :property_type OR Property_Type_2 LIKE :property_type)"
            params['property_type'] = f"%{property_type.strip()}%"
        else:  # User provides multiple slots or no specific slot
            if location:
                query += " AND Location LIKE :location"
                params['location'] = f"%{location.strip()}%"
            if bedrooms:
                query += " AND bedrooms LIKE :bedrooms"
                params['bedrooms'] = f"%{bedrooms.strip()}%"
            if bathrooms:
                query += " AND bathrooms LIKE :bathrooms"
                params['bathrooms'] = f"%{bathrooms.strip()}%"
            if price:
                query += " AND (price LIKE :price OR price < :less_than_price)"
                params['price'] = f"%{price.strip()}%"
                params['less_than_price'] = price.strip()
            if amenities:
                query += " AND Amenities LIKE :amenities  "  # Amend column names if needed
                params['amenities'] = f"%{amenities.strip()}%"

            if area:
                query += " AND Area LIKE :area "  # Amend column names if needed
                params['area'] = f"%{area.strip()}%"

            if property_type:
                query += " AND (Property_Type_1 LIKE :property_type OR Property_Type_2 LIKE :property_type)"  # Amend column names if needed
                params['property_type'] = f"%{property_type.strip()}%"
                    
        # Execute the query and fetch results
        print("Final SQL Query:", query)
        print("Parameters:", params)
        query += " ORDER BY Publish_Date DESC LIMIT 5"

        cursor.execute(query, params)
        results = cursor.fetchall()
        print(results)
        
        
        # Close the database connection
        conn.close()
        
        # Handle the results
        if not results:
            dispatcher.utter_message(template="utter_no_properties_found")
        else:
            # Format and send property listings to the user
            property_listings = "\n".join([
    f"Property ID: {row[0]}, Reference ID: {row[1]}, Verification: {row[2]}, "
    f"Property Type 1: {row[3]}, Property Type 2: {row[4]}, Property Status: {row[5]}, "
    f"Title: {row[6]}, Description: {row[7]}, Location: {row[8]}, Sub-Location: {row[9]}, "
    f"Bedrooms: {row[10]}, Bathrooms: {row[11]}, Price: {row[12]} AED, Map: {row[13]}, "
    f"Publish Date: {row[14]}, Area: {row[15]}, Agent Name: {row[16]}, Agency Name: {row[17]}, "
    f"Amenities: {row[18]}, Listed By: {row[19]}, Furnishing: {row[20]}, "
    f"PERMIT Number: {row[21]}, BRN Number: {row[22]}"
    for row in results
])
            print(property_listings)
            dispatcher.utter_message(template="utter_search_properties", property_listings=property_listings)
        
        return []

    

class ActionGetRecommendations(Action):
    def name(self) -> Text:
        return "action_get_recommendations"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract user preferences and criteria
        min_bedrooms = tracker.get_slot("min_bedrooms")
        max_price = tracker.get_slot("max_price")

        # Establish a connection to the SQLite database
        conn = sqlite3.connect('property_listings.db')
        cursor = conn.cursor()

        # SQL query to fetch property listings based on criteria
        query = "SELECT * FROM property_listings WHERE bedrooms >= ? AND price <= ?"
        cursor.execute(query, (min_bedrooms, max_price))
        results = cursor.fetchall()

        # Process the results and send them to the user
        if results:
            for row in results:
                # Format the result to be sent to the user
                property_info = (
                    f"Property ID: {row[0]}, Reference ID: {row[1]}, Verification: {row[2]}, "
                    f"Property Type 1: {row[3]}, Property Type 2: {row[4]}, Property Status: {row[5]}, "
                    f"Title: {row[6]}, Description: {row[7]}, Location: {row[8]}, Sub-Location: {row[9]}, "
                    f"Bedrooms: {row[10]}, Bathrooms: {row[11]}, Price: {row[12]} AED, Map: {row[13]}, "
                    f"Publish Date: {row[14]}, Area: {row[15]}, Agent Name: {row[16]}, Agency Name: {row[17]}, "
                    f"Amenities: {row[18]}, Listed By: {row[19]}, Furnishing: {row[20]}, "
                    f"PERMIT Number: {row[21]}, BRN Number: {row[22]}"
                )
                dispatcher.utter_message(text=property_info)
        else:
            dispatcher.utter_message(text="No properties found matching your criteria.")

        # Close the database connection
        conn.close()

        return []