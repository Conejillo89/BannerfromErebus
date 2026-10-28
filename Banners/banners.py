import io
import os
import base64
import zipfile
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(page_title="Banner Studio Pro Ultimate", layout="wide")
st.sidebar.image("Banners/assets/dibujo.png", width=250)


def obtener_base64(ruta_archivo):
    """Lee un archivo local y devuelve la cadena en formato Base64."""
    with open(ruta_archivo, "rb") as f:
        datos = f.read()
    return base64.b64encode(datos).decode()


ruta_fondo_local = "Banners/assets/fondo.png"
ruta_fondo_movil = "Banners/assets/fondo_mobile.png"
css_fondo = ""

try:
    base64_fondo = obtener_base64(ruta_fondo_local)
    
    try:
        base64_fondo_movil = obtener_base64(ruta_fondo_movil)
    except FileNotFoundError:
        base64_fondo_movil = base64_fondo

    css_fondo = f"""
    .stApp {{
        background-image: url("data:image/png;base64,{base64_fondo}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #0882fc;
    }}

    /* Adaptación perfecta para celulares */
    @media screen and (max-width: 768px) {{
        .stApp {{
            background-image: url("data:image/png;base64,{base64_fondo_movil}") !important;
            background-size: cover !important;
            background-position: center center !important;
            background-attachment: scroll !important;
        }}
    }}
    """
except FileNotFoundError:
    css_fondo = """
    .stApp {
        background-color: #96b5ff;
        color: #F8FAFC;
    }
    """


nombre_fuente_local = "Visionaries_2.ttf"

if not os.path.exists(nombre_fuente_local):
    nombre_fuente_local = "Banners/assets/visionaries_2.ttf"

css_fuente_h1_custom = ""

if os.path.exists(nombre_fuente_local):
    with open(nombre_fuente_local, "rb") as archivo_fuente:
        bytes_fuente = archivo_fuente.read()

    base64_fuente = base64.b64encode(bytes_fuente).decode()

    css_fuente_h1_custom = f"""
        @font-face {{
            font-family: 'VisionariesCustom';
            src: url("data:font/ttf;charset=utf-8;base64,{base64_fuente}") format('truetype');
        }}

        h1, .stApp h1, [data-testid="stMarkdownContainer"] h1 {{
            font-family: 'VisionariesCustom', sans-serif !important;
            font-size: clamp(32px, 6vw, 60px) !important;
            color: #000000 !important;
            letter-spacing: 2px !important;
        }}
    """
else:
    css_fuente_h1_custom = """
        h1, .stApp h1 {{
            color: #000000 !important; 
        }}
    """

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    header, [data-testid="stHeader"] {{
       <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    /* Ocultar el header superior SOLO en computadoras para mantener limpio el diseño */
    @media screen and (min-width: 769px) {
        header, [data-testid="stHeader"] {
            display: none !important;
        }
    }

    /* En celulares, SÍ mostramos el header para que aparezca el botón del menú lateral */
    @media screen and (max-width: 768px) {
        header, [data-testid="stHeader"] {
            display: block !important;
            background-color: transparent !important;
        }
    }

    .stApp {{
        margin-top: 0px; /* Evitamos márgenes negativos extraños en móvil */
    }}
    
    /* Resto de tus estilos... */
    }}

    .stApp {{
        margin-top: -20px;
    }}

    html, body, [class*="css"], .stMarkdown {{
        font-family: 'Poppins', sans-serif;
    }}

    {css_fondo}
    {css_fuente_h1_custom}

    /* ASEGURAR VISIBILIDAD DE LA BARRA LATERAL EN MÓVIL */
    [data-testid="stSidebar"] {{
        background-color: rgba(168, 198, 247, 0.98) !important;    
    }}

    /* Permitir que la barra lateral colapse de forma limpia en móvil sin desaparecer */
    @media screen and (max-width: 768px) {{
        [data-testid="stSidebar"] {{
            width: 85% !important;
        }}
    }}

    [data-testid="stCaptionContainer"] {{
        color: #000000 !important;
    }}

    h2, h3, .stApp h2, .stApp h3 {{
        color: #38BDF8 !important; 
    }}

    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {{
        color: #000000 !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 28px;
        border: none;
        width: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%);
        color: white;
        transform: translateY(-2px);
    }}

    div[data-baseweb="slider"] div[role="slider"] {{
        background-color: #2563EB !important;
        border-color: #1D4ED8 !important;
        box-shadow: 0 0 8px rgba(37, 99, 235, 0.4) !important;
    }}

    div[data-testid="stSlider"] label,
    div[data-testid="stSlider"] label p,
    div[data-testid="stWidgetLabel"] p {{
        color: #000000 !important;
        font-weight: 600 !important;
    }}
    </style>
