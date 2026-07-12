import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
from datetime import datetime, timedelta
from typing import Optional, Any
from modules.utils import sanitize_input, get_fifa_manual_entry

def run_ops_center(api_key: Optional[str] = None, ai_model: Optional[Any] = None) -> None:
    """
    Renders the Operations and Crowd Command Center dashboard page.
    Includes input sanitization, automated incident logging, GenAI advisory,
    and a RAG-based search tool of FIFA guidelines for stadium operations.
    """
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
    tab1, tab2, tab3, tab4 = st.tabs([
        "👁️ Real-time Crowd Flow", 
        "🚨 Incident Dispatch Log", 
        "🧠 GenAI Tactical Advice",
        "📖 FIFA RAG Operations Search"
    ])

    with tab1:
        st.subheader("👁️ Live Crowd Density & Predictions")
        # Draw metrics
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(
                """
                <article class="metric-card" role="status" aria-label="Critical Bottlenecks Count" style="border-left: 4px solid #ef4444 !important; background-color: #0c0c0f !important;">
                    <div class="muted-text" style="font-size: 0.8rem; font-weight: bold;">CRITICAL BOTTLENECKS</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #ef4444; margin: 0.3rem 0;">2 Sectors</div>
                    <div class="muted-text" style="font-size: 0.8rem;">Gate C & Transit Plaza</div>
                </article>
                """,
                unsafe_allow_html=True
            )
        with col_m2:
            st.markdown(
                """
                <article class="metric-card" role="status" aria-label="Total Stadium Crowd Status" style="border-left: 4px solid #fbbf24 !important; background-color: #0c0c0f !important;">
                    <div class="muted-text" style="font-size: 0.8rem; font-weight: bold;">TOTAL STADIUM CROWD</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #fbbf24; margin: 0.3rem 0;">78,450</div>
                    <div class="muted-text" style="font-size: 0.8rem;">98.1% Arena Occupancy</div>
                </article>
                """,
                unsafe_allow_html=True
            )
        with col_m3:
            st.markdown(
                """
                <article class="metric-card" role="status" aria-label="Active Deployed Staff Count" style="border-left: 4px solid #34d399 !important; background-color: #0c0c0f !important;">
                    <div class="muted-text" style="font-size: 0.8rem; font-weight: bold;">ACTIVE STAFF & VOLUNTEERS</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #34d399; margin: 0.3rem 0;">842 deployed</div>
                    <div class="muted-text" style="font-size: 0.8rem;">Across 7 sectors</div>
                </article>
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
                [87, 89, 92, 85, 78, 65, 45],  # Gate C North
                [92, 94, 96, 91, 79, 58, 30],  # Transit Plaza
                [45, 52, 60, 68, 70, 72, 75]   # Gate A East
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
                
                # Sanitize descriptive inputs to prevent custom tag rendering
                clean_desc = sanitize_input(inc["desc"])
                clean_sector = sanitize_input(inc["sector"])
                
                st.markdown(
                    f"""
                    <article class="metric-card" role="log" aria-label="Incident {inc["id"]} in {clean_sector}" style="margin-bottom: 0.75rem !important; background-color: #0c0c0f !important;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span class="mono-text">{inc["id"]}</span>
                            <span style="background-color: {badge_color}; color: #000000; padding: 0.1rem 0.4rem; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">{inc["urgency"]} Urgency</span>
                        </div>
                        <div style="font-weight: bold; font-size: 1.05rem; margin-bottom: 0.25rem;">{clean_sector} - {inc["category"]}</div>
                        <p style="margin: 0 0 0.5rem 0; font-size: 0.9rem; color: #d4d4d8;">{clean_desc}</p>
                        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: #a1a1aa;">
                            <span>Reported at {inc["time"]}</span>
                            <span style="color: {status_color}; font-weight: bold;" aria-live="polite">Status: {inc["status"]}</span>
                        </div>
                    </article>
                    """,
                    unsafe_allow_html=True
                )
                
                # Action actions
                if inc["status"] == "Active":
                    col_act1, col_act2 = st.columns(2)
                    with col_act1:
                        if st.button("⚡ AI Dispatch & Assign", key=f"dispatch_{inc['id']}"):
                            task_id = f"TSK-{random.randint(302, 399)}"
                            task_desc = f"GenAI Recommendation: Dispatch volunteers to {clean_sector} to handle {clean_desc}"
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
                        if st.button("✅ Resolve", key=f"resolve_{inc['id']}"):
                            inc["status"] = "Resolved"
                            st.rerun()

        with col_form:
            st.markdown("##### 📝 Report Incident")
            with st.form("new_incident_form"):
                new_sector = st.selectbox("Sector", ["Gate A Entrance", "Gate B Entrance", "Gate C Concourse", "Section 108 Corridor", "Transit Station Plaza", "Food Court West"])
                new_cat = st.selectbox("Category", ["Safety", "Crowd", "Accessibility", "Transport", "Facilities"])
                new_urg = st.selectbox("Urgency", ["Low", "Medium", "High"])
                new_desc = st.text_area("Description / Details", max_chars=1000)
                
                submit_inc = st.form_submit_button("Submit Report")
                if submit_inc:
                    # Sanitize input form values
                    safe_desc = sanitize_input(new_desc)
                    safe_sector = sanitize_input(new_sector)
                    
                    inc_id = f"INC-{random.randint(100, 999)}"
                    st.session_state.incidents.insert(0, {
                        "id": inc_id,
                        "sector": safe_sector,
                        "category": new_cat,
                        "urgency": new_urg,
                        "desc": safe_desc,
                        "status": "Active",
                        "time": datetime.now().strftime("%H:%M")
                    })
                    st.success(f"Report logged as {inc_id}!")
                    st.rerun()

            st.markdown("---")
            st.markdown("##### 📋 Deployed Tasks List")
            for tsk in st.session_state.dispatched_tasks:
                clean_task_desc = sanitize_input(tsk["task"])
                clean_assignee = sanitize_input(tsk["assignee"])
                st.markdown(
                    f"""
                    <div role="status" aria-label="Task {tsk["id"]}" style="background-color: #18181b; border: 1px solid #27272a; padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #a1a1aa; margin-bottom: 0.25rem;">
                            <span>{tsk["id"]} ({tsk["incident"]})</span>
                            <span style="color: #34d399; font-weight: bold;">{tsk["status"]}</span>
                        </div>
                        <div style="font-size: 0.85rem; font-weight: 500; color: #fafafa; margin-bottom: 0.25rem;">{clean_assignee}</div>
                        <div style="font-size: 0.8rem; color: #d4d4d8;">{clean_task_desc}</div>
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
                <pre style="margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #60a5fa; white-space: pre-wrap;">{sanitize_input(active_incidents_str)}</pre>
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
                        advice = f"⚠️ GenAI Advisor Error: {sanitize_input(str(e))}. Falling back to local simulation."
                
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
                
                # HTML escaped advice string rendered as Markdown inside styled container
                st.markdown(
                    f"""
                    <aside class="details-panel" role="region" aria-label="Tactical Action Plan" style="margin-top: 1rem;">
                        <div style="font-weight: bold; font-size: 1.1rem; color: #3b82f6; margin-bottom: 0.75rem;">📋 Tactical Action Plan</div>
                        <div style="font-size: 0.95rem; line-height: 1.6; color: #e4e4e7;">{advice}</div>
                    </aside>
                    """,
                    unsafe_allow_html=True
                )

    with tab4:
        st.subheader("📖 FIFA RAG Operations Search")
        st.write("Search the official simulated FIFA World Cup 2026 Operations manual to retrieve exact safety and crowd guidelines via GenAI.")
        
        search_query = st.text_input("Enter search keywords (e.g. 'evacuation', 'lost child', 'medical', 'transit'):", max_chars=200)
        
        if search_query:
            sanitized_search = sanitize_input(search_query)
            with st.spinner("Searching operations guidelines manual..."):
                # Retrieve matching entry from business logic database
                manual_clause = get_fifa_manual_entry(sanitized_search)
                
                summary = ""
                if api_key and ai_model:
                    try:
                        prompt = (
                            "You are a FIFA Operations Manual Assistant. Given this official guidebook clause:\n"
                            f"{manual_clause}\n"
                            "Provide a friendly, highly actionable 2-sentence summary/checklist for venue stewards. Be direct."
                        )
                        res = ai_model.generate_content(prompt)
                        summary = res.text
                    except Exception as e:
                        summary = f"⚠️ GenAI Assistant Error: {sanitize_input(str(e))}"
                
                if not summary or summary.startswith("⚠️"):
                    summary = (
                        "👉 **Action Item Checklist:** Follow safety directives, set local barriers or exit override modes immediately, "
                        "and notify Central security via your mobile terminal."
                    )
                
                st.markdown(
                    f"""
                    <aside class="details-panel" role="region" aria-label="FIFA Operations Manual Guidelines" style="margin-top: 1rem; border-left: 4px solid #fbbf24 !important;">
                        <div style="font-weight: bold; font-size: 1.05rem; color: #fbbf24; margin-bottom: 0.5rem;">📖 Retrieved Manual Regulation</div>
                        <div style="font-size: 0.95rem; color: #e4e4e7; line-height: 1.6; margin-bottom: 1rem;">{manual_clause}</div>
                        <div style="font-weight: bold; font-size: 0.95rem; color: #34d399; margin-bottom: 0.25rem;">📌 Steward Directives:</div>
                        <div style="font-size: 0.9rem; color: #d4d4d8; line-height: 1.5;">{summary}</div>
                    </aside>
                    """,
                    unsafe_allow_html=True
                )
