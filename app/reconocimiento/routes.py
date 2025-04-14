from flask import render_template, make_response, redirect, url_for
from . import reconocimiento
import jinja2
import pdfkit
import os

# Ruta base del módulo reconocimiento
path = os.path.dirname(__file__)

# Ruta del template
ruta_template = os.path.join(path, 'templates', 'template.html')

# Función para crear el PDF
def crea_pdf(ruta_template, info, rutacss=''):
    # Usamos os.path.join para manejar las rutas correctamente
    template_dir = os.path.dirname(ruta_template)
    template_name = os.path.basename(ruta_template)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    
    html = template.render(info)

    options = {
        'page-size': 'Letter',
        'margin-top': '0.05in',
        'margin-right': '0.05in',
        'margin-bottom': '0.05in',
        'margin-left': '0.05in',
        'encoding': 'UTF-8'
    }

    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

    # Ruta de salida del archivo PDF
    os.makedirs(os.path.join(path, 'static'), exist_ok=True)
    ruta_salida = os.path.join(path, 'static', 'reconocimiento_python.pdf')

    # Genera el PDF desde el HTML renderizado
    pdfkit.from_string(html, ruta_salida, css=rutacss, options=options, configuration=config)

    return ruta_salida  # Regresa la ruta del archivo PDF generado

# Vista de Flask para mostrar el formulario o template de reconocimiento
@reconocimiento.route('/reconocimiento')
def reconocimiento_view():
    return render_template('template.html')

# Ruta para vista previa del reconocimiento (no genera PDF, solo muestra la plantilla)
@reconocimiento.route('/reconocimiento_preview')
def reconocimiento_preview():
    # Define la información a pasar a la plantilla
    info = {
        "nombreAlumno": "Fernando Cortés",
        "nombreCurso": "Introducción a Python y HTML5",
        "fecha": "2023-10-01"
    }

    # Usamos os.path.join para manejar las rutas correctamente
    ruta_template = os.path.join(path, 'templates', 'template.html')

    # Renderiza la plantilla de reconocimiento para vista previa
    template_dir = os.path.dirname(ruta_template)
    template_name = os.path.basename(ruta_template)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    html = template.render(info)

    # Devuelve el HTML renderizado como una vista previa en la página
    return render_template('reconocimiento_preview.html', contenido=html)

# Ruta para generar el PDF y devolverlo en la respuesta
@reconocimiento.route('/generar_pdf')
def generar_pdf():
    # Define la información a pasar a la plantilla
    info = {
        "nombreAlumno": "Fernando Cortés",
        "nombreCurso": "Introducción a Python y HTML5",
        "fecha": "2023-10-01"
    }

    # Usamos os.path.join para manejar las rutas correctamente
    ruta_template = os.path.join(path, 'templates', 'template.html')

    # Llama a la función para crear el PDF
    pdf_path = crea_pdf(ruta_template, info)

    # Lee el PDF generado
    with open(pdf_path, 'rb') as f:
        pdf = f.read()

    # Devuelve el archivo PDF como respuesta en la aplicación Flask
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reconocimiento_python.pdf'

    return response