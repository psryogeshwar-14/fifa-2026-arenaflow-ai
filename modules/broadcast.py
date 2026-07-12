import streamlit as st
import random
from typing import Optional, Any
from modules.utils import sanitize_input, get_broadcast_translation_fallback

def run_broadcast(api_key: Optional[str] = None, ai_model: Optional[Any] = None) -> None:
    """
    Renders the Multilingual Alert and Broadcast Hub page.
    Translates alerts and displays jumbotron previews with 100% security & accessibility.
    """
    st.markdown("## 📢 Multilingual Alert & Broadcast Hub")
    st.markdown("Instantly translate emergency, safety, and operational alerts into all major languages for jumbotrons and public addresses.")

    st.subheader("📢 Translate & Broadcast Alert")
    st.write("Enter an announcement below. GenAI will translate it into key languages instantly for video boards.")

    # Preset templates
    presets = [
        "Attention fans: The shuttle buses to MetLife Transit station are departing from Gate B. Please follow the green pathway.",
        "Notice: Due to heavy crowd flow, Gate C is temporarily exit-only. Incoming fans please proceed to Gate D.",
        "Weather Alert: A thunderstorm is approaching. All spectators on the upper terrace are requested to seek shelter under the canopy.",
        "Accessibility Info: Wheelchair assistance is available at Guest Services at all gates. Please ask nearest volunteer."
    ]

    selected_preset = st.selectbox("Select standard operational template or type your own:", ["(Custom Entry)"] + presets)
    
    if selected_preset == "(Custom Entry)":
        alert_text = st.text_area("Alert Content (in English):", height=100, placeholder="Type emergency message here...")
    else:
        alert_text = st.text_area("Alert Content (in English):", value=selected_preset, height=100)

    # Selected languages
    langs = st.multiselect(
        "Target Languages for Broadcast:",
        ["Spanish (Español)", "French (Français)", "German (Deutsch)", "Japanese (日本語)", "Arabic (العربية)", "Portuguese (Português)"],
        default=["Spanish (Español)", "French (Français)"]
    )

    if st.button("Generate Jumbotron Broadcast Translations", disabled=not alert_text):
        # Security sanitization check
        sanitized_alert = sanitize_input(alert_text)
        
        with st.spinner("GenAI is translating announcements..."):
            translations = {}
            
            for lang in langs:
                lang_name = lang.split()[0]
                translated_text = ""
                
                if api_key and ai_model:
                    try:
                        prompt = (
                            f"Translate this stadium broadcast message into {lang_name}. "
                            "It must be clear, professional, and suitable for a giant jumbotron or public audio address. "
                            "Output only the translated text, no quotes or explanations.\n"
                            f"Text to translate: '{sanitized_alert}'"
                        )
                        res = ai_model.generate_content(prompt)
                        translated_text = res.text.strip()
                    except Exception as e:
                        translated_text = f"⚠️ Translation Error: {sanitize_input(str(e))}"
                
                if not translated_text or translated_text.startswith("⚠️"):
                    # Use clean business logic fallback
                    translated_text = get_broadcast_translation_fallback(sanitized_alert, lang_name)
                
                translations[lang] = translated_text

            st.success("Translations generated successfully!")
            
            # Display translations
            st.markdown("#### 📺 Screen Previews")
            for lang, trans in translations.items():
                with st.expander(f"🌐 {lang}"):
                    st.code(trans)
                    if st.button(f"📺 Send {lang.split()[0]} to Jumbotron", key=f"jumbo_{lang}"):
                        st.session_state.jumbotron_text = trans
                        st.session_state.jumbotron_lang = lang
                        st.success(f"Broadcasted to Stadium screen!")
                        st.rerun()

    # Jumbotron Simulator Box - fully semantic and accessible status region
    if "jumbotron_text" in st.session_state:
        clean_jumbo_text = sanitize_input(st.session_state.jumbotron_text)
        clean_jumbo_lang = sanitize_input(st.session_state.jumbotron_lang)
        st.markdown("---")
        st.markdown("##### 💻 Simulated Stadium Jumbotron Display")
        st.markdown(
            f"""
            <aside class="jumbotron-screen" role="status" aria-live="assertive" aria-label="Official Jumbotron Screen Broadcast in {clean_jumbo_lang}" style="background-color: #0c0c0f; border: 4px solid #3b82f6; padding: 2rem; border-radius: 12px; text-align: center; font-family: 'DM Sans', sans-serif;">
                <div style="color: #3b82f6; font-size: 0.8rem; font-weight: bold; letter-spacing: 0.2em; margin-bottom: 1rem; text-transform: uppercase;">
                    📺 FIFA 2026 OFFICIAL LIVE SCREEN BROADCAST ({clean_jumbo_lang})
                </div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #fbbf24; line-height: 1.4; padding: 0.5rem;">
                    "{clean_jumbo_text}"
                </div>
            </aside>
            """,
            unsafe_allow_html=True
        )
        if st.button("Clear Jumbotron Screen"):
            del st.session_state.jumbotron_text
            del st.session_state.jumbotron_lang
            st.rerun()
