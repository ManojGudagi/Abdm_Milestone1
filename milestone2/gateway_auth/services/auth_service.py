import uuid
import requests

# ✅ Clean absolute import starting from the milestone2 folder
from milestone2.utils import get_abdm_timestamp

def generate_gateway_token_service(client_id: str, client_secret: str) -> tuple[dict, int]:
    url = "https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions"
    
    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "X-CM-ID": "sbx"
    }

    payload = {
        "clientId": client_id,
        "clientSecret": client_secret,
        "grantType": "client_credentials"
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        return res.json(), res.status_code
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to connect to ABDM", "details": str(e)}, 503