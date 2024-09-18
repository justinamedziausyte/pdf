import fitz  # PyMuPDF

# Open the input PDF file
doc = fitz.open("input.pdf")

# Initialize an empty string to store the extracted text
text = ""

# Loop through each page and extract text
for page in doc:
    text += page.get_text()

# Write the text to an output file
with open("output.txt", "w") as f:
    f.write(text)
