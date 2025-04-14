# Instrucciones de Despliegue

Este documento proporciona instrucciones detalladas para desplegar la aplicación Generador PDF en Replit.

## Opción 1: Usando la herramienta de despliegue

Si deseas desplegar directamente esta aplicación o cualquier otra aplicación Flask desde GitHub:

1. Accede a la herramienta de despliegue: https://replit.com/@YourUsername/despliegue-flask (o el enlace a tu Replit actual)
2. Ingresa la URL del repositorio GitHub: https://github.com/Roinflames/generador-pdf-replit
3. Haz clic en "Desplegar" y espera a que el proceso finalice

## Opción 2: Despliegue manual en un nuevo Replit

Si prefieres crear un nuevo Replit y configurarlo manualmente:

1. Crea un nuevo Replit con plantilla Python
2. Abre la terminal y ejecuta:
   ```bash
   git clone https://github.com/Roinflames/generador-pdf-replit.git .
   pip install -r requirements.txt
   ```
3. Configura las variables de entorno necesarias (ver .env.example)
4. Crea un workflow para iniciar la aplicación:
   - Nombre: "Start application"
   - Comando: `gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app`

## Modificaciones realizadas para Replit

Esta versión ha sido adaptada específicamente para funcionar en Replit:

1. Manejo de errores cuando wkhtmltopdf no está disponible:
   - Se proporciona una vista HTML alternativa cuando la generación de PDF falla
   - Las rutas que generan PDFs tienen una ruta alternativa para mostrar HTML

2. Base de datos:
   - Configurada para usar SQLite con inicialización automática

3. Configuración del servidor:
   - Utiliza gunicorn para mejor rendimiento
   - Configurado para escuchar en 0.0.0.0 para accesibilidad externa

## Actualización de cambios

Para subir nuevos cambios al repositorio de GitHub:

1. Realiza tus modificaciones en Replit
2. Haz commit de los cambios:
   ```bash
   git add .
   git commit -m "Descripción de los cambios"
   ```
3. Sube los cambios (necesitarás tu token de GitHub):
   ```bash
   git push origin main
   ```

## Solución de problemas comunes

- **Error 500 al generar PDF**: La aplicación ahora mostrará una versión HTML alternativa ya que wkhtmltopdf no está disponible en Replit.
- **Archivos estáticos no encontrados**: Verifica que las rutas en los templates usen url_for correctamente.
- **Problemas de base de datos**: Prueba eliminar el archivo `instance/app.db` y reiniciar la aplicación para reconstruir la base de datos.