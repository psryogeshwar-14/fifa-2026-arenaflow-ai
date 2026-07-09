import streamlit as st
import pandas as pd
import plotly.express as px
import random

def run_sustainability(api_key=None, ai_model=None):
    st.markdown("## 🌿 Sustainability & Eco-Operations")
    st.markdown("Monitor stadium environmental impact, manage solar energy stats, and leverage GenAI to sort waste efficiently.")

    # Top KPI row for Sustainability
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="muted-text">WASTE DIVERTED</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #10b981; margin: 0.2rem 0;">14.2 Tons</div>
                <span class="muted-text" style="color: #34d399 !important;">⚡ 78% Recycle Rate</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="muted-text">SOLAR ENERGY SAVED</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #3b82f6; margin: 0.2rem 0;">4,850 kWh</div>
                <span class="muted-text" style="color: #60a5fa !important;">☀️ 12% Total Power Offset</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="muted-text">WATER REFILLED</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #60a5fa; margin: 0.2rem 0;">24,300 L</div>
                <span class="muted-text" style="color: #60a5fa !important;">🥤 48.6K Plastic Bottles Saved</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col4:
        st.markdown(
            """
            <div class="metric-card">
                <div class="muted-text">GREEN TRANSPORT ATTR</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #10b981; margin: 0.2rem 0;">64.2%</div>
                <span class="muted-text" style="color: #34d399 !important;">🚆 Metro & Transit shuttle</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    tab1, tab2 = st.tabs(["🗑️ GenAI Smart Waste Sorter", "💡 Venue Resource Optimization"])

    with tab1:
        st.subheader("🗑️ GenAI Waste Sorting Guide")
        st.write("Unsure how to dispose of your game-day waste? Ask our GenAI model to learn if it's Compost, Recycling, or Landfill.")

        waste_item = st.text_input("Enter waste item (e.g., 'hot dog wrapper', 'paper soda cup', 'plastic nacho tray'):")
        
        if waste_item:
            with st.spinner("AI is analyzing material composition..."):
                result = ""
                if api_key and ai_model:
                    try:
                        prompt = (
                            "You are the FIFA World Cup 2026 Eco-Sorter AI. "
                            f"The user wants to dispose of a '{waste_item}'. "
                            "Determine exactly which bin it goes to:\n"
                            "- Compost (food scraps, unlined paper, wood/bamboo)\n"
                            "- Recycling (clean plastic, glass bottles, aluminum cans, clean cardboard)\n"
                            "- Landfill (oily materials, styrofoam, dirty wrappers, mixed material bags)\n"
                            "Explain why in a concise sentence."
                        )
                        res = ai_model.generate_content(prompt)
                        result = res.text
                    except Exception as e:
                        result = f"⚠️ Eco-Sorter Error: {str(e)}. Falling back to local data."
                
                if not result or result.startswith("⚠️"):
                    # Local fallback database
                    item_lower = waste_item.lower()
                    if "paper" in item_lower or "cup" in item_lower or "napkin" in item_lower:
                        result = "♻️ **Recycling/Compost:** If it is a clean paper cup, it can be recycled. If it is a food-soiled paper plate or napkin, discard it in the **Compost** (Green Bin) to decompose organically."
                    elif "plastic" in item_lower or "bottle" in item_lower or "tray" in item_lower or "can" in item_lower:
                        result = "♻️ **Recycling (Blue Bin):** Rinse any leftover cheese or soda, then drop it in the **Recycling Bin** to be processed into new materials."
                    elif "food" in item_lower or "dog" in item_lower or "burger" in item_lower or "peel" in item_lower:
                        result = "🌱 **Compost (Green Bin):** Leftover food scraps are organic waste. Throw them in the **Compost Bin** to help make fertilizer for local farms."
                    else:
                        result = "🗑️ **Landfill (Black Bin):** General composite materials (like greasy foils or mixed wrappers) cannot be easily separated. Place this item in the **Landfill Bin** to maintain clean recycling flows."

                st.markdown(
                    f"""
                    <div class="details-panel" style="margin-top: 1rem; border-left: 4px solid #10b981 !important;">
                        <div style="font-weight: bold; font-size: 1.05rem; color: #10b981; margin-bottom: 0.5rem;">♻️ Disposal Recommendation</div>
                        <div style="font-size: 0.95rem; color: #e4e4e7;">{result}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with tab2:
        st.subheader("💡 GenAI Venue Energy & Food Waste Advice")
        st.write("AI-generated operational strategies for venue staff to reduce carbon footprint and resource waste based on ticketing data.")

        if st.button("Generate Sustainability Audit"):
            with st.spinner("Analyzing energy grids & food concessions..."):
                audit = ""
                if api_key and ai_model:
                    try:
                        prompt = (
                            "You are a Stadium Sustainability Auditor AI. Based on the stadium holding 78,450 fans, "
                            "and current high crowd density at Gate C concourse, provide 3 key actionable operational suggestions "
                            "for venue organizers to reduce electricity consumption, save food concession waste, "
                            "and optimize smart solar batteries. Be concise."
                        )
                        res = ai_model.generate_content(prompt)
                        audit = res.text
                    except Exception as e:
                        audit = f"⚠️ Auditor Error: {str(e)}."
                
                if not audit or audit.startswith("⚠️"):
                    audit = (
                        "### 💡 Venue Resource Audit Recommendations\n\n"
                        "1. **Concession Re-allocation:**\n"
                        "   - Shift 15% of fresh food inventory from low-density West concourses to Gate C (North) concessions to prevent post-match spoilage.\n\n"
                        "2. **Smart HVAC Zone Controls:**\n"
                        "   - Reduce HVAC cooling by 2°C in VIP and private box zones during peak match runtime (when boxes are empty/fans are in seats).\n\n"
                        "3. **Solar Battery Optimization:**\n"
                        "   - Discharge solar batteries stored during morning sunlight to power the field lighting grids between 19:30 - 21:30, reducing peak city grid drain by 300 kW."
                    )

                st.markdown(
                    f"""
                    <div class="details-panel" style="margin-top: 1rem;">
                        <div style="font-weight: bold; font-size: 1.05rem; color: #3b82f6; margin-bottom: 0.5rem;">🌿 Tactical Energy/Waste Audit Plan</div>
                        <div style="font-size: 0.95rem; color: #e4e4e7; line-height: 1.6;">{audit}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
