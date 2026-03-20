def run_full_validation(extracted_data, target_data):
    print("\n" + "="*40)
    print("RAPORT WALIDACJI DANYCH:")
    print("="*40)
    
    if "error" in extracted_data:
        print(f"BŁĄD: {extracted_data['error']}")
        return

    correct_fields = 0
    
    for key, target_val in target_data.items():
        extracted_val = extracted_data.get(key)
        is_correct = str(extracted_val).strip() == str(target_val).strip()
        
        status = "OK" if is_correct else f"BŁĄD (Oczekiwano: {target_val}, AI: {extracted_val})"
        if is_correct: 
            correct_fields += 1
            
        print(f"{key:15}: {status}")

    accuracy = (correct_fields / len(target_data)) * 100
    print("-" * 40)
    print(f"OGÓLNA POPRAWNOŚĆ: {accuracy:.2f}%")