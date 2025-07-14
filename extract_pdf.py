import PyPDF2

pdf_path = "Credit_Card_Databases-API/ERD.pdf"

with open(pdf_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    num_pages = len(reader.pages)
    print(f"Number of pages: {num_pages}")
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        print(f"\n--- Page {i+1} ---\n")
        print(text)
