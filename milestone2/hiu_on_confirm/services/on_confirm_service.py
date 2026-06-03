def process_hiu_on_confirm_callback(callback_data: dict) -> tuple[dict, int]:
    """API 5.3.12: Process the incoming On-Confirm webhook from ABDM."""
    
    print("\n" + "="*60)
    print("🎉 ABDM WEBHOOK RECEIVED: /on-confirm (Records Linked!)")
    print("="*60)
    
    print(f"Original Request ID: {callback_data['response'].get('requestId')}")
    print("-" * 60)
    
    patients = callback_data.get("patient", [])
    for p in patients:
        print(f"Link Reference : {p.get('referenceNumber')}")
        print(f"Record Type    : {p.get('hiType')} (Count: {p.get('count')})")
        
        print("Confirmed Care Contexts:")
        for cc in p.get('careContexts', []):
            print(f"  -> Context Ref: {cc.get('referenceNumber')} | Display: {cc.get('display')}")
            
    print("="*60 + "\n")
    
    # As per documentation, return an empty payload and a 202 Accepted status
    return {}, 202