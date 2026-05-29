import uuid
import requests
from milestone2.utils import get_abdm_timestamp

def get_openid_configuration_service() -> tuple[dict, int]:
    """API 3.2.2: Fetches OpenID configuration (JWKS URI)."""
    
    api_url = "https://dev.abdm.gov.in/api/hiecm/gateway/v3/.well-known/openid-configuration"

    headers = {
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "X-CM-ID": "sbx"
    }

    try:
        res = requests.get(api_url, headers=headers)
        
        # Safe JSON parsing
        if res.text:
            try:
                return res.json(), res.status_code
            except ValueError:
                return {"abdm_raw_response": res.text}, res.status_code
        return {"message": "Empty response"}, res.status_code

    except requests.exceptions.RequestException as e:
        return {"error": "Failed to connect to ABDM", "details": str(e)}, 503


def get_keycloak_certs_service() -> tuple[dict, int]:
    """API 3.2.3: Fetches the public Keycloak Certificates (RSA Keys)."""
    
    api_url = "https://dev.abdm.gov.in/api/hiecm/gateway/v3/certs"

    headers = {
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "X-CM-ID": "sbx"
    }

    try:
        res = requests.get(api_url, headers=headers)
        
        # Safe JSON parsing
        if res.text:
            try:
                return res.json(), res.status_code
            except ValueError:
                return {"abdm_raw_response": res.text}, res.status_code
        return {"message": "Empty response"}, res.status_code

    except requests.exceptions.RequestException as e:
        return {"error": "Failed to connect to ABDM", "details": str(e)}, 503