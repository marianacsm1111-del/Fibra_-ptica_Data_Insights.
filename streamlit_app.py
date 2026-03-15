import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DataInsight Pro · Fibra Óptica Colombia",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — Índigo + Slate palette
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ───────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root palette ───────────────────────── */
:root {
    --indigo-900: #1e1b4b;
    --indigo-800: #2e2a6b;
    --indigo-700: #3730a3;
    --indigo-600: #4f46e5;
    --indigo-500: #6366f1;
    --indigo-400: #818cf8;
    --indigo-300: #a5b4fc;
    --indigo-100: #e0e7ff;
    --slate-900:  #0f172a;
    --slate-800:  #1e293b;
    --slate-700:  #334155;
    --slate-600:  #475569;
    --slate-400:  #94a3b8;
    --slate-200:  #e2e8f0;
    --slate-100:  #f1f5f9;
    --white:      #ffffff;
    --accent-teal:#14b8a6;
    --accent-amber:#f59e0b;
}

/* ── Base ───────────────────────────────── */
html, body, [class*="css"]  {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--slate-900);
    color: var(--slate-200);
}

/* ── Hide Streamlit chrome ──────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0rem; padding-bottom: 2rem; }

/* ── Sidebar ────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--indigo-900) 0%, var(--slate-800) 100%);
    border-right: 1px solid var(--indigo-700);
}
section[data-testid="stSidebar"] * { color: var(--slate-200) !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label { color: var(--indigo-300) !important; font-weight: 600; font-size: 0.78rem; letter-spacing: 0.08em; text-transform: uppercase; }

/* ── Metric cards ───────────────────────── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, var(--indigo-900) 0%, var(--slate-800) 100%);
    border: 1px solid var(--indigo-700);
    border-radius: 12px;
    padding: 1rem 1.2rem;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] { color: var(--indigo-300) !important; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--white) !important; font-family: 'Syne', sans-serif; font-size: 1.8rem; }
[data-testid="metric-container"] [data-testid="stMetricDelta"] { color: var(--accent-teal) !important; }

/* ── Tabs ───────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: var(--slate-800);
    border-radius: 10px;
    padding: 4px;
    border-bottom: none;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: var(--slate-400);
    border-radius: 8px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 0.85rem;
    padding: 0.5rem 1.2rem;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: var(--indigo-600) !important;
    color: var(--white) !important;
}

/* ── Expanders ──────────────────────────── */
.streamlit-expanderHeader { color: var(--indigo-300) !important; font-size: 0.85rem; }
details { border: 1px solid var(--indigo-800) !important; border-radius: 8px !important; background: var(--slate-800) !important; }

/* ── Selectbox / Multiselect ────────────── */
.stSelectbox > div > div, .stMultiSelect > div > div {
    background: var(--slate-800) !important;
    border: 1px solid var(--indigo-700) !important;
    border-radius: 8px !important;
    color: var(--white) !important;
}

/* ── Section headers ────────────────────── */
.section-header {
    display: flex; align-items: center; gap: 10px;
    margin: 1.5rem 0 0.5rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--indigo-700);
}
.section-header h3 { font-family: 'Syne', sans-serif; font-size: 1.1rem; color: var(--white); margin: 0; }
.section-icon { font-size: 1.2rem; }

/* ── Info boxes ─────────────────────────── */
.info-box {
    background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(15,23,42,0.8) 100%);
    border-left: 3px solid var(--indigo-500);
    border-radius: 0 8px 8px 0;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0 1rem 0;
    font-size: 0.82rem;
    color: var(--slate-400);
    line-height: 1.5;
}
.info-box strong { color: var(--indigo-300); }