""", unsafe_allow_html=True)


st.sidebar.markdown("---")
st.sidebar.header("• Branding y Elementos")

logo_subido = st.sidebar.file_uploader(
    "1. Logotipo para el Banner (PNG Transparente):",
    type=["png"]
)

posicion_logo = st.sidebar.selectbox(
    "Ubicación del Logo en el Banner:",
    ["Superior Derecha", "Superior Izquierda", "Inferior Derecha", "Inferior Izquierda"]
)

fondo_subido = st.sidebar.file_uploader(
    "2. Imagen de Fondo (Horizontal o Vertical):",
    type=["png", "jpg", "jpeg"]
)

st.sidebar.markdown("---")
st.sidebar.header("• Tipografía y Textos para Banners")

FUENTES_SISTEMA = {
    "Arial (Limpia)": "arial.ttf",
    "Times New Roman (Clásica)": "times.ttf",
    "Courier New (Monospace)": "couri.ttf",
    "Verdana (Legible)": "verdana.ttf",
    "Impact (Título Grueso)": "impact.ttf",
    "Georgia (Elegante)": "georgia.ttf"
}

opcion_fuente = st.sidebar.selectbox("Fuente Estándar para Banners:", list(FUENTES_SISTEMA.keys()))
fuente_custom = st.sidebar.file_uploader("O sube fuente personalizada para los banners (.ttf/.otf):", type=["ttf", "otf"])

st.sidebar.markdown("### • Título Principal")
tamano_fuente = st.sidebar.slider("Tamaño Título (px):", min_value=15, max_value=120, value=36)
color_texto_hex = st.sidebar.color_picker("Color del Título:", "#000000")
alineacion_texto = st.sidebar.selectbox("Alineación del Título:", ["Izquierda", "Centro", "Derecha"])

st.sidebar.markdown("### • Línea 1: Subtítulo / Frase")
texto_subtitulo = st.sidebar.text_input("Texto del Subtítulo:", "¡Promoción por tiempo limitado!")
tamano_subtitulo = st.sidebar.slider("Tamaño Subtítulo (px):", min_value=10, max_value=80, value=22)
color_subtitulo_hex = st.sidebar.color_picker("Color del Subtítulo:", "#38BDF8")
alineacion_subtitulo = st.sidebar.selectbox("Alineación del Subtítulo:", ["Izquierda", "Centro", "Derecha"])

st.sidebar.markdown("### • Línea 2: Información de Contacto")
texto_contacto = st.sidebar.text_input("Texto de Contacto:", "📞 Tel: 555-0199 | www.tuweb.com")
tamano_contacto = st.sidebar.slider("Tamaño Contacto (px):", min_value=10, max_value=80, value=18)
color_contacto_hex = st.sidebar.color_picker("Color de Contacto:", "#FFFFFF")
alineacion_contacto = st.sidebar.selectbox("Alineación de Contacto:", ["Izquierda", "Centro", "Derecha"])

st.sidebar.markdown("---")
st.sidebar.header("• Control del Recuadro Traslúcido")

color_recuadro_hex = st.sidebar.color_picker("Color del Recuadro:", "#000000")
opacidad_franja = st.sidebar.slider("Opacidad Recuadro:", 0, 255, 180)
pos_y_franja_pct = st.sidebar.slider("Posición Vertical Recuadro (%)", 0, 100, 65)
pos_x_franja_pct = st.sidebar.slider("Posición Horizontal Recuadro (%)", 0, 100, 0)
ancho_franja_pct = st.sidebar.slider("Ancho Recuadro (%)", 10, 100, 100)
alto_franja_pct = st.sidebar.slider("Alto Recuadro (%)", 10, 100, 35)

# Layout principal adaptado para apilarse verticalmente en móviles de forma automática
col_panel, col_preview = st.columns([1, 1], gap="large")

with col_panel:
    st.title("Banner Studio Pro Ultimate")

    st.markdown(
        '<p style="font-size: 20px; font-weight: 500; color: #000000; margin-top: -10px;">'
        'Genera piezas publicitarias con control geométrico total.'
        '</p>',
        unsafe_allow_html=True
    )

    textos_entrada = st.text_area(
        label="Escribe tus frases principales (una por línea):",
        value="¡NUEVO LANZAMIENTO!\nENVÍO GRATIS HOY\nHASTA 12 CUOTAS SIN INTERÉS",
        height=140
    )


def hex_a_rgb(hex_str):
    hex_limpio = hex_str.lstrip('#')
    return (int(hex_limpio[0:2], 16), int(hex_limpio[2:4], 16), int(hex_limpio[4:6], 16))

def obtener_objeto_fuente(fuente_subida, fuente_combo, tamano):
    if fuente_subida is not None:
        try:
            return ImageFont.truetype(
                io.BytesIO(fuente_subida.getvalue()),
                size=tamano
            )
        except Exception:
            pass
    return ImageFont.load_default()

def calcular_posicion_logo(esquina, ancho_img, alto_img, ancho_lg, alto_lg, margen=20):
    if esquina == "Superior Izquierda":
        return (margen, margen)
    elif esquina == "Superior Derecha":
        return (ancho_img - ancho_lg - margen, margen)
    elif esquina == "Inferior Izquierda":
        return (margen, alto_img - alto_lg - margen)
    else: 
        return (ancho_img - ancho_lg - margen, alto_img - alto_lg - margen)

def construir_banner(foto_base, logo_file, pos_esquina, frase_principal, 
                     obj_fuente_tit, color_rgb_tit, alin_tit,
                     subtitulo_texto, obj_fuente_sub, color_rgb_sub, alin_sub,
                     contacto_texto, obj_fuente_cont, color_rgb_cont, alin_cont,
                     color_recuadro_rgb,
                     x_pct, y_pct, w_pct, h_pct, opacidad):
    
    img = foto_base.copy()
    ancho, alto = img.size

    x1 = int(ancho * (x_pct / 100))
    y1 = int(alto * (y_pct / 100))
    w_px = int(ancho * (w_pct / 100))
    h_px = int(alto * (h_pct / 100))
    x2 = min(x1 + w_px, ancho)
    y2 = min(y1 + h_px, alto)

    capa_franja = Image.new('RGBA', (ancho, alto), (0, 0, 0, 0))
    dibujo_capa = ImageDraw.Draw(capa_franja)
    
    color_con_alpha = color_recuadro_rgb + (opacidad,)
    dibujo_capa.rectangle((x1, y1, x2, y2), fill=color_con_alpha)
    img_resultado = Image.alpha_composite(img, capa_franja)

    if logo_file is not None:
        logo = Image.open(logo_file).convert("RGBA")
        ancho_logo = int(ancho * 0.15)
        alto_logo = max(1, int(logo.height * (ancho_logo / logo.width)))
        logo_resized = logo.resize((ancho_logo, alto_logo))
        pos_logo = calcular_posicion_logo(pos_esquina, ancho, alto, ancho_logo, alto_logo)
        img_resultado.paste(logo_resized, pos_logo, logo_resized)

    dibujo_texto = ImageDraw.Draw(img_resultado)
    ancho_franja_real = x2 - x1
    margen_interno = 20
    pos_actual_y = y1 + 15

    if frase_principal.strip():
        bbox_titulo = obj_fuente_tit.getbbox(frase_principal)
        ancho_texto_principal = bbox_titulo[2] - bbox_titulo[0]
        alto_texto_principal = bbox_titulo[3] - bbox_titulo[1]
        
        if alin_tit == "Centro":
            pos_texto_x = x1 + (ancho_franja_real - ancho_texto_principal) // 2
        elif alin_tit == "Derecha":
            pos_texto_x = x2 - ancho_texto_principal - margen_interno
        else:
            pos_texto_x = x1 + margen_interno

        dibujo_texto.text((pos_texto_x, pos_actual_y), frase_principal, fill=color_rgb_tit, font=obj_fuente_tit)
        pos_actual_y += alto_texto_principal + 12

    if subtitulo_texto.strip():
        bbox_sub = obj_fuente_sub.getbbox(subtitulo_texto)
        ancho_sub = bbox_sub[2] - bbox_sub[0]
        alto_sub = bbox_sub[3] - bbox_sub[1]
        
        if alin_sub == "Centro":
            pos_sub_x = x1 + (ancho_franja_real - ancho_sub) // 2
        elif alin_sub == "Derecha":
            pos_sub_x = x2 - ancho_sub - margen_interno
        else:
            pos_sub_x = x1 + margen_interno
            
        if pos_actual_y < (y2 - 10):
            dibujo_texto.text((pos_sub_x, pos_actual_y), subtitulo_texto, fill=color_rgb_sub, font=obj_fuente_sub)
            pos_actual_y += alto_sub + 12

    if contacto_texto.strip():
        bbox_cont = obj_fuente_cont.getbbox(contacto_texto)
        ancho_cont = bbox_cont[2] - bbox_cont[0]
        
        if alin_cont == "Centro":
            pos_cont_x = x1 + (ancho_franja_real - ancho_cont) // 2
        elif alin_cont == "Derecha":
            pos_cont_x = x2 - ancho_cont - margen_interno
        else:
            pos_cont_x = x1 + margen_interno
            
        if pos_actual_y < (y2 - 10):
            dibujo_texto.text((pos_cont_x, pos_actual_y), contacto_texto, fill=color_rgb_cont, font=obj_fuente_cont)

    return img_resultado


rgb_texto = hex_a_rgb(color_texto_hex)
rgb_subtitulo = hex_a_rgb(color_subtitulo_hex)
rgb_contacto = hex_a_rgb(color_contacto_hex)
rgb_recuadro = hex_a_rgb(color_recuadro_hex)

fuente_activa = obtener_objeto_fuente(fuente_custom, opcion_fuente, tamano_fuente)
fuente_sub_activa = obtener_objeto_fuente(fuente_custom, opcion_fuente, tamano_subtitulo)
fuente_cont_activa = obtener_objeto_fuente(fuente_custom, opcion_fuente, tamano_contacto)

lista_frases = [linea.strip() for linea in textos_entrada.split('\n') if linea.strip()]

with col_panel:
    ejecutar = st.button("🚀 Generar Campaña Completa")

with col_preview:
    st.subheader("🖼️ Vista Previa en Tiempo Real")
    
    if fondo_subido is not None:
        foto_base_original = Image.open(fondo_subido).convert("RGBA")
        
        frase_muestra = lista_frases[0] if lista_frases else "TEXTO MUESTRA"
        banner_preview = construir_banner(
            foto_base_original, logo_subido, posicion_logo, frase_muestra,
            fuente_activa, rgb_texto, alineacion_texto,
            texto_subtitulo, fuente_sub_activa, rgb_subtitulo, alineacion_subtitulo,
            texto_contacto, fuente_cont_activa, rgb_contacto, alineacion_contacto,
            rgb_recuadro,
            pos_x_franja_pct, pos_y_franja_pct,
            ancho_franja_pct, alto_franja_pct, opacidad_franja
        )
        
        st.image(banner_preview, use_container_width=True)

        if ejecutar:
            buffer_zip = io.BytesIO()
            with zipfile.ZipFile(buffer_zip, "w") as archivo_zip:
                for idx, frase in enumerate(lista_frases):
                    banner_temp = construir_banner(
                        foto_base_original, logo_subido, posicion_logo, frase,
                        fuente_activa, rgb_texto, alineacion_texto,
                        texto_subtitulo, fuente_sub_activa, rgb_subtitulo, alineacion_subtitulo,
                        texto_contacto, fuente_cont_activa, rgb_contacto, alineacion_contacto,
                        rgb_recuadro,
                        pos_x_franja_pct, pos_y_franja_pct,
                        ancho_franja_pct, alto_franja_pct, opacidad_franja
                    )
                    
                    buffer_img = io.BytesIO()
                    banner_temp.convert("RGB").save(buffer_img, format="PNG")
                    archivo_zip.writestr(f"banner_{idx+1}.png", buffer_img.getvalue())

            st.success(f"¡Se crearon {len(lista_frases)} banners con éxito!")
            st.download_button(
                label="📥 Descargar Paquete Completo (.ZIP)",
                data=buffer_zip.getvalue(),
                file_name="banners_studio_pro.zip",
                mime="application/zip"
            )
    else:
        st.info("💡 Sube una imagen de fondo en la barra lateral para activar la maquetación.")
