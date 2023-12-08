from docx import Document
from docx2pdf import convert
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def convert_docx_to_pdf(docx_file_path, pdf_file_path):
    # Convert DOCX to PDF (handles text)
    convert(docx_file_path, pdf_file_path)

    # Convert images to PDF using reportlab
    doc = Document(docx_file_path)
    pdf_canvas = canvas.Canvas(pdf_file_path, pagesize=letter)

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if run.bold:
                pdf_canvas.setFont("Helvetica-Bold", 12)
            else:
                pdf_canvas.setFont("Helvetica", 12)
            pdf_canvas.drawString(100, 750, run.text)
            pdf_canvas.showPage()

    pdf_canvas.save()

if __name__ == "__main__":
    docx_file_path = "example.docx"  # Replace with the path to your DOCX file
    pdf_file_path = "output.pdf"  # Replace with the desired output PDF path

    convert_docx_to_pdf(docx_file_path, pdf_file_path)
