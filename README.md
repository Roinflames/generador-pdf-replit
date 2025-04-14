# Generador PDF - Versión Replit

Una aplicación Flask para generar documentos jurídicos en formato PDF y HTML.

## Características

- Autenticación de usuarios
- Generación de diferentes tipos de documentos:
  - Reconocimiento de deuda
  - Escritura de compraventa
  - Delegación de poder
  - Diagrama
  - Liquidación de persona natural
  - Generación de informes
- Versión adaptada para funcionar en Replit
- Vista HTML alternativa cuando wkhtmltopdf no está disponible

## Notas técnicas

- Basado en Flask y SQLAlchemy
- Utiliza wkhtmltopdf para generación de PDFs (cuando está disponible)
- Desplegada en Replit con configuración automática

## Uso

1. Crear una cuenta o iniciar sesión
2. Navegar a la sección del documento que desee generar
3. Completar el formulario con los datos requeridos
4. Generar el documento en formato PDF o HTML