def process_hiu_on_init_callback(callback_data: dict) -> tuple[dict, int]:
    """API 5.3.8: Process the incoming On-Init webhook from ABDM."""
    
    print("\n" + "="*60)
    print("📲 ABDM WEBHOOK RECEIVED: /on-init (OTP Session Ready)")
    print("="*60)
    
    print(f"Transaction ID: {callback_data.get('transactionId')}")
    print(f"Original Request ID: {callback_data['response'].get('requestId')}")
    print("-" * 60)
    
    if "link" in callback_data:
        link_data = callback_data["link"]
        meta_data = link_data.get("meta", {})
        print("✅ SUCCESS: Patient needs to verify identity.")
        print(f"Auth Type: {link_data.get('authenticationType')}")
        print(f"Method   : {meta_data.get('communicationMedium')} ({meta_data.get('communicationHint')})")
        print(f"Ref No   : {link_data.get('referenceNumber')}")
    elif "error" in callback_data:
        err_data = callback_data["error"]
        print(f"❌ ERROR: {err_data.get('code')} - {err_data.get('message')}")
        
    print("="*60 + "\n")
    
    # As per documentation, return an empty payload and a 202 Accepted status
    return {}, 202