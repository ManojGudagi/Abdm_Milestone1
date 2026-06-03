import uuid
import requests
from milestone2.utils import get_abdm_timestamp, get_abdm_access_token

def send_sms_notification_service(notification_data: dict) -> tuple[dict, int]:
    """API 4.3.8: Send an SMS notification to the patient."""
    api_url = "https://dev.abdm.gov.in/api/hiecm/hip/v3/link/patient/links/sms/notify2"

    access_token = get_abdm_access_token()
    if not access_token:
        return {"error": "Gateway token missing."}, 401

    # Generate these once so they match in both headers and body
    req_id = str(uuid.uuid4())
    timestamp = get_abdm_timestamp()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "REQUEST-ID": req_id,
        "TIMESTAMP": timestamp,
        "X-CM-ID": "sbx"
    }

    # ✅ Build the exact root payload required by ABDM
    payload = {
        "requestId": req_id,
        "timestamp": timestamp,
        "notification": notification_data
    }

    try:
        res = requests.post(api_url, headers=headers, json=payload)
        
        # Bulletproof JSON parsing
        if res.text:
            try:
                return res.json(), res.status_code
            except ValueError:
                return {"abdm_raw_response": res.text}, res.status_code
                
        return {"message": "SMS Notification triggered successfully (ABDM returned empty 202)"}, res.status_code

    except requests.exceptions.RequestException as e:
        return {"error": "Failed to connect to ABDM", "details": str(e)}, 503