## Plataforma Educativa con Flask

Este proyecto es una plataforma educativa desarrollada con Flask. A continuación se describen los requisitos, pasos de instalación y comandos para inicializar la base de datos, crear el usuario administrador y ejecutar la aplicación.

### Requisitos previos
- Python 3.11 (se recomienda igual o superior a 3.10).
- pip (gestor de paquetes de Python).
- Git (opcional si clonas el repositorio).

### 1. Clonar o copiar el proyecto
Si aún no tienes el código localmente:
```bash
git clone <url-del-repositorio>
cd educative-platform
```
Si ya cuentas con la carpeta `educative-platform`, simplemente navega hacia ella:
```bash
cd c:\Users\Joel\Downloads\proyecto\educative-platform
```

### 2. Crear y activar un entorno virtual (recomendado)
En Windows PowerShell:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
En CMD:
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### 3. Instalar dependencias
Con el entorno virtual activo:
```bash
pip install -r requirements.txt
```

### 4. Inicializar la base de datos con datos de ejemplo
Ejecutar desde la carpeta `educative-platform`:
```bash
python app/init_database.py
```
Este script elimina tablas previas, crea la nueva estructura e inserta usuarios, actividades, preguntas y resultados de prueba.

### 5. Crear o verificar el usuario administrador
Tras inicializar la base de datos:
```bash
python app/create_admin.py
```
Si el usuario admin no existe, se creará con:
- Usuario: `admin`
- Contraseña: `admin123`

### 6. Ejecutar la aplicación
Desde la carpeta `educative-platform`:
```bash
python run.py
```
o directamente con Flask si configuras la variable de entorno:
```bash
set FLASK_APP=run.py
flask run
```
La aplicación se expondrá por defecto en `http://127.0.0.1:5000`.

### 7. Acceso inicial
Usuarios creados por `app/init_database.py`:
- Administrador: `admin / admin123`
- Docentes: `profesor1 / profesor123`, `maria_lopez / maria123`
- Estudiantes: `juan_perez / juan123`, `ana_garcia / ana123`, `carlos_rodriguez / carlos123`, `lucia_martinez / lucia123`, `pedro_sanchez / pedro123`

### 8. Estructura principal de carpetas
```
educative-platform/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes.py
│   ├── logic.py
│   ├── init_database.py
│   ├── create_admin.py
│   ├── static/
│   └── templates/
├── instance/database.db
├── config.py
├── requirements.txt
└── run.py
```

### Notas finales
- Antes de ejecutar `run.py` en un servidor real, actualiza la `SECRET_KEY` en `config.py`.
- `app/init_database.py` elimina los datos existentes, úsalo solo en entornos de desarrollo o cuando seas consciente de la pérdida de información.
- Si instalas nuevas dependencias, recuerda actualizar `requirements.txt` para mantener la reproducibilidad.
