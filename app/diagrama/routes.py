from flask import render_template, make_response, redirect, url_for, flash
from . import diagrama_bp
import os
from pathlib import Path

# Directorio donde guardar el archivo temporal
pdf_dir = os.path.join(os.path.dirname(__file__), 'static', 'pdfs')
image_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
image_path = os.path.join(image_dir, 'flowchart.png')
firma_path = os.path.join(image_dir, 'firma.jpg')
firma_uri = Path(firma_path).as_uri()
image_uri = Path(image_path).as_uri()
print(firma_uri)

os.makedirs(pdf_dir, exist_ok=True)
os.makedirs(image_dir, exist_ok=True)

# Ruta para visualizar el diagrama (vista previa)
@diagrama_bp.route('/diagrama')
def diagrama_view():
    # Generar el archivo de imagen del diagrama
    image_filename = 'diagrama_placeholder.png'
    firma_filename = 'firma.jpg'
    
    # URL para las imágenes
    image_url = url_for('diagrama.static', filename=f'images/{image_filename}')
    firma_url = url_for('diagrama.static', filename=f'images/{firma_filename}')
    
    # Verificar si existe la imagen de diagrama placeholder
    if not os.path.exists(os.path.join(image_dir, image_filename)):
        # Si no existe, generamos una representación HTML del diagrama en lugar de usar Graphviz
        return render_template('diagrama_html.html', firma_url=firma_url)
    
    try:
        # Intentar crear el diagrama con graphviz si está disponible
        import graphviz
        
        # Crear el diagrama de flujo con graphviz
        dot = graphviz.Digraph(comment='Business Flowchart')

        # Crear grafo horizontal
        dot.attr(rankdir='LR')  # Horizontal
        # Estilo general
        dot.attr('node', shape='plaintext')

        # Nodos con etiquetas HTML
        dot.node('A', '''<
            <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" BGCOLOR="lightgreen">
                <TR><TD><B>Paso 1</B></TD></TR>
                <TR><TD>Inicio del proceso</TD></TR>
            </TABLE>>''')

        dot.node('B', '''<
            <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" BGCOLOR="lightblue">
                <TR><TD><B>Paso 2</B></TD></TR>
                <TR><TD>Validación inicial</TD></TR>
            </TABLE>>''')

        dot.node('C', '''<
            <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" BGCOLOR="lightyellow">
                <TR><TD><B>Paso 3</B></TD></TR>
                <TR><TD>Procesamiento de datos</TD></TR>
            </TABLE>>''')

        dot.node('D', '''<
            <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" BGCOLOR="orange">
                <TR><TD><B>Paso 4</B></TD></TR>
                <TR><TD>Verificación</TD></TR>
            </TABLE>>''')

        dot.node('E', '''<
            <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" BGCOLOR="lightcoral">
                <TR><TD><B>Paso 5</B></TD></TR>
                <TR><TD>Finalización</TD></TR>
            </TABLE>>''')

        # Conectar nodos secuencialmente
        dot.edge('A', 'B')
        dot.edge('B', 'C')
        dot.edge('C', 'D')
        dot.edge('D', 'E')

        # Renderizar el diagrama
        dot.render(filename=os.path.join(image_dir, 'flowchart'), format='png', cleanup=True)
        
        return render_template('diagrama_preview.html', image_url=image_url, firma_url=firma_url)
    
    except (ImportError, Exception) as e:
        # Si GraphViz no está instalado o hay un error al generarlo, mostrar diagrama HTML alternativo
        print(f"Error al generar diagrama: {str(e)}")
        return render_template('diagrama_html.html', firma_url=firma_url)

@diagrama_bp.route('/generar_pdf_diagrama')
def generar_pdf_diagrama():
    # Contenido HTML con las imágenes y la firma
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Business Flowchart</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            .header {{ margin-bottom: 20px; }}
            .diagram {{ margin: 30px 0; }}
            .footer {{ margin-top: 40px; font-size: 0.8em; color: #666; }}
            .step {{ 
                display: inline-block; 
                margin: 10px;
                padding: 15px;
                border: 1px solid #ccc;
                text-align: center;
                width: 120px;
            }}
            .step1 {{ background-color: #d4edda; }}
            .step2 {{ background-color: #d1ecf1; }}
            .step3 {{ background-color: #fff3cd; }}
            .step4 {{ background-color: #ffeeba; }}
            .step5 {{ background-color: #f8d7da; }}
            .arrow {{ display: inline-block; margin: 0 5px; font-size: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="{firma_uri}" alt="Firma Alfaro Madariaga" width="200">
                <h1>Business Process</h1>
            </div>
            
            <div class="diagram">
                <img src="{image_uri}" alt="Business Flowchart" width="600"><br>
            </div>
            
            <p>This document shows the business process flow...</p>
            
            <div class="footer">
                <p>Documento generado el {os.environ.get('DATE', '2025-04-14')}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Ruta donde se guardará el archivo PDF generado
    pdf_path = os.path.join(pdf_dir, 'diagrama_flujo.pdf')
    
    try:
        # Intentar importar e usar pdfkit si está disponible
        import pdfkit
        
        options = {
            'page-size': 'Letter',
            'encoding': 'UTF-8',
            'enable-local-file-access': None
        }

        # Genera el archivo PDF y lo guarda en pdf_path
        pdfkit.from_string(html_content, pdf_path, options=options)
        
        # Abre el archivo PDF y lee su contenido en binario
        with open(pdf_path, 'rb') as f:
            pdf = f.read()
        
        # Crea la respuesta con el archivo PDF
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=diagrama_flujo.pdf'
        
        return response
    except Exception as e:
        # Si hay un error con pdfkit, mostrar la versión HTML del documento
        print(f"Error al generar PDF: {str(e)}")
        return make_response(html_content)