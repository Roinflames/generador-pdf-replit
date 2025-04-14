proyecto/
│
├── app/
│   ├── __init__.py
│   ├── auth/                     # Autenticación
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   ├── main/                     # Módulo principal, home, dashboard
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   │       └── home.html
│   ├── reconocimiento/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   │       └── template.html
│   ├── generar_informe/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── datos_contactos.json
│   │   └── templates/
│   │       └── informe.html
│   ├── diagrama/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── static/
│   │   │   ├── firma.jpg
│   │   │   ├── flowchart
│   │   │   └── flowchart.png
│   │   └── graphzis.md
│   ├── escritura_compraventa/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   │       └── plantilla_compraventa.html
│   ├── liquidacion/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── README.md
│   ├── delega_poder/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   │       └── template.html
│   └── static/
│       └── alfaro_madariaga.jpg
│
├── run.py                  # Punto de entrada de la app
├── .gitignore
├── Pipfile
├── Pipfile.lock
└── README.md