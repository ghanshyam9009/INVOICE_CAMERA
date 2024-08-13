


import os
from flask import Flask, Blueprint, request, jsonify, current_app
from mysql.connector import connect, Error
from models.ocr import perform_ocr
from models.ner import perform_ner
from models.table_extraction import extract_table_data_from_image
import numpy as np
import cv2
import base64
import tempfile
import logging

app = Flask(__name__)

# Blueprint setup
api = Blueprint('api', __name__)

def create_connection():
    """ Create a database connection to the MySQL database """
    try:
        connection = connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DATABASE'],
            port=current_app.config['MYSQL_PORT']
        )
        logging.info("Connection to MySQL DB successful")
        return connection
    except Error as e:
        logging.error(f"The error '{e}' occurred")
        return None

@api.route('/process-image', methods=['POST'])
def process_image():
    connection = create_connection()
    if connection is None:
        return jsonify({"error": "Failed to connect to the database."}), 500

    try:
        data = request.get_json()
        image_data = data.get('image_data')

        # Decode the base64 image
        image_data = image_data.split(',')[1]
        img = np.frombuffer(base64.b64decode(image_data), np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        if img is not None:
            logging.info(f"Image received successfully. Shape: {img.shape}")

            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                temp_file_path = temp_file.name
                cv2.imwrite(temp_file_path, img)

            extracted_text = perform_ocr(temp_file_path)
            logging.info(f"Extracted text: {extracted_text}")

            text_data = ' '.join(extracted_text)
            entities = perform_ner(text_data)
            logging.info(f"Extracted entities: {entities}")

            table_data = extract_table_data_from_image(temp_file_path)
            logging.info(f"Extracted table data: {table_data}")

            supplier_details = entities.get('Supplier', {})
            retailer_details = entities.get('Retailer', {})

            extracted_data_final = {
                'full_data': ' '.join(extracted_text),
                'supplier_details': supplier_details,
                'retailer_details': retailer_details,
                'table_data': table_data,
            }

            # with connection.cursor() as cursor:
            #     sql = """
            #         INSERT INTO extracted_data2 (full_data, supplier_details, retailer_details, table_data)
            #         VALUES (%s, %s, %s, %s)
            #     """
            #     cursor.execute(sql, (
            #         extracted_data_final['full_data'],
            #         str(supplier_details),
            #         str(retailer_details),
            #         str(table_data)
            #     ))
            #     connection.commit()

            #     if cursor.rowcount > 0:
            #         logging.info("Data inserted successfully.")
            #     else:
            #         logging.warning("No data was inserted.")

            os.remove(temp_file_path)

            return jsonify(extracted_data_final)
        else:
            return jsonify({"error": "Failed to process the image."}), 400

    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

@api.route('/store-data', methods=['POST'])
def store_data():
    connection = create_connection()
    if connection is None:
        return jsonify({"error": "Failed to connect to the database."}), 500

    try:
        data = request.get_json()

        # Assuming the data contains 'full_data', 'supplier_details', 'retailer_details', and 'table_data'
        full_data = data.get('full_data')
        supplier_details = data.get('supplier_details', {})
        retailer_details = data.get('retailer_details', {})
        table_data = data.get('table_data', {})

        with connection.cursor() as cursor:
            sql = """
                INSERT INTO extracted_data2 (full_data, supplier_details, retailer_details, table_data)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (
                full_data,
                str(supplier_details),
                str(retailer_details),
                str(table_data)
            ))
            connection.commit()

            if cursor.rowcount > 0:
                logging.info("Data inserted successfully.")
                return jsonify({"message": "Data stored successfully."}), 201
            else:
                logging.warning("No data was inserted.")
                return jsonify({"error": "No data inserted."}), 400

    except Exception as e:
        logging.error(f"Error storing data: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

# Register the blueprint
app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True)
