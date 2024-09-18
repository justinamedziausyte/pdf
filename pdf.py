import fitz  # PyMuPDF
import pytesseract
from PIL import Image

# Open the input PDF file
pdf_filename = "input.pdf"
doc = fitz.open(pdf_filename)

# Initialize an empty string to store the extracted text
text = ""

# Loop through each page and extract text
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    
    # Extract text directly if available
    page_text = page.get_text()
    
    if page_text.strip():
        # If text is found, append to the text variable
        text += page_text
    else:
        # If no text is found, attempt OCR
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        ocr_text = pytesseract.image_to_string(img)
        text += ocr_text

    # Debugging output for each page
    print(f"Page {page_num + 1} text length: {len(page_text)} OCR text length: {len(ocr_text) if not page_text.strip() else ''}")

# Write the text to an output file
with open("output.txt", "w") as f:
    f.write(text)

# Debugging output for total text length
print(f"Total extracted text length: {len(text)}")
