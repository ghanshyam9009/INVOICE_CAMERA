
import requests
import json
import os

# Define the API URL and image path
url = 'https://app.nanonets.com/api/v2/OCR/Model/63ab7f45-d03d-469f-8bc9-40ad18b03b4b/LabelFile/?async=false'
# image_path = r'C:\Users\ghans\OneDrive\Pictures\Desktop\invoice_detection\data\20201023_171147 - indersingh manawat.jpg'

def extract_table_data_from_image(image_path):
    # Prepare the data for the POST request
    data = {'file': open(image_path, 'rb')}

    # Make the POST request
    response = requests.post(url, auth=requests.auth.HTTPBasicAuth('510ed11a-5097-11ef-bb37-0e9d044952e6', ''), files=data)

    # Load the JSON response
    result = response.json()

    # Initialize an array to hold the extracted table data
    table_data = []

    # Check if the response is successful
    if result["message"] == "Success":
        for prediction in result["result"]:
            for item in prediction['prediction']:
                if item['label'] == "table":
                    # Create a dictionary to hold the rows
                    row_data = {}

                    # Extracting text from the 'cells' key and organizing it by row and column
                    if 'cells' in item:
                        for cell in item['cells']:
                            row = cell['row']
                            col = cell['col']
                            text = cell['text']

                            # Initialize the row in the dictionary if it doesn't exist
                            if row not in row_data:
                                row_data[row] = {}

                            # Assign the cell text to the corresponding column
                            row_data[row][col] = text

                    # Store the extracted data in the array
                    for row in sorted(row_data.keys()):
                        row_entry = []
                        for col in sorted(row_data[row].keys()):
                            row_entry.append(row_data[row][col])
                        table_data.append(row_entry)

    return table_data
