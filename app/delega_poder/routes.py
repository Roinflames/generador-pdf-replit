# en routes.py o el archivo de rutas correspondiente
from flask import render_template, make_response, redirect, url_for
from . import delega_bp
import os
import pdfkit

# Directorio donde guardar el archivo temporal
pdf_dir = os.path.join(os.path.dirname(__file__), 'static', 'pdfs')
os.makedirs(pdf_dir, exist_ok=True)

# Ruta para mostrar la vista previa
@delega_bp.route('/delega_poder')
def delega_poder_view():
    # Datos a pasar a la plantilla
    data = {
        "tribunal": "S.J.L. En lo Civil de Santiago (25º)",
        "abogado_patrocinante": "EDUARDO MAURICIO LARA QUIROZ",
        "caratula": "“TORRES/BANCO DE CHILE”",
        "rol": "Rol C-7440-2024",
        "demandado": "BASTIÁN ADONIS RAMÍREZ ROCHA",
        "rut_demandado": "19.499.895-3",
    }

    # Renderiza la plantilla 'delega_poder.html' con los datos
    return render_template('delega_poder_preview.html', **data)

# Ruta para generar el PDF
@delega_bp.route('/generar_pdf')
def generar_pdf():
    # Datos a pasar a la plantilla
    data = {
        "tribunal": "S.J.L. En lo Civil de Santiago (25º)",
        "abogado_patrocinante": "EDUARDO MAURICIO LARA QUIROZ",
        "caratula": "“TORRES/BANCO DE CHILE”",
        "rol": "Rol C-7440-2024",
        "demandado": "BASTIÁN ADONIS RAMÍREZ ROCHA",
        "rut_demandado": "19.499.895-3",
    }

    # Renderiza la plantilla 'delega_poder.html' con los datos
    html_contenido = render_template('delega_poder.html', **data)

    # Opciones para pdfkit (como tamaño de página, etc.)
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'enable-local-file-access': None  # Esto es para permitir que pdfkit acceda a archivos locales si es necesario
    }

    # Ruta del archivo PDF
    pdf_path = os.path.join(pdf_dir, 'delega_poder.pdf')

    # Elimina el archivo PDF anterior si ya existe
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    # Genera el PDF desde el contenido HTML renderizado
    pdfkit.from_string(html_contenido, pdf_path, options=options)

    # Abre el archivo PDF y lee su contenido en binario
    with open(pdf_path, 'rb') as f:
        pdf = f.read()

    # Crear la respuesta PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=delega_poder.pdf'

    return response