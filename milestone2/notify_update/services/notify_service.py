import uuid
import requests
from milestone2.utils import get_abdm_timestamp, get_abdm_access_token

def notify_update_service(payload_data: dict, hip_id: str) -> tuple[dict, int]:
    """API 4.3.6: Notify ABDM about an updated health record."""
    api_url = "https://dev.abdm.gov.in/api/hiecm/hip/v3/link/context/notify"

    access_token = get_abdm_access_token()
    if not access_token:
        return {"error": "Gateway token missing."}, 401

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "X-CM-ID": "sbx",
        "X-HIP-ID": hip_id
    }

    try:
        res = requests.post(api_url, headers=headers, json=payload_data)
        
        # Bulletproof JSON parsing
        if res.text:
            try:
                return res.json(), res.status_code
            except ValueError:
                return {"abdm_raw_response": res.text}, res.status_code
                
        return {"message": "Notification sent (ABDM returned empty 202 response)"}, res.status_code

    except requests.exceptions.RequestException as e:
        return {"error": "Failed to connect to ABDM", "details": str(e)}, 503