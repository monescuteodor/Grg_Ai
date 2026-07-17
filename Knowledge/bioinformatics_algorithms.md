Advanced Bioinformatics Algorithms Complete Reference
CHAPTER 1: GETTING STARTED WITH BIOINFORMATICS ALGORITHMS
Remarks
Bioinformatics algorithms solve computational problems in biology, focusing on sequence analysis, structural prediction, and evolutionary relationships. Key areas: Sequence alignment (global/local), String matching, Phylogenetics, Genome assembly, and Protein structure prediction. Challenges: Huge data volumes (NGS), noisy data, complex biological variations. Applications: Drug discovery, personalized medicine, evolutionary biology, agricultural genetics.
Tools: Python (Biopython, Scikit-bio), C++ (for performance-critical steps), BLAST+, Bowtie2, BWA, SPAdes, RAxML.
Hello Sequence Alignment
# hello_bioalg.py
"""
First bioinformatics algorithm: Needleman-Wunsch Global Alignment.
"""
import numpy as np

def needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=-2):
    """
    Perform global alignment using dynamic programming.
    Returns aligned sequences and score.
    """
    n = len(seq1)
    m = len(seq2)
    
    # Initialize scoring matrix
    F = np.zeros((n + 1, m + 1))
    
    # Initialize first row and column
    for i in range(n + 1):
        F[i, 0] = i * gap
    for j in range(m + 1):
        F[0, j] = j * gap
        
    # Fill matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if seq1[i-1] == seq2[j-1]:
                diag = F[i-1, j-1] + match
            else:
                diag = F[i-1, j-1] + mismatch
            up = F[i-1, j] + gap
            left = F[i, j-1] + gap
            F[i, j] = max(diag, up, left)
            
    # Traceback
    align1, align2 = [], []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and F[i, j] == F[i-1, j-1] + (match if seq1[i-1]==seq2[j-1] else mismatch):
            align1.append(seq1[i-1])
            align2.append(seq2[j-1])
            i -= 1
            j -= 1
        elif i > 0 and F[i, j] == F[i-1, j] + gap:
            align1.append(seq1[i-1])
            align2.append('-')
            i -= 1
        else:
            align1.append('-')
            align2.append(seq2[j-1])
            j -= 1
            
    return ''.join(reversed(align1)), ''.join(reversed(align2)), F[n, m]

s1 = "GATTACA"
s2 = "GCATGCU"
a1, a2, score = needleman_wunsch(s1, s2)
print(f"Seq1: {a1}")
print(f"Seq2: {a2}")
print(f"Score: {score}")

Dynamic Programming in Biology
# Used for: Alignment, RNA secondary structure prediction, Viterbi algorithm for HMMs.
# Complexity: Often O(N*M) for pairwise comparisons.

CHAPTER 2: STRING MATCHING & INDEXING
Exact Matching
# Naive: O(N*M).
# Knuth-Morris-Pratt (KMP): O(N+M). Uses failure function to skip mismatches.
# Boyer-Moore: Skips sections of text based on bad character/heuristic rules.

Approximate Matching
# Allows k mismatches or edits.
# Used in read mapping (aligning short reads to a reference genome).

Suffix Trees & Arrays
# Suffix Tree: Compressed trie of all suffixes. O(N) construction.
# Suffix Array: Sorted array of suffixes. Space-efficient alternative.
# Used for: Fast pattern searching, repeat finding, longest common substring.

Burrows-Wheeler Transform (BWT)
# Reversible transformation that groups similar characters together.
# Basis for FM-index used in Bowtie/BWA.
# Enables efficient compression and searching of large genomes.

def bwt_transform(s):
    """Compute Burrows-Wheeler Transform."""
    s += '$'  # End marker
    rotations = [s[i:] + s[:i] for i in range(len(s))]
    rotations.sort()
    return ''.join([rot[-1] for rot in rotations])

print(f"BWT of 'BANANA': {bwt_transform('BANANA')}")

CHAPTER 3: GENOME ASSEMBLY
Overlap-Layout-Consensus (OLC)
# 1. Overlap: Find overlaps between all reads.
# 2. Layout: Order reads based on overlaps.
# 3. Consensus: Derive final sequence from layout.
# Good for long reads (PacBio, Nanopore), but O(N^2) overlap step is expensive.

De Bruijn Graphs
# Breaks reads into k-mers.
# Nodes: k-1 mers. Edges: k-mers.
# Eulerian path through graph reconstructs genome.
# Efficient for short reads (Illumina). Used in SPAdes, Velvet.

def build_de_bruijn(reads, k):
    """Build De Bruijn graph from reads."""
    edges = set()
    for read in reads:
        for i in range(len(read) - k + 1):
            kmer = read[i:i+k]
            prefix = kmer[:-1]
            suffix = kmer[1:]
            edges.add((prefix, suffix))
    return edges

reads = ["ATG", "TGC", "GCA", "CAT"]
k = 3
graph = build_de_bruijn(reads, k)
print(f"De Bruijn Edges: {graph}")

Assembly Challenges
# Repeats: Cause cycles in graph.
# Errors: Create bubbles/branches.
# Coverage bias: Some regions sequenced more than others.

CHAPTER 4: PHYLOGENETICS
Distance-Based Methods
# UPGMA: Assumes molecular clock (constant rate).
# Neighbor-Joining (NJ): Does not assume molecular clock. Fast, O(N^3).

Character-Based Methods
# Maximum Parsimony: Minimizes total number of changes. NP-hard.
# Maximum Likelihood (ML): Finds tree that maximizes probability of observed data. Computationally intensive.
# Bayesian Inference: Uses MCMC to sample tree space.

Bootstrapping
# Resampling columns of alignment to estimate confidence in tree branches.
# High bootstrap value (>70%) indicates robust branch.

CHAPTER 5: PROTEIN STRUCTURE PREDICTION
Homology Modeling
# Uses known structure of a homologous protein as template.
# Accurate if sequence identity >30%.

Ab Initio Prediction
# Predicts structure from physical principles alone.
# Very difficult due to vast conformational space.

Deep Learning Revolution
# AlphaFold2: Uses attention mechanisms and multiple sequence alignments (MSA).
# Achieves near-experimental accuracy.
# RoseTTAFold: Alternative deep learning architecture.

Secondary Structure Prediction
# Chou-Fasman: Statistical propensity of amino acids.
# Neural Networks: Input window of residues, output helix/sheet/coil.

CHAPTER 6: ADVANCED TOPICS AND RESOURCES
Variant Calling
# Identifying SNPs and Indels from NGS data.
# Pipeline: Alignment -> Duplicate Marking -> Base Quality Recalibration -> Variant Calling (GATK).

Metagenomics
# Analyzing genetic material from environmental samples.
# Taxonomic classification: Kraken, MetaPhlAn.
# Functional annotation: HUMAnN.

Single-Cell Analysis
# Clustering cells based on gene expression profiles.
# Dimensionality reduction: PCA, t-SNE, UMAP.
# Trajectory inference: Pseudotime analysis.

Recommended Reading
# - "Biological Sequence Analysis" by Durbin et al.
# - "Algorithms on Strings, Trees and Sequences" by Gusfield
# - "Bioinformatics Algorithms" by Jones & Pevzner
# - Biopython Tutorial: https://biopython.org/wiki/Documentation

# End of Advanced Bioinformatics Algorithms Reference