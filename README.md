# 🏟️ ArenaFlow AI: FIFA 2026 Smart Stadium & Operations Command Center

ArenaFlow AI is a modern, Generative AI-powered SaaS-grade dashboard and fan companion platform built for the **FIFA World Cup 2026** (specifically modeled around the MetLife Stadium in NYNJ). It focuses on enhancing the tournament experience for fans and optimizing match-day operations for organizers, volunteers, and venue staff.

Developed as a submission for **Challenge 4: Smart Stadiums & Tournament Operations**.

---

## 🌟 Key Features

### 1. 🏟️ Fan Experience & Multilingual Hub
* **💬 Multilingual Fan AI**: Instantly answers queries in any language (English, Spanish, French, etc.) regarding stadium entry, transport, accessibility, and facilities.
* **🗺️ Smart Path Navigator**: Generates customized, optimized walking directions (Standard, Wheelchair-Accessible, Sensory/Low-Noise, or Carbon-Optimized Eco-Paths) from gates to seats.
* **🌱 Green Fan Rewards**: Encourages fans to participate in sustainability actions (recycling waste, transit choices) to earn eco-points redeemable for official World Cup merchandise coupons.

### 2. 📊 Operations & Crowd Command Center
* **👁️ Live Crowd Density & Predictions**: Displays real-time sector occupancy levels with automated bottleneck alerts and 60-minute Plotly-powered density forecasts.
* **🚨 Incident Dispatch Log**: Track, report, and assign volunteers to safety, transport, facilities, or crowd issues.
* **🧠 GenAI Tactical Advisor**: Analyzes current active stadium incidents to provide operations directors with instant tactical dispatch and mitigation recommendations.

### 3. 🌿 Sustainability & Eco-Operations
* **🗑️ GenAI Waste Sorting Guide**: Directs users on how to dispose of game-day waste (Compost, Recycle, Landfill) with material analysis.
* **💡 Resource Audits**: Suggests smart zone control settings for HVAC and solar battery discharge to reduce energy footprints by up to 30%.

### 4. 📢 Multilingual Alert & Broadcast Hub
* **📢 Broadcast Translation**: Translates jumbotron alerts instantly into the official languages of the match-day teams.
* **📺 Jumbotron Screen Simulator**: Previews official stadium broadcast banners.

---

## 🛠️ Tech Stack
* **Frontend/Backend**: [Streamlit](https://streamlit.io/) (Python)
* **Visualizations**: [Plotly Express](https://plotly.com/)
* **AI Integration**: [Google Gemini API](https://ai.google.dev/) (`google-generativeai`)
* **Styling**: Zinc/shadcn dark-theme inspired UI custom CSS injections

---

## 🚀 Getting Started

### Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/psryogeshwar-14/fifa-2026-arenaflow-ai.git
   cd fifa-2026-arenaflow-ai
   ```
2. Initialize virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
5. Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ Deployment

ArenaFlow AI is ready to be deployed to **Streamlit Community Cloud** in seconds:
1. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Click **New app** and connect your GitHub repository.
3. Set the Main File path to `app.py`.
4. In Advanced settings -> Secrets, add your Google Gemini API Key:
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key"
   ```
5. Click **Deploy**!
