from flask import render_template, make_response, redirect, url_for, flash
from . import reconocimiento
import jinja2
import os
import sys

# Intenta importar pdfkit, pero maneja el caso si no está disponible
try:
    import pdfkit
    PDFKIT_DISPONIBLE = True
except (ImportError, Exception):
    print("pdfkit o wkhtmltopdf no está disponible. La funcionalidad de PDF será limitada.", file=sys.stderr)
    PDFKIT_DISPONIBLE = False

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
    
    # Ruta de salida del archivo PDF
    os.makedirs(os.path.join(path, 'static'), exist_ok=True)
    ruta_salida = os.path.join(path, 'static', 'reconocimiento_python.pdf')
    
    # Verificar si pdfkit está disponible
    if not PDFKIT_DISPONIBLE:
        # Si no está disponible, retornamos None para indicar que no se pudo generar el PDF
        print("No se pudo generar el PDF: wkhtmltopdf no está disponible", file=sys.stderr)
        return None
        
    try:
        options = {
            'page-size': 'Letter',
            'margin-top': '0.05in',
            'margin-right': '0.05in',
            'margin-bottom': '0.05in',
            'margin-left': '0.05in',
            'encoding': 'UTF-8'
        }
        
        # Intentamos la configuración de manera flexible
        try:
            # Primero intentamos sin configuración específica
            pdfkit.from_string(html, ruta_salida, css=rutacss, options=options)
        except Exception as e:
            print(f"Error con configuración predeterminada: {e}", file=sys.stderr)
            # Si falla, intentamos con una configuración específica para Linux
            try:
                # Buscar wkhtmltopdf en Linux
                pdfkit.from_string(html, ruta_salida, css=rutacss, options=options)
            except Exception as e:
                print(f"Error al generar PDF con pdfkit: {e}", file=sys.stderr)
                return None
                
        return ruta_salida  # Regresa la ruta del archivo PDF generado
        
    except Exception as e:
        print(f"Error general al crear PDF: {e}", file=sys.stderr)
        return None

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
    
    # Verifica si se pudo generar el PDF
    if pdf_path is None:
        # Si no se pudo generar el PDF, muestra una vista previa HTML en su lugar
        template_dir = os.path.dirname(ruta_template)
        template_name = os.path.basename(ruta_template)
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
        template = env.get_template(template_name)
        html = template.render(info)
        
        # Mostrar mensaje de error y la vista HTML como alternativa
        return render_template('reconocimiento_preview.html', 
                              contenido=html, 
                              mensaje_error="No se pudo generar el PDF debido a que wkhtmltopdf no está disponible en este entorno. Se muestra la vista HTML en su lugar.")
    
    try:
        # Lee el PDF generado
        with open(pdf_path, 'rb') as f:
            pdf = f.read()

        # Devuelve el archivo PDF como respuesta en la aplicación Flask
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=reconocimiento_python.pdf'

        return response
        
    except Exception as e:
        # Si hay error al leer el archivo, mostrar vista previa HTML
        template_dir = os.path.dirname(ruta_template)
        template_name = os.path.basename(ruta_template)
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
        template = env.get_template(template_name)
        html = template.render(info)
        
        print(f"Error al leer el archivo PDF: {e}", file=sys.stderr)
        return render_template('reconocimiento_preview.html', 
                              contenido=html, 
                              mensaje_error=f"Error al generar el PDF: {str(e)}. Se muestra la vista HTML en su lugar.")