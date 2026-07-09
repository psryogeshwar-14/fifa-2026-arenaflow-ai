import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load local environment variables if available
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="ArenaFlow AI - FIFA 2026 Smart Stadium & Operations",
    page_icon="🏟️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and inject custom CSS stylesheet
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("styles.css")

# --- GENAI CONFIGURATION ---
api_key = os.getenv("GEMINI_API_KEY")

# Sidebar Configuration
st.sidebar.markdown(
    """
    <div style="text-align: center; padding-bottom: 1.5rem;">
        <span style="font-size: 2.5rem;">🏟️</span>
        <h2 style="margin-top: 0.5rem; margin-bottom: 0.2rem; font-size: 1.6rem; letter-spacing: -0.03em;">ArenaFlow AI</h2>
        <div style="font-size: 0.8rem; color: #71717a; font-weight: 500;">FIFA World Cup 2026 Operations</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("### ⚙️ System Settings")

# Input field for Gemini API Key in sidebar (optional fallback to simulation)
user_key = st.sidebar.text_input(
    "Google Gemini API Key:",
    type="password",
    value=api_key or "",
    help="Enter your Gemini API key to activate real-time GenAI suggestions. Leave blank for Simulation Mode."
)

if user_key:
    api_key = user_key
    try:
        genai.configure(api_key=api_key)
        # Using gemini-1.5-flash as default, fallback to gemini-pro if needed
        ai_model = genai.GenerativeModel('gemini-1.5-flash')
        st.sidebar.markdown(
            '<div class="alert-container alert-success"><span style="font-size: 1.1rem;">⚡</span><div><b>Live GenAI Active</b><br/>Connected to Gemini API.</div></div>',
            unsafe_allow_html=True
        )
    except Exception as e:
        ai_model = None
        st.sidebar.markdown(
            f'<div class="alert-container alert-error"><span style="font-size: 1.1rem;">⚠️</span><div><b>Connection Failed</b><br/>{str(e)}</div></div>',
            unsafe_allow_html=True
        )
else:
    ai_model = None
    st.sidebar.markdown(
        '<div class="alert-container alert-warning"><span style="font-size: 1.1rem;">🤖</span><div><b>Simulation Mode</b><br/>Running local heuristic AI.</div></div>',
        unsafe_allow_html=True
    )

st.sidebar.markdown("---")

# Navigation menu
st.sidebar.markdown("### 🗺️ Navigation Dashboard")
nav_choice = st.sidebar.radio(
    "Go To:",
    [
        "🏟️ Fan Experience Hub",
        "📊 Operations & Crowd Command",
        "🌿 Sustainability & Eco-Ops",
        "📢 Multilingual Broadcast Hub"
    ]
)

# Live Match Context Widget
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="background-color: #18181b; border: 1px solid #27272a; padding: 1rem; border-radius: 8px;">
        <div style="font-size: 0.75rem; color: #a1a1aa; font-weight: bold; text-transform: uppercase; margin-bottom: 0.5rem;">🎮 Live Match Context</div>
        <div style="font-weight: bold; font-size: 1.1rem; margin-bottom: 0.25rem; color: #fbbf24;">USA vs MEXICO</div>
        <div style="font-size: 0.85rem; color: #fafafa; margin-bottom: 0.5rem;">Group Stage - Match 14</div>
        <div style="font-size: 0.8rem; color: #71717a;">📍 MetLife Stadium, NYNJ</div>
        <div style="font-size: 0.8rem; color: #71717a;">⏰ Kickoff: 20:00 (Local)</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Main Application Router
from modules.fan_hub import run_fan_hub
from modules.ops_center import run_ops_center
from modules.sustainability import run_sustainability
from modules.broadcast import run_broadcast

if "Fan" in nav_choice:
    run_fan_hub(api_key, ai_model)
elif "Operations" in nav_choice:
    run_ops_center(api_key, ai_model)
elif "Sustainability" in nav_choice:
    run_sustainability(api_key, ai_model)
else:
    run_broadcast(api_key, ai_model)

# Footer info
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #71717a; font-size: 0.8rem; padding: 1rem;">
        ⚽ ArenaFlow AI • Build for Challenge 4 (Smart Stadiums & Operations) • FIFA World Cup 2026
    </div>
    """,
    unsafe_allow_html=True
)
