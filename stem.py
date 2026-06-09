import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="STAYHER Connect",
    page_icon="💜",
    layout="wide"
)

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("💜 STAYHER Connect")

pagina = st.sidebar.radio(
    "Navegación",
    [
        "Inicio",
        "Mi Perfil IA",
        "Vacantes",
        "Comunidad",
        "Eventos",
        "Historias",
        "Empresas"
    ]
)

# ==========================
# INICIO
# ==========================

if pagina == "Inicio":

    st.title("💜 STAYHER Connect")
    st.subheader(
        "Conectando mujeres STEM con oportunidades laborales y crecimiento profesional"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Mujeres Registradas", "1,250")

    with col2:
        st.metric("Empresas Aliadas", "48")

    with col3:
        st.metric("Vacantes Activas", "320")

    st.markdown("---")

    st.write("""
    STAYHER Connect es una plataforma diseñada para mujeres STEM
    que conecta talento, oportunidades laborales y networking profesional
    mediante inteligencia artificial.
    """)

# ==========================
# PERFIL IA
# ==========================

elif pagina == "Mi Perfil IA":

    st.title("🤖 Perfil Inteligente")

    nombre = st.text_input("Nombre")

    profesion = st.selectbox(
        "Área STEM",
        [
            "Ingeniería Biomédica",
            "Ingeniería de Sistemas",
            "Electrónica",
            "Mecánica",
            "Ciencia de Datos",
            "Investigación"
        ]
    )

    intereses = st.text_area(
        "¿Cuáles son tus intereses profesionales?"
    )

    disponibilidad = st.slider(
        "Horas disponibles por semana",
        1,
        60,
        20
    )

    modalidad = st.selectbox(
        "Modalidad preferida",
        ["Remoto", "Híbrido", "Presencial"]
    )

    if st.button("Generar Perfil"):

        st.success("Perfil generado correctamente")

        st.markdown("### Resultado")

        st.info(
            f"""
            {nombre} es una profesional del área de {profesion}
            con interés en {intereses}.

            Tiene una disponibilidad efectiva de
            {disponibilidad} horas semanales y prefiere
            modalidad {modalidad}.

            Compatibilidad estimada para vacantes STEM:
            88%.
            """
        )

# ==========================
# VACANTES
# ==========================

elif pagina == "Vacantes":

    st.title("💼 Vacantes Recomendadas")

    vacantes = pd.DataFrame(
        {
            "Empresa": [
                "MedTech",
                "BioData",
                "HealthAI",
                "Innovatech"
            ],
            "Cargo": [
                "Ingeniera Clínica",
                "Analista Biomédica",
                "Especialista en Datos",
                "Investigadora Junior"
            ],
            "Compatibilidad": [
                "92%",
                "88%",
                "84%",
                "80%"
            ]
        }
    )

    st.dataframe(vacantes, use_container_width=True)

# ==========================
# COMUNIDAD
# ==========================

elif pagina == "Comunidad":

    st.title("🌎 Comunidad STEM")

    st.markdown("""
    ### Publicaciones recientes

    👩‍🔬 Ana Gómez

    "Acabo de iniciar mi práctica en ingeniería clínica.
    ¿Algún consejo?"

    ---

    👩‍💻 Laura Martínez

    "Comparto convocatoria para mujeres en IA y salud digital."

    ---

    👩‍🔬 María Rodríguez

    "¿Quién asistirá al evento STEM Connect Cali?"
    """)

# ==========================
# EVENTOS
# ==========================

elif pagina == "Eventos":

    st.title("🎤 Eventos STEM Connect")

    st.success("Próximo evento semestral")

    st.write("""
    📅 Fecha: 15 de septiembre

    📍 Lugar: Universidad Autónoma de Occidente

    Participarán:

    - Empresas tecnológicas
    - Hospitales
    - Centros de investigación
    - Mujeres líderes STEM
    """)

# ==========================
# HISTORIAS
# ==========================

elif pagina == "Historias":

    st.title("✨ Historias que Inspiran")

    st.markdown("""
    ### De estudiante a ingeniera clínica

    Camila logró ingresar a una multinacional de dispositivos médicos
    después de participar en eventos de networking STEM.

    ---

    ### Liderando proyectos de IA

    Laura comenzó como practicante y hoy dirige un equipo de ciencia
    de datos en el sector salud.

    ---

    ### Emprendimiento biomédico

    Andrea creó una startup enfocada en telemedicina para zonas rurales.
    """)

# ==========================
# EMPRESAS
# ==========================

elif pagina == "Empresas":

    st.title("🏢 Empresas Aliadas")

    empresas = [
        "MedTech",
        "BioData",
        "HealthAI",
        "Hospital Universitario",
        "Innovatech"
    ]

    for empresa in empresas:
        st.card if False else None
        st.write(f"✅ {empresa}")

    st.markdown("---")

    st.subheader("Beneficios")

    st.write("""
    - Acceso a talento femenino STEM.
    - Participación en eventos semestrales.
    - Employer Branding.
    - Reclutamiento inteligente mediante IA.
    """)
