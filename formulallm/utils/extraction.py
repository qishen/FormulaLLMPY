import zipfile, fitz, os
from PyPDF2 import PdfReader

def extract_images_docx(docx_file: str, output_path: str):
    z = zipfile.ZipFile(docx_file)

    all_files = z.namelist()

    images = filter(lambda x: x.startswith('word/media/'), all_files)
    for img in images:
        z.extract(img, output_path)

def extract_pdf_drawings(pdf_file: str, output_path: str):
    doc = fitz.open(pdf_file)
    page = doc[0]
    paths = page.get_drawings()  

    outpdf = fitz.open()
    outpage = outpdf.new_page(width=page.rect.width, height=page.rect.height)
    shape = outpage.new_shape()  

    for path in paths:
        for item in path["items"]:  
            if item[0] == "l":  
                shape.draw_line(item[1], item[2])
            elif item[0] == "re":  
                shape.draw_rect(item[1])
            elif item[0] == "qu": 
                shape.draw_quad(item[1])
            elif item[0] == "c":
                shape.draw_bezier(item[1], item[2], item[3], item[4])
            else:
                raise ValueError("unhandled drawing", item)

        shape.finish(
            fill=path["fill"],  
            color=path["color"],  
            dashes=path["dashes"], 
            even_odd=path.get("even_odd", True),  
            closePath=path["closePath"],  
            width=path["width"],  
            stroke_opacity=1,  
            fill_opacity=1, 
            )

    shape.commit()
    pm = outpage.get_pixmap()
    file_name = os.path.basename(pdf_file)
    pm.save(output_path + r'pdfs/' + file_name + r'.png')

def pdf2text(pdf_file_path: str):
    text_formula_doc = []
    reader = PdfReader(pdf_file_path)
    for page in reader.pages:
        text_formula_doc.append(page.extract_text())
    return "".join(text_formula_doc)

def file2text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
