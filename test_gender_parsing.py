"""Test gender percentage parsing in persona generator"""
import re

def test_gender_parsing():
    """Test various gender input formats"""
    
    test_cases = [
        "Gender: Male (51.24%), Female (48.76%)",
        "Male (51.24%), Female (48.76%)",
        "Male: 51.24%, Female: 48.76%",
        "Gender distribution: Male 51.24%, Female 48.76%",
        "51.24% Male, 48.76% Female",
    ]
    
    print("Testing gender percentage extraction:")
    print("=" * 60)
    
    for test_input in test_cases:
        print(f"\nInput: {test_input}")
        
        gender_str = test_input.lower()
        male_match = re.search(r'male[:\s]*\(?(\d+\.?\d*)\s*%', gender_str, re.IGNORECASE)
        female_match = re.search(r'female[:\s]*\(?(\d+\.?\d*)\s*%', gender_str, re.IGNORECASE)
        
        if male_match and female_match:
            male_pct = float(male_match.group(1)) / 100.0
            female_pct = float(female_match.group(1)) / 100.0
            
            # Normalize
            total = male_pct + female_pct
            if total > 0:
                male_pct = male_pct / total
                female_pct = female_pct / total
            
            print(f"  ✅ Extracted: Male={male_pct:.4f} ({male_pct*100:.2f}%), Female={female_pct:.4f} ({female_pct*100:.2f}%)")
        else:
            print(f"  ❌ Could not extract percentages")
            if male_match:
                print(f"     Male found: {male_match.group(1)}%")
            if female_match:
                print(f"     Female found: {female_match.group(1)}%")
    
    print("\n" + "=" * 60)
    print("Test complete!")

if __name__ == "__main__":
    test_gender_parsing()
