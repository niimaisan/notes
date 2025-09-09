# Notes
Proyecto de aplicación de notas desarrollado en Python con PySide.

## Características

- Editor de texto con soporte Markdown y vista previa en tiempo real
- Sidebar para navegación y gestión de páginas
- Creación y eliminación de páginas
- Guardado automático en archivos locales (JSON)

## Requisitos

- Python 3.11
- PySide6
- rich (para salida bonita en terminal si se requiere)
- pytest (para pruebas)

## Instalación

```bash
git clone https://github.com/niimaisan/notes.git
cd notes
pip install -r requirements.txt
python src/main.py
```

## Uso
- Crear nuevas páginas con el botón "Nueva página".
- Eliminar páginas con el botón "Eliminar página".
- Escribe en el editor para ver la lista previa de Markdown al instante.
- Todos los cambios se guardan automáticamente.

## Contribución
1. Hacer un fork del repositorio
2. Crear una rama feature/nombre
3. Abrir un pull request