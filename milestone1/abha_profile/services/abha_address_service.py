import uuid
import requests
from datetime import datetime, timezone

def get_abdm_timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

# =========================================================
# ✅ 6A: GET ABHA SUGGESTIONS
# =========================================================
def get_abha_suggestions(txn_id, auth_header):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/suggestion"

    # ABDM uniquely requires the txnId in the HEADERS for this GET request
    headers = {
        "Transaction_Id": str(txn_id),
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header
    }

    print("GET SUGGESTIONS HEADERS:", headers)

    response = requests.get(url=url, headers=headers)

    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        response_data = {"error": "Non-JSON response", "details": response.text}

    print("GET SUGGESTIONS RESPONSE:", response_data)

    return {
        "status_code": response.status_code,
        "data": response_data
    }

# =========================================================
# ✅ 6B: CREATE CUSTOM ABHA ADDRESS
# =========================================================
def create_abha_address(txn_id, abha_address, auth_header):
    url = "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/abha-address"

    headers = {
        "Content-Type": "application/json",
        "REQUEST-ID": str(uuid.uuid4()),
        "TIMESTAMP": get_abdm_timestamp(),
        "Authorization": auth_header
    }

    payload = {
        "txnId": str(txn_id),
        "abhaAddress": str(abha_address),
        "preferred": 1
    }

    print("CREATE ABHA PAYLOAD:", payload)

    response = requests.post(url=url, json=payload, headers=headers)

    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        response_data = {"error": "Non-JSON response", "details": response.text}

    print("CREATE ABHA RESPONSE:", response_data)

    return {
        "status_code": response.status_code,
        "data": response_data
    }