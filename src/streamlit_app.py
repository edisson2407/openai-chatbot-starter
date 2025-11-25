import os
import urllib.parse
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# 1. CONFIGURACIÓN DE PÁGINA
load_dotenv()
st.set_page_config(page_title="AlzerTech", page_icon="💻", layout="wide")

# === Ajuste para Secrets (OpenAI) ===
API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL") or st.secrets.get("OPENAI_MODEL", "gpt-4o-mini")

# === Ajuste para imágenes desde GitHub ===
# Opción simple: una sola base
IMG_BASE_URL = os.getenv("IMG_BASE_URL") or st.secrets.get("IMG_BASE_URL")

# Opción por partes (se usa si no definiste IMG_BASE_URL)
GITHUB_USER = os.getenv("GITHUB_USER") or st.secrets.get("GITHUB_USER")
GITHUB_REPO = os.getenv("GITHUB_REPO") or st.secrets.get("GITHUB_REPO")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH") or st.secrets.get("GITHUB_BRANCH", "main")
IMG_PATH = os.getenv("IMG_PATH") or st.secrets.get("IMG_PATH", "assets/img")

def img_url(filename: str) -> str:
    """
    Resuelve la URL final de la imagen:
    1) Si hay IMG_BASE_URL, utiliza ese prefijo.
    2) Si no, intenta construir la URL cruda de GitHub con USER/REPO/BRANCH/IMG_PATH.
    3) Si nada está configurado, usa un placeholder.
    """
    if IMG_BASE_URL:
        return f"{IMG_BASE_URL.rstrip('/')}/{filename}"
    if GITHUB_USER and GITHUB_REPO:
        return f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{IMG_PATH}/{filename}"
    # Placeholder de emergencia (si no configuraste nada)
    return f"https://placehold.co/300x200/png?text={urllib.parse.quote(filename)}"

# 2. DATOS DE PRODUCTOS (QUEMADOS EN CÓDIGO)
# Ahora "img" es solo el nombre de archivo; se resuelve con img_url(...)
productos = [
    {"id": 1, "nombre": "Laptop Lenovo IdeaPad Slim 3", "precio": 329.99, "specs": "Ryzen 3 7320U, 8GB RAM, 256GB SSD", "img": "lenovo-slim.jpg"},
    {"id": 2, "nombre": "HP Envy x360 2-in-1", "precio": 850.00, "specs": "Core i7 1355U, 16GB RAM, Pantalla Táctil", "img": "hp-envy.jpg"},
    {"id": 3, "nombre": "MacBook Air M1", "precio": 799.00, "specs": "Chip M1, 8GB RAM, 256GB SSD, Silver", "img": "macbook-air-m1.jpg"},
    {"id": 4, "nombre": "Asus Vivobook Go", "precio": 409.99, "specs": "Ryzen 5 7520U, 16GB RAM, 512GB SSD", "img": "asus-vivobook-go.jpg"},
    {"id": 5, "nombre": "Monitor Gamer Samsung Odyssey", "precio": 250.00, "specs": "27 pulgadas, 144Hz, Curvo", "img": "samsung-odyssey.jpg"},
    {"id": 6, "nombre": "Mouse Logitech MX Master 3S", "precio": 99.00, "specs": "Ergonómico, Bluetooth, 8000 DPI", "img": "logitech-mx-master-3s.jpg"},
]

# Convertimos los productos a texto para que la IA los entienda
inventario_texto = "\n".join([f"- {p['nombre']}: ${p['precio']} ({p['specs']})" for p in productos])

# 3. CONFIGURACIÓN CSS (ESTILOS Y BURBUJA FLOTANTE)
st.markdown("""
<style>
    /* Navbar Estilo NomadaWare */
    .navbar {
        background-color: #111;
        padding: 20px;
        color: white;
        margin-bottom: 30px;
        border-bottom: 3px solid #e91e63;
        display: flex; 
        justify-content: space-between; 
        align-items: center;
    }
    
    /* Tarjetas de producto */
    .card {
        background-color: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .price { color: #e91e63; font-size: 1.2em; font-weight: bold; }
    .name { font-weight: bold; margin: 10px 0; color: #333; }
    .specs { font-size: 0.8em; color: #666; margin-bottom: 10px;}

    /* BURBUJA FLOTANTE (CSS HACK) 
       Esto mueve el botón del st.popover a la esquina inferior derecha */
    [data-testid="stPopover"] {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 9999;
    }
    
    /* Estilo del botón de la burbuja */
    [data-testid="stPopover"] > div > button {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background-color: #e91e63;
        color: white;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        font-size: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    [data-testid="stPopover"] > div > button:hover {
        background-color: #c2185b;
        transform: scale(1.1);
        transition: all 0.2s;
    }
    
    /* Ajuste para que el contenido no quede oculto tras la burbuja */
    .block-container { padding-bottom: 100px; }

</style>
""", unsafe_allow_html=True)

