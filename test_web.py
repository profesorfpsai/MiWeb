import pytest
import requests

URL = "https://miweb-7ywr.onrender.com"

def test_pagina_responde_ok():
    response = requests.get(URL)
    assert response.status_code == 200