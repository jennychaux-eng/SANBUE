import streamlit as st
import json
import random
from datetime import datetime
import time

st.set_page_config(
    page_title="STAYHER Connect — Plataforma Inteligente para Mujeres STEM",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Styles ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #2d1b69 0%, #4a2080 50%, #7c3aed 100%);
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] .stRadio label { color: white !important; }

/* Cards */
.card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid #f0e6ff;
    box-shadow: 0 2px 12px rgba(124,58,237,0.07);
    margin-bottom: 1rem;
}
.card-purple {
    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
    color: white;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.card-pink {
    background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
    color: white;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* IPP meter */
.ipp-bar-bg {
    background: #f0e6ff;
    border-radius: 99px;
    height: 18px;
    width: 100%;
}
.ipp-bar-fill {
    background: linear-gradient(90deg, #7c3aed, #ec4899);
    border-radius: 99px;
    height: 18px;
    transition: width 1s ease;
}

/* Chat bubble */
.bubble-ai {
    background: #f5f0ff;
    border-radius: 16px 16px 16px 4px;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.95rem;
    border-left: 3px solid #7c3aed;
    color: #1a1a2e;
}
.bubble-user {
    background: #7c3aed;
    color: white;
    border-radius: 16px 16px 4px 16px;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0 0.4rem 2rem;
    font-size: 0.95rem;
}

/* Tags */
.tag {
    display: inline-block;
    background: #f0e6ff;
    color: #6d28d9;
    border-radius: 99px;
    padding: 3px 12px;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 2px;
}
.tag-pink {
    background: #fce7f3;
    color: #9d174d;
}

/* Section header */
.section-header {
    font-size: 1.6rem;
    font-weight: 700;
    color: #4a1d96;
    margin-bottom: 0.2rem;
}
.section-sub {
    color: #6b7280;
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
}

/* Stats */
.stat-number {
    font-size: 2rem;
    font-weight: 700;
    color: #7c3aed;
}
.stat-label {
    font-size: 0.8rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Event card */
.event-card {
    border-left: 4px solid #7c3aed;
    background: #faf5ff;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}

/* Story card */
.story-card {
    border-left: 4px solid #ec4899;
    background: #fff5f9;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}

/* Community post */
.post-card {
    background: white;
    border: 1px solid #f0e6ff;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# ── Session state init ───────────────────────────────────────────────────────
defaults = {
    "page": "Inicio",
    "chat_history": [],
    "chat_step": 0,
    "user_profile": {},
    "ipp_score": None,
    "ipp_components": {},
    "interview_done": False,
    "community_posts": [
        {"autor": "Ana Martínez", "area": "Ciencia de Datos", "texto": "¿Alguien tiene experiencia con MLflow para tracking de experimentos en producción? Busco recomendaciones 🚀", "likes": 14, "comments": 3, "tiempo": "hace 2h"},
        {"autor": "Lucía Torres", "area": "Ingeniería de Software", "texto": "¡Acabo de conseguir mi primer rol como Senior Dev siendo mamá de dos! El síndrome del impostor es real, pero se supera 💜 AMA", "likes": 87, "comments": 21, "tiempo": "hace 5h"},
        {"autor": "Valentina Ríos", "area": "Electrónica", "texto": "Convocatoria: beca completa para mujeres en electrónica de potencia — Universidad Nacional. Cierra el 30 de junio.", "likes": 43, "comments": 9, "tiempo": "hace 1d"},
        {"autor": "Sofía Mendoza", "area": "Investigación", "texto": "Paper aceptado en IEEE sobre detección temprana de cáncer con visión por computador 🎉 ¡Gracias a todas las que me apoyaron!", "likes": 102, "comments": 34, "tiempo": "hace 2d"},
    ]
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Interview flow ───────────────────────────────────────────────────────────
INTERVIEW_STEPS = [
    {"key": "area", "pregunta": "¡Hola! Soy STAYHER AI 💜 Estoy aquí para conocerte de verdad — no solo tu CV. ¿En qué área STEM trabajas o estudias actualmente?", "tipo": "text"},
    {"key": "tecnologias", "pregunta": "¡Qué interesante! ¿Qué tecnologías, lenguajes o herramientas manejas con mayor confianza?", "tipo": "text"},
    {"key": "proyectos_orgullo", "pregunta": "Cuéntame de un proyecto o logro del que te sientas especialmente orgullosa. Puede ser profesional, académico o personal.", "tipo": "text"},
    {"key": "areas_explorar", "pregunta": "¿Qué áreas o roles te gustaría explorar en tu próximo paso profesional?", "tipo": "text"},
    {"key": "personas_cargo", "pregunta": "¿Tienes personas a cargo (hijos, familiares, etc.)? Esto nos ayuda a entender tu contexto de vida, sin ningún tipo de juicio.", "tipo": "select", "opciones": ["No", "Sí, hijos pequeños (< 5 años)", "Sí, hijos en edad escolar", "Sí, cuido a un familiar adulto", "Sí, múltiples responsabilidades"]},
    {"key": "modalidad", "pregunta": "¿Cuál es tu modalidad de trabajo ideal?", "tipo": "select", "opciones": ["100% Remoto", "Híbrido (2-3 días en oficina)", "Presencial", "Flexible (varía según el proyecto)"]},
    {"key": "horas_productivas", "pregunta": "¿En qué franja horaria te sientes más productiva y enfocada?", "tipo": "select", "opciones": ["Madrugada (5am-8am)", "Mañana temprana (8am-12pm)", "Tarde (12pm-6pm)", "Noche (6pm-12am)", "Varía mucho, no tengo un patrón fijo"]},
    {"key": "horas_disponibles", "pregunta": "¿Cuántas horas diarias puedes dedicar al trabajo sin comprometer tu bienestar?", "tipo": "slider", "min": 2, "max": 12, "default": 6},
    {"key": "importancia_flexibilidad", "pregunta": "En una escala del 1 al 5, ¿qué tan importante es la flexibilidad horaria para ti?", "tipo": "slider", "min": 1, "max": 5, "default": 4},
    {"key": "liderazgo", "pregunta": "¿Cómo describirías tu estilo de liderazgo o trabajo en equipo?", "tipo": "select", "opciones": ["Líder natural, me gusta tomar iniciativa", "Colaboradora activa, prefiero co-crear", "Especialista técnica, aporto desde la profundidad", "Facilitadora, conecto personas e ideas", "Aún lo estoy descubriendo"]},
    {"key": "cursos_completados", "pregunta": "Aproximadamente, ¿cuántos cursos, certificaciones o programas de formación has completado en los últimos 2 años?", "tipo": "slider", "min": 0, "max": 20, "default": 3},
    {"key": "adaptabilidad", "pregunta": "Última pregunta 🎉 ¿Qué tan cómoda te sientes con los cambios y entornos de incertidumbre?", "tipo": "select", "opciones": ["Muy cómoda, me energizan los retos nuevos", "Bastante cómoda con el cambio gradual", "Prefiero estabilidad pero me adapto bien", "Me resulta desafiante, prefiero estructura clara"]},
]

def calcular_ipp(perfil):
    """Calcula el Índice de Productividad Potencial (IPP)"""
    # Competencias (0.4)
    tech_score = min(len(perfil.get("tecnologias", "").split(",")) * 12, 100)
    cursos = perfil.get("cursos_completados", 3)
    competencias = min((tech_score * 0.6) + (min(cursos * 8, 100) * 0.4), 100)

    # Cumplimiento (0.3)
    proyectos = len(perfil.get("proyectos_orgullo", "").split())
    cumplimiento = min(40 + proyectos * 3, 100)

    # Disponibilidad efectiva (0.2)
    horas = perfil.get("horas_disponibles", 6)
    hora_prod = perfil.get("horas_productivas", "Mañana temprana (8am-12pm)")
    concentracion = 1.3 if "temprana" in hora_prod or "tarde" in hora_prod else 1.0
    disponibilidad = min((horas * concentracion / 10) * 100, 100)

    # Adaptabilidad (0.1)
    adapt_map = {
        "Muy cómoda, me energizan los retos nuevos": 100,
        "Bastante cómoda con el cambio gradual": 80,
        "Prefiero estabilidad pero me adapto bien": 65,
        "Me resulta desafiante, prefiero estructura clara": 50,
    }
    adaptabilidad = adapt_map.get(perfil.get("adaptabilidad", ""), 70)

    # Bonus por flexibilidad (contexto de vida)
    flex_importance = perfil.get("importancia_flexibilidad", 4)
    personas_cargo = perfil.get("personas_cargo", "No")
    bonus = 5 if personas_cargo != "No" else 0  # Bonus por resiliencia

    ipp = (competencias * 0.4 + cumplimiento * 0.3 + disponibilidad * 0.2 + adaptabilidad * 0.1) + bonus
    ipp = round(min(ipp, 100), 1)

    return ipp, {
        "Competencias técnicas": round(competencias, 1),
        "Historial de cumplimiento": round(cumplimiento, 1),
        "Disponibilidad efectiva": round(disponibilidad, 1),
        "Adaptabilidad": round(adaptabilidad, 1),
    }


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💜 STAYHER Connect")
    st.markdown("*Donde el potencial vale más que el horario*")
    st.markdown("---")
    page = st.radio("", [
        "🏠 Inicio",
        "🤖 Entrevista IA",
        "📊 Mi Perfil IPP",
        "💼 Empleos",
        "👥 Comunidad",
        "📅 Eventos",
        "📖 Mentorías",
    ], key="nav")
    st.session_state.page = page

    if st.session_state.interview_done:
        st.markdown("---")
        st.markdown("**Tu IPP**")
        ipp = st.session_state.ipp_score
        color = "#22c55e" if ipp >= 80 else "#f59e0b" if ipp >= 60 else "#ef4444"
        st.markdown(f"<div style='font-size:2rem;font-weight:700;color:{color};'>{ipp}</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.75rem;color:#d4bbff;'>Índice de Productividad Potencial</div>", unsafe_allow_html=True)


# ── Pages ────────────────────────────────────────────────────────────────────
p = st.session_state.page

# ── HOME ────────────────────────────────────────────────────────────────────
if "Inicio" in p:

    # ── TOP BAR: Nombre + eslogan ──
    st.markdown("""
    <div style='display:flex;align-items:center;justify-content:space-between;padding:1.2rem 0 0.5rem;border-bottom:1px solid #f0e6ff;margin-bottom:2rem;flex-wrap:wrap;gap:1rem;'>
        <div>
            <span style='font-size:1.6rem;font-weight:800;color:#3b0764;letter-spacing:-0.02em;'>STAYHER</span>
            <span style='font-size:1.6rem;font-weight:300;color:#7c3aed;letter-spacing:-0.02em;'> Connect</span>
            <div style='font-size:0.85rem;color:#9ca3af;font-style:italic;margin-top:2px;'>Conectamos talento, creamos oportunidades.</div>
        </div>
        <div style='display:flex;gap:8px;flex-wrap:wrap;'>
            <span style='background:#f5f0ff;color:#5b21b6;border-radius:99px;padding:5px 14px;font-size:0.78rem;font-weight:600;'>100+ Vacantes</span>
            <span style='background:#fce7f3;color:#9d174d;border-radius:99px;padding:5px 14px;font-size:0.78rem;font-weight:600;'>20 Áreas STEM</span>
            <span style='background:#f0fdf4;color:#166534;border-radius:99px;padding:5px 14px;font-size:0.78rem;font-weight:600;'>Summit Nov 2026</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── HERO ──
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1e0a3c 0%,#3b1278 55%,#7c3aed 100%);border-radius:24px;padding:3.5rem 3rem 3.5rem;margin-bottom:2.5rem;color:white;position:relative;overflow:hidden;'>
        <div style='position:absolute;top:-40px;right:-40px;width:280px;height:280px;background:rgba(236,72,153,0.12);border-radius:50%;'></div>
        <div style='position:absolute;bottom:-60px;right:120px;width:180px;height:180px;background:rgba(167,139,250,0.1);border-radius:50%;'></div>
        <div style='position:relative;max-width:580px;'>
            <div style='display:inline-block;background:rgba(236,72,153,0.25);border:1px solid rgba(236,72,153,0.4);border-radius:99px;padding:5px 16px;font-size:0.75rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:1.4rem;color:#f9a8d4;'>
                Inteligencia Artificial · Empleo · Comunidad
            </div>
            <h1 style='font-size:2.8rem;font-weight:800;line-height:1.13;margin:0 0 1.2rem;letter-spacing:-0.02em;'>
                El talento no se mide<br>en horas. Se mide<br>en <span style='color:#f9a8d4;'>resultados.</span>
            </h1>
            <p style='font-size:1rem;line-height:1.75;opacity:0.82;margin:0 0 2rem;max-width:500px;'>
                La plataforma que conecta a mujeres STEM con empresas que valoran quién eres, no solo cuánto tiempo tienes. Perfil inteligente, matching real, comunidad que impulsa.
            </p>
            <div style='display:flex;gap:2rem;flex-wrap:wrap;border-top:1px solid rgba(255,255,255,0.12);padding-top:1.5rem;'>
                <div>
                    <div style='font-size:2rem;font-weight:800;line-height:1;'>1,200+</div>
                    <div style='font-size:0.72rem;opacity:0.6;text-transform:uppercase;letter-spacing:0.08em;margin-top:3px;'>Profesionales</div>
                </div>
                <div style='border-left:1px solid rgba(255,255,255,0.15);padding-left:2rem;'>
                    <div style='font-size:2rem;font-weight:800;line-height:1;'>85+</div>
                    <div style='font-size:0.72rem;opacity:0.6;text-transform:uppercase;letter-spacing:0.08em;margin-top:3px;'>Empresas aliadas</div>
                </div>
                <div style='border-left:1px solid rgba(255,255,255,0.15);padding-left:2rem;'>
                    <div style='font-size:2rem;font-weight:800;line-height:1;'>94%</div>
                    <div style='font-size:0.72rem;opacity:0.6;text-transform:uppercase;letter-spacing:0.08em;margin-top:3px;'>Tasa de satisfacción</div>
                </div>
                <div style='border-left:1px solid rgba(255,255,255,0.15);padding-left:2rem;'>
                    <div style='font-size:2rem;font-weight:800;line-height:1;'>20</div>
                    <div style='font-size:0.72rem;opacity:0.6;text-transform:uppercase;letter-spacing:0.08em;margin-top:3px;'>Áreas STEM</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("  Crear mi perfil con IA  →", type="primary"):
        st.session_state.page = "🤖 Entrevista IA"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── MÓDULOS ──
    st.markdown("<div style='font-size:1rem;font-weight:700;color:#6b7280;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1rem;'>Todo lo que necesitas, en un solo lugar</div>", unsafe_allow_html=True)

    modulos = [
        ("🤖", "Matching Inteligente", "#f5f0ff", "#5b21b6", "#e9d5ff",
         "Entrevista con IA que construye tu perfil 360° y calcula tu Índice de Productividad Potencial para conectarte con las vacantes que realmente encajan con tu vida."),
        ("👥", "Comunidad STEM", "#fff5f9", "#9d174d", "#fce7f3",
         "20 espacios temáticos por área. Comparte logros, conecta con colegas, encuentra convocatorias y crece junto a una red de mujeres que entiende tu camino."),
        ("📅", "Eventos Connect", "#eff6ff", "#1e40af", "#dbeafe",
         "Summit semestral con +30 empresas aliadas, conferencias de líderes STEM y networking estructurado entre profesionales y reclutadores."),
        ("📖", "Mentorías & Historias", "#f0fdf4", "#166534", "#dcfce7",
         "Aprende de quienes ya recorrieron tu camino. Historias reales de mujeres STEM que crecieron profesionalmente sin renunciar a su vida personal."),
    ]

    c1, c2 = st.columns(2)
    cols = [c1, c2, c1, c2]
    for col, (icon, title, bg, tc, border, desc) in zip(cols, modulos):
        with col:
            st.markdown(f"""
            <div style='background:{bg};border:1px solid {border};border-radius:16px;padding:1.4rem 1.5rem;margin-bottom:1rem;'>
                <div style='display:flex;align-items:center;gap:10px;margin-bottom:0.7rem;'>
                    <span style='font-size:1.4rem;'>{icon}</span>
                    <span style='font-weight:700;font-size:0.95rem;color:{tc};'>{title}</span>
                </div>
                <div style='font-size:0.87rem;color:#4b5563;line-height:1.7;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── EMPRESAS ALIADAS ──
    st.markdown("""
    <div style='text-align:center;margin-bottom:1.2rem;'>
        <div style='font-size:0.8rem;font-weight:600;color:#9ca3af;text-transform:uppercase;letter-spacing:0.12em;'>Empresas que confían en nuestro talento</div>
    </div>
    """, unsafe_allow_html=True)

    empresas = [
        ("BC", "#1e3a5f", "Bancolombia Tech"),
        ("GC", "#1a73e8", "Google Colombia"),
        ("MS", "#00a4ef", "Microsoft LATAM"),
        ("RP", "#ff441a", "Rappi Engineering"),
        ("EP", "#00875a", "EPM Digital"),
        ("BS", "#7c3aed", "BioSystems"),
        ("TC", "#ec4899", "TechCorp Latam"),
        ("NV", "#0f766e", "NeuralMind"),
        ("SX", "#b45309", "SpaceX Partners"),
        ("ID", "#4338ca", "InnovaData"),
    ]

    cols_e = st.columns(len(empresas))
    for col, (initials, color, name) in zip(cols_e, empresas):
        with col:
            st.markdown(f"""
            <div style='text-align:center;padding:0.5rem 0;'>
                <div style='width:42px;height:42px;border-radius:10px;background:{color};display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:0.75rem;margin:0 auto 5px;letter-spacing:0.02em;'>{initials}</div>
                <div style='font-size:0.62rem;color:#9ca3af;line-height:1.3;text-align:center;'>{name}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='border-top:1px solid #f0e6ff;margin:2rem 0;'></div>", unsafe_allow_html=True)

    # ── TESTIMONIOS ──
    st.markdown("""
    <div style='text-align:center;margin-bottom:1.5rem;'>
        <div style='font-size:1.25rem;font-weight:700;color:#1a1a2e;'>Lo que dicen quienes ya lo vivieron</div>
        <div style='font-size:0.88rem;color:#9ca3af;margin-top:4px;'>Historias reales de mujeres STEM que transformaron su carrera</div>
    </div>
    """, unsafe_allow_html=True)

    t1, t2, t3 = st.columns(3)
    testimonios = [
        (
            "Laura P.", "CTO · Bogotá",
            "LC", "#7c3aed",
            "Después de 3 años sin respuesta de empresas convencionales, STAYHER Connect me conectó con un equipo que valoró mi portafolio y mi disponibilidad real. Hoy lidero un equipo de 12 personas.",
            "Ingeniería de Software"
        ),
        (
            "María F.", "Data Scientist · Medellín",
            "MF", "#ec4899",
            "Soy madre de dos y trabajaba 4 horas al día. Ningún ATS me pasaba. Aquí mi IPP fue 88/100 y en dos semanas tenía tres entrevistas. Encontré un rol 100% remoto que se adapta a mi vida.",
            "Ciencia de Datos & IA"
        ),
        (
            "Valentina R.", "Investigadora · Cali",
            "VR", "#0f766e",
            "Migré desde provincia y no tenía red de contactos. La comunidad de STAYHER me ayudó a encontrar una beca, una mentora y mi primer contrato internacional. Todo en menos de 6 meses.",
            "Investigación Científica"
        ),
    ]
    for col, (nombre, cargo, ini, color, texto, area) in zip([t1, t2, t3], testimonios):
        with col:
            st.markdown(f"""
            <div style='background:white;border:1px solid #f0e6ff;border-radius:18px;padding:1.5rem;height:100%;'>
                <div style='font-size:1.3rem;color:#7c3aed;margin-bottom:0.8rem;line-height:1;'>"</div>
                <div style='font-size:0.88rem;color:#374151;line-height:1.7;margin-bottom:1.2rem;'>{texto}</div>
                <div style='border-top:1px solid #f5f0ff;padding-top:1rem;display:flex;align-items:center;gap:10px;'>
                    <div style='width:38px;height:38px;border-radius:50%;background:{color};display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:0.78rem;flex-shrink:0;'>{ini}</div>
                    <div>
                        <div style='font-weight:600;font-size:0.88rem;color:#1a1a2e;'>{nombre}</div>
                        <div style='font-size:0.75rem;color:#9ca3af;'>{cargo}</div>
                        <div style='font-size:0.7rem;color:{color};font-weight:600;margin-top:1px;'>{area}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── IPP BANNER ──
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1e0a3c,#4c1d95);border-radius:20px;padding:2rem 2.5rem;color:white;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:2rem;'>
        <div style='flex:1;min-width:240px;'>
            <div style='font-size:0.72rem;text-transform:uppercase;letter-spacing:0.12em;opacity:0.55;margin-bottom:0.4rem;'>Nuestra innovación</div>
            <div style='font-size:1.2rem;font-weight:700;margin-bottom:0.5rem;'>Índice de Productividad Potencial (IPP)</div>
            <div style='font-size:0.88rem;opacity:0.8;max-width:400px;line-height:1.6;'>No medimos cuántas horas tienes. Medimos lo que puedes lograr con las horas que tienes.</div>
        </div>
        <div style='display:flex;gap:1rem;flex-wrap:wrap;'>
            <div style='background:rgba(255,255,255,0.08);border-radius:12px;padding:0.9rem 1.1rem;text-align:center;min-width:80px;'>
                <div style='font-size:1.3rem;font-weight:800;color:#c4b5fd;'>40%</div>
                <div style='font-size:0.7rem;opacity:0.65;margin-top:3px;'>Competencias</div>
            </div>
            <div style='background:rgba(255,255,255,0.08);border-radius:12px;padding:0.9rem 1.1rem;text-align:center;min-width:80px;'>
                <div style='font-size:1.3rem;font-weight:800;color:#f9a8d4;'>30%</div>
                <div style='font-size:0.7rem;opacity:0.65;margin-top:3px;'>Cumplimiento</div>
            </div>
            <div style='background:rgba(255,255,255,0.08);border-radius:12px;padding:0.9rem 1.1rem;text-align:center;min-width:80px;'>
                <div style='font-size:1.3rem;font-weight:800;color:#6ee7b7;'>20%</div>
                <div style='font-size:0.7rem;opacity:0.65;margin-top:3px;'>Disponibilidad</div>
            </div>
            <div style='background:rgba(255,255,255,0.08);border-radius:12px;padding:0.9rem 1.1rem;text-align:center;min-width:80px;'>
                <div style='font-size:1.3rem;font-weight:800;color:#fcd34d;'>10%</div>
                <div style='font-size:0.7rem;opacity:0.65;margin-top:3px;'>Adaptabilidad</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── ENTREVISTA IA ────────────────────────────────────────────────────────────
elif "Entrevista" in p:
    st.markdown("<div class='section-header'>🤖 Entrevista con IA</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>No te preguntamos cuántas horas tienes. Te preguntamos quién eres.</div>", unsafe_allow_html=True)

    step = st.session_state.chat_step
    history = st.session_state.chat_history

    # Show history
    for msg in history:
        role_class = "bubble-ai" if msg["role"] == "ai" else "bubble-user"
        st.markdown(f"<div class='{role_class}'>{msg['text']}</div>", unsafe_allow_html=True)

    if step < len(INTERVIEW_STEPS) and not st.session_state.interview_done:
        current = INTERVIEW_STEPS[step]

        # Show AI question if not already shown
        if not history or history[-1]["role"] != "ai":
            st.markdown(f"<div class='bubble-ai'>{current['pregunta']}</div>", unsafe_allow_html=True)

        # Input
        with st.form(key=f"step_{step}"):
            if current["tipo"] == "text":
                respuesta = st.text_area("Tu respuesta:", height=80, placeholder="Escribe aquí...", label_visibility="collapsed")
            elif current["tipo"] == "select":
                respuesta = st.selectbox("Elige una opción:", current["opciones"], label_visibility="collapsed")
            elif current["tipo"] == "slider":
                respuesta = st.slider("", current["min"], current["max"], current["default"], label_visibility="collapsed")
                respuesta = str(respuesta)

            submitted = st.form_submit_button("Enviar →", type="primary")

        if submitted and (respuesta if isinstance(respuesta, str) else True):
            st.session_state.chat_history.append({"role": "ai", "text": current["pregunta"]})
            st.session_state.chat_history.append({"role": "user", "text": str(respuesta)})
            st.session_state.user_profile[current["key"]] = respuesta if not isinstance(respuesta, str) else respuesta
            # Convert slider strings to int/float
            if current["tipo"] == "slider":
                st.session_state.user_profile[current["key"]] = int(respuesta)

            st.session_state.chat_step += 1

            if st.session_state.chat_step >= len(INTERVIEW_STEPS):
                # Calculate IPP
                ipp, components = calcular_ipp(st.session_state.user_profile)
                st.session_state.ipp_score = ipp
                st.session_state.ipp_components = components
                st.session_state.interview_done = True
                st.session_state.chat_history.append({
                    "role": "ai",
                    "text": f"¡Gracias! 🎉 Tu perfil está completo. He calculado tu Índice de Productividad Potencial: **{ipp}/100**. Puedes ver el análisis completo en '📊 Mi Perfil IPP'."
                })
            st.rerun()

    elif st.session_state.interview_done:
        st.markdown(f"<div class='bubble-ai'>🎉 ¡Tu entrevista está completa! Tu IPP es <strong>{st.session_state.ipp_score}/100</strong>. Ve a <strong>📊 Mi Perfil IPP</strong> para ver el análisis detallado.</div>", unsafe_allow_html=True)
        if st.button("Ver mi perfil IPP →", type="primary"):
            st.session_state.page = "📊 Mi Perfil IPP"
            st.rerun()

        if st.button("Reiniciar entrevista", type="secondary"):
            for k in ["chat_history", "chat_step", "user_profile", "ipp_score", "ipp_components", "interview_done"]:
                st.session_state[k] = defaults[k]
            st.rerun()

    # Progress
    total = len(INTERVIEW_STEPS)
    current_step = min(step, total)
    st.markdown(f"<div style='margin-top:1.5rem;'><div style='font-size:0.8rem;color:#6b7280;margin-bottom:4px;'>Progreso: {current_step}/{total}</div><div class='ipp-bar-bg'><div class='ipp-bar-fill' style='width:{int(current_step/total*100)}%;'></div></div></div>", unsafe_allow_html=True)


# ── PERFIL IPP ────────────────────────────────────────────────────────────────
elif "IPP" in p:
    st.markdown("<div class='section-header'>📊 Mi Perfil IPP</div>", unsafe_allow_html=True)

    if not st.session_state.interview_done:
        st.info("Aún no has completado la entrevista. Ve a **🤖 Entrevista IA** para comenzar.")
    else:
        perfil = st.session_state.user_profile
        ipp = st.session_state.ipp_score
        components = st.session_state.ipp_components

        col1, col2 = st.columns([1, 2])
        with col1:
            color = "#22c55e" if ipp >= 80 else "#f59e0b" if ipp >= 60 else "#7c3aed"
            st.markdown(f"""
            <div class='card' style='text-align:center;padding:2rem;'>
                <div style='font-size:0.85rem;color:#6b7280;text-transform:uppercase;letter-spacing:0.1em;'>Índice de Productividad Potencial</div>
                <div style='font-size:4rem;font-weight:800;color:{color};line-height:1;margin:1rem 0;'>{ipp}</div>
                <div style='font-size:1rem;color:#4a1d96;font-weight:600;'>{"Excelente potencial" if ipp >= 80 else "Buen potencial" if ipp >= 60 else "Potencial en desarrollo"}</div>
                <div style='font-size:0.8rem;color:#6b7280;margin-top:0.5rem;'>sobre 100 puntos</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("**Desglose del IPP**")
            weights = [0.4, 0.3, 0.2, 0.1]
            for (name, score), w in zip(components.items(), weights):
                st.markdown(f"<div style='display:flex;justify-content:space-between;margin-bottom:4px;font-size:0.9rem;'><span style='color:#374151;'>{name}</span><span style='font-weight:600;color:#7c3aed;'>{score}/100</span></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='ipp-bar-bg' style='margin-bottom:10px;'><div class='ipp-bar-fill' style='width:{score}%;'></div></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.75rem;color:#9ca3af;'>Fórmula: Competencias×0.4 + Cumplimiento×0.3 + Disponibilidad×0.2 + Adaptabilidad×0.1</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Tu perfil de vida**")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class='card'>
                <div style='font-weight:600;color:#4a1d96;margin-bottom:0.5rem;'>🧑‍💻 Profesional</div>
                <div style='font-size:0.9rem;color:#374151;'><b>Área:</b> {perfil.get('area','—')}<br>
                <b>Tecnologías:</b> {perfil.get('tecnologias','—')[:60]}...<br>
                <b>Cursos completados:</b> {perfil.get('cursos_completados','—')}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class='card'>
                <div style='font-weight:600;color:#4a1d96;margin-bottom:0.5rem;'>🏠 Personal</div>
                <div style='font-size:0.9rem;color:#374151;'><b>Personas a cargo:</b> {perfil.get('personas_cargo','—')}<br>
                <b>Modalidad ideal:</b> {perfil.get('modalidad','—')}<br>
                <b>Horas disponibles:</b> {perfil.get('horas_disponibles','—')}h/día</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class='card'>
                <div style='font-weight:600;color:#4a1d96;margin-bottom:0.5rem;'>⚡ Productividad</div>
                <div style='font-size:0.9rem;color:#374151;'><b>Pico productivo:</b> {perfil.get('horas_productivas','—')}<br>
                <b>Estilo:</b> {perfil.get('liderazgo','—')[:40]}<br>
                <b>Flexibilidad:</b> {'⭐'*int(perfil.get('importancia_flexibilidad',4))}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💼 Ver empleos compatibles →", type="primary"):
            st.session_state.page = "💼 Empleos"
            st.rerun()


# ── EMPLEOS ───────────────────────────────────────────────────────────────────
elif "Empleos" in p:
    st.markdown("<div class='section-header'>💼 Empleos</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Vacantes que se adaptan a tu vida, no al revés.</div>", unsafe_allow_html=True)

    ipp = st.session_state.ipp_score

    empleos = [
        {"empresa": "TechCorp Latam", "rol": "Data Scientist Senior", "compatibilidad": 94, "modalidad": "Remoto", "horario": "Flexible", "area": "Ciencia de Datos & IA", "salario": "$4,500–6,000 USD/mes", "tags": ["Python", "ML", "Spark"], "descripcion": "Equipo 100% femenino en liderazgo. Horarios asíncronos. Resultados sobre horas."},
        {"empresa": "BioSystems S.A.", "rol": "Ingeniera de Software Biomédico", "compatibilidad": 88, "modalidad": "Híbrido", "horario": "3 días semana", "area": "Ingeniería Biomédica", "salario": "$3,200–4,500 USD/mes", "tags": ["Java", "IoT", "Salud"], "descripcion": "Empresa liderada por mujeres. Política de maternidad extendida."},
        {"empresa": "InnovaData", "rol": "ML Engineer", "compatibilidad": 82, "modalidad": "Remoto", "horario": "20h/semana", "area": "Ciencia de Datos & IA", "salario": "$2,800–3,500 USD/mes", "tags": ["TensorFlow", "Python", "AWS"], "descripcion": "Rol part-time. Ideal para mujeres con responsabilidades adicionales."},
        {"empresa": "Universidad Nacional", "rol": "Investigadora Postdoctoral", "compatibilidad": 76, "modalidad": "Presencial", "horario": "Horario flexible", "area": "Investigación Científica", "salario": "$2,000–2,500 USD/mes", "tags": ["R", "Estadística", "Publicaciones"], "descripcion": "Grupo de investigación comprometido con equidad de género."},
        {"empresa": "StartupX", "rol": "Full Stack Developer", "compatibilidad": 71, "modalidad": "Remoto", "horario": "Resultados, no horas", "area": "Ingeniería de Software", "salario": "$3,000–4,000 USD/mes", "tags": ["React", "Node.js", "PostgreSQL"], "descripcion": "Startup en crecimiento. Cultura asíncrona y enfocada en impacto."},
        {"empresa": "SecureNet Colombia", "rol": "Analista de Ciberseguridad", "compatibilidad": 85, "modalidad": "Híbrido", "horario": "Flexible", "area": "Ciberseguridad", "salario": "$3,500–5,000 USD/mes", "tags": ["Pentesting", "SIEM", "ISO 27001"], "descripcion": "Equipo diverso e inclusivo. Certificaciones pagadas por la empresa."},
        {"empresa": "RoboTech LATAM", "rol": "Ingeniera de Robótica Jr.", "compatibilidad": 79, "modalidad": "Presencial", "horario": "Jornada flexible", "area": "Robótica & Automatización", "salario": "$2,500–3,500 USD/mes", "tags": ["ROS", "Python", "Arduino"], "descripcion": "Laboratorio de innovación con enfoque en talento femenino en robótica."},
        {"empresa": "EcoSoluciones", "rol": "Ingeniera Ambiental Senior", "compatibilidad": 83, "modalidad": "Híbrido", "horario": "4 días semana", "area": "Ingeniería Ambiental", "salario": "$2,800–3,800 USD/mes", "tags": ["GIS", "AutoCAD", "Normas ISO"], "descripcion": "Empresa B Corp. Comprometida con la conciliación vida-trabajo."},
        {"empresa": "NeuralMind", "rol": "Investigadora en Neurociencias Computacionales", "compatibilidad": 80, "modalidad": "Remoto", "horario": "Autónomo", "area": "Neurociencias", "salario": "$3,000–4,200 USD/mes", "tags": ["MATLAB", "Python", "fMRI"], "descripcion": "Laboratorio 100% remoto con publicaciones en Nature y Science."},
        {"empresa": "Bancolombia Tech", "rol": "Arquitecta de Software Cloud", "compatibilidad": 91, "modalidad": "Híbrido", "horario": "Flexible", "area": "Arquitectura de Software & DevOps", "salario": "$5,000–7,000 USD/mes", "tags": ["AWS", "Kubernetes", "Terraform"], "descripcion": "Programa de liderazgo femenino activo. Bono por resultados, no por horas."},
        {"empresa": "PharmaBio", "rol": "Biotecnóloga de I+D", "compatibilidad": 74, "modalidad": "Presencial", "horario": "Jornada reducida disponible", "area": "Biotecnología", "salario": "$2,600–3,600 USD/mes", "tags": ["CRISPR", "Cultivo celular", "GMP"], "descripcion": "Laboratorio farmacéutico con guarderías corporativas y horario de lactancia."},
        {"empresa": "SpaceX Partners CO", "rol": "Ingeniera de Sistemas Aeroespaciales", "compatibilidad": 68, "modalidad": "Presencial", "horario": "40h/semana", "area": "Astrofísica & Ciencias del Espacio", "salario": "$4,000–6,500 USD/mes", "tags": ["MATLAB", "Simulink", "CAD"], "descripcion": "Proyecto satélital LATAM. Buscan diversidad de pensamiento en el equipo técnico."},
        {"empresa": "DataMinds", "rol": "Estadística & Analista Cuantitativa", "compatibilidad": 87, "modalidad": "Remoto", "horario": "20–30h/semana", "area": "Matemáticas & Estadística", "salario": "$2,400–3,200 USD/mes", "tags": ["R", "SAS", "Power BI"], "descripcion": "Consultora de datos con cultura 100% asíncrona y equipos distribuidos."},
        {"empresa": "DesignFlow", "rol": "UX Researcher & Designer", "compatibilidad": 77, "modalidad": "Remoto", "horario": "Flexible", "area": "Diseño UX/UI", "salario": "$2,200–3,000 USD/mes", "tags": ["Figma", "User testing", "Accesibilidad"], "descripcion": "Agencia de diseño inclusivo. 70% del equipo son mujeres."},
        {"empresa": "ElectroSur", "rol": "Ingeniera Electrónica de Potencia", "compatibilidad": 72, "modalidad": "Híbrido", "horario": "Flexible", "area": "Electrónica & Telecomunicaciones", "salario": "$3,000–4,500 USD/mes", "tags": ["FPGA", "VHDL", "PCB Design"], "descripcion": "Empresa energética comprometida con paridad de género en roles técnicos."},
        {"empresa": "QuímiCO Lab", "rol": "Química de Procesos Industriales", "compatibilidad": 69, "modalidad": "Presencial", "horario": "Turnos flexibles", "area": "Ingeniería Química", "salario": "$2,500–3,500 USD/mes", "tags": ["HPLC", "GC-MS", "Buenas prácticas"], "descripcion": "Laboratorio con salas de lactancia, guarderías y permisos de cuidado extendidos."},
        {"empresa": "MechaNova", "rol": "Ingeniera Mecánica de Producto", "compatibilidad": 75, "modalidad": "Híbrido", "horario": "4 días semana", "area": "Ingeniería Mecánica", "salario": "$2,800–4,000 USD/mes", "tags": ["SolidWorks", "FEA", "Lean Manufacturing"], "descripcion": "Empresa manufacturera con programa de retorno tras maternidad o cuidados."},
        {"empresa": "IndusTech", "rol": "Ingeniera Industrial & Procesos", "compatibilidad": 78, "modalidad": "Híbrido", "horario": "Flexible", "area": "Ingeniería Industrial", "salario": "$2,600–3,800 USD/mes", "tags": ["Six Sigma", "SAP", "Lean"], "descripcion": "Multinacional con política de trabajo flexible y metas por objetivos."},
        {"empresa": "FísicaLab", "rol": "Investigadora en Física de Materiales", "compatibilidad": 70, "modalidad": "Presencial", "horario": "Jornada flexible", "area": "Física", "salario": "$2,200–3,000 USD/mes", "tags": ["Simulación", "Nanomateriales", "Python"], "descripcion": "Centro de investigación con becas para madres investigadoras."},
        {"empresa": "VenturaAI", "rol": "Fundadora Técnica en Residencia", "compatibilidad": 86, "modalidad": "Remoto", "horario": "Autónomo", "area": "Emprendimiento Tecnológico", "salario": "Equity + $1,500 USD/mes", "tags": ["IA", "Product", "Fundraising"], "descripcion": "Aceleradora exclusiva para mujeres fundadoras en tecnología. Inversión semilla incluida."},
    ]

    areas_empleo = [
        "Todas", "Ciencia de Datos & IA", "Ingeniería de Software", "Ingeniería Biomédica",
        "Electrónica & Telecomunicaciones", "Ingeniería Mecánica", "Ingeniería Química",
        "Ingeniería Ambiental", "Ingeniería Industrial", "Ciberseguridad",
        "Robótica & Automatización", "Astrofísica & Ciencias del Espacio", "Biotecnología",
        "Matemáticas & Estadística", "Física", "Neurociencias", "Investigación Científica",
        "Arquitectura de Software & DevOps", "Diseño UX/UI", "Emprendimiento Tecnológico",
        "Ingeniería Química",
    ]
    col1, col2 = st.columns([2, 1])
    with col1:
        filtro_area = st.selectbox("Filtrar por área", areas_empleo)
    with col2:
        filtro_modalidad = st.selectbox("Modalidad", ["Todas", "Remoto", "Híbrido", "Presencial"])

    for emp in empleos:
        if filtro_area != "Todas" and emp["area"] != filtro_area:
            continue
        if filtro_modalidad != "Todas" and emp["modalidad"] != filtro_modalidad:
            continue

        c = emp["compatibilidad"]
        bar_color = "#22c55e" if c >= 85 else "#f59e0b" if c >= 70 else "#7c3aed"

        tags_html = "".join(f"<span class='tag'>{t}</span>" for t in emp["tags"])
        ipp_note = ""
        if ipp:
            diff = abs(ipp - c)
            if diff <= 10:
                ipp_note = " <span style='color:#22c55e;font-size:0.8rem;'>✓ Compatible con tu IPP</span>"

        st.markdown(f"""
        <div class='card'>
            <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                <div>
                    <div style='font-weight:700;font-size:1.05rem;color:#1a1a2e;'>{emp['rol']}</div>
                    <div style='color:#7c3aed;font-weight:500;font-size:0.9rem;'>{emp['empresa']}</div>
                    <div style='color:#6b7280;font-size:0.85rem;margin-top:2px;'>{emp['salario']} · {emp['modalidad']} · {emp['horario']}</div>
                </div>
                <div style='text-align:right;'>
                    <div style='font-size:1.6rem;font-weight:800;color:{bar_color};'>{c}%{ipp_note}</div>
                    <div style='font-size:0.75rem;color:#9ca3af;'>Compatibilidad</div>
                </div>
            </div>
            <div style='margin:0.8rem 0 0.4rem;font-size:0.88rem;color:#4b5563;'>{emp['descripcion']}</div>
            <div>{tags_html}</div>
        </div>
        """, unsafe_allow_html=True)


# ── COMUNIDAD ─────────────────────────────────────────────────────────────────
elif "Comunidad" in p:
    st.markdown("<div class='section-header'>👥 Comunidad STEM</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Tu red profesional, construida por y para mujeres.</div>", unsafe_allow_html=True)

    # Spaces
    areas = [
        "Todas",
        "Ciencia de Datos & IA",
        "Ingeniería de Software",
        "Ingeniería Biomédica",
        "Electrónica & Telecomunicaciones",
        "Ingeniería Mecánica",
        "Ingeniería Química",
        "Ingeniería Ambiental",
        "Ingeniería Industrial",
        "Ciberseguridad",
        "Robótica & Automatización",
        "Astrofísica & Ciencias del Espacio",
        "Biotecnología",
        "Matemáticas & Estadística",
        "Física",
        "Química",
        "Neurociencias",
        "Investigación Científica",
        "Arquitectura de Software & DevOps",
        "Diseño UX/UI",
        "Emprendimiento Tecnológico",
    ]
    area_sel = st.pills("Espacios temáticos", areas, default="Todas")

    # New post
    with st.expander("✏️ Nueva publicación"):
        texto_post = st.text_area("¿Qué quieres compartir hoy?", placeholder="Una pregunta, un logro, una convocatoria...", height=80)
        area_post = st.selectbox("Área", areas[1:])
        if st.button("Publicar →", type="primary"):
            st.session_state.community_posts.insert(0, {
                "autor": "Tú",
                "area": area_post,
                "texto": texto_post,
                "likes": 0,
                "comments": 0,
                "tiempo": "ahora"
            })
            st.success("¡Publicado! 🎉")
            st.rerun()

    st.markdown("---")
    for post in st.session_state.community_posts:
        if area_sel and area_sel != "Todas" and post["area"] != area_sel:
            continue
        initials = "".join(w[0].upper() for w in post["autor"].split()[:2])
        st.markdown(f"""
        <div class='post-card'>
            <div style='display:flex;align-items:center;gap:10px;margin-bottom:8px;'>
                <div style='width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#7c3aed,#ec4899);display:flex;align-items:center;justify-content:center;color:white;font-weight:600;font-size:0.8rem;flex-shrink:0;'>{initials}</div>
                <div>
                    <div style='font-weight:600;font-size:0.9rem;color:#1a1a2e;'>{post['autor']}</div>
                    <div style='font-size:0.75rem;color:#9ca3af;'><span class='tag' style='font-size:0.7rem;padding:2px 8px;'>{post['area']}</span> · {post['tiempo']}</div>
                </div>
            </div>
            <div style='font-size:0.92rem;color:#374151;line-height:1.6;'>{post['texto']}</div>
            <div style='margin-top:8px;font-size:0.82rem;color:#9ca3af;'>❤️ {post['likes']}  &nbsp; 💬 {post['comments']}</div>
        </div>
        """, unsafe_allow_html=True)


# ── EVENTOS ───────────────────────────────────────────────────────────────────
elif "Eventos" in p:
    st.markdown("<div class='section-header'>📅 Eventos STAYHER Connect</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Encuentros semestrales donde las conexiones reales suceden.</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='card-purple'>
        <div style='font-size:0.8rem;opacity:0.8;text-transform:uppercase;letter-spacing:0.1em;'>Próximo evento</div>
        <div style='font-size:1.8rem;font-weight:800;margin:0.3rem 0;'>STAYHER Connect Summit 2025</div>
        <div style='opacity:0.9;'>Noviembre 15–16 · Bogotá, Colombia · Centro de Convenciones Ágora</div>
        <div style='margin-top:1rem;font-size:0.9rem;opacity:0.85;'>El evento semestral más grande de mujeres STEM en Latinoamérica. +30 empresas, +20 conferencias, networking real.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Zona de Reclutamiento**")
        empresas_stands = ["TechCorp Latam", "BioSystems S.A.", "Google Colombia", "Microsoft LATAM", "Bancolombia Tech", "InnovaData", "Rappi Engineering", "EPM Digital"]
        for e in empresas_stands:
            st.markdown(f"<div class='event-card'><span style='font-weight:500;color:#4a1d96;'>🏢 {e}</span><br><span style='font-size:0.82rem;color:#6b7280;'>Stand + entrevistas exprés disponibles</span></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("**Conferencias**")
        conferencias = [
            ("Día 1, 9:00", "Keynote: Mujeres que cambian el juego en IA", "Dra. Carmen López"),
            ("Día 1, 11:00", "Síndrome del impostor: cómo superarlo en STEM", "Ing. Mónica Arias"),
            ("Día 1, 14:00", "Migrar y crecer: historias desde Silicon Valley", "Panel internacional"),
            ("Día 1, 16:00", "Ser madre y CTO: mi historia sin filtros", "Laura Pérez, CTO"),
            ("Día 2, 9:00", "IA y el futuro del trabajo flexible para mujeres", "Dra. Rosa Suárez"),
            ("Día 2, 11:00", "De pregrado a investigadora: el camino real", "Panel investigadoras"),
            ("Día 2, 15:00", "Networking estructurado 1:1", "Todas las participantes"),
        ]
        for hora, titulo, speaker in conferencias:
            st.markdown(f"<div class='event-card'><div style='font-size:0.75rem;color:#9ca3af;'>{hora}</div><div style='font-weight:600;color:#4a1d96;font-size:0.9rem;'>{titulo}</div><div style='font-size:0.82rem;color:#6b7280;'>{speaker}</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Registrarme al Summit 2025**")
    col1, col2 = st.columns(2)
    with col1:
        nombre_ev = st.text_input("Nombre completo")
        email_ev = st.text_input("Correo electrónico")
    with col2:
        tipo_ev = st.selectbox("Asistir como", ["Profesional STEM", "Estudiante", "Empresa aliada", "Universidad / Centro de investigación"])
        interes_ev = st.multiselect("¿Qué te interesa más?", ["Networking empresas", "Conferencias", "Entrevistas exprés", "Talleres técnicos"])

    if st.button("Registrarme →", type="primary"):
        if nombre_ev and email_ev:
            st.success(f"✅ ¡{nombre_ev}, tu registro fue exitoso! Te enviaremos confirmación a {email_ev}")
        else:
            st.warning("Por favor completa tu nombre y correo.")


# ── MENTORÍAS ────────────────────────────────────────────────────────────────
elif "Mentor" in p:
    st.markdown("<div class='section-header'>📖 Mentorías e Historias</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Experiencias reales de mujeres que abrieron camino.</div>", unsafe_allow_html=True)

    historias = [
        {
            "titulo": "Cómo conseguí mi primer empleo en data siendo autodidacta",
            "autora": "María Fernanda Gómez",
            "area": "Ciencia de Datos",
            "resumen": "Nadie me contrató por mi título — me contrataron por mi portafolio en GitHub y la historia que supe contar sobre mis proyectos personales. Aquí te cuento todo el proceso.",
            "tags": ["Primer empleo", "Autodidacta", "Portafolio"],
            "lectura": "8 min"
        },
        {
            "titulo": "Mamá de dos y CTO: lo que nadie te dice",
            "autora": "Laura Pérez",
            "area": "Liderazgo",
            "resumen": "Llegar a CTO mientras criaba a dos hijos fue el reto más difícil y gratificante de mi vida. Hubo empresas que me cerraron puertas — y otras que me las abrieron. Esta es mi historia sin filtros.",
            "tags": ["Maternidad", "Liderazgo", "CTO"],
            "lectura": "12 min"
        },
        {
            "titulo": "Síndrome del impostor en ingeniería: guía de supervivencia",
            "autora": "Ing. Sofía Castro",
            "area": "Bienestar profesional",
            "resumen": "Años sintiéndome 'la que no debía estar ahí'. Te comparto las estrategias concretas que usé para construir confianza real — no solo aparentarla.",
            "tags": ["Síndrome impostor", "Confianza", "Mental health"],
            "lectura": "6 min"
        },
        {
            "titulo": "Migré a Alemania para trabajar en electrónica: todo lo que necesitas saber",
            "autora": "Valentina Ríos",
            "area": "Electrónica",
            "resumen": "Visa, salarios, cultura de trabajo, redes de apoyo. Lo que ojalá alguien me hubiera contado antes de subirme al avión.",
            "tags": ["Migración", "Europa", "Electrónica"],
            "lectura": "15 min"
        },
        {
            "titulo": "De pasante a investigadora senior en 4 años",
            "autora": "Dra. Ana Castillo",
            "area": "Investigación",
            "resumen": "La academia tiene sus laberintos. Te cuento cómo navegar publicaciones, becas, redes y la presión de publicar sin perder tu bienestar en el camino.",
            "tags": ["Academia", "Investigación", "Becas"],
            "lectura": "10 min"
        },
        {
            "titulo": "Trabajar 20 horas semanales y ganar más que antes trabajando 40",
            "autora": "Camila Moreno",
            "area": "Freelance STEM",
            "resumen": "Decidí que mi tiempo era mío. Armé mi portafolio, encontré clientes internacionales y rediseñé mi vida laboral completamente. Así lo hice.",
            "tags": ["Freelance", "Flexibilidad", "Salario"],
            "lectura": "9 min"
        },
    ]

    # Filter
    todas_areas = ["Todas"] + list(set(h["area"] for h in historias))
    area_sel = st.pills("Categorías", todas_areas, default="Todas")

    st.markdown("---")
    col1, col2 = st.columns(2)
    cols = [col1, col2]
    idx = 0
    for h in historias:
        if area_sel and area_sel != "Todas" and h["area"] != area_sel:
            continue
        tags_html = "".join(f"<span class='tag tag-pink'>{t}</span>" for t in h["tags"])
        with cols[idx % 2]:
            st.markdown(f"""
            <div class='story-card'>
                <div style='font-size:0.75rem;color:#9ca3af;'>{h['area']} · {h['lectura']} de lectura</div>
                <div style='font-weight:700;font-size:1rem;color:#1a1a2e;margin:4px 0;'>{h['titulo']}</div>
                <div style='font-size:0.82rem;color:#6b7280;font-weight:500;margin-bottom:6px;'>Por {h['autora']}</div>
                <div style='font-size:0.88rem;color:#374151;line-height:1.5;margin-bottom:8px;'>{h['resumen']}</div>
                {tags_html}
            </div>
            """, unsafe_allow_html=True)
        idx += 1

    st.markdown("---")
    st.markdown("**¿Quieres ser mentora?**")
    st.markdown("<div style='color:#6b7280;font-size:0.9rem;margin-bottom:1rem;'>Comparte tu historia y ayuda a otras mujeres STEM a encontrar su camino.</div>", unsafe_allow_html=True)
    nombre_m = st.text_input("Tu nombre")
    area_m = st.selectbox("Tu área", [
        "Ciencia de Datos & IA", "Ingeniería de Software", "Ingeniería Biomédica",
        "Electrónica & Telecomunicaciones", "Ingeniería Mecánica", "Ingeniería Química",
        "Ingeniería Ambiental", "Ingeniería Industrial", "Ciberseguridad",
        "Robótica & Automatización", "Astrofísica & Ciencias del Espacio",
        "Biotecnología", "Matemáticas & Estadística", "Física", "Química",
        "Neurociencias", "Investigación Científica", "Arquitectura de Software & DevOps",
        "Diseño UX/UI", "Emprendimiento Tecnológico", "Liderazgo", "Otro"
    ])
    historia_m = st.text_area("Cuéntanos tu historia en pocas palabras", height=80)
    if st.button("Postularme como mentora →", type="primary"):
        if nombre_m and historia_m:
            st.success(f"¡Gracias, {nombre_m}! Te contactaremos pronto para publicar tu historia. 💜")
        else:
            st.warning("Por favor completa nombre e historia.")
