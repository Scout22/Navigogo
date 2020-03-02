import requests
import re

REGEX_CSRF_TOKEN_ATTESTATION = r'name="attestation\[_token\]" value="(.*)"'

NAVIGO_URL = "https://www.jegeremacartenavigo.fr/attestation/"


def _check_response_valid_user_token(session):
    token_valid = True
    user_id_valid = True
    if session.status_code != 200:
        user_id_valid = False
    if session.headers["Set-Cookie"].startswith("wasLogged=deleted"):
        token_valid = False
    return token_valid, user_id_valid


def check_user_id_and_token(user_id, token):
    cookies = {
        'REMEMBERME': token
    }
    session = requests.session()
    response = session.get(NAVIGO_URL + str(user_id), cookies=cookies)

    return _check_response_valid_user_token(response)


def download_attestation(user_id, token, destination_path, month, year):
    cookies = {
        'REMEMBERME': token
    }

    session = requests.session()
    response = session.get(NAVIGO_URL + str(user_id), cookies=cookies)
    token_valid, user_valid = _check_response_valid_user_token(response)

    if not token_valid:
        raise AttributeError("Token is invalid")

    if not user_valid:
        raise AttributeError("User id provided is invalid")

    attestation_token = re.findall(REGEX_CSRF_TOKEN_ATTESTATION, response.text)

    data = {
        'attestation[moisDebut]': str(month),
        'attestation[anneeDebut]': str(year),
        'attestation[moisFin]': str(month),
        'attestation[anneeFin]': str(year),
        'attestation[_token]': attestation_token
    }

    response2 = session.post(NAVIGO_URL + 'attestation.pdf', cookies=cookies, data=data)
    if not response2.text.startswith("%PDF-1.4"):
        raise AttributeError(f"No attestation found for the {month}/{year}")

    with open(destination_path, 'wb') as f:
        f.write(response2.content)
