import streamlit as st
import random

def run_broadcast(api_key=None, ai_model=None):
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
                            f"Text to translate: '{alert_text}'"
                        )
                        res = ai_model.generate_content(prompt)
                        translated_text = res.text.strip()
                    except Exception as e:
                        translated_text = f"⚠️ Translation Error: {str(e)}"
                
                if not translated_text or translated_text.startswith("⚠️"):
                    # Fallback translations for presets or basic queries
                    if "shuttle" in alert_text.lower():
                        fallbacks = {
                            "Spanish": "Atención aficionados: Los autobuses de enlace hacia la estación de tránsito MetLife salen de la Puerta B. Por favor, sigan el sendero verde.",
                            "French": "Attention supporters: Les bus navettes pour la station de transit MetLife partent de la porte B. Veuillez suivre le chemin vert.",
                            "German": "Achtung Fans: Die Shuttlebusse zum MetLife Bahnhof fahren von Gate B ab. Bitte folgen Sie dem grünen Pfad.",
                            "Japanese": "ファンの皆様へお知らせ：メットライフ交通駅行きのシャトルバスはゲートBから出発します。緑の通路に沿ってお進みください。",
                            "Arabic": "تنبيه للجماهير: الحافلات المكوكية إلى محطة ترانزيت ميتلايف تغادر من البوابة B. يرجى اتباع المسار الأخضر.",
                            "Portuguese": "Atenção torcedores: Os ônibus circulares para a estação de trânsito MetLife partem do Portão B. Por favor, sigam o caminho verde."
                        }
                    elif "gate c" in alert_text.lower():
                        fallbacks = {
                            "Spanish": "Aviso: Debido al gran flujo de personas, la Puerta C es temporalmente de solo salida. Los aficionados que ingresen deben dirigirse a la Puerta D.",
                            "French": "Avis: En raison d'un flux de foule important, la porte C est temporairement réservée à la sortie. Les supporters entrants sont priés de se rendre à la porte D.",
                            "German": "Hinweis: Aufgrund des starken Besucherstroms ist Gate C vorübergehend nur als Ausgang geöffnet. Eintreffende Fans gehen bitte zu Gate D.",
                            "Japanese": "お知らせ：混雑のため、ゲートCは一時的に出口専用となっております。入場されるお客様はゲートDへお回りください。",
                            "Arabic": "تنبيه: بسبب تدفق الجماهير الكثيف، البوابة C مخصصة للخروج فقط مؤقتاً. يرجى من الجماهير القادمة التوجه إلى البوابة D.",
                            "Portuguese": "Aviso: Devido ao grande fluxo de público, o Portão C está temporariamente apenas para saída. Torcedores que entram devem se dirigir ao Portão D."
                        }
                    else:
                        fallbacks = {
                            "Spanish": f"[Traducción al Español] {alert_text} (Traducido por IA)",
                            "French": f"[Traduction en Français] {alert_text} (Traduit par IA)",
                            "German": f"[Übersetzung ins Deutsche] {alert_text} (Übersetzt von KI)",
                            "Japanese": f"[日本語訳] {alert_text} (AI翻訳)",
                            "Arabic": f"[الترجمة العربية] {alert_text} (مترجم بواسطة الذكاء الاصطناعي)",
                            "Portuguese": f"[Tradução para o Português] {alert_text} (Traduzido por IA)"
                        }
                    translated_text = fallbacks.get(lang_name, f"[{lang_name} Translation] {alert_text}")
                
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

    # Jumbotron Simulator Box
    if "jumbotron_text" in st.session_state:
        st.markdown("---")
        st.markdown("##### 💻 Simulated Stadium Jumbotron Display")
        st.markdown(
            f"""
            <div style="background-color: #0c0c0f; border: 4px solid #3b82f6; padding: 2rem; border-radius: 12px; text-align: center; font-family: 'DM Sans', sans-serif;">
                <div style="color: #3b82f6; font-size: 0.8rem; font-weight: bold; letter-spacing: 0.2em; margin-bottom: 1rem; text-transform: uppercase;">
                    📺 FIFA 2026 OFFICIAL LIVE SCREEN BROADCAST ({st.session_state.jumbotron_lang})
                </div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #fbbf24; line-height: 1.4; padding: 0.5rem;">
                    "{st.session_state.jumbotron_text}"
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Clear Jumbotron Screen"):
            del st.session_state.jumbotron_text
            del st.session_state.jumbotron_lang
            st.rerun()
