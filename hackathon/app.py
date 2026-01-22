import streamlit as st
import json
import pandas as pd
import plotly.express as px
import random

from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Bhu-Smruti: Soil Wisdom Memory Bank",
    page_icon="🌱",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #2E7D32;
    text-align: center;
}
.sub-header {
    color: #388E3C;
    font-size: 1.5rem;
}
.soil-card {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 10px;
    border-left: 5px solid #8BC34A;
}
.wisdom-card {
    background: #FFF3E0;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 10px;
    border-left: 5px solid #FF9800;
}
.info-box {
    background: #E3F2FD;
    padding: 1rem;
    border-radius: 8px;
    border-left: 5px solid #2196F3;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE INIT ----------------
if "simulation_mode" not in st.session_state:
    st.session_state.simulation_mode = True

if "soil_data" not in st.session_state:
    with open("data/soil_samples.json", "r") as f:
        st.session_state.soil_data = json.load(f)

if "wisdom_data" not in st.session_state:
    with open("data/wisdom_audio.json", "r") as f:
        st.session_state.wisdom_data = json.load(f)

# ---------------- TITLE ----------------
st.markdown('<h1 class="main-header">🌱 Bhu-Smruti: Soil Wisdom Memory Bank</h1>', unsafe_allow_html=True)
st.markdown("<center>Preserving Indigenous Farming Knowledge with AI</center>", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🌾 Navigation")
    app_mode = st.selectbox(
        "Select Mode",
        [
            "🏠 Dashboard",
            "🔍 Soil Search",
            "👴 Wisdom Search",
            "📊 Analytics",
            "🔄 Memory Reinforcement",
            "📚 About"
        ]
    )

    st.markdown("---")
    st.metric("Soil Samples", len(st.session_state.soil_data))
    st.metric("Wisdom Snippets", len(st.session_state.wisdom_data))

# ---------------- DASHBOARD ----------------
if app_mode == "🏠 Dashboard":
    st.markdown('<h2 class="sub-header">Welcome</h2>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    <b>Bhu-Smruti (भू-स्मृति)</b> means "Earth Memory".
    This system stores soil conditions and indigenous farming wisdom
    and retrieves the best practices using AI-powered similarity search.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🌟 Key Features")
    st.write("""
    - 🔍 Semantic Soil Search  
    - 👴 Indigenous Wisdom Retrieval  
    - 💡 Smart Recommendations  
    - 🔄 Learning from farmer feedback  
    - 📊 Data-driven insights  
    """)

# ---------------- SOIL SEARCH ----------------
elif app_mode == "🔍 Soil Search":
    st.markdown('<h2 class="sub-header">🔍 Search Similar Soils</h2>', unsafe_allow_html=True)

    query = st.text_area(
        "Describe your soil condition:",
        "Red soil, low moisture, acidic, suitable for millet"
    )

    if st.button("🔎 Search"):
        results = random.sample(st.session_state.soil_data, 5)

        for i, soil in enumerate(results, 1):
            st.markdown(f"""
            <div class="soil-card">
            <h4>#{i} {soil['soil_type']} Soil</h4>
            <b>Location:</b> {soil['location']['state']}<br/>
            <b>Crop:</b> {soil['crop_grown']}<br/>
            <b>Methods:</b> {", ".join(soil['traditional_methods'])}<br/>
            <b>Yield:</b> {soil['yield_quality']}<br/>
            <b>Success Score:</b> {soil['reinforcement_score']}
            </div>
            """, unsafe_allow_html=True)

            if st.button("Select", key=f"soil_{i}"):
                st.session_state.selected_soil = soil["id"]
                st.success("Soil selected for reinforcement")

# ---------------- WISDOM SEARCH ----------------
elif app_mode == "👴 Wisdom Search":
    st.markdown('<h2 class="sub-header">👴 Traditional Wisdom Search</h2>', unsafe_allow_html=True)

    query = st.text_area(
        "What advice are you looking for?",
        "Improve water retention in sandy soil"
    )

    if st.button("👂 Search Wisdom"):
        results = random.sample(st.session_state.wisdom_data, 5)

        for i, w in enumerate(results, 1):
            st.markdown(f"""
            <div class="wisdom-card">
            <h4>#{i} {w['title']}</h4>
            <b>Elder:</b> {w['elder_name']} ({w['experience_years']} yrs)<br/>
            <b>Soil Type:</b> {w['soil_type']}<br/><br/>
            <i>"{w['wisdom_text']}"</i>
            </div>
            """, unsafe_allow_html=True)

# ---------------- ANALYTICS ----------------
elif app_mode == "📊 Analytics":
    st.markdown('<h2 class="sub-header">📊 Analytics</h2>', unsafe_allow_html=True)

    df = pd.DataFrame(st.session_state.soil_data)
    fig = px.histogram(df, x="soil_type", title="Soil Type Distribution")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- MEMORY REINFORCEMENT ----------------
elif app_mode == "🔄 Memory Reinforcement":
    st.markdown('<h2 class="sub-header">🔄 Reinforce Knowledge</h2>', unsafe_allow_html=True)

    if "selected_soil" not in st.session_state:
        st.info("Please select a soil sample first from Soil Search.")
    else:
        score = st.slider("How successful was the recommendation?", 0.0, 1.0, 0.8)
        if st.button("✅ Submit Feedback"):
            st.success("Memory updated successfully!")

# ---------------- ABOUT ----------------
elif app_mode == "📚 About":
    st.markdown('<h2 class="sub-header">📚 About Bhu-Smruti</h2>', unsafe_allow_html=True)

    st.markdown("""
    **Bhu-Smruti** is an AI-powered soil memory and wisdom retrieval system.

    **Tech Stack**
    - Python
    - Streamlit
    - Vector Search (Qdrant – extendable)
    - Indigenous Knowledge Systems

    **Use Case**
    - Sustainable agriculture
    - Rural innovation
    - Knowledge preservation

    Built for hackathons & research.
    """)

