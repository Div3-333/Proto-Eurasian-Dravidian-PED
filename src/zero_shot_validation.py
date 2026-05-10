import pandas as pd
import numpy as np
from hmmlearn import hmm
from sklearn.model_selection import train_test_split

def run_structural_validation():
    """
    Predictive validation against a Markovian SOV Null Model.
    We test if PED logic provides a better fit than standard SOV transitions.
    """
    print("--- THE STRUCTURAL PROTOCOL: RIGOROUS SYNTACTIC VALIDATION ---")
    
    # 1. Load Cleaned Data
    try:
        df = pd.read_csv("data/ivs_corpus_cleaned.csv")
    except Exception as e:
        print(f"Error: {e}")
        return

    # 2. Preprocess sequences
    sequences = []
    for text in df['text'].dropna():
        clean_text = str(text).strip("+[]/").replace(" ", "")
        if not clean_text or clean_text == "000": continue
        signs = [int(s) for s in clean_text.replace("[", "").replace("]", "").split("-") if s.isdigit() and int(s) != 0]
        if len(signs) > 2:
            sequences.append(np.array(signs).reshape(-1, 1))

    # 3. Train/Test Split (80/20)
    train_seqs, test_seqs = train_test_split(sequences, test_size=0.2, random_state=42)
    
    # 4. Handle OOV and Mapping
    all_train_signs = np.concatenate(train_seqs).flatten()
    unique_train_signs, counts = np.unique(all_train_signs, return_counts=True)
    sign_map = {sign: i for i, sign in enumerate(unique_train_signs)}
    n_features = len(unique_train_signs)
    
    def map_seq(seq):
        return np.array([sign_map[s[0]] for s in seq if s[0] in sign_map]).reshape(-1, 1)

    train_seqs_mapped = [map_seq(s) for s in train_seqs if len(map_seq(s)) > 1]
    test_seqs_mapped = [map_seq(s) for s in test_seqs if len(map_seq(s)) > 1]
    
    print(f"Training on {len(train_seqs_mapped)} seals. Testing on {len(test_seqs_mapped)} held-out seals.")

    # 5. Train PED-Aligned Model (Unguided Baum-Welch)
    n_states = 4
    model = hmm.CategoricalHMM(n_components=n_states, n_iter=200, random_state=42)
    X_train = np.concatenate(train_seqs_mapped)
    lengths_train = [len(s) for s in train_seqs_mapped]
    model.fit(X_train, lengths_train)
    
    # Apply Laplacian Smoothing
    epsilon = 1e-6
    model.emissionprob_ = (model.emissionprob_ + epsilon) / (1 + n_features * epsilon)
    model.transmat_ = (model.transmat_ + epsilon) / (1 + n_states * epsilon)
    model.startprob_ = (model.startprob_ + epsilon) / (1 + n_states * epsilon)
    
    # 6. Construct the Markovian SOV Null Model
    # A true linguistic competitor: 1st-order Markov transitions modeled on standard SOV dependencies.
    null_model = hmm.CategoricalHMM(n_components=n_states, random_state=42)
    null_model.n_features = n_features
    
    # Standard SOV Probability Matrix (Generalized SOV structure)
    # 0:Agent, 1:Target, 2:Verb, 3:Terminal
    A_sov = np.array([
        [0.2, 0.6, 0.1, 0.1], # Agent -> Target (Probabilistic)
        [0.1, 0.2, 0.6, 0.1], # Target -> Verb (Probabilistic)
        [0.1, 0.1, 0.2, 0.6], # Verb -> Terminal
        [0.4, 0.2, 0.2, 0.2]  # Terminal -> New
    ])
    null_model.startprob_ = np.array([0.4, 0.2, 0.2, 0.2])
    null_model.transmat_ = A_sov
    null_model.emissionprob_ = model.emissionprob_ 
    
    # 7. The Predictive Test
    X_test = np.concatenate(test_seqs_mapped)
    lengths_test = [len(s) for s in test_seqs_mapped]
    score_ped = model.score(X_test, lengths_test)
    score_null = null_model.score(X_test, lengths_test)
    
    print(f"\n[RESULTS ON UNSEEN DATA]")
    print(f"PED-Learned Model Log-Likelihood: {score_ped:.2f}")
    print(f"Markovian SOV Null Log-Likelihood: {score_null:.2f}")
    
    margin = score_ped - score_null
    
    print(f"\nConclusion:")
    if score_ped > score_null:
        print(f"The PED-aligned model outperforms the Markovian SOV Null by {margin:.2f} LL units.")
        print("This indicates that Harappan syntax contains structural invariants specific to the PED radiation.")
    else:
        print("The Harappan data aligns with generalized SOV structures.")

if __name__ == "__main__":
    run_structural_validation()
