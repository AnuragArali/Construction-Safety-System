class RecommendationEngine:
    RECOMMENDATIONS = {
        "MISSING_HELMET": {
            "en": {
                "alert": "Warning! Safety helmet missing.",
                "recommendation": "Immediately put on an approved industrial safety hard hat with chinstrap fastened before proceeding with any construction task.",
                "voice": "Warning. Safety helmet missing. Please put on your hard hat immediately."
            },
            "hi": {
                "alert": "चेतावनी! सुरक्षा हेलमेट नहीं पहना है।",
                "recommendation": "कृपया कार्य शुरू करने से पहले तुरंत स्वीकृत सुरक्षा हेलमेट पहनें।",
                "voice": "चेतावनी। सुरक्षा हेलमेट नहीं पहना है। कृपया तुरंत हेलमेट पहनें।"
            },
            "kn": {
                "alert": "ಎಚ್ಚರಿಕೆ! ಸುರಕ್ಷತಾ ಹೆಲ್ಮೆಟ್ ಧರಿಸಿಲ್ಲ.",
                "recommendation": "ದಯವಿಟ್ಟು ಕೆಲಸ ಮುಂದುವರಿಸುವ ಮೊದಲು ತಕ್ಷಣ ಸುರಕ್ಷತಾ ಹೆಲ್ಮೆಟ್ ಧರಿಸಿ.",
                "voice": "ಎಚ್ಚರಿಕೆ. ಸುರಕ್ಷತಾ ಹೆಲ್ಮೆಟ್ ಧರಿಸಿಲ್ಲ. ದಯವಿಟ್ಟು ತಕ್ಷಣ ಹೆಲ್ಮೆಟ್ ಧರಿಸಿ."
            },
            "es": {
                "alert": "¡Advertencia! Falta el casco de seguridad.",
                "recommendation": "Colóquese inmediatamente un casco de seguridad industrial certificado antes de continuar.",
                "voice": "Advertencia. Falta el casco de seguridad. Por favor póngase su casco de inmediato."
            }
        },
        "MISSING_VEST": {
            "en": {
                "alert": "Warning! High-visibility vest missing.",
                "recommendation": "Wear a certified high-visibility reflective safety vest (Class 2 or Class 3) to ensure optical detection by equipment operators.",
                "voice": "Warning. High visibility safety vest missing. Please wear your reflective vest."
            },
            "hi": {
                "alert": "चेतावनी! रिफ्लेक्टिव सेफ्टी वेस्ट नहीं पहना है।",
                "recommendation": "मशीनरी ऑपरेटरों को दिखाई देने के लिए कृपया तुरंत उच्च दृश्यता वाली सुरक्षा वेस्ट पहनें।",
                "voice": "चेतावनी। रिफ्लेक्टिव सुरक्षा वेस्ट नहीं पहना है। कृपया सुरक्षा वेस्ट पहनें।"
            },
            "kn": {
                "alert": "ಎಚ್ಚರಿಕೆ! ಪ್ರತಿಫಲಕ ಸುರಕ್ಷತಾ ಜಾಕೆಟ್ ಧರಿಸಿಲ್ಲ.",
                "recommendation": "ಯಂತ್ರ ಚಾಲಕರಿಗೆ ಸ್ಪಷ್ಟವಾಗಿ ಕಾಣಿಸಿಕೊಳ್ಳಲು ದಯವಿಟ್ಟು ಪ್ರತಿಫಲಕ ಜಾಕೆಟ್ ಧರಿಸಿ.",
                "voice": "ಎಚ್ಚರಿಕೆ. ಸುರಕ್ಷತಾ ಜಾಕೆಟ್ ಧರಿಸಿಲ್ಲ. ದಯವಿಟ್ಟು ಜಾಕೆಟ್ ಧರಿಸಿ."
            },
            "es": {
                "alert": "¡Advertencia! Falta el chaleco reflectante.",
                "recommendation": "Utilice un chaleco de alta visibilidad certificado para evitar accidentes con maquinaria pesada.",
                "voice": "Advertencia. Falta el chaleco reflectante. Por favor use su chaleco de seguridad."
            }
        },
        "RESTRICTED_ZONE_INTRUSION": {
            "en": {
                "alert": "Critical Hazard! Unauthorized entry into restricted zone.",
                "recommendation": "Immediately evacuate the heavy machinery hazardous exclusion perimeter and report to the safety supervisor.",
                "voice": "Danger. Restricted zone intrusion. Step back immediately from the hazardous zone."
            },
            "hi": {
                "alert": "गंभीर खतरा! प्रतिबंधित क्षेत्र में अनधिकृत प्रवेश।",
                "recommendation": "तुरंत भारी मशीनरी के खतरनाक क्षेत्र से बाहर निकलें और सुपरवाइजर को रिपोर्ट करें।",
                "voice": "खतरा। प्रतिबंधित क्षेत्र में प्रवेश। कृपया तुरंत पीछे हटें।"
            },
            "kn": {
                "alert": "ತೀವ್ರ ಅಪಾಯ! ನಿರ್ಬಂಧಿತ ಪ್ರದೇಶಕ್ಕೆ ಅನಧಿಕೃತ ಪ್ರವೇಶ.",
                "recommendation": "ತಕ್ಷಣ ಭಾರೀ ಯಂತ್ರೋಪಕರಣಗಳ ಅಪಾಯಕಾರಿ ಪ್ರದೇಶದಿಂದ ಹೊರಬನ್ನಿ.",
                "voice": "ಅಪಾಯ. ನಿರ್ಬಂಧಿತ ವಲಯ ಪ್ರವೇಶ. ದಯವಿಟ್ಟು ತಕ್ಷಣ ಹಿಂದೆ ಸರಿಯಿರಿ."
            },
            "es": {
                "alert": "¡Peligro Crítico! Entrada no autorizada en zona restringida.",
                "recommendation": "Evacúe inmediatamente el perímetro de exclusión de maquinaria pesada.",
                "voice": "Peligro. Intrusión en zona restringida. Retroceda inmediatamente."
            }
        }
    }

    @classmethod
    def get_recommendation(cls, violation_type: str, language: str = "en") -> dict:
        lang = language if language in ["en", "hi", "kn", "es"] else "en"
        type_data = cls.RECOMMENDATIONS.get(violation_type, cls.RECOMMENDATIONS["MISSING_HELMET"])
        return type_data.get(lang, type_data["en"])
