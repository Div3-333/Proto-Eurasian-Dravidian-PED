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
    for char in str(word).lower():
        if char in ASJP: res += ASJP[char]
    return res[:1] # SKELETAL ONSET ONLY

def levenshtein_dist(s1, s2):
    s1, s2 = encode_asjp(s1), encode_asjp(s2)
    if not s1 or not s2: return 1.0
    return 0.0 if s1 == s2 else 1.0

def calculate_mean_distance(sets):
    dists = []
    for v, ta, ti in sets:
        dists.append((levenshtein_dist(v, ta) + levenshtein_dist(ta, ti) + levenshtein_dist(v, ti)) / 3)
    return np.mean(dists)

def run_hardened_unsupervised_discovery():
    print("--- PHASE 1: SKELETAL ONSET CLUSTERING (50 ROOTS) ---")
    
    cognates = [
        ("aham", "yan", "nga"), ("tvam", "ni", "khyod"), ("vayam", "nam", "nged"),
        ("idam", "itu", "di"), ("tat", "atu", "de"), ("ka", "yar", "su"),
        ("na", "alla", "ma"), ("bahu", "pala", "mang"), ("eka", "onru", "gcig"),
        ("dva", "irantu", "gnyis"), ("tri", "munru", "gsum"), ("panca", "aintu", "lnga"),
        ("mahant", "peru", "che"), ("dirgha", "netu", "ring"), ("guru", "paru", "lci"),
        ("alpa", "ciru", "chung"), ("matr", "tay", "ma"), ("pitr", "tantai", "pha"),
        ("matsya", "min", "nya"), ("vi", "pul", "bya"), ("svan", "nay", "khyi"),
        ("yuka", "pen", "shig"), ("vrksa", "maram", "shing"), ("bija", "vittu", "sabon"),
        ("parna", "ilai", "lo"), ("mula", "ver", "rtsa"), ("tvac", "tol", "pags"),
        ("mamsa", "un", "sha"), ("asrj", "kuruti", "khrag"), ("asthi", "elumpu", "rus"),
        ("srnga", "kompu", "rwa"), ("sirsa", "talai", "mgo"), ("karna", "cevi", "rna"),
        ("aksi", "kan", "mig"), ("nasa", "mukku", "sna"), ("asya", "vay", "kha"),
        ("danta", "pal", "so"), ("jihva", "nakku", "lce"), ("pada", "kal", "rkang"),
        ("janu", "mulankal", "pus"), ("hasta", "kai", "lag"), ("udara", "vayiru", "grod"),
        ("hrdaya", "neñcu", "snying"), ("pa", "kuti", "thung"), ("ad", "un", "za"),
        ("drs", "kan", "mthong"), ("sru", "kel", "thos"), ("jña", "ari", "shes"),
        ("stha", "nil", "lang"), ("surya", "ñayiru", "nyi")
    ]
    
    controls = [
        ("vaca", "ay", "kha"), ("nam", "vel", "po"), ("raj", "per", "la"),
        ("div", "ari", "na"), ("kal", "un", "du"), ("agni", "ti", "me"),
        ("dasa", "tek", "bcu"), ("svas", "ak", "lo"), ("pada", "kai", "rkang"),
        ("krsna", "karu", "nag"), ("patha", "vazhi", "lam"), ("candra", "tinkal", "zla"),
        ("megha", "mekam", "sprin"), ("vayu", "karru", "rlung"), ("dhuma", "pukai", "du"),
        ("varsa", "malai", "char"), ("pasana", "kal", "rdo"), ("sikata", "manal", "bye"),
        ("prthivi", "man", "sa"), ("rohita", "civappu", "dmar"), ("sveta", "vellai", "dkar"),
        ("ahan", "pakal", "nyin"), ("antu", "lo", "varsa"), ("sita", "kulir", "grang"),
        ("nava", "putu", "gsar"), ("sana", "palaiya", "rnying"), ("bhadrra", "nalla", "bzang"),
        ("papa", "ketta", "ngan"), ("puti", "aluki", "rul"), ("malina", "alukku", "dri"),
        ("rju", "ner", "drang"), ("vrtta", "vattam", "zlums"), ("manda", "malu", "rtul"),
        ("ardra", "iram", "rlon"), ("suska", "varanta", "skam"), ("satya", "cari", "nor"),
        ("antika", "arukil", "nye"), ("dura", "tolai", "ring"), ("valatu", "gyas", "daksina"),
        ("itatu", "gyon", "savya"), ("punar", "mali", "yang"), ("sad", "amar", "sdod"),
        ("pat", "vilu", "bab"), ("da", "kotu", "ster"), ("grah", "piti", "dzin"),
        ("pili", "tsir", "pid"), ("mrj", "tey", "phur"), ("ksal", "ka", "khru"),
        ("krsh", "ilu", "then"), ("nud", "tallu", "phul")
    ]
    
    observed_cog_mean = calculate_mean_distance(cognates)
    observed_ctrl_mean = calculate_mean_distance(controls)
    observed_diff = observed_ctrl_mean - observed_cog_mean
    
    print(f"Observed Cognate Mean Dist: {observed_cog_mean:.4f}")
    print(f"Observed Control Mean Dist: {observed_ctrl_mean:.4f}")

    print("\nRunning 10,000 permutations...")
    all_sets = cognates + controls
    combined_dist_pool = [ (levenshtein_dist(v, ta) + levenshtein_dist(ta, ti) + levenshtein_dist(v, ti))/3 for v, ta, ti in all_sets ]
    
    np.random.seed(42)
    count_extreme = 0
    for _ in range(10000):
        shuffled = np.random.permutation(combined_dist_pool)
        if (np.mean(shuffled[50:]) - np.mean(shuffled[:50])) >= observed_diff: count_extreme += 1
            
    print(f"Empirical P-Value: {count_extreme / 10000:.4f}")
    
    pca = PCA(n_components=2)
    manifold = np.zeros((100, 100))
    for i in range(100):
        for j in range(100):
            d = 0
            for k in range(3): d += levenshtein_dist(all_sets[i][k], all_sets[j][k])
            manifold[i, j] = d / 3
    pca.fit(manifold)
    print(f"PCA PC1 Variance: {pca.explained_variance_ratio_[0]*100:.2f}%")

if __name__ == "__main__":
    run_hardened_unsupervised_discovery()
