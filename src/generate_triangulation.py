import os
import random

def get_primary_data():
    # Primary attested forms from the oldest "Daughter" strata
    # No more Protos as "facts". We use the actual recorded words.
    data = {
        "tree/wood": {
            "Vedic": "dāru", 
            "Old_Tamil": "tāram", 
            "Old_Tibetan": "shing", 
            "PED_Candidate": "*T'ar-"
        },
        "to point/show": {
            "Vedic": "diś-", 
            "Old_Tamil": "tikku", 
            "Old_Tibetan": "thig", 
            "PED_Candidate": "*T'ik-"
        },
        "water": {
            "Vedic": "ud-an-", 
            "Old_Tamil": "nīr", 
            "Old_Tibetan": "chu", 
            "PED_Candidate": "*T'uH-"
        },
        "to be": {
            "Vedic": "as-ti", 
            "Old_Tamil": "iru-", 
            "Old_Tibetan": "yod", 
            "PED_Candidate": "*es-"
        },
        "eye/see": {
            "Vedic": "akṣi", 
            "Old_Tamil": "kaṇ", 
            "Old_Tibetan": "mig", 
            "PED_Candidate": "*K'en-"
        }
    }
    return data

def generate_triangulation_report():
    out_dir = "docs/triangulation"
    os.makedirs(out_dir, exist_ok=True)
    
    with open(f"{out_dir}/methodology.tex", "w", encoding="utf-8") as f:
        f.write(r"""\chapter{The Triangulation Methodology: Escaping Circularity}
\section{The Primary Data Mandate}
To resolve the critique of 'circular reconstruction,' we abandon reliance on Proto-Indo-European (PIE) or Proto-Dravidian (PD) abstractions. Instead, we anchor our PED reconstruction directly in the earliest attested literary strata of Eurasia:
\begin{itemize}
    \item \textbf{Vedic Sanskrit (c. 1500 BCE):} The \textit{Rigveda} provides our Western anchor.
    \item \textbf{Old Tamil (c. 300 BCE):} The \textit{Caṅkam} literature provides our Southern anchor.
    \item \textbf{Old Tibetan (c. 700 CE):} The Dunhuang manuscripts provide our Eastern anchor.
\end{itemize}

\section{Trans-Disciplinary Convergence}
We move beyond linguistics by integrating independent data streams. The PED signal is verified only when three conditions are met:
\begin{enumerate}
    \item \textbf{Phonological Fit:} The Vedic, Tamil, and Tibetan forms follow the Glottalic Shift Law.
    \item \textbf{Genetic Proxy:} High-density occurrences of the R1a/L-M20/O-M175 haplogroup clusters in the Altai-Pamir corridor.
    \item \textbf{Archaeological Horizon:} Correlation with the Upper Paleolithic 'micro-blade' cultural expansion (35,000--40,000 BP).
\end{enumerate}

\section{The Non-Linear Signal Detection}
We utilize a 'Holographic' model of reconstruction. Rather than a tree-branch (Stammbaum), we treat the primary data as reflections of a single source. If Vedic \textit{dāru} and Tamil \textit{tāram} point to a shared ejective \textit{*T'}, and this coincides with Altai archaeological strata, the probability of 'random noise' vanishes.
""")

if __name__ == "__main__":
    generate_triangulation_report()
    print("Triangulation methodology generated in docs/triangulation/")
