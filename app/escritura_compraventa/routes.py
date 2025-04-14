from flask import render_template, make_response, redirect, url_for
from . import escritura_bp
import sys

# Intentar importar pdfkit, pero manejar el caso si no está disponible
try:
    import pdfkit
    PDFKIT_DISPONIBLE = True
except (ImportError, Exception):
    print("pdfkit o wkhtmltopdf no está disponible. La funcionalidad de PDF será limitada.", file=sys.stderr)
    PDFKIT_DISPONIBLE = False

@escritura_bp.route('/escritura_compraventa')
def escritura_compraventa_view():
    data = {
        "ciudad": "Santiago",
        "dia": "7",
        "mes": "abril",
        "anio": "2025",
        "notario": "Juan Pérez",
        "vendedor_nombre": "Rodrigo Reyes",
        "vendedor_rut": "12.345.678-9",
        "vendedor_domicilio": "Av. Libertador Bernardo O'Higgins 1234",
        "comprador_nombre": "Diego López",
        "comprador_rut": "23.456.789-0",
        "comprador_domicilio": "Calle Ficticia 5678",
        "inmueble_direccion": "Av. Providencia 2500",
        "inmueble_descripcion": "Departamento de 2 dormitorios, 1 baño",
        "precio_venta": "50.000.000",
        "precio_venta_numero": "50000000",
        "metodo_pago": "Transferencia bancaria",
        "declaraciones_adicionales": "El bien se entrega libre de cargas y gravámenes."
    }

    # Renderizar la plantilla para vista previa en HTML
    return render_template('plantilla_compraventa_preview.html', **data)

@escritura_bp.route('/generar_pdf')
def generar_pdf():
    data = {
        "ciudad": "Santiago",
        "dia": "7",
        "mes": "abril",
        "anio": "2025",
        "notario": "Juan Pérez",
        "vendedor_nombre": "Rodrigo Reyes",
        "vendedor_rut": "12.345.678-9",
        "vendedor_domicilio": "Av. Libertador Bernardo O'Higgins 1234",
        "comprador_nombre": "Diego López",
        "comprador_rut": "23.456.789-0",
        "comprador_domicilio": "Calle Ficticia 5678",
        "inmueble_direccion": "Av. Providencia 2500",
        "inmueble_descripcion": "Departamento de 2 dormitorios, 1 baño",
        "precio_venta": "50.000.000",
        "precio_venta_numero": "50000000",
        "metodo_pago": "Transferencia bancaria",
        "declaraciones_adicionales": "El bien se entrega libre de cargas y gravámenes."
    }

    # Renderizar la plantilla para el PDF
    html = render_template('plantilla_compraventa.html', **data)
    
    # Verificar si pdfkit está disponible
    if PDFKIT_DISPONIBLE:
        try:
            # Generar PDF con pdfkit
            pdf = pdfkit.from_string(html, False)
            
            # Generar el PDF como respuesta
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'inline; filename=escritura_compraventa.pdf'
            
            return response
            
        except Exception as e:
            # Si hay error, registrarlo y mostrar la vista HTML
            print(f"Error al generar PDF: {e}", file=sys.stderr)
            return render_template('plantilla_compraventa_preview.html', 
                                  mensaje_error="No se pudo generar el PDF debido a un error. Se muestra la vista HTML en su lugar.",
                                  **data)
    else:
        # Si pdfkit no está disponible, mostrar la vista HTML con un mensaje
        return render_template('plantilla_compraventa_preview.html', 
                              mensaje_error="La generación de PDF no está disponible en este entorno. Se muestra la vista HTML en su lugar.",
                              **data)