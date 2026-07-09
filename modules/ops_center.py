import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
from datetime import datetime, timedelta

def run_ops_center(api_key=None, ai_model=None):
    st.markdown("## 📊 Operations & Crowd Command Center")
    st.markdown("Real-time crowd flow analysis, incident response systems, and GenAI-powered decision support for venue staff.")

    # Initialize session state data if not present
    if "incidents" not in st.session_state:
        st.session_state.incidents = [
            {"id": "INC-001", "sector": "Gate C Concourse", "category": "Crowd", "urgency": "High", "desc": "Ticket scanner queue length exceeds 50 meters, causing localized bottleneck.", "status": "Active", "time": "18:22"},
            {"id": "INC-002", "sector": "Section 108 Concourse", "category": "Safety", "urgency": "Medium", "desc": "Beverage spill near escalator entrance, slip hazard.", "status": "Active", "time": "18:35"},
            {"id": "INC-003", "sector": "Transit Hub Hub", "category": "Transport", "urgency": "Low", "desc": "Slight bus shuttle delay due to outer perimeter traffic.", "status": "Assigned", "time": "18:10"},
        ]
    
    if "dispatched_tasks" not in st.session_state:
        st.session_state.dispatched_tasks = [
            {"id": "TSK-301", "incident": "INC-002", "assignee": "Volunteer Team 4", "task": "Deploy hazard wet floor cones and request cleaning crew near Section 108.", "status": "In Progress"}
        ]

    # Sub-tabs
    tab1, tab2, tab3 = st.tabs(["👁️ Real-time Crowd Flow", "🚨 Incident Dispatch Log", "🧠 GenAI Operational Advice"])

    with tab1:
        st.subheader("👁️ Live Crowd Density & Predictions")
        
        # Sector status grid
        sectors = [
            {"name": "Gate C North Concourse", "density": 87, "status": "High (Bottleneck)", "color": "red"},
            {"name": "Gate A East Entrance", "density": 45, "status": "Normal", "color": "green"},
            {"name": "Section 108 Exit Corridor", "density": 72, "status": "Moderate", "color": "orange"},
            {"name": "Transit Station Plaza", "density": 92, "status": "Critical", "color": "red"},
            {"name": "West Concourse Food Court", "density": 64, "status": "Normal", "color": "green"},
            {"name": "VIP Terrace Level", "density": 22, "status": "Low", "color": "green"}
        ]

        # Draw metrics
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(
                """
                <div class="metric-card" style="border-left: 4px solid #ef4444 !important;">
                    <div class="muted-text">CRITICAL BOTTLENECKS</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #ef4444; margin: 0.3rem 0;">2 Sectors</div>
                    <div class="muted-text" style="font-size: 0.8rem;">Gate C & Transit Plaza</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_m2:
            st.markdown(
                """
                <div class="metric-card" style="border-left: 4px solid #f59e0b !important;">
                    <div class="muted-text">TOTAL STADIUM CROWD</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #fbbf24; margin: 0.3rem 0;">78,450</div>
                    <div class="muted-text" style="font-size: 0.8rem;">98.1% Arena Occupancy</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_m3:
            st.markdown(
                """
                <div class="metric-card" style="border-left: 4px solid #10b981 !important;">
                    <div class="muted-text">ACTIVE STAFF & VOLUNTEERS</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #34d399; margin: 0.3rem 0;">842 deployed</div>
                    <div class="muted-text" style="font-size: 0.8rem;">Across 7 sectors</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Plotly predictive crowd flow chart
        st.markdown("##### 📈 Predictive Crowd Density (Next 60 Minutes)")
        times = [datetime.now() + timedelta(minutes=10 * i) for i in range(7)]
        time_labels = [t.strftime("%H:%M") for t in times]
        
        # Build simulated dataframe
        chart_data = pd.DataFrame({
            "Time": time_labels * 3,
            "Crowd Density (%)": np.concatenate([
                [87, 89, 92, 85, 78, 65, 45], # Gate C North
                [92, 94, 96, 91, 79, 58, 30], # Transit Plaza
                [45, 52, 60, 68, 70, 72, 75]  # Gate A East
            ]),
            "Sector": ["Gate C Concourse"] * 7 + ["Transit Station Plaza"] * 7 + ["Gate A Entrance"] * 7
        })

        fig = px.line(
            chart_data, 
            x="Time", 
            y="Crowd Density (%)", 
            color="Sector", 
            markers=True,
            color_discrete_map={"Gate C Concourse": "#ef4444", "Transit Station Plaza": "#ec4899", "Gate A Entrance": "#3b82f6"}
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#fafafa',
            xaxis=dict(showgrid=True, gridcolor='#1e1e24'),
            yaxis=dict(showgrid=True, gridcolor='#1e1e24'),
            margin=dict(l=20, r=20, t=10, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("🚨 Incident Dispatch Log")
        
        col_list, col_form = st.columns([2, 1])

        with col_list:
            st.markdown("##### Active Reports")
            for inc in st.session_state.incidents:
                badge_color = "#ef4444" if inc["urgency"] == "High" else ("#f59e0b" if inc["urgency"] == "Medium" else "#3b82f6")
                status_color = "#f87171" if inc["status"] == "Active" else "#60a5fa"
                
                st.markdown(
                    f"""
                    <div class="metric-card" style="margin-bottom: 0.75rem !important;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span class="mono-text">{inc["id"]}</span>
                            <span style="background-color: {badge_color}; color: #000000; padding: 0.1rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">{inc["urgency"]} Urgency</span>
                        </div>
                        <div style="font-weight: bold; font-size: 1.05rem; margin-bottom: 0.25rem;">{inc["sector"]} - {inc["category"]}</div>
                        <p style="margin: 0 0 0.5rem 0; font-size: 0.9rem; color: #d4d4d8;">{inc["desc"]}</p>
                        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #a1a1aa;">
                            <span>Reported at {inc["time"]}</span>
                            <span style="color: {status_color}; font-weight: bold;">Status: {inc["status"]}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Action actions
                if inc["status"] == "Active":
                    col_act1, col_act2 = st.columns(2)
                    with col_act1:
                        if st.button(f"⚡ AI Dispatch & Assign", key=f"dispatch_{inc['id']}"):
                            task_id = f"TSK-{random.randint(302, 399)}"
                            task_desc = f"GenAI Recommendation: Dispatch volunteers to {inc['sector']} to handle {inc['desc']}"
                            st.session_state.dispatched_tasks.append({
                                "id": task_id,
                                "incident": inc["id"],
                                "assignee": "Volunteer Quick Response Team",
                                "task": task_desc,
                                "status": "Dispatched"
                            })
                            inc["status"] = "Assigned"
                            st.success(f"Dispatched Task {task_id} successfully!")
                            st.rerun()
                    with col_act2:
                        if st.button(f"✅ Resolve", key=f"resolve_{inc['id']}"):
                            inc["status"] = "Resolved"
                            st.rerun()

        with col_form:
            st.markdown("##### 📝 Report Incident")
            with st.form("new_incident_form"):
                new_sector = st.selectbox("Sector", ["Gate A Entrance", "Gate B Entrance", "Gate C Concourse", "Section 108 Corridor", "Transit Station Plaza", "Food Court West"])
                new_cat = st.selectbox("Category", ["Safety", "Crowd", "Accessibility", "Transport", "Facilities"])
                new_urg = st.selectbox("Urgency", ["Low", "Medium", "High"])
                new_desc = st.text_area("Description / Details")
                
                submit_inc = st.form_submit_button("Submit Report")
                if submit_inc:
                    inc_id = f"INC-{random.randint(100, 999)}"
                    st.session_state.incidents.insert(0, {
                        "id": inc_id,
                        "sector": new_sector,
                        "category": new_cat,
                        "urgency": new_urg,
                        "desc": new_desc,
                        "status": "Active",
                        "time": datetime.now().strftime("%H:%M")
                    })
                    st.success(f"Report logged as {inc_id}!")
                    st.rerun()

            st.markdown("---")
            st.markdown("##### 📋 Deployed Tasks List")
            for tsk in st.session_state.dispatched_tasks:
                st.markdown(
                    f"""
                    <div style="background-color: #18181b; border: 1px solid #27272a; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #a1a1aa; margin-bottom: 0.25rem;">
                            <span>{tsk["id"]} ({tsk["incident"]})</span>
                            <span style="color: #34d399;">{tsk["status"]}</span>
                        </div>
                        <div style="font-size: 0.85rem; font-weight: 500; color: #fafafa; margin-bottom: 0.25rem;">{tsk["assignee"]}</div>
                        <div style="font-size: 0.8rem; color: #d4d4d8;">{tsk["task"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with tab3:
        st.subheader("🧠 GenAI Real-Time Situational Advisor")
        st.write("Leverage Generative AI to receive instant emergency mitigation and crowd-routing recommendations based on current stadium incidents.")

        # Gather active incidents to build prompt context
        active_incidents_str = ""
        for inc in st.session_state.incidents:
            if inc["status"] in ["Active", "Assigned"]:
                active_incidents_str += f"- [{inc['urgency']} Urgency] Incident at {inc['sector']}: {inc['desc']}\n"
        
        if not active_incidents_str:
            active_incidents_str = "No active critical incidents."

        st.markdown(
            f"""
            <div style="background-color: #18181b; border: 1px solid #27272a; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                <div style="font-size: 0.8rem; color: #a1a1aa; font-weight: bold; margin-bottom: 0.5rem;">CURRENT CONTEXT TO FEED AI:</div>
                <pre style="margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #60a5fa; white-space: pre-wrap;">{active_incidents_str}</pre>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Generate Tactical Recommendations"):
            with st.spinner("GenAI is analyzing stadium flow..."):
                advice = ""
                if api_key and ai_model:
                    try:
                        prompt = (
                            "You are the Operations Director GenAI Advisor for the FIFA World Cup 2026. "
                            "Given these active stadium incidents:\n"
                            f"{active_incidents_str}\n"
                            "Provide tactical recommendations for venue staff to mitigate crowd issues, "
                            "redirect pedestrian flows, handle accessibility concerns, and optimize transit. "
                            "Be structured, actionable, and concise. Use bullet points."
                        )
                        res = ai_model.generate_content(prompt)
                        advice = res.text
                    except Exception as e:
                        advice = f"⚠️ GenAI Advisor Error: {str(e)}. Falling back to local simulation."
                
                if not advice or advice.startswith("⚠️"):
                    # Local fallback rule engine
                    advice = (
                        "### 🧠 Tactical Recommendations (Simulated AI Engine)\n\n"
                        "1. **Gate C Bottleneck Mitigation:**\n"
                        "   - Divert incoming fans from the North Concourse towards **Gate D** (West) which currently has lower crowd density.\n"
                        "   - Broadcast navigation changes on the outer stadium giant screens in English, Spanish, and French.\n\n"
                        "2. **Section 108 Spill Containment:**\n"
                        "   - Dispatch Volunteer Quick Response Team with 'wet floor' safety cones immediately.\n"
                        "   - Instruct elevator operator nearby to hold high-traffic passenger flow for 3 minutes until cleanup is complete.\n\n"
                        "3. **Transit Plaza Operations:**\n"
                        "   - Pre-alert shuttle drivers to increase turnaround frequency to MetLife Station due to peak train passenger load.\n"
                        "   - Coordinate with local city traffic management to request green-light priority on transit roads."
                    )
                
                st.markdown(
                    f"""
                    <div class="details-panel" style="margin-top: 1rem;">
                        <div style="font-weight: bold; font-size: 1.1rem; color: #3b82f6; margin-bottom: 0.75rem;">📋 Tactical Action Plan</div>
                        <div style="font-size: 0.95rem; line-height: 1.6; color: #e4e4e7;">{advice}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
