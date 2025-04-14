import jinja2
import pdfkit

machine = 'PC'  # Cambia a 'notebook' si estás en el notebook

if machine == 'notebook':
    path = 'C:/Users/rodre/source/repos/generador-pdf/01_reconocimiento/'
else:
    path = 'C:/Users/Rodrigo/Documents/Code/generador-pdf/01_reconocimiento/'

def crea_pdf(ruta_template, info, rutacss=''):
    nombre_template = ruta_template.split('/')[-1]
    ruta_template = ruta_template.replace(nombre_template, '')

    print("nombre_template: ", nombre_template)
    print("ruta_template: ", ruta_template)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(ruta_template))
    template = env.get_template(nombre_template)
    html = template.render(info)

    print(html)

    options = {
        'page-size': 'Letter',
        'margin-top': '0.05in',
        'margin-right': '0.05in',
        'margin-bottom': '0.05in',
        'margin-left': '0.05in',
        'encoding': 'UTF-8'
    }

    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

    # ruta_salida = 'C:/Users/rodre/source/repos/generador-pdf/reconocimiento_python.pdf' #Notebook
    ruta_salida = path + 'reconocimiento_python.pdf' #PC

    pdfkit.from_string(html, ruta_salida, css=rutacss, options=options, configuration=config)

if __name__ == "__main__":
    # ruta_template = 'C:/Users/rodre/source/repos/generador-pdf/template.html'#notebook
    ruta_template = path + 'template.html'#PC
    info = {"nombreAlumno": "Fernando Cortés", "nombreCurso": "Introducción a Python y HTML5", "fecha": "2023-10-01"}
    crea_pdf(ruta_template, info)
