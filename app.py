import os
import streamlit as st
import base64
from openai import OpenAI

# ==========================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Análisis Visual IA",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================================
# DISEÑO VISUAL: FUTURISTA, GRAFITO, VIOLETA Y TURQUESA
# ==========================================================

st.markdown("""
<style>

/* Fondo general */
.stApp {
    background:
        radial-gradient(
            circle at 10% 5%,
            rgba(124, 58, 237, 0.18),
            transparent 35%
        ),
        radial-gradient(
            circle at 90% 45%,
            rgba(45, 212, 191, 0.10),
            transparent 30%
        ),
        linear-gradient(
            145deg,
            #09090F 0%,
            #151521 50%,
            #0B1120 100%
        );
    color: #F8FAFC;
}

/* Contenedor principal */
.block-container {
    max-width: 900px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* Título principal */
h1 {
    color: #FFFFFF !important;
    font-size: 2.6rem !important;
    font-weight: 850 !important;
    text-align: center;
    letter-spacing: -1.2px;
    line-height: 1.2 !important;
    padding-bottom: 0.5rem;
    text-shadow: 0 0 30px rgba(167, 139, 250, 0.20);
}

/* Encabezados */
h2, h3, h4 {
    color: #F5F3FF !important;
    font-weight: 750 !important;
    letter-spacing: -0.4px;
}

/* Texto general */
.stApp p,
.stApp label,
.stMarkdown,
.stCaption,
[data-testid="stWidgetLabel"] p {
    color: #D4D4E4 !important;
}

/* Texto introductorio */
.intro-text {
    color: #A5B4FC;
    text-align: center;
    font-size: 1rem;
    line-height: 1.8;
    margin: 0 auto 1.8rem auto;
    max-width: 620px;
}

/* Etiqueta decorativa superior */
.eyebrow {
    text-align: center;
    color: #5EEAD4;
    text-transform: uppercase;
    letter-spacing: 3px;
    font-size: 0.72rem;
    font-weight: 800;
    margin-bottom: 0.8rem;
}

/* Campos de texto */
.stTextInput input,
.stTextArea textarea {
    background-color: rgba(24, 24, 39, 0.92) !important;
    color: #FFFFFF !important;
    border: 1px solid #45405F !important;
    border-radius: 13px !important;
    padding: 0.75rem 1rem !important;
    caret-color: #5EEAD4 !important;
    transition: border-color 0.2s ease,
                box-shadow 0.2s ease;
}

/* Placeholder */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #9292AB !important;
    opacity: 1 !important;
}

/* Enfoque de campos */
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #A78BFA !important;
    box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.16) !important;
}

/* Interruptor */
[data-testid="stToggle"] {
    background: rgba(30, 27, 50, 0.55);
    border: 1px solid #39334F;
    border-radius: 12px;
    padding: 12px 15px;
}

/* Color del interruptor activo */
[data-testid="stToggle"] [data-checked="true"] {
    background-color: #8B5CF6 !important;
}

/* Botones principales */
.stButton > button {
    background: linear-gradient(
        110deg,
        #7C3AED 0%,
        #6D28D9 55%,
        #4F46E5 100%
    ) !important;
    color: #FFFFFF !important;
    border: 1px solid #A78BFA !important;
    border-radius: 13px !important;
    min-height: 49px;
    font-weight: 750 !important;
    letter-spacing: 0.2px;
    box-shadow: 0 5px 20px rgba(109, 40, 217, 0.20);
    transition: all 0.25s ease;
}

/* Texto de los botones */
.stButton > button p {
    color: #FFFFFF !important;
    font-weight: 750 !important;
}

/* Hover de botones */
.stButton > button:hover {
    background: linear-gradient(
        110deg,
        #8B5CF6,
        #6366F1
    ) !important;
    border-color: #5EEAD4 !important;
    box-shadow: 0 8px 28px rgba(139, 92, 246, 0.32);
    transform: translateY(-2px);
}

/* Botón al pulsar */
.stButton > button:active {
    transform: translateY(0);
}

/* Área de carga de imágenes */
[data-testid="stFileUploader"] {
    background: linear-gradient(
        145deg,
        rgba(30, 27, 50, 0.88),
        rgba(17, 24, 39, 0.90)
    ) !important;
    border: 1px dashed #71629A !important;
    border-radius: 18px !important;
    padding: 18px !important;
    transition: border-color 0.2s ease;
}

/* Hover del área de carga */
[data-testid="stFileUploader"]:hover {
    border-color: #5EEAD4 !important;
}

/* Texto del cargador */
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] small {
    color: #E2E8F0 !important;
}

/* Botón de selección de archivo */
[data-testid="stFileUploader"] button {
    background: #29243F !important;
    color: #FFFFFF !important;
    border: 1px solid #65558C !important;
    border-radius: 9px !important;
}

/* Imagen cargada */
[data-testid="stImage"] {
    background: rgba(20, 20, 35, 0.85);
    padding: 10px;
    border: 1px solid #51446F;
    border-radius: 17px;
    box-shadow: 0 10px 35px rgba(0, 0, 0, 0.22);
}

/* Imagen dentro de la interfaz */
[data-testid="stImage"] img {
    border-radius: 10px;
}

/* Expansor de imagen */
[data-testid="stExpander"] {
    background: rgba(24, 24, 39, 0.65);
    border: 1px solid #45405F;
    border-radius: 15px;
    overflow: hidden;
}

/* Encabezado del expansor */
[data-testid="stExpander"] summary {
    color: #E9D5FF !important;
    font-weight: 650;
}

/* Mensajes de información */
[data-testid="stAlert"] {
    background: rgba(30, 27, 50, 0.80);
    border: 1px solid #51446F;
    border-radius: 13px;
}

/* Texto de alertas */
[data-testid="stAlert"] p {
    color: #F1F5F9 !important;
}

/* Respuestas en Markdown */
[data-testid="stMarkdownContainer"] {
    color: #E2E8F0 !important;
    line-height: 1.85;
}

/* Texto destacado */
[data-testid="stMarkdownContainer"] strong {
    color: #5EEAD4 !important;
}

/* Código */
.stCodeBlock,
[data-testid="stCode"] {
    border: 1px solid #45405F;
    border-radius: 12px;
}

/* Separadores */
hr {
    border-color: #39334F !important;
}

/* Indicador de procesamiento */
[data-testid="stSpinner"] p {
    color: #C4B5FD !important;
}

/* Pie visual */
.footer-note {
    text-align: center;
    color: #77778F;
    font-size: 0.78rem;
    padding-top: 1.5rem;
    letter-spacing: 0.3px;
}

/* Diseño adaptable a móviles */
@media (max-width: 640px) {
    .block-container {
        padding: 1.3rem 1rem 2rem 1rem;
    }

    h1 {
        font-size: 2rem !important;
        letter-spacing: -0.7px;
    }

    .stButton > button {
        width: 100%;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# FUNCIÓN ORIGINAL: CODIFICAR IMAGEN
# ==========================================================

def encode_image(image_file):
    return base64.b64encode(
        image_file.getvalue()
    ).decode("utf-8")


# ==========================================================
# INTERFAZ PRINCIPAL
# ==========================================================

st.markdown(
    '<div class="eyebrow">✦ Inteligencia artificial visual ✦</div>',
    unsafe_allow_html=True
)

st.title("Análisis de Imagen 🔮")

st.markdown(
    """
    <div class="intro-text">
        Explora el contenido de tus imágenes con inteligencia artificial.
        Carga una imagen, añade contexto opcional y descubre lo que contiene.
    </div>
    """,
    unsafe_allow_html=True
)

# Clave de API
ke = st.text_input(
    "🔑 Ingresa tu Clave",
    type="password",
    placeholder="Introduce tu clave de OpenAI"
)

os.environ['OPENAI_API_KEY'] = ke

# Recuperar clave de API
api_key = os.environ['OPENAI_API_KEY']

# Inicializar cliente OpenAI
client = OpenAI(api_key=api_key)

# Cargar imagen
uploaded_file = st.file_uploader(
    "📁 Sube tu imagen para comenzar",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file:
    with st.expander("🖼️ Vista previa de la imagen", expanded=True):
        st.image(
            uploaded_file,
            caption=uploaded_file.name,
            use_container_width=True
        )

# Contexto adicional
show_details = st.toggle(
    "✍️ Pregunta algo específico sobre la imagen",
    value=False
)

if show_details:
    additional_details = st.text_area(
        "Contexto o pregunta adicional",
        placeholder="Ejemplo: Explica los objetos que aparecen en la imagen...",
        disabled=not show_details
    )

# Botón de análisis
analyze_button = st.button(
    "✦ Analizar imagen",
    type="secondary"
)

# Lógica original de análisis
if uploaded_file is not None and api_key and analyze_button:

    with st.spinner("Analizando tu imagen..."):

        base64_image = encode_image(uploaded_file)

        prompt_text = (
            "Describe what you see in the image in spanish"
        )

        if show_details and additional_details:
            prompt_text += (
                f"\n\nAdditional Context Provided by the User:\n"
                f"{additional_details}"
            )

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": (
                                f"data:image/jpeg;base64,{base64_image}"
                            )
                        }
                    }
                ]
            }
        ]

        try:
            full_response = ""
            message_placeholder = st.empty()

            for completion in client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1200,
                stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += (
                        completion.choices[0].delta.content
                    )
                    message_placeholder.markdown(
                        full_response + "▌"
                    )

            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    if not uploaded_file and analyze_button:
        st.warning("Please upload an image.")

    if not api_key:
        st.warning("Por favor ingresa tu API key.")

# Pie visual
st.markdown(
    """
    <div class="footer-note">
        VISUAL AI STUDIO · POWERED BY OPENAI
    </div>
    """,
    unsafe_allow_html=True
)
