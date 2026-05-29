import uuid
import requests

from milestone2.utils import get_abdm_timestamp, get_abdm_access_token

def link_facility_service(payload_data: dict) -> tuple[dict, int]:
    # ✅ URL provided in your documentation
    api_url = "https://apihspsbx.abdm.gov.in/v4/int/v1/bridges/MutipleHRPAddUpdateServices"

    access_token = get_abdm_access_token()
    if not access_token:
        return {"error": "Gateway token missing. Please run the Auth Token API first."}, 401

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp()
    }

    try:
        # Pass the fully validated dictionary directly to json
        res = requests.post(api_url, headers=headers, json=payload_data)
        
        if res.text:
            return res.json(), res.status_code
        return {"message": "Facility linked successfully"}, res.status_code
        
    except requests.exceptions.RequestException as e:
        return {"error": "Failed to connect to ABDM", "details": str(e)}, 503