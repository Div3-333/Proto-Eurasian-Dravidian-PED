# import Levenshtein # Removed due to missing dependency

def apply_glottalic_shift(root, family):
    """
    Applies the Glottalic Shift Law to a PED root.
    T' -> d (PIE), t (PD), th (PST)
    K' -> g (PIE), k (PD), kh (PST)
    P' -> b (PIE), p (PD), ph (PST)
    """
    shifted = root
    if family == "PIE":
        shifted = shifted.replace("T'", "d").replace("K'", "g").replace("P'", "b")
    elif family == "PD":
        shifted = shifted.replace("T'", "t").replace("K'", "k").replace("P'", "p")
    elif family == "PST":
        shifted = shifted.replace("T'", "th").replace("K'", "kh").replace("P'", "ph")
    return shifted

def simulate_numeral_evolution():
    # Proposed PED Numerals (The "Deep Binary/Quinary" layer)
    ped_numerals = {
        "1": "oK'n", 
        "2": "T'uH",
        "3": "T'er",
        "4": "K'et",
        "5": "P'en",
        "8": "oK't",
        "10": "T'eK'"
    }
    
    # Attested Proto-Reflexes (Simplified for comparison)
    attested = {
        "PIE": {"1": "oin", "2": "du", "3": "tre", "4": "kwet", "5": "pen", "8": "okt", "10": "dek"},
        "PD": {"1": "on", "2": "tu", "3": "mu", "4": "nal", "5": "cay", "8": "et", "10": "pat"},
        "PST": {"1": "it", "2": "ni", "3": "sum", "4": "li", "5": "nga", "8": "ryat", "10": "gip"}
    }
    
    print("--- PED Numeral Evolution Simulation ---\n")
    print(f"{'Num':<5} | {'PED Root':<10} | {'PIE Sim':<10} | {'PD Sim':<10} | {'PST Sim':<10}")
    print("-" * 55)
    
    for num, root in ped_numerals.items():
        pie_sim = apply_glottalic_shift(root, "PIE")
        pd_sim = apply_glottalic_shift(root, "PD")
        pst_sim = apply_glottalic_shift(root, "PST")
        
        print(f"{num:<5} | {root:<10} | {pie_sim:<10} | {pd_sim:<10} | {pst_sim:<10}")

if __name__ == "__main__":
    simulate_numeral_evolution()
