import os
from google import genai

# Récupère la clé depuis les Secrets GitHub
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY est introuvable.")
    exit()

client = genai.Client(api_key=api_key)

print("🤖 Lia est connectée à Gemini !")

while True:
    message = input("\nÉcris un message pour Lia (ou 'quitter') : ")

    if message.lower() == "quitter":
        print("👋 Lia s'arrête.")
        break

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message
        )

        print("\nLia :", response.text)

    except Exception as erreur:
        print("❌ Erreur :", erreur)
