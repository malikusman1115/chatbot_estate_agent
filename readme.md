Property Finder Chatbot
Introduction
This project implements a chatbot using Rasa, an open-source machine learning framework for automated text and voice-based conversations. The chatbot assists users in finding properties based on their preferences such as location, number of bedrooms, bathrooms, price range, amenities, and area. It leverages SQLite for property listings storage and retrieval.

Features
Fetch property listings based on user preferences.
Custom actions to search properties and provide recommendations.
Integration with SQLite database for dynamic property data handling.
Flask server to expose a webhook for Rasa chatbot interaction.
Prerequisites
Python 3.6 or newer
Rasa 2.0 or newer
SQLite3
Installation
Clone the Repository

bash
 https://github.com/malikusman1115/chatbot_estate_agent.git
cd your-repository
Set Up a Virtual Environment (Optional, but recommended)

bash

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies


pip install -r requirements.txt
Training the Rasa Model
Navigate to the project directory and run:


rasa train
This command trains a new Rasa model using your NLU data and stories.

Running the Actions Server
Open a new terminal window and activate the virtual environment if necessary. Then, start the Rasa action server:

arduino

rasa run actions
Running the Flask App


python app.py
This command starts the Flask server with the webhook configured for Rasa to interact with.

Usage
Interact with the Chatbot through the Command Line
Start the Rasa shell in your terminal:


rasa shell
You can now interact with the chatbot directly in the command line.

Interact via Webhook
Send a POST request to the Flask server's /webhook endpoint with a JSON body containing the user's message. For example:


curl -X POST http://localhost:5000/webhook -d "{\"message\": \"Hello\"}" -H "Content-Type: application/json"
The server will return the chatbot's response as JSON.

Database Configuration
The project uses an SQLite database (property_listings.db) to store and query property listings. Ensure that the database and table schemas are set up as per your project's requirements.

Customizing the Chatbot
You can customize the chatbot's behavior and responses by editing the domain.yml, config.yml, data/nlu.yml, and data/stories.yml files according to the Rasa documentation.

License
Specify the license under which your project is released.