from flask import render_template, make_response, redirect, url_for
from . import escritura_bp
import pdfkit

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
    pdf = pdfkit.from_string(html, False)

    # Generar el PDF
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=escritura_compraventa.pdf'

    return response