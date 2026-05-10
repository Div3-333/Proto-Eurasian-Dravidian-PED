import numpy as np

def simulate_lexical_decay(initial_vocab_size, years, decay_rate_per_1000, trials=1000):
    time_steps = years // 1000
    results = []
    for _ in range(trials):
        current_vocab = initial_vocab_size
        for _ in range(time_steps):
            survived = np.random.binomial(current_vocab, 1 - decay_rate_per_1000)
            current_vocab = survived
        results.append(current_vocab)
    return results

if __name__ == "__main__":
    np.random.seed(42) # For reproducibility
    initial_size = 100 
    y = 40000
    
    print("======================================================")
    print("MONTE CARLO SURVIVAL LOGS: DEICTICS & CORE (2% DECAY)")
    print("======================================================")
    print(f"Initial Vocabulary: {initial_size} words")
    print(f"Time Horizon: {y} years")
    print(f"Decay Rate: 2% (0.02) per millennium\n")
    
    # 2% Decay Rate (Deictics/Ultra-Conservative)
    sim_results = simulate_lexical_decay(initial_size, y, 0.02, trials=5000)
    
    mean_survival = np.mean(sim_results)
    prob_nonzero = np.mean(np.array(sim_results) > 0) * 100
    prob_above_40 = np.mean(np.array(sim_results) >= 40) * 100
    
    print("--- RAW TRIAL OUTPUT (First 20 runs) ---")
    for i in range(20):
        print(f"Trial {i+1:02d}: {sim_results[i]} words survived.")
    
    print("\n--- STATISTICAL SUMMARY ---")
    print(f"Mean Surviving Words: {mean_survival:.2f} out of {initial_size}")
    print(f"Probability of retaining at least 1 word: {prob_nonzero:.2f}%")
    print(f"Probability of retaining 40+ words: {prob_above_40:.2f}%")
    
    # 15% Decay Rate (Standard Nouns / Control)
    print("\n--- CONTROL: STANDARD NOUNS (15% DECAY) ---")
    control_results = simulate_lexical_decay(initial_size, y, 0.15, trials=5000)
    mean_control = np.mean(control_results)
    print(f"Mean Surviving Words: {mean_control:.4f} out of {initial_size}")
