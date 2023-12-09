from docx2pdf import convert as docx2pdf_convert

def convert_and_save(input_path, output_path):
    docx_file_path = input_path
    pdf_file_path = output_path
    docx2pdf_convert(docx_file_path, pdf_file_path)
    return pdf_file_path

if __name__ == '__main__':
    convert_and_save("modified_A.docx", "modified_A.pdf")
