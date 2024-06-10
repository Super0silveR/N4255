# BaseClient.py

import requests


class BaseClient(object):
    def __init__(self, base_url: str, headers: dict = {}):
        self._base_url = base_url
        self._headers = headers

    # Ajouts de Params en tant que parametre de la fonction
    def http_request(
        self,
        method: str,
        json_body: dict = {},
        params: dict = {},
        headers: dict = {},
        verify_ssl: bool = False,
    ):

        response = requests.request(
            method=method,
            url=self._base_url,
            params=params,
            json=json_body,
            headers=headers,
            verify=verify_ssl,
        )

        return response
