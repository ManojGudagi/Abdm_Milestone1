def process_on_discover_callback(callback_data: dict) -> tuple[dict, int]:
    """API 5.3.4: Process the incoming Health Record Discovery webhook from ABDM."""
    
    print("\n" + "="*60)
    print("🏥 ABDM WEBHOOK RECEIVED: /on-discover (Records Found!)")
    print("="*60)
    
    print(f"Transaction ID: {callback_data.get('transactionId')}")
    print(f"Original Request ID: {callback_data['response'].get('requestId')}")
    print("-" * 60)
    
    # Loop through the array and print the medical records found
    patients = callback_data.get('patient', [])
    for p in patients:
        print(f"Patient Ref : {p.get('referenceNumber')} ({p.get('display')})")
        print(f"Record Type : {p.get('hiType')} (Count: {p.get('count')})")
        
        for cc in p.get('careContexts', []):
            print(f"  -> Context Ref: {cc.get('referenceNumber')} | Display: {cc.get('display')}")
            
    print("="*60 + "\n")
    
    # Note: The documentation explicitly states this should return a 200 OK
    return {"message": "Discovery callback received successfully"}, 200