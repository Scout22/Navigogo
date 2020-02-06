MONTH_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "novembre",
            "décembre"]


def get_email_text(first_name, last_name, year, month):
    body = f"Bonjour,\n\rMerci de trouver en piece jointe l'attestation de transport correspondant au mois de " \
        f"{MONTH_FR[month - 1]} {year}." \
        f"\n\rCordialement.\n\r\n\r" \
        f"{first_name.capitalize()} {last_name.upper()}"
    subject = f"Attestation de transport du mois de {MONTH_FR[month - 1]} {year}"
    return body, subject


def get_email_text_invalid_token():
    body = "Bonjour,\n\rUne erreur s'est produite lors du telechargement de votre attestation. " \
           "Merci de mettre a jours vos identifisants Navigo sur Navigogo"
    subject = "Indentifiant Navigo expiré"
    return body, subject


def success_email():
    body = "Votre inscription au service Navigogo, \n\r\n\r" \
           "Votre inscription au service d'envoie automatisé d'attestation Navigo est validée. " \
           "Vous receverais dorenavant par email votre attestation Navigo avec le service RH en copie."
    subject = "Confirmation d'inscription au service Navigogo"
    return body, subject
