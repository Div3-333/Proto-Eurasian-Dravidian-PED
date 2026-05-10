import random
import math

def calculate_alignment_probability(num_roots=2000, matches_found=15, phoneme_inventory_size=20, families=3):
    """
    Calculates the probability of finding a specific phonetic alignment 
    across multiple language families by pure chance.
    
    num_roots: Size of the lexical pool being compared.
    matches_found: Number of successful alignments observed.
    phoneme_inventory_size: Number of possible phonemes in each slot.
    families: Number of families being compared.
    """
    # Probability that a single root matches a specific sound law across N families
    # For a 3-way match, we need the 1st family to have a phoneme, and the 
    # 2nd and 3rd to follow a specific rule (1/inventory_size for each).
    p_match = (1 / phoneme_inventory_size) ** (families - 1)
    
    # Binomial distribution: Probability of getting at least 'matches_found' successes
    # We use a Poisson approximation for small p and large n
    mu = num_roots * p_match
    
    # Cumulative probability P(X >= matches_found)
    prob_chance = 0
    for k in range(matches_found, 100): # Summing up to a reasonable cap
        prob_chance += (mu**k * math.exp(-mu)) / math.factorial(k)
        
    return prob_chance

if __name__ == "__main__":
    # Parameters based on our research
    POOL_SIZE = 2000  # Number of potential proto-roots scanned
    MATCHES = 15     # Number of Glottalic Shift matches we identified
    PHONEMES = 25    # Estimated size of the consonant inventory
    FAMILIES = 3     # PIE, PD, PST
    
    print("--- Bayesian Phonetic Alignment Test ---")
    print(f"Lexical Pool: {POOL_SIZE} roots")
    print(f"Matches Observed: {MATCHES}")
    print(f"Phoneme Inventory: {PHONEMES}")
    print(f"Families Compared: {FAMILIES}\n")
    
    p_value = calculate_alignment_probability(POOL_SIZE, MATCHES, PHONEMES, FAMILIES)
    
    print(f"Probability of matches occurring by chance (p-value): {p_value:.6f}")
    
    if p_value < 0.05:
        print("RESULT: Statistically Significant (p < 0.05)")
    if p_value < 0.01:
        print("RESULT: Highly Significant (p < 0.01)")
    if p_value < 0.001:
        print("RESULT: Extremely Significant (p < 0.001)")
    else:
        print("RESULT: Not Significant. Likely coincidental.")
