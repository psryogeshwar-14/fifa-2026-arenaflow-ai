import html
import re
from typing import Optional, List, Dict, Tuple, Any

def sanitize_input(text: Optional[str]) -> str:
    """
    Sanitizes user input by removing potential HTML tags and escaping special characters
    to prevent XSS and prompt injection.
    """
    if not text:
        return ""
    # Strip HTML tags
    clean_text = re.sub(r'<[^>]*>', '', text)
    # Escape HTML entities
    return html.escape(clean_text.strip())

def get_routing_steps(gate: str, section: str, route_pref: str) -> List[Tuple[str, str, str]]:
    """
    Business logic for seat and amenity path optimization.
    Returns list of steps as (step_number, instruction, visual_icon/time).
    """
    if "Standard" in route_pref:
        return [
            ("1", f"Enter {gate}, proceed to level 1 main concourse.", "🚶 2 min"),
            ("2", "Take the escalator near Section 102 up to the level 2 concourse.", "🧗 3 min"),
            ("3", f"Walk past Section 108 concession stalls to reach {section}.", "🚶 1 min"),
            ("4", "Locate your Row and Seat inside the block.", "🎯 Arrived")
        ]
    elif "Accessible" in route_pref:
        return [
            ("1", f"Enter via {gate} main ramp (sloped, elevator bank access).", "♿ 3 min"),
            ("2", "Take Elevator 4 (South Wing) to the Level 2 ADA seating terrace.", "🛗 2 min"),
            ("3", "Follow the blue tactile floor guidance strip designed for level transit.", "♿ 1 min"),
            ("4", f"Arrive at wheelchair-accessible seating platform at {section}.", "🎯 Arrived")
        ]
    elif "Sensory" in route_pref:
        return [
            ("1", f"Enter via {gate} (lowest average crowd density point).", "🤫 2 min"),
            ("2", "Use back hallway corridor behind concession stands to avoid noise/flashing lights.", "🚶 4 min"),
            ("3", "Pass the Sensory Room (available for brief quiet rests if needed).", "💚 1 min"),
            ("4", f"Access {section} from the quietest corridor entryway.", "🎯 Arrived")
        ]
    else: # Eco-Path
        return [
            ("1", f"Enter via {gate}, check in your plastic waste for green points.", "🌱 2 min"),
            ("2", "Pass by the World Cup Eco-Hub & Water Hydration Station to fill your cup.", "💧 2 min"),
            ("3", "Take the solar-powered escalator to the upper concourse.", "🧗 2 min"),
            ("4", f"Reach {section} while reducing carbon emissions footprint.", "🎯 Arrived")
        ]

def get_waste_sorting_recommendation(waste_item: str) -> str:
    """
    Heuristic sorting advice based on waste item names.
    Used as fallback and verification logic.
    """
    item_lower = waste_item.lower()
    if "paper" in item_lower or "cup" in item_lower or "napkin" in item_lower:
        return "♻️ **Recycling/Compost:** If it is a clean paper cup, it can be recycled. If it is a food-soiled paper plate or napkin, discard it in the **Compost** (Green Bin) to decompose organically."
    elif "plastic" in item_lower or "bottle" in item_lower or "tray" in item_lower or "can" in item_lower:
        return "♻️ **Recycling (Blue Bin):** Rinse any leftover cheese or soda, then drop it in the **Recycling Bin** to be processed into new materials."
    elif "food" in item_lower or "dog" in item_lower or "burger" in item_lower or "peel" in item_lower or "banana" in item_lower:
        return "🌱 **Compost (Green Bin):** Leftover food scraps are organic waste. Throw them in the **Compost Bin** to help make fertilizer for local farms."
    else:
        return "🗑️ **Landfill (Black Bin):** General composite materials (like greasy foils or mixed wrappers) cannot be easily separated. Place this item in the **Landfill Bin** to maintain clean recycling flows."

def get_broadcast_translation_fallback(alert_text: str, target_lang: str) -> str:
    """
    Fallback translation mapping for preset stadium alerts.
    """
    lang_clean = target_lang.split()[0]
    alert_lower = alert_text.lower()
    
    if "shuttle" in alert_lower:
        fallbacks = {
            "Spanish": "Atención aficionados: Los autobuses de enlace hacia la estación de tránsito MetLife salen de la Puerta B. Por favor, sigan el sendero verde.",
            "French": "Attention supporters: Les bus navettes pour la station de transit MetLife partent de la porte B. Veuillez suivre le chemin vert.",
            "German": "Achtung Fans: Die Shuttlebusse zum MetLife Bahnhof fahren von Gate B ab. Bitte folgen Sie dem grünen Pfad.",
            "Japanese": "ファンの皆様へお知らせ：メットライフ交通駅行きのシャトルバスはゲートBから出発します。緑の通路に沿ってお進みください。",
            "Arabic": "تنبيه للجماهير: الحافلات المكوكية إلى محطة ترانزيت ميتلايف تغادر من البوابة B. يرجى اتباع المسار الأخضر.",
            "Portuguese": "Atenção torcedores: Os ônibus circulares para a estação de trânsito MetLife partem do Portão B. Por favor, sigam o caminho verde."
        }
    elif "gate c" in alert_lower:
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
    return fallbacks.get(lang_clean, f"[{lang_clean} Translation] {alert_text}")
