
import pprint

def reverse_words_in_lines(text):
    # Split text into lines and reverse the order of words in each line
    lines = text.strip().split('\n')
    reversed_lines = [' '.join(line.split()[::-1]) for line in lines]
    return reversed_lines

def extract_info(text):
    # Initialize variables to store extracted entities
    gstin = "Not Found"
    phone_numbers = []
    dl_no = "Not Found"
    invoice_no = "Not Found"
    date = "Not Found"

    # Split text into lines and reverse the order of words in each line
    lines = text.strip().split('\n')
    reversed_lines = reverse_words_in_lines(text)

    # Iterate through each reversed line to extract information
    for line in reversed_lines:
        if "GSTIN" in line:
            gstin = line.split(":")[-1].strip()  # Extract the GSTIN value
        elif "Phone" in line:
            phones = line.split(":")[-1].strip().split(",")
            for phone in phones:
                phone_numbers.append(phone.strip())
        elif "D.L.No" in line:
            dl_no = line.split(":")[-1].strip()  # Extract the D.L. No. value
        elif "Invoice" in line:
            invoice_no = line.split(":")[-1].strip()  # Extract the Invoice No. value
        elif "Date" in line:
            date = line.split(":")[-1].strip()  # Extract the Date value

    # Clean up extracted values
    gstin = gstin.replace("GSTIN", "").strip()
    phone_numbers = [phone.replace("Phone", "").strip() for phone in phone_numbers]

    # Return the extracted data as a nested object
    return {
        "GSTIN": gstin,
        "Phone Numbers": phone_numbers,
        "D.L. No.": dl_no,
        "Invoice No": invoice_no,
        "Date": date,
    }

def perform_ner(text_data):
    # Split the text data into left and right portions
    lines = text_data.strip().split('\n')
    mid_index = len(lines) // 2
    left_text = "\n".join(lines[:mid_index])  # Left portion
    right_text = "\n".join(lines[mid_index:])  # Right portion

    # Extract information from both left and right texts
    left_info = extract_info(left_text)
    right_info = extract_info(right_text)

    # Create nested objects for supplier and retailer
    output_data = {
        "Supplier": {
            "Details": left_info
        },
        "Retailer": {
            "Details": right_info
        },
    }

    pprint.pprint(output_data)
    # Return the output data
    return output_data


# Print the output data using pprint
# print("Using pprint:")
# pprint.pprint(output_data)

