import PyPDF2

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            print(f"Number of pages: {num_pages}")
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                print(f"\n--- Page {i+1} ---\n")
                if text:
                    print(text)
                else:
                    print("[No extractable text on this page]")
    except Exception as e:
        print(f"Error reading PDF: {e}")

if __name__ == "__main__":
    pdf_path = "ERD.pdf"
    extract_text_from_pdf(pdf_path)
