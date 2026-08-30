import os
import imaplib
import email
from email.header import decode_header
from google import genai

GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
    print("❌ Les identifiants Gmail sont manquants.")
    exit()

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY est manquante.")
    exit()

client = genai.Client(api_key=GEMINI_API_KEY)


def obtenir_texte(message):
    texte = ""

    if message.is_multipart():
        for partie in message.walk():
            if partie.get_content_type() == "text/plain":
                contenu = partie.get_payload(decode=True)

                if contenu:
                    texte += contenu.decode(
                        partie.get_content_charset() or "utf-8",
                        errors="ignore"
                    )
    else:
        contenu = message.get_payload(decode=True)

        if contenu:
            texte = contenu.decode(
                message.get_content_charset() or "utf-8",
                errors="ignore"
            )

    return texte


def analyser_email(expediteur, sujet, contenu):
    prompt = f"""
Tu es Lia, l'assistante IA de la marque UNGRIFF.

Analyse cet e-mail.

Expéditeur :
{expediteur}

Sujet :
{sujet}

Message :
{contenu}

Donne :
1. La catégorie du message : accueil, question, partenariat ou autre.
2. Un résumé très court.
3. Une réponse que Lia pourrait envoyer.

Pour une demande de partenariat, indique que la personne peut contacter
UNGRIFF sur TikTok : @ungriff_officiel et demande-lui son propre TikTok
afin que l'équipe UNGRIFF puisse l'identifier.

Ne prétends jamais être un humain.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def lire_emails():
    print("📩 Connexion à Gmail...")

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
    mail.select("INBOX")

    statut, donnees = mail.search(None, "UNSEEN")

    if statut != "OK":
        print("❌ Impossible de lire les e-mails.")
        mail.logout()
        return

    ids = donnees[0].split()

    if not ids:
        print("📭 Aucun nouvel e-mail.")
        mail.logout()
        return

    for identifiant in ids:
        statut, donnees = mail.fetch(identifiant, "(RFC822)")

        if statut != "OK":
            continue

        message = email.message_from_bytes(donnees[0][1])

        expediteur = message.get("From", "")
        sujet = message.get("Subject", "")
        contenu = obtenir_texte(message)

        print("\n==============================")
        print("📧 NOUVEL E-MAIL")
        print("De :", expediteur)
        print("Sujet :", sujet)
        print("==============================")

        analyse = analyser_email(
            expediteur,
            sujet,
            contenu[:5000]
        )

        print("\n🤖 ANALYSE DE LIA :")
        print(analyse)

    mail.logout()


try:
    lire_emails()
    print("\n✅ Lia a terminé son analyse.")
except Exception as erreur:
    print("\n❌ Erreur :", erreur)
