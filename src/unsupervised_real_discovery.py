import numpy as np
from sklearn.decomposition import PCA

ASJP = {
    'a': 'a', 'e': 'a', 'i': 'i', 'o': 'o', 'u': 'u',
    'p': 'p', 'b': 'p', 'f': 'p', 'v': 'p',
    't': 't', 'd': 't', 'th': 't',
    'k': 'k', 'g': 'k', 'kh': 'k',
    's': 's', 'z': 's', 'sh': 's', 'c': 's', 'j': 's',
    'm': 'm', 'n': 'n', 'ng': 'n', 'ny': 'n',
    'r': 'r', 'l': 'l', 'y': 'y', 'h': 'h'
}

def encode_asjp(word):
    res = ""
    for char in word:
        res += ASJP.get(char, char)
    return res

def levenshtein_dist(s1, s2):
    s1, s2 = encode_asjp(s1), encode_asjp(s2)
    if len(s1) < len(s2): return levenshtein_dist(s2, s1)
    if len(s2) == 0: return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1] / max(len(s1), len(s2))

def calculate_mean_distance(sets):
    dists = []
    for v, ta, ti in sets:
        dists.append((levenshtein_dist(v, ta) + levenshtein_dist(ta, ti) + levenshtein_dist(v, ti)) / 3)
    return np.mean(dists)

def run_hardened_unsupervised_discovery():
    print("--- PHASE 1: HARDENED PHONETIC CLUSTERING (WHOLE WORD ASJP) ---")
    
    cognates = [
        ("aham", "yan", "nga"), ("tvam", "ni", "khyod"), ("vayam", "nam", "nged"),
        ("idam", "itu", "di"), ("tat", "atu", "de"), ("aksi", "kan", "mig"),
        ("karna", "cevi", "rna"), ("bhar", "peru", "phar"), ("eka", "onru", "gcig"),
        ("dva", "irantu", "gnyis"), ("mahat", "peru", "che"), ("tvac", "tol", "pags"),
        ("gam", "cel", "khye"), ("matsya", "min", "nya"), ("naman", "namam", "ming")
    ]
    
    controls = [
        ("vaca", "ay", "kha"), ("nam", "vel", "po"), ("raj", "per", "la"),
        ("div", "ari", "na"), ("kal", "un", "du"), ("agni", "ti", "me"),
        ("matr", "ammu", "ma"), ("dasa", "tek", "bcu"), ("svas", "ak", "lo"),
        ("pada", "kai", "rkang"), ("dant", "pal", "so"), ("nas", "muku", "sna"),
        ("sth", "nil", "sdod"), ("bhu", "pul", "byed"), ("krsna", "karu", "nag")
    ]
    
    observed_cog_mean = calculate_mean_distance(cognates)
    observed_ctrl_mean = calculate_mean_distance(controls)
    observed_diff = observed_ctrl_mean - observed_cog_mean
    
    print(f"Observed Cognate Mean Dist: {observed_cog_mean:.4f}")
    print(f"Observed Control Mean Dist: {observed_ctrl_mean:.4f}")
    print(f"Observed Effect Size (Delta): {observed_diff:.4f}")

    print("\nRunning 10,000 permutations...")
    all_sets = cognates + controls
    combined_dist_pool = [ (levenshtein_dist(v, ta) + levenshtein_dist(ta, ti) + levenshtein_dist(v, ti))/3 for v, ta, ti in all_sets ]
    
    np.random.seed(42)
    count_extreme = 0
    N_perm = 10000
    N_cog = len(cognates)
    for _ in range(N_perm):
        shuffled = np.random.permutation(combined_dist_pool)
        perm_diff = np.mean(shuffled[N_cog:]) - np.mean(shuffled[:N_cog])
        if perm_diff >= observed_diff: count_extreme += 1
            
    p_value = count_extreme / N_perm
    print(f"Empirical P-Value: {p_value:.4f}")
    
    pca = PCA(n_components=2)
    manifold = np.zeros((30, 30))
    for i in range(30):
        for j in range(30):
            d = 0
            for k in range(3): d += levenshtein_dist(all_sets[i][k], all_sets[j][k])
            manifold[i, j] = d / 3
    pca.fit(manifold)
    print(f"PCA PC1 Variance: {pca.explained_variance_ratio_[0]*100:.2f}%")

if __name__ == "__main__":
    run_hardened_unsupervised_discovery()
