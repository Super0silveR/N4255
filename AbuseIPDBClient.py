# AbuseIPDBClient.py

# ajout de Socket pour récuperer une adresse ip a partir d'un nom
# de domaine
import socket

# ajout de json afin de traduire notre reponse string en dictionaire
# pour faciliter l'accès aux données
import json
from BaseClient import BaseClient


class AbuseIPDBClient(BaseClient):
    def __init__(self, base_url: str, api_key: str):
        self._base_url = base_url
        self._api_key = api_key

    def check_reputation(self, ip: str = None, domain: str = None):
        # Cas de base sans ip et sans domaine
        if ip == domain == None:
            raise SyntaxError  ## TODO

        if not ip == None:
            response = self.http_request(
                method="GET",
                params={"ipAddress": ip},
                headers={"Accept": "application/json", "Key": self._api_key},
                verify_ssl=True,
            )

        if not domain == None:
            domainIp = socket.gethostbyname(domain)
            response = self.http_request(
                method="GET",
                params={"ipAddress": domainIp},
                headers={"Accept": "application/json", "Key": self._api_key},
                verify_ssl=True,
            )

        if response.ok:
            decodedResponse = json.loads(response.text)
            return decodedResponse["data"]["abuseConfidenceScore"]
        else:
            raise SyntaxError  ## TODO
