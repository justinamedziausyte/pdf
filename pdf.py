import fitz  # PyMuPDF
import pytesseract
from PIL import Image

# Ensure Lithuanian language package for Tesseract OCR is installed correctly
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
LANGUAGE = 'lit'  # Lithuanian language code for Tesseract OCR

# Open the input PDF file
pdf_filename = "input.pdf"
doc = fitz.open(pdf_filename)

# Initialize a list to store extracted content by page
extracted_content = []

# Loop through each page and extract text
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    
    # Extract text directly if available
    page_text = page.get_text()
    
    if not page_text.strip():
        # If no text is found, attempt OCR for Lithuanian
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        page_text = pytesseract.image_to_string(img, lang=LANGUAGE)
    
    extracted_content.append(page_text)
    # Debugging output for each page
    print(f"Page {page_num + 1} text length: {len(page_text)}")

# Join all extracted content
text = "\n".join(extracted_content)

# Basic identification for questions and answers (Simple heuristics)
questions_and_answers = []
lines = text.split('\n')
for i, line in enumerate(lines):
    if "?" in line:
        question = line.strip()
        # Look for possible answers (next few lines)
        possible_answers = []
        for j in range(1, 5):  # Assume next 4 lines could be answers
            if i + j < len(lines):
                answer_line = lines[i + j].strip()
                if answer_line and not any(char in answer_line for char in "?"):
                    possible_answers.append(answer_line)
        questions_and_answers.append((question, possible_answers))

# Write the detected questions and answers to an output file
with open("output.txt", "w") as f:
    for question, answers in questions_and_answers:
        f.write(f"Question: {question}\n")
        for answer in answers:
            f.write(f"  Answer: {answer}\n")
        f.write("\n")

# Debugging output for total text length
print(f"Total extracted text length: {len(text)}")
