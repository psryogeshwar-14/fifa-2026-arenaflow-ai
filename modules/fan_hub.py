import streamlit as st
import pandas as pd
import random

def run_fan_hub(api_key=None, ai_model=None):
    st.markdown("## 🏟️ Fan Experience & Multilingual Hub")
    st.markdown("Your smart companion for navigating the stadium, translating help, and unlocking eco-friendly rewards.")

    # Tabs for different Fan Hub features
    tab1, tab2, tab3 = st.tabs(["💬 Multilingual Fan AI", "🗺️ Smart Path Navigator", "🌱 Green Fan Rewards"])

    with tab1:
        st.subheader("💬 Ask FanAI")
        st.caption("Ask questions in any language about stadium entry, transport, accessibility, food, or safety. FanAI translates and answers instantly!")

        # Initialize Chat History
        if "fan_chat_history" not in st.session_state:
            st.session_state.fan_chat_history = [
                {"role": "assistant", "content": "Hello! I am your FIFA 2026 Stadium FanAI Companion. Ask me anything in your preferred language! Examples:\n* *How do I get to Gate C from the transit hub?*\n* *Where is the nearest sensory-friendly quiet zone?*\n* *¿Dónde puedo reciclar mi vaso de plástico?*"}
            ]

        # Display Chat Messages
        for msg in st.session_state.fan_chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Input box
        user_query = st.chat_input("Type your question here (e.g., 'Where is the nearest water station?')")

        if user_query:
            # Append user message
            st.session_state.fan_chat_history.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.write(user_query)

            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("FanAI is thinking..."):
                    response_text = ""
                    if api_key and ai_model:
                        try:
                            # Direct GenAI Call
                            system_prompt = (
                                "You are FanAI, a highly helpful multilingual AI assistant for the FIFA World Cup 2026. "
                                "You help fans with stadium navigation, transportation, accessibility amenities, safety, "
                                "concessions queue times, and sustainability guides. Answer in the same language the user asks. "
                                "Be polite, concise, and highly informative."
                            )
                            # Combine prompt
                            full_prompt = f"{system_prompt}\n\nUser Question: {user_query}"
                            response = ai_model.generate_content(full_prompt)
                            response_text = response.text
                        except Exception as e:
                            response_text = f"⚠️ GenAI Error: {str(e)}. Falling back to local assistant."
                    
                    if not response_text or response_text.startswith("⚠️"):
                        # Local Fallback Responses
                        query_lower = user_query.lower()
                        if "gate" in query_lower or "puerta" in query_lower:
                            response_text = "🚪 **Stadium Entry Navigation:** All gates (A to G) open 3 hours before kickoff. Gate C is on the North side, closest to the light rail terminal. Ramps are available at all gates for stroller and wheelchair access."
                        elif "water" in query_lower or "agua" in query_lower or "refill" in query_lower:
                            response_text = "💧 **Hydration Stations:** To promote sustainability, single-use plastic bottles are restricted. You can refill your reusable flasks at our water stations located near Sections 104, 118, 203, and 224."
                        elif "quiet" in query_lower or "sensory" in query_lower or "accessible" in query_lower or "wheelchair" in query_lower:
                            response_text = "♿ **Accessibility & Inclusion:** Accessible seating is located in rows A-C of Sections 100 and 200. A sensory-friendly quiet zone is situated behind Section 112 for fans who need a calmer environment. Noise-canceling headphones can be borrowed at Guest Services (Gate A)."
                        elif "metro" in query_lower or "transit" in query_lower or "bus" in query_lower or "train" in query_lower or "transport" in query_lower:
                            response_text = "🚌 **Smart Transportation:** Free shuttle buses run to MetLife Transit Hub every 5 minutes after the match. You can follow the green pathway from Gate B directly to the train platform."
                        elif "recycle" in query_lower or "trash" in query_lower or "reciclar" in query_lower:
                            response_text = "♻️ **Sustainability Sorting:** Help us make FIFA 2026 the greenest World Cup! Use green bins for compostables (food waste, paper packaging) and blue bins for clean plastics/aluminum. Locate your nearest bin using our Smart Map!"
                        else:
                            response_text = "🤖 **FanAI Answer:** Thank you for your question! To ensure absolute safety and crowd flow during the match, please keep your digital ticket ready. You can find restrooms and food concessions on all main concourses, spaced every 50 meters."
                    
                    st.write(response_text)
                    st.session_state.fan_chat_history.append({"role": "assistant", "content": response_text})

            # Clear button
            if st.button("Clear Chat History", key="clear_fan_chat"):
                st.session_state.fan_chat_history = st.session_state.fan_chat_history[:1]
                st.rerun()

    with tab2:
        st.subheader("🗺️ Seat & Amenity Path Finder")
        st.write("Specify your ticket info to see customized, AI-optimized navigation routes to your seat and nearest points of interest.")

        col1, col2 = st.columns(2)
        with col1:
            gate = st.selectbox("Your Entry Gate", ["Gate A (East)", "Gate B (South)", "Gate C (North)", "Gate D (West)"])
            section = st.selectbox("Your Section Block", [f"Section {100 + i}" for i in range(1, 20)] + [f"Section {200 + i}" for i in range(1, 20)])
        with col2:
            route_pref = st.radio(
                "AI Route Optimization Preference",
                ["⚡ Standard Route (Fastest)", "♿ Accessible Route (No stairs, elevators)", "🤫 Sensory/Low-Noise Route", "🌱 Eco-Path (Passes recycling & water refills)"]
            )

        st.markdown("---")
        st.markdown(f"#### 🧭 Optimized Path: **{gate}** to **{section}** via **{route_pref}**")

        # Interactive path description based on selection
        steps = []
        if "Standard" in route_pref:
            steps = [
                ("1", "Enter Gate A, proceed to level 1 main concourse.", "🚶 2 min"),
                ("2", "Take the escalator near Section 102 up to the level 2 concourse.", "🧗 3 min"),
                ("3", "Walk past Section 108 concession stalls to reach your section entrance.", "🚶 1 min"),
                ("4", "Locate Row K, Seat 14 inside the block.", "🎯 Arrived")
            ]
        elif "Accessible" in route_pref:
            steps = [
                ("1", "Enter via Gate B main ramp (sloped, elevator bank access).", "♿ 3 min"),
                ("2", "Take Elevator 4 (South Wing) to the Level 2 ADA seating terrace.", "🛗 2 min"),
                ("3", "Follow the blue floor guidance strip designed for level transit.", "♿ 1 min"),
                ("4", "Arrive at wheelchair-accessible seating platform Section 108.", "🎯 Arrived")
            ]
        elif "Sensory" in route_pref:
            steps = [
                ("1", "Enter via Gate D (lowest average crowd density).", "🤫 2 min"),
                ("2", "Use back hallway corridor behind concession stands to avoid noise/flashing lights.", "🚶 4 min"),
                ("3", "Pass the Sensory Room (available for brief quiet rests if needed).", "💚 1 min"),
                ("4", "Access Seat Block from the quietest corridor entryway.", "🎯 Arrived")
            ]
        else: # Eco-Path
            steps = [
                ("1", "Enter via Gate C, check in your plastic waste for green points.", "🌱 2 min"),
                ("2", "Pass by the World Cup Eco-Hub & Water Hydration Station 3 to fill your cup.", "💧 2 min"),
                ("3", "Take the solar-powered escalator to Section 108.", "🧗 2 min"),
                ("4", "Reach seat while reducing carbon emissions footprint.", "🎯 Arrived")
            ]

        # Draw beautiful steps
        for num, text, time in steps:
            st.markdown(
                f"""
                <div class="metric-card" style="padding: 0.75rem 1rem !important; margin-bottom: 0.5rem !important;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: bold; color: #2563eb; margin-right: 1rem;">Step {num}</span>
                        <span style="flex-grow: 1; font-size: 0.95rem;">{text}</span>
                        <span class="mono-text">{time}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with tab3:
        st.subheader("🌱 Green Fan Rewards Program")
        st.write("FIFA 2026 aims for net-zero carbon operations. Earn points for eco-actions and redeem them for exclusive World Cup merch!")

        # Initialize user points
        if "eco_points" not in st.session_state:
            st.session_state.eco_points = 50

        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("##### Log an Action:")
            
            action_type = st.selectbox(
                "Choose your sustainability action:",
                [
                    "♻️ Recycled plastic/aluminum at smart bin",
                    "🚌 Arrived via public transit (light rail/bus)",
                    "💧 Used reusable water bottle instead of single-use plastic",
                    "🥗 Purchased certified local organic/vegan food concession"
                ]
            )

            if st.button("Submit Action & Scan QR Code"):
                pts = random.choice([10, 15, 20])
                st.session_state.eco_points += pts
                st.success(f"🎉 QR scanned successfully! Added **+{pts} Green Points** to your wallet.")
                st.balloons()
        
        with col2:
            st.markdown(
                f"""
                <div class="metric-card" style="text-align: center; background-color: #18181b !important;">
                    <h5 style="color: #10b981; margin: 0;">Green Fan Balance</h5>
                    <div style="font-size: 3rem; font-weight: 800; margin: 0.5rem 0; color: #34d399;">{st.session_state.eco_points}</div>
                    <div class="muted-text">Points Earned</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown("##### 🎁 Redeemable Rewards")
        
        rewards = [
            ("☕ Free Organic Coffee / Cold Drink", "100 Points", "Redeem at any Concourse A vendor"),
            ("🧴 FIFA 2026 Eco-friendly Reusable Bottle", "200 Points", "Collect at Guest Services (Gate A)"),
            ("👕 15% discount on official World Cup Merch", "300 Points", "Apply coupon inside official store"),
            ("🎟️ Post-match VIP Pitch Walk Entry Ticket", "500 Points", "Subject to stadium availability")
        ]

        for title, price, location in rewards:
            price_val = int(price.split()[0])
            can_redeem = st.session_state.eco_points >= price_val
            
            col_r1, col_r2 = st.columns([3, 1])
            with col_r1:
                st.markdown(f"**{title}**  \n<span class='muted-text'>{location}</span>", unsafe_allow_html=True)
            with col_r2:
                if st.button(f"Claim ({price})", key=f"redeem_{title}", disabled=not can_redeem):
                    st.session_state.eco_points -= price_val
                    st.success(f"Redeemed! Show this ticket code at the counter: **WC26-ECO-{random.randint(1000, 9999)}**")
                    st.rerun()
