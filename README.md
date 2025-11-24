# OpenAI Chatbot Starter (Windows 11, Python)

Este starter te guía paso a paso para crear un chatbot en **Python** usando el **OpenAI API**. Incluye:
- Chatbot por **consola** (`src/chatbot.py`)
- **Interfaz básica** con **Streamlit** (`src/streamlit_app.py`)
- **API web** mínima con **Flask** (`src/web_api.py`)
- Manejo de variables de entorno con **python-dotenv**
- Ejemplos de **reintentos** por límites de tasa (rate limits)

## 0) Requisitos
- Windows 11 con **Python 3.10+** instalado.
- Una **API key** de OpenAI.

## 1) Crea la carpeta del proyecto
```powershell
# Elige una ubicación (Documentos, Escritorio, etc.)
cd $env:USERPROFILE\Documents
mkdir openai-chatbot-starter
cd openai-chatbot-starter
```

## 2) Crea y activa el entorno virtual
```powershell
py -m venv .venv
# Activar
.\.venv\Scripts\activate
# (verás (.venv) al inicio de tu terminal)
```

## 3) Descarga este starter y entra a la carpeta
Coloca todos los archivos en esta carpeta (o clona el repo si lo subes a Git).

## 4) Instala dependencias
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 5) Configura tu API Key
1. Copia `.env.example` a `.env` y pega tu clave:
```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
```
2. (Opcional en Windows) Define la variable de entorno de manera permanente en tu usuario:
```cmd
setx OPENAI_API_KEY "sk-..."
```

## 6) Prueba el chatbot por consola
```powershell
python src/chatbot.py
```
Escribe tu mensaje y presiona **Enter**. Para salir, escribe `salir` o `exit`.

## 7) Interfaz básica (Streamlit)
```powershell
streamlit run src/streamlit_app.py
```
Abre el URL local que te muestra (generalmente `http://localhost:8501`).

## 8) API HTTP (Flask)
```powershell
set FLASK_APP=src/web_api.py
flask run
```
Luego prueba con (PowerShell):
```powershell
Invoke-WebRequest -UseBasicParsing `
  -Uri http://127.0.0.1:5000/chat `
  -Method POST `
  -ContentType "application/json" `
  -Body '{ "message": "Hola", "history": [] }'
```

## 9) Notas
- El **modelo** se puede ajustar con la variable `OPENAI_MODEL` (por defecto `gpt-4o-mini`). 
- El código maneja errores comunes y reintenta automáticamente ante respuestas 429 (rate limit).

## 10) Estructura
```
openai-chatbot-starter/
├─ .gitignore
├─ .env.example
├─ requirements.txt
├─ README.md
└─ src/
   ├─ chatbot.py
   ├─ streamlit_app.py
   └─ web_api.py
```

---

### Créditos & Docs
- Python SDK oficial de OpenAI
- Documentación para Chat Completions de OpenAI
- Buenas prácticas para variables de entorno y límites de tasa