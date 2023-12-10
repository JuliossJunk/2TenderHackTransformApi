from docx2pdf import convert as docx2pdf_convert
import os
import subprocess
def convert_docx_to_pdf(input_file, output_file):
    """Convert a DOCX file to PDF using LibreOffice."""
    command = ['libreoffice', '--convert-to', 'pdf', output_file, input_file]
    subprocess.call(command)
    return output_file
# #pypandoc.download_pandoc()
# def convert_docx_to_pdf(input_file, output_file):
#     try:
#         # Convert DOCX to PDF using pypandoc
#         pypandoc.convert_file(input_file, 'pdf', outputfile=output_file, extra_args=['--pdf-engine=pdflatex'])
#
#         print(f"Conversion successful. PDF saved to {output_file}")
#         return output_file
#     except Exception as e:
#         print(f"Error during conversion: {e}")



def convert_and_save(input_path, output_path):
    docx_file_path = input_path
    pdf_file_path = output_path
    docx2pdf_convert(docx_file_path, pdf_file_path)
    return pdf_file_path

if __name__ == '__main__':

    #convert_and_save("modified_A.docx", "modified_A.pdf")
    # Replace 'input.docx' with the path to your DOCX file
    input_file_path = "modified_A.docx"

    # Replace 'output.pdf' with the desired path and name for the output PDF file
    output_file_path = "modified_A.pdf"

    convert_docx_to_pdf(input_file_path, output_file_path)