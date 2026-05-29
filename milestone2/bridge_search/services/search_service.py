import uuid
import requests
from milestone2.utils import get_abdm_timestamp, get_abdm_access_token

def find_bridge_by_service_id(service_id: str) -> tuple[dict, int]:
    """API 3.2.6: Fetches bridge details for a specific service ID."""
    
    api_url = f"https://dev.abdm.gov.in/api/hiecm/gateway/v3/bridge-service/serviceId/{service_id}"

    access_token = get_abdm_access_token()
    if not access_token:
        return {"error": "Gateway token missing. Please run the Auth Token API first."}, 401

    headers = {
        "Authorization": f"Bearer {access_token}",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "X-CM-ID": "sbx"
    }

    try:
        res = requests.get(api_url, headers=headers)
        
        # ✅ BULLETPROOF JSON PARSING
        if res.text:
            try:
                return res.json(), res.status_code
            except ValueError:
                return {"abdm_raw_response": res.text}, res.status_code
                
        return {"message": "ABDM returned an empty response"}, res.status_code

    except requests.exceptions.RequestException as e:
        return {"error": "Failed to connect to ABDM", "details": str(e)}, 503


def find_services_by_bridge_id() -> tuple[dict, int]:
    """API 3.2.7: Fetches all service IDs linked to your authenticated Bridge."""
    
    api_url = "https://dev.abdm.gov.in/api/hiecm/gateway/v3/bridge-services"

    access_token = get_abdm_access_token()
    if not access_token:
        return {"error": "Gateway token missing. Please run the Auth Token API first."}, 401

    headers = {
        "Authorization": f"Bearer {access_token}",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "X-CM-ID": "sbx"
    }

    try:
        res = requests.get(api_url, headers=headers)
        
        # ✅ BULLETPROOF JSON PARSING
        if res.text:
            try:
                return res.json(), res.status_code
            except ValueError:
                return {"abdm_raw_response": res.text}, res.status_code
                
        return {"message": "ABDM returned an empty response"}, res.status_code

    except requests.exceptions.RequestException as e:
        return {"error": "Failed to connect to ABDM", "details": str(e)}, 503