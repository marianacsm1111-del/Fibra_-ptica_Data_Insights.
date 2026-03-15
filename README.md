# 🔷 DataInsight Pro — Proyecto Nacional de Fibra Óptica · Colombia

> Plataforma de análisis profesional construida con **Streamlit** para explorar, filtrar y visualizar el dataset del Proyecto Nacional de Fibra Óptica (PNFO) de Colombia, administrado por FONTIC / MinTIC.

---

## 📸 Vista General

La aplicación consta de dos módulos principales:

| Módulo | Descripción |
|---|---|
| 🏠 **Landing Page** | Hero section con estadísticas globales, descripción del dataset y guía de uso |
| 📊 **Workspace Analítico** | Panel interactivo con KPIs, 4 pestañas temáticas y explorador de datos |

---

## 🚀 Instalación y Ejecución

### 1. Clonar o descargar el proyecto

```bash
git clone https://github.com/tu-usuario/datainsight-pro.git
cd datainsight-pro
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS / Linux:
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Colocar el dataset

Asegúrate de que el archivo CSV esté en la raíz del proyecto con el nombre exacto:

```
Proyecto_Nacional_de_Fibra_Óptica_20260314.csv
```

### 5. Ejecutar la aplicación

```bash
streamlit run app.py
```

La app se abrirá automáticamente en `http://localhost:8501`

---

## 📁 Estructura del Proyecto

```
datainsight-pro/
│
├── app.py                                          # Aplicación principal Streamlit
├── requirements.txt                                # Dependencias Python
├── README.md                                       # Este archivo
└── Proyecto_Nacional_de_Fibra_Óptica_20260314.csv  # Dataset (debes colocarlo aquí)
```

---

## 📊 Sobre el Dataset

| Atributo | Detalle |
|---|---|
| **Fuente** | MinTIC · FONTIC · Datos Abiertos Colombia |
| **Período** | Enero 2013 – Julio 2023 |
| **Registros** | 788 municipios |
| **Cobertura** | 6 regiones · 27 departamentos · 729 municipios únicos |
| **Última actualización** | Octubre 2023 |

### Columnas principales

| Columna | Tipo | Descripción |
|---|---|---|
| `REGION` | Texto | 6 grandes regiones del país |
| `DEPARTAME_NOMBRE` | Texto | Nombre del departamento |
| `MUNICIPIO_NOMBRE` | Texto | Nombre del municipio |
| `FECHA OPERACION` | Fecha | Inicio del contrato de operación |
| `FECHA FIN OPERACION` | Fecha | Vencimiento del contrato |
| `ESTADO ACTUAL` | Texto | Estado del contrato (En Operación) |
| `INVERSION FONTIC` | Numérico | Aporte estatal FONTIC (COP) |
| `INVERSION CONTRAPARTIDA` | Numérico | Aporte del operador privado (COP) |
| `INVERSION TOTAL` | Numérico | Inversión total del proyecto (COP) |

---

## 🎨 Características de la App

### 🏠 Landing Page
- Hero section con estadísticas globales en tiempo real
- Tarjetas de características interactivas
- Esquema del dataset con descripción de columnas
- CTA para navegar al Workspace

### 📊 Workspace Analítico
- **KPIs dinámicos**: municipios, departamentos, inversión total, FONTIC y contrapartida
- **Filtros en sidebar**: región, departamento y rango de años de operación
- **Descarga CSV** de los datos filtrados

#### Pestañas del Workspace

**🗺 Cobertura Geográfica**
- Barras horizontales: municipios por región
- Heatmap: municipios por departamento × región
- Barras verticales: top 15 departamentos por cobertura

**💰 Análisis de Inversión**
- Barras agrupadas: FONTIC vs Contrapartida por región
- Donut chart: mix financiero público/privado global
- Top 15 departamentos por inversión total acumulada
- Histograma con KDE: distribución de inversión por municipio
- Boxplot: dispersión de inversión total por región
- Scatter plot: FONTIC vs Contrapartida por municipio

**📅 Evolución Temporal**
- Gráfico dual eje: proyectos iniciados (barras) + inversión total (línea)
- Área apilada: inversión acumulada por región y año
- Tabla resumen anual con métricas clave

**🔍 Explorador de Datos**
- Buscador por municipio o departamento
- Tabla interactiva ordenable con todas las columnas relevantes
- Estadísticas descriptivas completas (media, mediana, desviación, percentiles)

---

## 🎨 Paleta de Diseño

| Color | Uso |
|---|---|
| `#6366f1` Índigo 500 | Color principal, barras primarias |
| `#4f46e5` Índigo 600 | Botones, acentos fuertes |
| `#818cf8` Índigo 400 | Títulos hero, etiquetas |
| `#14b8a6` Teal | Contrapartida, líneas secundarias |
| `#f59e0b` Ámbar | Medianas en boxplots, highlights |
| `#0f172a` Slate 900 | Fondo principal |
| `#1e293b` Slate 800 | Cards y paneles |

---

## 🛠 Tecnologías Utilizadas

| Librería | Versión mínima | Uso |
|---|---|---|
| `streamlit` | 1.35.0 | Framework de la app |
| `pandas` | 2.0.0 | Procesamiento de datos |
| `numpy` | 1.25.0 | Cálculos numéricos |
| `seaborn` | 0.13.0 | Visualizaciones estadísticas |
| `matplotlib` | 3.8.0 | Gráficos base y composición |

---

## ⚙️ Notas Técnicas

- El dataset usa codificación **Latin-1**; la app lo decodifica automáticamente a UTF-8.
- Los valores de inversión se muestran en **millones de COP (M)** y **miles de millones (B)** para mejor legibilidad.
- El gráfico scatter usa una muestra aleatoria de 500 registros para optimizar el rendimiento.
- Todos los gráficos están optimizados con `@st.cache_data` para el dataset principal.
- La columna `INVERSION FONTIC` es constante ($552,241,234 COP) para todos los registros; la variabilidad de la inversión total proviene íntegramente de la contrapartida privada.

---

## 📄 Licencia

Este proyecto es de uso libre para fines educativos y de análisis. Los datos provienen de fuentes públicas del Gobierno de Colombia (datos.gov.co).

---

*Desarrollado con 🔷 DataInsight Pro · Powered by Streamlit*
