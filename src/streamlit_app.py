import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

# === NUEVO: para traer imágenes y embebidas en base64 ===
import requests
from io import BytesIO
import base64

# 1. CONFIGURACIÓN DE PÁGINA
load_dotenv()
st.set_page_config(page_title="NomadaWare AI", page_icon="💻", layout="wide")

# === Ajuste pequeño para Secrets (Streamlit Cloud) ===
API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL") or st.secrets.get("OPENAI_MODEL", "gpt-4o-mini")

# 2. DATOS DE PRODUCTOS (QUEMADOS EN CÓDIGO)
productos = [
    {"id": 1, "nombre": "Laptop Lenovo IdeaPad Slim 3", "precio": 329.99, "specs": "Ryzen 3 7320U, 8GB RAM, 256GB SSD", "img": "https://placehold.co/300x200/png?text=Lenovo+Slim"},
    {"id": 2, "nombre": "HP Envy x360 2-in-1", "precio": 850.00, "specs": "Core i7 1355U, 16GB RAM, Pantalla Táctil", "img": "https://placehold.co/300x200/png?text=HP+Envy"},
    {"id": 3, "nombre": "MacBook Air M1", "precio": 799.00, "specs": "Chip M1, 8GB RAM, 256GB SSD, Silver", "img": "https://placehold.co/300x200/png?text=MacBook+Air"},
    {"id": 4, "nombre": "Asus Vivobook Go", "precio": 409.99, "specs": "Ryzen 5 7520U, 16GB RAM, 512GB SSD", "img": "https://placehold.co/300x200/png?text=Asus+Vivo"},
    {"id": 5, "nombre": "Monitor Gamer Samsung Odyssey", "precio": 250.00, "specs": "27 pulgadas, 144Hz, Curvo", "img": "https://placehold.co/300x200/png?text=Samsung+Odyssey"},
    {"id": 6, "nombre": "Mouse Logitech MX Master 3S", "precio": 99.00, "specs": "Ergonómico, Bluetooth, 8000 DPI", "img": "https://placehold.co/300x200/png?text=MX+Master+3S"},
]

inventario_texto = "\n".join([f"- {p['nombre']}: ${p['precio']} ({p['specs']})" for p in productos])

# === NUEVO: helper para traer imagen y retornarla como data-uri base64 ===
@st.cache_data(show_spinner=False)
def image_data_uri(url: str) -> str:
    def _fallback(seed: int):
        r = requests.get(f"https://picsum.photos/seed/{seed}/600/400", timeout=10)
        r.raise_for_status()
        return r.content, "image/jpeg"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        content = r.content
        # Deducir mime simple por extensión conocida
        mime = "image/png" if ".png" in url.lower() else "image/jpeg"
    except Exception:
        # Fallback si falla la URL original
        seed = abs(hash(url)) % 9999
        content, mime = _fallback(seed)

    b64 = base64.b64encode(content).decode("utf-8")
    return f"data:{mime};base64,{b64}"

# 3. CONFIGURACIÓN CSS (ESTILOS Y BURBUJA FLOTANTE)
st.markdown("""
<style>
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
    .card img {
        width: 100%;
        border-radius: 5px;
        margin-bottom: 10px;
        display: block;
    }
    .price { color: #e91e63; font-size: 1.2em; font-weight: bold; }
    .name { font-weight: bold; margin: 10px 0; color: #333; }
    .specs { font-size: 0.8em; color: #666; margin-bottom: 10px;}
    [data-testid="stPopover"] {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 9999;
    }
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
    .block-container { padding-bottom: 100px; }
</style>
""", unsafe_allow_html=True)

# 4. INTERFAZ VISUAL (LA TIENDA)
st.markdown(f"""
<div class="navbar">
    <div style="font-size:24px; font-weight:bold;">NomadaWare <span style="font-size:14px; font-weight:normal;">AI Store</span></div>
    <div>🛒 Carrito (0) &nbsp; | &nbsp; 👤 Cuenta</div>
</div>
""", unsafe_allow_html=True)

col_search, col_void = st.columns([3,1])
with col_search:
    search = st.text_input("🔍 ¿Qué estás buscando?", placeholder="Ej: Laptop Gamer, Mouse...")

st.subheader("🔥 Ofertas Destacadas")

productos_visibles = [p for p in productos if search.lower() in p['nombre'].lower()]

# === AJUSTE: embebemos la imagen con data-uri dentro del HTML de la card ===
for i in range(0, len(productos_visibles), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(productos_visibles):
            prod = productos_visibles[i + j]
            # Construir data URI (cacheado)
            img_uri = image_data_uri(prod["img"])
            with cols[j]:
                st.markdown(f"""
                <div class="card">
                    <img src="{img_uri}" alt="{prod['nombre']}">
                    <div class="name">{prod['nombre']}</div>
                    <div class="specs">{prod['specs']}</div>
                    <div class="price">${prod['precio']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Agregar al Carrito", key=f"btn_{prod['id']}"):
                    st.toast(f"{prod['nombre']} agregado! 🛒")

# 5. CHATBOT INTEGRADO (EN BURBUJA)
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": f"""
        Eres el asistente virtual de NomadaWare. 
        Tu objetivo es ayudar al cliente a comprar productos de tecnología.
        Sé amable, breve y persuasivo.
        
        ESTE ES EL INVENTARIO ACTUAL QUE TIENES DISPONIBLE:
        {inventario_texto}
        
        Si te preguntan por algo que no está en la lista, di que no lo tienes pero ofrece una alternativa similar de la lista.
        Responde siempre en español.
        """}
    ]

# Cliente OpenAI con API key desde env o secrets
client = OpenAI(api_key=API_KEY)

with st.popover("💬"):
    st.markdown("### 🤖 Asistente NomadaWare")
    st.caption("Pregúntame por precios o recomendaciones.")
    
    chat_container = st.container(height=300)
    with chat_container:
        for msg in st.session_state.history:
            if msg["role"] != "system":
                st.chat_message(msg["role"]).write(msg["content"])
    
    prompt = st.chat_input("Escribe aquí...", key="chat_input_bubble")
    if prompt:
        st.session_state.history.append({"role": "user", "content": prompt})
        with chat_container:
            st.chat_message("user").write(prompt)
        try:
            with st.spinner("..."):
                resp = client.chat.completions.create(
                    model=MODEL,
                    messages=st.session_state.history,
                    temperature=0.7,
                )
                reply = resp.choices[0].message.content
                st.session_state.history.append({"role": "assistant", "content": reply})
                with chat_container:
                    st.chat_message("assistant").write(reply)
        except Exception as e:
            st.error(f"Error: {e}")