/* ── Hero landing ───────────────────────── */
.hero-wrap {
    background: linear-gradient(135deg, var(--indigo-900) 0%, var(--slate-900) 60%, #0d1117 100%);
    border: 1px solid var(--indigo-700);
    border-radius: 20px;
    padding: 3.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -80px; right: -80px;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(99,102,241,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title { font-family: 'Syne', sans-serif; font-size: 3rem; font-weight: 800; color: var(--white); line-height: 1.1; margin: 0 0 0.5rem 0; }
.hero-title span { color: var(--indigo-400); }
.hero-sub { font-size: 1.05rem; color: var(--slate-400); max-width: 580px; line-height: 1.6; margin: 0 0 2rem 0; }
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(99,102,241,0.2); border: 1px solid var(--indigo-600);
    border-radius: 20px; padding: 0.35rem 0.9rem;
    font-size: 0.78rem; color: var(--indigo-300); font-weight: 600;
    margin-right: 8px; margin-bottom: 8px;
}
.hero-stat { text-align: center; padding: 1rem; }
.hero-stat-value { font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 700; color: var(--indigo-400); }
.hero-stat-label { font-size: 0.75rem; color: var(--slate-400); text-transform: uppercase; letter-spacing: 0.07em; }

/* ── Feature cards ──────────────────────── */
.feature-card {
    background: var(--slate-800);
    border: 1px solid var(--slate-700);
    border-radius: 14px;
    padding: 1.4rem;
    text-align: center;
    transition: border-color 0.2s;
    height: 100%;
}
.feature-card:hover { border-color: var(--indigo-500); }
.feature-icon { font-size: 2rem; margin-bottom: 0.6rem; }
.feature-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.95rem; color: var(--white); margin-bottom: 0.4rem; }
.feature-desc { font-size: 0.8rem; color: var(--slate-400); line-height: 1.5; }

/* ── CTA button ─────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--indigo-600) 0%, var(--indigo-700) 100%);
    color: var(--white);
    border: none;
    border-radius: 10px;
    padding: 0.65rem 2rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.03em;
    transition: all 0.2s;
    box-shadow: 0 4px 20px rgba(99,102,241,0.3);
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--indigo-500) 0%, var(--indigo-600) 100%);
    transform: translateY(-1px);
    box-shadow: 0 6px 28px rgba(99,102,241,0.45);
}

/* ── Dataframe ──────────────────────────── */
.stDataFrame { border: 1px solid var(--indigo-800); border-radius: 10px; overflow: hidden; }

/* ── Divider ────────────────────────────── */
hr { border-color: var(--indigo-900) !important; }

/* ── Tooltip ────────────────────────────── */
.tooltip-tag {
    background: rgba(99,102,241,0.15); border: 1px solid var(--indigo-700);
    border-radius: 6px; padding: 0.15rem 0.5rem;
    font-size: 0.72rem; color: var(--indigo-300); font-weight: 600;
    cursor: help; margin-left: 6px; vertical-align: middle;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  DATA LOADER
# ─────────────────────────────────────────────
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="latin1")
    # Fix encoding for text columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].apply(
            lambda x: x.encode("latin1").decode("utf-8") if isinstance(x, str) else x
        )
    # Parse dates
    for col in ["FECHA OPERACION", "FECHA FIN OPERACION", "FEC CARGUE", "FECHA VIGENCIA"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    # Derived columns
    df["AÑO OPERACION"] = df["FECHA OPERACION"].dt.year
    df["INVERSION_FONTIC_M"] = df["INVERSION FONTIC"] / 1_000_000
    df["INVERSION_CONTRAP_M"] = df["INVERSION CONTRAPARTIDA"] / 1_000_000
    df["INVERSION_TOTAL_M"] = df["INVERSION TOTAL"] / 1_000_000
    df["PCT_FONTIC"] = (df["INVERSION FONTIC"] / df["INVERSION TOTAL"] * 100).round(1)
    df["PCT_CONTRAP"] = (df["INVERSION CONTRAPARTIDA"] / df["INVERSION TOTAL"] * 100).round(1)
    # Short region names
    region_map = {
        "Región Caribe":        "Caribe",
        "Región Centro Orient": "C. Oriente",
        "Región Eje Cafetero":  "Eje Cafetero",
        "Región Pacífico":      "Pacífico",
        "Región Centro Sur":    "C. Sur",
        "Región Llano":         "Llano",
    }
    df["REGION_CORTA"] = df["REGION"].map(region_map).fillna(df["REGION"])
    return df


# ─────────────────────────────────────────────
#  SEABORN / MATPLOTLIB STYLE
# ─────────────────────────────────────────────
INDIGO_PALETTE = ["#6366f1", "#818cf8", "#4f46e5", "#a5b4fc", "#3730a3", "#c7d2fe", "#14b8a6", "#f59e0b"]
BG_DARK   = "#0f172a"
BG_CARD   = "#1e293b"
BG_CARD2  = "#1a2236"
TEXT_MAIN = "#e2e8f0"
TEXT_SUB  = "#94a3b8"
GRID_CLR  = "#1e293b"

def apply_dark_style(fig: plt.Figure, ax=None):
    fig.patch.set_facecolor(BG_CARD)
    axes = [ax] if ax else fig.get_axes()
    for a in axes:
        a.set_facecolor(BG_CARD2)
        a.tick_params(colors=TEXT_SUB, labelsize=9)
        a.xaxis.label.set_color(TEXT_SUB)
        a.yaxis.label.set_color(TEXT_SUB)
        a.title.set_color(TEXT_MAIN)
        for spine in a.spines.values():
            spine.set_edgecolor(GRID_CLR)
        a.grid(color=GRID_CLR, linewidth=0.7, linestyle="--")
    return fig


def fmt_million(x, pos): return f"${x/1e3:.0f}B" if x >= 1000 else f"${x:.0f}M"


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar(df: pd.DataFrame):
    with st.sidebar:
        st.markdown("""
        <div style="padding: 1rem 0 1.2rem 0; border-bottom: 1px solid #3730a3;">
            <div style="font-family:'Syne',sans-serif; font-size:1.3rem; font-weight:800; color:#e0e7ff; letter-spacing:-0.02em;">
                🔷 DataInsight Pro
            </div>
            <div style="font-size:0.72rem; color:#6366f1; text-transform:uppercase; letter-spacing:0.12em; margin-top:3px;">
                Fibra Óptica · Colombia
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**🗂 Navegación**")
        page = st.radio(
            "Página",
            ["🏠 Landing", "📊 Workspace Analítico"],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**🔽 Filtros Globales**")
        st.caption("Aplican en el Workspace")

        regiones = sorted(df["REGION_CORTA"].dropna().unique())
        sel_reg = st.multiselect("Región", regiones, default=regiones, key="f_region")

        deptos = sorted(df[df["REGION_CORTA"].isin(sel_reg)]["DEPARTAME_NOMBRE"].dropna().unique())
        sel_dep = st.multiselect("Departamento", deptos, default=deptos, key="f_depto")

        años = sorted(df["AÑO OPERACION"].dropna().unique().astype(int))
        sel_año = st.select_slider(
            "Año inicio operación",
            options=años,
            value=(int(min(años)), int(max(años))),
            key="f_año",
        )

        st.markdown("---")
        st.markdown("**📥 Datos**")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Descargar CSV filtrado", csv, "fibra_optica_filtrado.csv", "text/csv")

        total_mun = len(df[
            df["REGION_CORTA"].isin(sel_reg) &
            df["DEPARTAME_NOMBRE"].isin(sel_dep) &
            df["AÑO OPERACION"].between(sel_año[0], sel_año[1])
        ])
        st.markdown(f"""
        <div style="background:rgba(99,102,241,0.12); border:1px solid #3730a3; border-radius:8px; padding:0.6rem; margin-top:0.5rem; text-align:center;">
            <div style="font-size:0.7rem; color:#818cf8; text-transform:uppercase; letter-spacing:0.08em;">Registros visibles</div>
            <div style="font-family:'Syne',sans-serif; font-size:1.6rem; font-weight:700; color:#e0e7ff;">{total_mun:,}</div>
        </div>
        """, unsafe_allow_html=True)

    return page, sel_reg, sel_dep, sel_año


# ─────────────────────────────────────────────
#  LANDING PAGE
# ─────────────────────────────────────────────
def render_landing(df: pd.DataFrame):
    st.markdown(f"""
    <div class="hero-wrap">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:1rem;">
            <span class="hero-badge">🔷 DataInsight Pro</span>
            <span class="hero-badge">🇨🇴 Colombia</span>
            <span class="hero-badge">🗓 2013 – 2023</span>
        </div>
        <p class="hero-title">Proyecto Nacional de<br><span>Fibra Óptica</span></p>
        <p class="hero-sub">
            Plataforma de análisis profesional para explorar la inversión, cobertura y despliegue
            de infraestructura de conectividad digital en Colombia — impulsada por FONTIC.
        </p>
        <div style="display:flex; gap:2.5rem; margin-top:2rem; flex-wrap:wrap;">
            <div class="hero-stat">
                <div class="hero-stat-value">{df['MUNICIPIO_NOMBRE'].nunique():,}</div>
                <div class="hero-stat-label">Municipios cubiertos</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value">{df['DEPARTAME_NOMBRE'].nunique()}</div>
                <div class="hero-stat-label">Departamentos</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value">6</div>
                <div class="hero-stat-label">Regiones</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value">${df['INVERSION_TOTAL_M'].sum()/1000:.1f}B</div>
                <div class="hero-stat-label">Inversión total (COP)</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Features
    st.markdown("""
    <div style="font-family:'Syne',sans-serif; font-size:1.4rem; font-weight:700; color:#e0e7ff; margin-bottom:1rem;">
        ¿Qué puedes explorar?
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    features = [
        ("📍", "Cobertura Geográfica", "Distribución de municipios por región y departamento con métricas de densidad."),
        ("💰", "Análisis de Inversión", "Comparativa FONTIC vs. contrapartida privada, rangos y eficiencia del gasto."),
        ("📅", "Evolución Temporal", "Tendencias anuales de proyectos iniciados y acumulado de inversión 2013–2023."),
        ("🔍", "Explorador de Datos", "Filtros interactivos, tabla detallada y exportación del conjunto de datos."),
    ]
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Dataset overview
    st.markdown("""
    <div class="section-header">
        <span class="section-icon">📋</span>
        <h3>Sobre el Dataset</h3>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("""
        <div class="info-box">
            <strong>Fuente:</strong> Ministerio de Tecnologías de la Información y las Comunicaciones (MinTIC) · FONTIC<br><br>
            <strong>Descripción:</strong> Registros del Proyecto Nacional de Fibra Óptica que documenta los contratos de operación
            de infraestructura de conectividad en municipios colombianos, incluyendo inversión pública y contrapartida privada.<br><br>
            <strong>Período:</strong> Enero 2013 – Julio 2023 · <strong>Última actualización:</strong> Octubre 2023
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-box">
            <strong>Columnas clave:</strong><br>
            · <strong>REGION / DEPARTAMENTO / MUNICIPIO</strong> — Jerarquía geográfica<br>
            · <strong>FECHA OPERACION</strong> — Inicio del contrato de operación<br>
            · <strong>INVERSION FONTIC</strong> — Aporte estatal (COP)<br>
            · <strong>INVERSION CONTRAPARTIDA</strong> — Aporte operador privado (COP)<br>
            · <strong>INVERSION TOTAL</strong> — Suma del proyecto por municipio (COP)
        </div>
        """, unsafe_allow_html=True)

    with c2:
        # Quick schema table
        schema = pd.DataFrame({
            "Columna": ["REGION", "DEPARTAME_NOMBRE", "MUNICIPIO_NOMBRE", "FECHA OPERACION",
                        "INVERSION FONTIC", "INVERSION CONTRAPARTIDA", "INVERSION TOTAL", "ESTADO ACTUAL"],
            "Tipo": ["Texto", "Texto", "Texto", "Fecha", "Numérico", "Numérico", "Numérico", "Texto"],
            "Descripción": [
                "6 grandes regiones del país",
                "27 departamentos con cobertura",
                "729 municipios únicos",
                "Fecha inicio operación",
                "Inversión FONTIC (COP)",
                "Aporte contrapartida (COP)",
                "Inversión total del proyecto",
                "Estado del contrato",
            ],
        })
        st.dataframe(schema, use_container_width=True, hide_index=True, height=290)

    st.markdown("<br>", unsafe_allow_html=True)

    # CTA
    st.markdown("""
    <div style="text-align:center; padding:2rem; background:linear-gradient(135deg,rgba(79,70,229,0.15),rgba(15,23,42,0.8));
                border:1px solid #3730a3; border-radius:16px;">
        <div style="font-family:'Syne',sans-serif; font-size:1.5rem; font-weight:700; color:#e0e7ff; margin-bottom:0.5rem;">
            Listo para analizar
        </div>
        <div style="color:#94a3b8; margin-bottom:1.2rem; font-size:0.9rem;">
            Navega al <strong style="color:#818cf8;">📊 Workspace Analítico</strong> desde el menú lateral para explorar los gráficos y filtros.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  WORKSPACE — KPI ROW
# ─────────────────────────────────────────────
def render_kpis(dff: pd.DataFrame):
    c1, c2, c3, c4, c5 = st.columns(5)
    inv_total = dff["INVERSION TOTAL"].sum()
    inv_fontic = dff["INVERSION FONTIC"].sum()
    inv_contra = dff["INVERSION CONTRAPARTIDA"].sum()
    avg_total = dff["INVERSION_TOTAL_M"].mean()
    pct_fontic = inv_fontic / inv_total * 100 if inv_total else 0

    c1.metric("🏙 Municipios", f"{dff['MUNICIPIO_NOMBRE'].nunique():,}", help="Municipios únicos en la selección")
    c2.metric("🏛 Departamentos", f"{dff['DEPARTAME_NOMBRE'].nunique():,}")
    c3.metric("💰 Inversión Total", f"${inv_total/1e9:.2f}B COP", help="Suma inversión total (Miles de millones COP)")
    c4.metric("🏦 Aporte FONTIC", f"${inv_fontic/1e9:.2f}B COP", f"{pct_fontic:.1f}% del total")
    c5.metric("🤝 Contrapartida", f"${inv_contra/1e9:.2f}B COP", f"Prom/Mun: ${avg_total:.0f}M")


# ─────────────────────────────────────────────
#  CHART: Municipios por Región (barras horizontales)
# ─────────────────────────────────────────────
def chart_municipios_region(dff: pd.DataFrame):
    data = dff.groupby("REGION_CORTA")["MUNICIPIO_NOMBRE"].nunique().sort_values()
    fig, ax = plt.subplots(figsize=(6, 3.6))
    colors = [INDIGO_PALETTE[i % len(INDIGO_PALETTE)] for i in range(len(data))]
    bars = ax.barh(data.index, data.values, color=colors, edgecolor="none", height=0.6)
    for bar, val in zip(bars, data.values):
        ax.text(val + 1, bar.get_y() + bar.get_height() / 2,
                f"{val}", va="center", ha="left", color=TEXT_MAIN, fontsize=8, fontweight="600")
    ax.set_xlabel("Municipios", fontsize=8)
    ax.set_title("Municipios por Región", fontsize=10, fontweight="bold", pad=10)
    ax.set_xlim(0, data.max() * 1.18)
    apply_dark_style(fig, ax)
    return fig


# ─────────────────────────────────────────────
#  CHART: Inversión Total por Región (barras agrupadas FONTIC+Contrapartida)
# ─────────────────────────────────────────────
def chart_inversion_region(dff: pd.DataFrame):
    grp = dff.groupby("REGION_CORTA").agg(
        fontic=("INVERSION_FONTIC_M", "sum"),
        contra=("INVERSION_CONTRAP_M", "sum"),
    ).sort_values("fontic", ascending=False)

    x = np.arange(len(grp))
    w = 0.38
    fig, ax = plt.subplots(figsize=(7, 4))
    b1 = ax.bar(x - w / 2, grp["fontic"], w, label="FONTIC", color=INDIGO_PALETTE[0], edgecolor="none")
    b2 = ax.bar(x + w / 2, grp["contra"], w, label="Contrapartida", color=INDIGO_PALETTE[6], edgecolor="none")
    ax.set_xticks(x)
    ax.set_xticklabels(grp.index, rotation=25, ha="right", fontsize=8)
    ax.set_ylabel("Millones COP", fontsize=8)
    ax.set_title("Inversión por Región · FONTIC vs Contrapartida", fontsize=10, fontweight="bold", pad=10)
    ax.legend(fontsize=8, framealpha=0, labelcolor=TEXT_SUB)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_million))
    apply_dark_style(fig, ax)
    return fig


# ─────────────────────────────────────────────
#  CHART: Top 15 Departamentos por Inversión Total
# ─────────────────────────────────────────────
def chart_top_deptos(dff: pd.DataFrame):
    top = (dff.groupby("DEPARTAME_NOMBRE")["INVERSION_TOTAL_M"]
           .sum().sort_values(ascending=False).head(15))
    fig, ax = plt.subplots(figsize=(6, 5))
    palette = sns.color_palette([INDIGO_PALETTE[0], INDIGO_PALETTE[1]], n_colors=15)
    sns.barplot(x=top.values, y=top.index, palette=palette, ax=ax, edgecolor="none")
    for bar, val in zip(ax.patches, top.values):
        ax.text(val + top.max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f"${val/1000:.1f}B", va="center", fontsize=7.5, color=TEXT_MAIN)
    ax.set_xlabel("Inversión Total (M COP)", fontsize=8)
    ax.set_ylabel("")
    ax.set_title("Top 15 Departamentos · Inversión Total", fontsize=10, fontweight="bold", pad=10)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_million))
    apply_dark_style(fig, ax)
    return fig


# ─────────────────────────────────────────────
#  CHART: Evolución temporal (proyectos iniciados por año)
# ─────────────────────────────────────────────
def chart_evolucion_temporal(dff: pd.DataFrame):
    anual = dff.groupby("AÑO OPERACION").agg(
        proyectos=("MUNICIPIO_NOMBRE", "count"),
        inversion=("INVERSION_TOTAL_M", "sum"),
    ).reset_index().dropna()

    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax2 = ax1.twinx()

    # Barras proyectos
    ax1.bar(anual["AÑO OPERACION"], anual["proyectos"],
            color=INDIGO_PALETTE[0], alpha=0.7, edgecolor="none", label="Proyectos iniciados", zorder=2)
    # Línea inversión
    ax2.plot(anual["AÑO OPERACION"], anual["inversion"],
             color=INDIGO_PALETTE[6], lw=2.5, marker="o", markersize=5, label="Inversión Total (M)", zorder=3)
    ax2.fill_between(anual["AÑO OPERACION"], anual["inversion"], alpha=0.12, color=INDIGO_PALETTE[6])

    ax1.set_xlabel("Año", fontsize=8)
    ax1.set_ylabel("Proyectos iniciados", fontsize=8, color=INDIGO_PALETTE[1])
    ax2.set_ylabel("Inversión Total (M COP)", fontsize=8, color=INDIGO_PALETTE[6])
    ax1.set_title("Evolución Temporal · Proyectos e Inversión por Año", fontsize=10, fontweight="bold", pad=10)
    ax1.tick_params(axis="y", colors=INDIGO_PALETTE[1])
    ax2.tick_params(axis="y", colors=INDIGO_PALETTE[6])
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_million))

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=8, framealpha=0, labelcolor=TEXT_MAIN, loc="upper right")

    apply_dark_style(fig, ax1)
    ax2.set_facecolor(BG_CARD2)
    ax2.tick_params(colors=TEXT_SUB, labelsize=9)
    for spine in ax2.spines.values():
        spine.set_edgecolor(GRID_CLR)
    fig.patch.set_facecolor(BG_CARD)
    return fig


# ─────────────────────────────────────────────
#  CHART: Distribución % FONTIC vs Contrapartida (pie / donut por región)
# ─────────────────────────────────────────────
def chart_donut_mix(dff: pd.DataFrame):
    total_fontic = dff["INVERSION FONTIC"].sum()
    total_contra = dff["INVERSION CONTRAPARTIDA"].sum()
    sizes = [total_fontic, total_contra]
    labels = ["FONTIC\n(Público)", "Contrapartida\n(Privado)"]
    colors = [INDIGO_PALETTE[0], INDIGO_PALETTE[6]]

    fig, ax = plt.subplots(figsize=(4, 4))
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors,
        autopct="%1.1f%%", startangle=90,
        pctdistance=0.75, wedgeprops=dict(width=0.55, edgecolor=BG_CARD, linewidth=2),
    )
    for t in texts:
        t.set_color(TEXT_MAIN); t.set_fontsize(8)
    for at in autotexts:
        at.set_color(BG_DARK); at.set_fontsize(8); at.set_fontweight("bold")
    ax.set_title("Mix Financiero\n(Global)", fontsize=9, fontweight="bold", color=TEXT_MAIN)
    fig.patch.set_facecolor(BG_CARD)
    ax.set_facecolor(BG_CARD)
    return fig


# ─────────────────────────────────────────────
#  CHART: Heatmap Departamento × Región (conteo municipios)
# ─────────────────────────────────────────────
def chart_heatmap_depto_region(dff: pd.DataFrame):
    pivot = dff.pivot_table(
        index="DEPARTAME_NOMBRE", columns="REGION_CORTA",
        values="MUNICIPIO_NOMBRE", aggfunc="count", fill_value=0,
    )
    # Limitar a top 20 departamentos
    top20 = dff["DEPARTAME_NOMBRE"].value_counts().head(20).index
    pivot = pivot.loc[pivot.index.isin(top20)]

    fig, ax = plt.subplots(figsize=(7, 6))
    cmap = sns.color_palette("mako", as_cmap=True)
    sns.heatmap(
        pivot, annot=True, fmt="d", cmap=cmap, ax=ax,
        linewidths=0.4, linecolor=BG_DARK,
        cbar_kws={"shrink": 0.6},
        annot_kws={"size": 7, "color": TEXT_MAIN},
    )
    ax.set_title("Municipios por Departamento y Región (Top 20 Depts)", fontsize=9, fontweight="bold", pad=10)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(labelsize=7.5, colors=TEXT_SUB)
    fig.patch.set_facecolor(BG_CARD)
    ax.set_facecolor(BG_CARD2)
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(colors=TEXT_SUB, labelsize=7)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    return fig


# ─────────────────────────────────────────────
#  CHART: Boxplot inversión total por región
# ─────────────────────────────────────────────
def chart_boxplot_region(dff: pd.DataFrame):
    order = dff.groupby("REGION_CORTA")["INVERSION_TOTAL_M"].median().sort_values(ascending=False).index
    fig, ax = plt.subplots(figsize=(7, 4))
    palette_box = {r: INDIGO_PALETTE[i % len(INDIGO_PALETTE)] for i, r in enumerate(order)}
    sns.boxplot(
        data=dff, x="REGION_CORTA", y="INVERSION_TOTAL_M",
        order=order, palette=palette_box, ax=ax,
        linewidth=0.9, flierprops=dict(marker="o", color=INDIGO_PALETTE[3], markersize=3, alpha=0.5),
        medianprops=dict(color="#f59e0b", linewidth=2),
    )
    ax.set_xlabel("Región", fontsize=8)
    ax.set_ylabel("Inversión Total (M COP)", fontsize=8)
    ax.set_title("Distribución de Inversión Total por Región", fontsize=10, fontweight="bold", pad=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_million))
    plt.xticks(rotation=20, ha="right")
    apply_dark_style(fig, ax)
    return fig


# ─────────────────────────────────────────────
#  CHART: Scatter inversión FONTIC vs Contrapartida
# ─────────────────────────────────────────────
def chart_scatter_inversiones(dff: pd.DataFrame):
    sample = dff.sample(min(len(dff), 500), random_state=42)
    region_colors = {r: INDIGO_PALETTE[i % len(INDIGO_PALETTE)] for i, r in enumerate(sample["REGION_CORTA"].unique())}
    fig, ax = plt.subplots(figsize=(6, 4))
    for reg, grp in sample.groupby("REGION_CORTA"):
        ax.scatter(
            grp["INVERSION_FONTIC_M"], grp["INVERSION_CONTRAP_M"],
            color=region_colors.get(reg, INDIGO_PALETTE[0]),
            alpha=0.65, s=25, edgecolors="none", label=reg,
        )
    ax.set_xlabel("Inversión FONTIC (M COP)", fontsize=8)
    ax.set_ylabel("Inversión Contrapartida (M COP)", fontsize=8)
    ax.set_title("FONTIC vs Contrapartida por Municipio", fontsize=10, fontweight="bold", pad=10)
    ax.legend(fontsize=7, framealpha=0, labelcolor=TEXT_MAIN, loc="upper left")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_million))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_million))
    apply_dark_style(fig, ax)
    return fig


# ─────────────────────────────────────────────
#  CHART: Histograma inversión total
# ─────────────────────────────────────────────
def chart_hist_inversion(dff: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 3.8))
    sns.histplot(dff["INVERSION_TOTAL_M"], bins=30, color=INDIGO_PALETTE[0],
                 ax=ax, edgecolor="none", alpha=0.85, kde=True,
                 line_kws={"color": INDIGO_PALETTE[6], "lw": 2})
    ax.set_xlabel("Inversión Total (M COP)", fontsize=8)
    ax.set_ylabel("Frecuencia", fontsize=8)
    ax.set_title("Distribución de Inversión Total por Municipio", fontsize=10, fontweight="bold", pad=10)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_million))
    apply_dark_style(fig, ax)
    return fig


# ─────────────────────────────────────────────
#  WORKSPACE PAGE
# ─────────────────────────────────────────────
def render_workspace(df: pd.DataFrame, sel_reg, sel_dep, sel_año):
    dff = df[
        df["REGION_CORTA"].isin(sel_reg) &
        df["DEPARTAME_NOMBRE"].isin(sel_dep) &
        df["AÑO OPERACION"].between(sel_año[0], sel_año[1])
    ].copy()

    st.markdown("""
    <div style="font-family:'Syne',sans-serif; font-size:1.7rem; font-weight:800; color:#e0e7ff;
                border-left:4px solid #6366f1; padding-left:14px; margin-bottom:1.2rem;">
        📊 Workspace Analítico
        <span style="font-size:0.85rem; font-weight:400; color:#6366f1; margin-left:12px;">
            Proyecto Nacional de Fibra Óptica · Colombia
        </span>
    </div>
    """, unsafe_allow_html=True)

    if dff.empty:
        st.warning("⚠️ No hay datos con los filtros seleccionados. Ajusta los filtros en el panel lateral.")
        return

    # ── KPIs ────────────────────────────────
    render_kpis(dff)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── TABS ────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺 Cobertura Geográfica",
        "💰 Análisis de Inversión",
        "📅 Evolución Temporal",
        "🔍 Explorador de Datos",
    ])

    # ════════════════════════════════════════
    #  TAB 1 — COBERTURA
    # ════════════════════════════════════════
    with tab1:
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📍</span>
            <h3>Distribución Geográfica de Municipios</h3>
        </div>
        <div class="info-box">
            <strong>ℹ️ Contexto:</strong> El PNFO cubre municipios en <strong>6 regiones</strong> del país,
            priorizando zonas sin conectividad previa. La Región Centro Oriente concentra el mayor número de municipios
            debido a la alta densidad poblacional de Boyacá y Cundinamarca.
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([1, 1])
        with c1:
            fig = chart_municipios_region(dff)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        with c2:
            fig = chart_heatmap_depto_region(dff)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown("""
        <div class="section-header" style="margin-top:1.5rem;">
            <span class="section-icon">🏆</span>
            <h3>Top 15 Departamentos por Municipios Cubiertos</h3>
        </div>
        <div class="info-box">
            <strong>ℹ️ Lectura:</strong> Boyacá lidera en número de municipios gracias a su alta fragmentación
            territorial (123 municipios en total). La cobertura refleja la estrategia de alcanzar municipios
            apartados con baja conectividad preexistente.
        </div>
        """, unsafe_allow_html=True)

        top_dep = (dff.groupby("DEPARTAME_NOMBRE")["MUNICIPIO_NOMBRE"]
                   .nunique().sort_values(ascending=False).head(15))
        fig2, ax2 = plt.subplots(figsize=(10, 3.5))
        colors = sns.color_palette([INDIGO_PALETTE[0], INDIGO_PALETTE[1]], n_colors=15)
        sns.barplot(x=top_dep.index, y=top_dep.values, palette=colors, ax=ax2, edgecolor="none")
        for bar, val in zip(ax2.patches, top_dep.values):
            ax2.text(bar.get_x() + bar.get_width() / 2, val + 0.3,
                     str(val), ha="center", fontsize=8, color=TEXT_MAIN, fontweight="600")
        ax2.set_xlabel("")
        ax2.set_ylabel("Municipios", fontsize=8)
        ax2.set_title("", fontsize=9)
        plt.xticks(rotation=30, ha="right", fontsize=8)
        apply_dark_style(fig2, ax2)
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)

    # ════════════════════════════════════════
    #  TAB 2 — INVERSIÓN
    # ════════════════════════════════════════
    with tab2:
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">💰</span>
            <h3>Estructura y Distribución de la Inversión</h3>
        </div>
        <div class="info-box">
            <strong>ℹ️ Contexto:</strong> La inversión se compone de dos fuentes:
            <strong>FONTIC</strong> (fondo estatal, constante en ~$552M COP por municipio) y la
            <strong>contrapartida del operador privado</strong> (variable, refleja costos reales de despliegue).
            La varianza en inversión total es explicada enteramente por la contrapartida.
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([3, 2])
        with c1:
            fig = chart_inversion_region(dff)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        with c2:
            fig = chart_donut_mix(dff)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown("<br>", unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3:
            st.markdown("""
            <div class="section-header">
                <span class="section-icon">📦</span>
                <h3>Top 15 Deptos · Inversión Total</h3>
            </div>
            <div class="info-box">
                <strong>ℹ️</strong> Boyacá y Cundinamarca lideran por número de municipios,
                no por inversión per cápita. La inversión total acumulada refleja cobertura, no intensidad.
            </div>
            """, unsafe_allow_html=True)
            fig = chart_top_deptos(dff)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        with c4:
            st.markdown("""
            <div class="section-header">
                <span class="section-icon">🔬</span>
                <h3>Distribución por Municipio</h3>
            </div>
            <div class="info-box">
                <strong>ℹ️</strong> La distribución unimodal con cola derecha indica que la mayoría
                de municipios recibe inversiones similares, con algunos outliers de alta inversión
                en municipios más remotos.
            </div>
            """, unsafe_allow_html=True)
            fig = chart_hist_inversion(dff)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📐</span>
            <h3>Boxplot · Dispersión por Región</h3>
        </div>
        <div class="info-box">
            <strong>ℹ️</strong> La línea naranja marca la mediana. Las cajas muestran el rango intercuartil (IQR).
            Los puntos fuera de las cajas son municipios con inversiones atípicamente altas o bajas,
            generalmente asociados a distancia geográfica extrema.
        </div>
        """, unsafe_allow_html=True)
        fig = chart_boxplot_region(dff)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown("""
        <div class="section-header">
            <span class="section-icon">🔗</span>
            <h3>Correlación FONTIC vs Contrapartida</h3>
        </div>
        <div class="info-box">
            <strong>ℹ️</strong> La aportación FONTIC es fija ($552M COP) para todos los municipios,
            por lo que la variabilidad en el eje X es mínima. La dispersión vertical refleja que el operador
            privado ajusta su contrapartida según los costos reales de cada municipio.
        </div>
        """, unsafe_allow_html=True)
        fig = chart_scatter_inversiones(dff)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    # ════════════════════════════════════════
    #  TAB 3 — TEMPORAL
    # ════════════════════════════════════════
    with tab3:
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📅</span>
            <h3>Evolución Temporal del Proyecto</h3>
        </div>
        <div class="info-box">
            <strong>ℹ️ Contexto:</strong> El PNFO inició en 2013 con las primeras operaciones.
            Los picos de actividad reflejan convocatorias masivas de contratos. Los años con más proyectos
            iniciados coinciden con las fases de expansión del programa hacia zonas rurales.
        </div>
        """, unsafe_allow_html=True)

        fig = chart_evolucion_temporal(dff)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown("<br>", unsafe_allow_html=True)

        # Acumulado
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📈</span>
            <h3>Inversión Acumulada por Región y Año</h3>
        </div>
        <div class="info-box">
            <strong>ℹ️</strong> Área apilada del total acumulado de inversión por región.
            Permite identificar qué regiones concentraron desembolsos en cada período.
        </div>
        """, unsafe_allow_html=True)

        pivot_time = dff.groupby(["AÑO OPERACION", "REGION_CORTA"])["INVERSION_TOTAL_M"].sum().unstack(fill_value=0)
        pivot_time = pivot_time.cumsum()

        fig2, ax2 = plt.subplots(figsize=(10, 4.5))
        colors_stack = INDIGO_PALETTE[:len(pivot_time.columns)]
        ax2.stackplot(pivot_time.index, pivot_time.T.values, labels=pivot_time.columns,
                      colors=colors_stack, alpha=0.82)
        ax2.legend(loc="upper left", fontsize=8, framealpha=0, labelcolor=TEXT_MAIN)
        ax2.set_xlabel("Año", fontsize=8)
        ax2.set_ylabel("Inversión Acumulada (M COP)", fontsize=8)
        ax2.set_title("Inversión Acumulada por Región", fontsize=10, fontweight="bold", pad=10)
        ax2.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_million))
        apply_dark_style(fig2, ax2)
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)

        # Tabla resumen anual
        st.markdown("""
        <div class="section-header" style="margin-top:1rem;">
            <span class="section-icon">📋</span>
            <h3>Resumen Anual</h3>
        </div>
        """, unsafe_allow_html=True)
        anual_tab = dff.groupby("AÑO OPERACION").agg(
            Proyectos=("MUNICIPIO_NOMBRE", "count"),
            Inv_Total_M=("INVERSION_TOTAL_M", "sum"),
            Inv_FONTIC_M=("INVERSION_FONTIC_M", "sum"),
            Inv_Contra_M=("INVERSION_CONTRAP_M", "sum"),
            Prom_Municipal_M=("INVERSION_TOTAL_M", "mean"),
        ).reset_index()
        anual_tab.columns = ["Año", "Proyectos", "Inv. Total (M)", "FONTIC (M)", "Contrapartida (M)", "Promedio/Mun (M)"]
        for col in ["Inv. Total (M)", "FONTIC (M)", "Contrapartida (M)", "Promedio/Mun (M)"]:
            anual_tab[col] = anual_tab[col].apply(lambda x: f"${x:,.0f}M")
        st.dataframe(anual_tab, use_container_width=True, hide_index=True)

    # ════════════════════════════════════════
    #  TAB 4 — EXPLORADOR
    # ════════════════════════════════════════
    with tab4:
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">🔍</span>
            <h3>Explorador de Registros</h3>
        </div>
        <div class="info-box">
            <strong>ℹ️</strong> Tabla interactiva con todos los registros filtrados. Puedes ordenar por cualquier columna
            haciendo clic en el encabezado. Usa el botón <strong>Descargar CSV</strong> en la barra lateral para exportar.
        </div>
        """, unsafe_allow_html=True)

        # Sub-filtro texto
        search = st.text_input("🔎 Buscar municipio o departamento", "", placeholder="Ej: BOGOTA, BOYACA...")
        if search:
            mask = (
                dff["MUNICIPIO_NOMBRE"].str.upper().str.contains(search.upper()) |
                dff["DEPARTAME_NOMBRE"].str.upper().str.contains(search.upper())
            )
            dff_show = dff[mask]
        else:
            dff_show = dff

        st.caption(f"Mostrando **{len(dff_show):,}** registros")

        cols_show = ["REGION_CORTA", "DEPARTAME_NOMBRE", "MUNICIPIO_NOMBRE",
                     "AÑO OPERACION", "INVERSION_FONTIC_M", "INVERSION_CONTRAP_M",
                     "INVERSION_TOTAL_M", "PCT_FONTIC", "PCT_CONTRAP"]
        rename_map = {
            "REGION_CORTA": "Región", "DEPARTAME_NOMBRE": "Departamento",
            "MUNICIPIO_NOMBRE": "Municipio", "AÑO OPERACION": "Año Op.",
            "INVERSION_FONTIC_M": "FONTIC (M)", "INVERSION_CONTRAP_M": "Contrapartida (M)",
            "INVERSION_TOTAL_M": "Inv. Total (M)", "PCT_FONTIC": "% FONTIC", "PCT_CONTRAP": "% Contra",
        }
        st.dataframe(
            dff_show[cols_show].rename(columns=rename_map).reset_index(drop=True),
            use_container_width=True,
            height=440,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📊</span>
            <h3>Estadísticas Descriptivas</h3>
        </div>
        """, unsafe_allow_html=True)
        desc = dff[["INVERSION_FONTIC_M", "INVERSION_CONTRAP_M", "INVERSION_TOTAL_M"]].describe().round(2)
        desc.columns = ["FONTIC (M COP)", "Contrapartida (M COP)", "Total (M COP)"]
        st.dataframe(desc, use_container_width=True)


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    DATA_PATH = "Proyecto_Nacional_de_Fibra_Óptica_20260314.csv"
    df = load_data(DATA_PATH)
    page, sel_reg, sel_dep, sel_año = render_sidebar(df)

    if "Landing" in page:
        render_landing(df)
    else:
        render_workspace(df, sel_reg, sel_dep, sel_año)


if __name__ == "__main__":
    main()