# 4. INTERFAZ VISUAL (LA TIENDA)

# Header HTML
st.markdown(f"""
<div class="navbar">
    <div style="font-size:24px; font-weight:bold;">AlzerTech <span style="font-size:14px; font-weight:normal;">Store</span></div>
    <div>🛒 Carrito (0) &nbsp; | &nbsp; 👤 Cuenta</div>
</div>
""", unsafe_allow_html=True)

# Buscador y Filtros (Visual)
col_search, col_void = st.columns([3,1])
with col_search:
    search = st.text_input("🔍 ¿Qué estás buscando?", placeholder="Ej: Laptop Gamer, Mouse...")

st.subheader("🔥 Ofertas Destacadas")

# GRID DE PRODUCTOS
# Filtramos productos según búsqueda
productos_visibles = [p for p in productos if search.lower() in p['nombre'].lower()]

# Lógica para mostrar en columnas de 3
for i in range(0, len(productos_visibles), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(productos_visibles):
            prod = productos_visibles[i + j]
            with cols[j]:
                # Construir la URL de la imagen a partir del nombre de archivo
                img_src = img_url(prod['img'])
                st.markdown(f"""
                <div class="card">
                    <img src="{img_src}" style="width:100%; border-radius:5px;">
                    <div class="name">{prod['nombre']}</div>
                    <div class="specs">{prod['specs']}</div>
                    <div class="price">${prod['precio']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Agregar al Carrito", key=f"btn_{prod['id']}"):
                    st.toast(f"{prod['nombre']} agregado! 🛒")

# 5. CHATBOT INTEGRADO (EN BURBUJA)
# Usamos st.popover para crear el efecto de ventana emergente

# Iniciamos el historial con el contexto de los productos
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": f"""
        Eres el asistente virtual de AlzerTech. 
        Tu objetivo es ayudar al cliente a comprar productos de tecnología.
        Unicamente responde sobre el contexto de la pagina, no de otros temas.
        Sé amable, breve y persuasivo.
        
        ESTE ES EL INVENTARIO ACTUAL QUE TIENES DISPONIBLE:
        {inventario_texto}
        
        Si te preguntan por algo que no está en la lista, di que no lo tienes pero ofrece una alternativa similar de la lista.
        Responde siempre en español.
        """}
    ]

# Cliente OpenAI con API key desde env o secrets
client = OpenAI(api_key=API_KEY)

# Este es el componente mágico: Una "Caja" que se abre al hacer clic
# El CSS de arriba lo posiciona en la esquina inferior derecha
with st.popover("💬"):
    st.markdown("### 🤖 Asistente AlzerTech")
    st.caption("Pregúntame por precios o recomendaciones.")
    
    # Contenedor del chat (scrollable)
    chat_container = st.container(height=300)
    
    with chat_container:
        for msg in st.session_state.history:
            if msg["role"] != "system":
                st.chat_message(msg["role"]).write(msg["content"])
    
    # Input del chat (dentro de la burbuja)
    prompt = st.chat_input("Escribe aquí...", key="chat_input_bubble")
    
    if prompt:
        # 1. Mostrar mensaje usuario
        st.session_state.history.append({"role": "user", "content": prompt})
        with chat_container:
            st.chat_message("user").write(prompt)
        
        # 2. Llamar a OpenAI
        try:
            with st.spinner("..."):
                resp = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.history,
                    temperature=0.7,
                )
                reply = resp.choices[0].message.content
                
                # 3. Mostrar respuesta
                st.session_state.history.append({"role": "assistant", "content": reply})
                with chat_container:
                    st.chat_message("assistant").write(reply)
                    
        except Exception as e:
            st.error(f"Error: {e}")
