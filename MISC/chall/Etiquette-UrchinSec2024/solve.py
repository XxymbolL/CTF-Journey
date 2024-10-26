import pdfplumber
import re

text = ""
with pdfplumber.open("Etiquette_Book.pdf") as pdf:
    for page in pdf.pages:
        text += page.extract_text() + "\n"

# Now `text` contains all the text from the PDF
# Find all 13-letter words
words_13_letters = re.findall(r'\b\w{13}\b', text)

# Print found words
print(words_13_letters)

