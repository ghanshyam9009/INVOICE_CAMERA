import pytesseract
from PIL import Image, ImageDraw

def perform_ocr(image_path):
    """Perform OCR on the image and process text from the upper 40% section."""
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return "", ""  # Return empty strings instead of None

    ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    # Extract text and bounding boxes
    text_data = ocr_data['text']
    bounding_boxes = list(zip(ocr_data['left'], ocr_data['top'], ocr_data['width'], ocr_data['height']))
    image_height = image.height
    split_point = image.width // 2

    # Prepare to collect text data
    left_text_lines, right_text_lines = [], []

    for i in range(len(text_data)):
        text = text_data[i].strip()
        if not text:
            continue

        left, top, width, height = bounding_boxes[i]

        # Only consider text in the upper 40% of the image
        if top < image_height * 0.4:
            if left + width <= split_point:  # Left portion
                left_text_lines.append((text, left, top, width, height))
            else:  # Right portion
                right_text_lines.append((text, left, top, width, height))

    # Draw bounding boxes on the image (optional)
    draw_bounding_boxes(image, left_text_lines, right_text_lines)

    # Generate formatted text outputs
    left_text = format_text_for_invoice(left_text_lines)
    right_text = format_text_for_invoice(right_text_lines)
    
    print("\nLeft Portion:\n" + left_text)
    print("\nRight Portion:\n" + right_text)

    return left_text, right_text

def draw_bounding_boxes(image, left_text_lines, right_text_lines):
    """Draw bounding boxes and text on the image."""
    draw = ImageDraw.Draw(image)
    
    for text, left, top, width, height in left_text_lines:
        draw.rectangle([left, top, left + width, top + height], outline="red", width=2)  # Draw red box
        draw.text((left, top - 10), text, fill="red")
    
    for text, left, top, width, height in right_text_lines:
        draw.rectangle([left, top, left + width, top + height], outline="green", width=2)  # Draw green box
        draw.text((left, top - 10), text, fill="green")

    image.show()  # Show the image with bounding boxes (consider commenting this out for production)

def format_text_for_invoice(text_lines):
    """Format extracted text lines for invoice layout."""
    # Sort text lines by their vertical and then horizontal position
    text_lines.sort(key=lambda x: (x[2], x[1]))  
    formatted_text = []
    current_line = []
    last_top = None

    for text, left, top, _, _ in text_lines:
        if last_top is not None and abs(top - last_top) > 20:  # Significant gap, start a new line
            formatted_text.append(" ".join(current_line))
            current_line = []

        current_line.append(text)
        last_top = top

    if current_line:
        formatted_text.append(" ".join(current_line))

    return "\n".join(formatted_text)





# import pytesseract
# from PIL import Image, ImageDraw

# def perform_ocr(image_path):
#     """Perform OCR on the image and process text from the upper 40% section."""
#     try:
#         image = Image.open(image_path)
#     except Exception as e:
#         print(f"Error opening image: {e}")
#         return "", ""  # Return empty strings instead of None

#     ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

#     # Extract text and bounding boxes
#     text_data = ocr_data['text']
#     bounding_boxes = list(zip(ocr_data['left'], ocr_data['top'], ocr_data['width'], ocr_data['height']))
#     image_height = image.height
#     split_point = image.width // 2

#     # Prepare to collect text data
#     left_text_lines, right_text_lines = [], []

#     for i in range(len(text_data)):
#         text = text_data[i].strip()
#         if not text:
#             continue

#         left, top, width, height = bounding_boxes[i]

#         # Only consider text in the upper 40% of the image
#         if top < image_height * 0.4:
#             if left + width <= split_point:  # Left portion
#                 left_text_lines.append((text, left, top, width, height))
#             else:  # Right portion
#                 right_text_lines.append((text, left, top, width, height))

#     # Draw bounding boxes on the image
#     draw_bounding_boxes(image, left_text_lines, right_text_lines)

#     # Generate formatted text outputs
#     left_text = format_text_for_invoice(left_text_lines)
#     right_text = format_text_for_invoice(right_text_lines)

#     print("\nLeft Portion:\n" + left_text)
#     print("\nRight Portion:\n" + right_text)

#     return left_text, right_text

# def draw_bounding_boxes(image, left_text_lines, right_text_lines):
#     """Draw bounding boxes and text on the image."""
#     draw = ImageDraw.Draw(image)

#     for text, left, top, width, height in left_text_lines:
#         draw.rectangle([left, top, left + width, top + height], outline="red", width=2)  # Draw red box
#         draw.text((left, top - 10), text, fill="red")

#     for text, left, top, width, height in right_text_lines:
#         draw.rectangle([left, top, left + width, top + height], outline="green", width=2)  # Draw green box
#         draw.text((left, top - 10), text, fill="green")

#     image.show()  # Show the image with bounding boxes (consider commenting this out for production)

# def format_text_for_invoice(text_lines):
#     """Format extracted text lines for invoice layout."""
#     # Sort text lines by their vertical and then horizontal position
#     text_lines.sort(key=lambda x: (x[2], x[1]))  
#     formatted_text = []
#     current_line = []
#     last_top = None

#     for text, left, top, _, _ in text_lines:
#         # Clean up common OCR errors
#         text = clean_text(text)

#         if last_top is not None and abs(top - last_top) > 20:  # Significant gap, start a new line
#             formatted_text.append(" ".join(current_line))
#             current_line = []

#         current_line.append(text)
#         last_top = top

#     if current_line:
#         formatted_text.append(" ".join(current_line))

#     return "\n".join(formatted_text)

# def clean_text(text):
#     """Clean up common OCR errors in the extracted text."""
#     text = text.replace("’", "'")  # Replace curly apostrophes with straight ones
#     text = text.replace(" i ", " : ")  # Correct common misrecognition of colon
#     text = text.replace(" - ", "-")  # Remove spaces around dashes
#     text = text.replace(" (", "(")  # Remove space before parenthesis
#     text = text.replace(") ", ")")  # Remove space after parenthesis
#     # Add more replacements as necessary

#     return text

