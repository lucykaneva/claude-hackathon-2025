import streamlit as st

st.set_page_config(
    page_title="ChristmasGiftCircle",
    page_icon="🎄🎁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme toggle
mode = st.sidebar.radio("Theme", ["Light 🎄", "Dark 🌙"])

# -----------------------
# CSS: light/dark mode + card blobs + uniform card size
# -----------------------
if mode.startswith("Light"):
    app_bg = "#fff"
    sidebar_bg = "#f5f5f5"
    card_bg = "#fff"
    text_color = "#000"
else:
    app_bg = "#0f172a"
    sidebar_bg = "#1f2937"
    card_bg = "#1e293b"
    text_color = "#e5e5e5"

st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(to bottom, {app_bg}, #fff7f0) !important;
    color: {text_color} !important;
    font-family: 'Segoe UI', sans-serif;
    transition: all 0.5s ease;
}}

[data-testid="stSidebar"] {{
    background: {sidebar_bg} !important;
    transition: all 0.5s ease;
}}

.main-title {{
    font-size: 72px !important;
    font-weight: 800;
    text-align: center;
    color: #b30000;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    animation: fadeIn 1.5s ease;
}}

.subtitle {{
    font-size: 26px !important;
    font-weight: 500;
    text-align: center;
    color: #0c5e32;
    margin-bottom: 40px;
    animation: fadeIn 2s ease;
}}

.card {{
    background: {card_bg};
    color: {text_color};
    padding: 20px;
    border-radius: 25px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    margin: 20px 0;
    position: relative;
    min-height: 250px; /* uniform card height */
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.2);
}}

.card-blob {{
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, #ff4b4b, #ff7f50);
    border-radius: 50%;
    margin: -50px auto 20px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    color: white;
    font-weight: bold;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    animation: blobBounce 2s infinite alternate;
}}

@keyframes blobBounce {{
    0% {{ transform: translateY(0); }}
    100% {{ transform: translateY(-10px); }}
}}

@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}

p, li, span, div {{
    font-size: 20px !important;
    color: {text_color} !important;
}}
</style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER
# -----------------------
st.markdown('<p class="main-title">🎁 ChristmasGiftCircle</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Donate or Find perfect gifts for Christmas</p>', unsafe_allow_html=True)
st.markdown("---")

# -----------------------
# HOW IT WORKS SECTION
# -----------------------
st.header("How It Works:")

col1, col2, col3 = st.columns(3)

cards = [
    {"icon": "📦", "title": "Donate!", "text": "Upload photos of items in good condition to give away for the holiday season."},
    {"icon": "🤖", "title": "AI Matches", "text": "Claude AI will review item quality and find a perfect match."},
    {"icon": "🎉", "title": "Connect", "text": "Coordinate delivery and brighten a child's holiday!"}
]

for col, card in zip([col1, col2, col3], cards):
    col.markdown(f'''
    <div class="card">
        <div class="card-blob">{card["icon"]}</div>
        <h3>{card["title"]}</h3>
        <p>{card["text"]}</p>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("---")

# -----------------------
# COMMUNITY IMPACT
# -----------------------
st.header("🎄 Community Impact")
st.write("Impact metrics coming soon!")
st.markdown("---")
st.info("🎄 Use the sidebar to donate, request items, or browse gifts!")
