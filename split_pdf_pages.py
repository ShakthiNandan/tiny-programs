import os
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(input_pdf_path, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Read the input PDF
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)

    print(f"Total pages in input PDF: {total_pages}")

    for page_num in range(total_pages):
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num])

        output_filename = os.path.join(output_folder, f"page_{page_num + 1}.pdf")
        with open(output_filename, "wb") as output_pdf:
            writer.write(output_pdf)

        print(f"Saved: {output_filename}")

# Example usage
if __name__ == "__main__":
    input_pdf_path = "2.pdf"  # Replace with your PDF file path
    output_folder = "split_pages"         # Replace with desired output folder name
    split_pdf(input_pdf_path, output_folder)
