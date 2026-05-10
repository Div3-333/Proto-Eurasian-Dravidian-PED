import numpy as np
import matplotlib.pyplot as plt

def simulate_lexical_decay(initial_vocab_size=100, years=40000, decay_rate_per_1000=0.15, trials=1000):
    """
    Simulates lexical decay over time using a Monte Carlo approach.
    
    initial_vocab_size: Number of core words (e.g., Swadesh 100).
    years: Total time span.
    decay_rate_per_1000: Probability a word is replaced every 1000 years.
    trials: Number of simulation runs to establish a distribution.
    """
    time_steps = years // 1000
    results = []
    
    for _ in range(trials):
        current_vocab = initial_vocab_size
        for _ in range(time_steps):
            # Each word has a (1 - decay_rate) chance of surviving the millennium
            survived = np.random.binomial(current_vocab, 1 - decay_rate_per_1000)
            current_vocab = survived
        results.append(current_vocab)
        
    return results

def plot_results(results, initial_vocab_size, years, decay_rate):
    plt.figure(figsize=(10, 6))
    plt.hist(results, bins=range(initial_vocab_size + 1), alpha=0.7, color='blue', edgecolor='black')
    plt.title(f"Lexical Survival Distribution after {years} Years\n(Initial: {initial_vocab_size}, Decay Rate: {decay_rate}/1k years)")
    plt.xlabel("Number of Surviving Words")
    plt.ylabel("Frequency (Trials)")
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('docs/lexical_decay_simulation.png')
    # plt.show() # Can't show in CLI, save to file

if __name__ == "__main__":
    initial_size = 100 
    y = 40000
    rates = [0.15, 0.05, 0.02] 
    
    print(f"Starting Multi-Rate Simulation: {initial_size} words, {y} years\n")
    
    for rate in rates:
        print(f"--- Decay Rate: {rate}/1k years ---")
        sim_results = simulate_lexical_decay(initial_size, y, rate)
        mean_survival = np.mean(sim_results)
        prob_nonzero = np.mean(np.array(sim_results) > 0) * 100
        
        print(f"Mean Surviving Words: {mean_survival:.2f}")
        print(f"Probability of >0 Survivors: {prob_nonzero:.1f}%")
        print(f"Max Surviving in Trials: {max(sim_results)}\n")
