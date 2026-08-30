import os

GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

print("Lia UNGRIFF démarre...")

if not GMAIL_ADDRESS:
    print("❌ GMAIL_ADDRESS n'est pas configuré.")
else:
    print("✅ Adresse Gmail détectée.")

if not GMAIL_APP_PASSWORD:
    print("❌ GMAIL_APP_PASSWORD n'est pas configuré.")
else:
    print("✅ Mot de passe d'application détecté.")

print("Lia V1 est prête.")
