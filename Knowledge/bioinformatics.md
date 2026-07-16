Bioinformatics & Computational Biology Complete Reference
CHAPTER 1: GETTING STARTED WITH BIOINFORMATICS
Remarks
Bioinformatics applies computational techniques to analyze biological data: DNA/RNA/protein sequences, gene expression, structures, and interactions. Key areas: sequence alignment, phylogenetics, genomics, proteomics, transcriptomics, systems biology, structural biology. Modern breakthroughs: next-generation sequencing (NGS), CRISPR, AlphaFold (protein structure prediction), single-cell genomics.
Tools: Python (Biopython, scikit-bio, PyMOL), R (Bioconductor), BLAST, Bowtie, BWA, SAMtools, GATK, ClustalW, MEGA, UCSC Genome Browser.
Hello Bioinformatics
# hello_bioinformatics.py
"""
First bioinformatics program: analyze a DNA sequence.
"""
from collections import Counter

def analyze_dna(sequence: str) -> dict:
    """Basic DNA sequence analysis."""
    sequence = sequence.upper().replace(" ", "")
    
    # Validate
    valid_bases = set("ACGTN")
    if not all(base in valid_bases for base in sequence):
        raise ValueError("Invalid DNA sequence")
    
    # Length
    length = len(sequence)
    
    # Base composition
    counts = Counter(sequence)
    composition = {base: counts[base] / length for base in "ACGT"}
    
    # GC content
    gc_content = (counts['G'] + counts['C']) / length
    
    # Reverse complement
    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N'}
    rev_comp = ''.join(complement[base] for base in reversed(sequence))
    
    # Codons (reading frame 1)
    codons = [sequence[i:i+3] for i in range(0, length - 2, 3)]
    
    # Simple ORF finding (ATG to stop codon)
    start_codon = "ATG"
    stop_codons = ["TAA", "TAG", "TGA"]
    
    orfs = []
    for frame in range(3):
        i = frame
        while i < length - 2:
            if sequence[i:i+3] == start_codon:
                # Find stop codon
                j = i + 3
                while j < length - 2:
                    if sequence[j:j+3] in stop_codons:
                        orf_length = (j + 3 - i) // 3
                        if orf_length >= 30:  # Minimum 30 codons
                            orfs.append({
                                'frame': frame,
                                'start': i,
                                'end': j + 3,
                                'length_codons': orf_length,
                                'sequence': sequence[i:j+3]
                            })
                        i = j + 3
                        break
                    j += 3
                else:
                    i += 3
            else:
                i += 3
    
    return {
        'length': length,
        'composition': composition,
        'gc_content': gc_content,
        'reverse_complement': rev_comp,
        'codons': codons[:10],  # First 10
        'orfs': orfs
    }

# Example: analyze a gene sequence
gene = """
ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG
"""

result = analyze_dna(gene)

print("=== DNA Sequence Analysis ===")
print(f"Length: {result['length']} bp")
print(f"GC content: {result['gc_content']:.2%}")
print(f"Base composition:")
for base, freq in result['composition'].items():
    print(f"  {base}: {freq:.2%}")
print(f"Reverse complement: {result['reverse_complement']}")
print(f"First 10 codons: {result['codons']}")
print(f"ORFs found: {len(result['orfs'])}")
for i, orf in enumerate(result['orfs'][:3]):
    print(f"  ORF {i+1}: frame {orf['frame']}, "
          f"position {orf['start']}-{orf['end']}, "
          f"{orf['length_codons']} codons")

Central Dogma of Molecular Biology
# DNA → RNA → Protein
# Transcription: DNA → mRNA
# Translation: mRNA → Protein

def transcribe(dna: str) -> str:
    """Convert DNA to mRNA (T → U)."""
    return dna.upper().replace('T', 'U')

def translate(mrna: str) -> str:
    """Translate mRNA to protein using standard genetic code."""
    codon_table = {
        'AUG': 'M',  # Start
        'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
        'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
        'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
        'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
        'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
        'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
        'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
        'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
        'UAU': 'Y', 'UAC': 'Y', 'UAA': '*', 'UAG': '*',  # Stop
        'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
        'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
        'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W',
        'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
        'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
        'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
    }
    
    protein = []
    for i in range(0, len(mrna) - 2, 3):
        codon = mrna[i:i+3]
        amino_acid = codon_table.get(codon, 'X')
        if amino_acid == '*':
            break  # Stop codon
        protein.append(amino_acid)
    
    return ''.join(protein)

# Example
dna = "ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG"
mrna = transcribe(dna)
protein = translate(mrna)

print(f"\n=== Central Dogma ===")
print(f"DNA:     {dna}")
print(f"mRNA:    {mrna}")
print(f"Protein: {protein}")

Biological Data Formats
# FASTA: sequence format
# >sequence_id description
# ATCGATCGATCG...

# FASTQ: sequencing reads with quality scores
# @read_id
# ATCGATCG
# +
# IIIIIIII  (Phred quality scores)

# GenBank: annotated sequence
# LOCUS       ABC123    1000 bp    DNA     linear   PLN 01-JAN-2024
# FEATURES    ...
# ORIGIN
# 1 atcgatcgat cgatcgatcg ...

# VCF: variant call format
# #CHROM POS ID REF ALT QUAL FILTER INFO
# chr1 100 . A T 30 PASS .

# BED: genomic intervals
# chr1 1000 2000 gene1

# GFF/GTF: gene annotations
# chr1 source gene 1000 2000 . + . ID=gene1

import re

def parse_fasta(fasta_text: str) -> dict:
    """Parse FASTA format into dict of {id: sequence}."""
    sequences = {}
    current_id = None
    current_seq = []
    
    for line in fasta_text.strip().split('\n'):
        line = line.strip()
        if line.startswith('>'):
            if current_id:
                sequences[current_id] = ''.join(current_seq)
            current_id = line[1:].split()[0]  # First word after >
            current_seq = []
        elif line:
            current_seq.append(line)
    
    if current_id:
        sequences[current_id] = ''.join(current_seq)
    
    return sequences

def parse_fastq(fastq_text: str) -> list:
    """Parse FASTQ format into list of reads."""
    reads = []
    lines = fastq_text.strip().split('\n')
    
    for i in range(0, len(lines), 4):
        if i + 3 < len(lines):
            read = {
                'id': lines[i][1:],  # Remove @
                'sequence': lines[i+1],
                'quality': lines[i+3]
            }
            reads.append(read)
    
    return reads

# Example FASTA
fasta_data = """
>gene1 Homo sapiens insulin
ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTGGCCCTCTGGGGACCTG
>gene2 Mus musculus insulin
ATGGCCCTGTGGATGCGCCTCCTGCCCCTGCTGGCGCTGCTGGCCCTCTGGGGACCTG
"""

sequences = parse_fasta(fasta_data)
print(f"\n=== FASTA Parsing ===")
for seq_id, seq in sequences.items():
    print(f"{seq_id}: {len(seq)} bp")
    print(f"  {seq[:50]}...")

CHAPTER 2: SEQUENCE ALIGNMENT
Global Alignment (Needleman-Wunsch)
# Align two sequences end-to-end
# Dynamic programming algorithm
# Score = match - mismatch - gap_penalty

import numpy as np

def needleman_wunsch(seq1: str, seq2: str, 
                      match_score: int = 1,
                      mismatch_score: int = -1,
                      gap_penalty: int = -2) -> tuple:
    """
    Needleman-Wunsch global alignment algorithm.
    
    Returns: (aligned_seq1, aligned_seq2, score)
    """
    n, m = len(seq1), len(seq2)
    
    # Initialize scoring matrix
    F = np.zeros((n + 1, m + 1), dtype=int)
    
    # Initialize first row and column (gap penalties)
    for i in range(n + 1):
        F[i, 0] = i * gap_penalty
    for j in range(m + 1):
        F[0, j] = j * gap_penalty
    
    # Fill matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # Match/mismatch
            if seq1[i-1] == seq2[j-1]:
                diag = F[i-1, j-1] + match_score
            else:
                diag = F[i-1, j-1] + mismatch_score
            
            # Gap in seq2 (insertion)
            up = F[i-1, j] + gap_penalty
            
            # Gap in seq1 (deletion)
            left = F[i, j-1] + gap_penalty
            
            F[i, j] = max(diag, up, left)
    
    # Traceback
    aligned1, aligned2 = [], []
    i, j = n, m
    
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            if seq1[i-1] == seq2[j-1]:
                score = match_score
            else:
                score = mismatch_score
            
            if F[i, j] == F[i-1, j-1] + score:
                aligned1.append(seq1[i-1])
                aligned2.append(seq2[j-1])
                i -= 1
                j -= 1
                continue
        
        if i > 0 and F[i, j] == F[i-1, j] + gap_penalty:
            aligned1.append(seq1[i-1])
            aligned2.append('-')
            i -= 1
        elif j > 0:
            aligned1.append('-')
            aligned2.append(seq2[j-1])
            j -= 1
    
    # Reverse (we built backwards)
    aligned1 = ''.join(reversed(aligned1))
    aligned2 = ''.join(reversed(aligned2))
    
    score = F[n, m]
    
    return aligned1, aligned2, score

# Example
seq1 = "GATTACA"
seq2 = "GCATGCU"

aligned1, aligned2, score = needleman_wunsch(seq1, seq2)

print("=== Needleman-Wunsch Global Alignment ===")
print(f"Seq1: {seq1}")
print(f"Seq2: {seq2}")
print(f"\nAlignment:")
print(f"  {aligned1}")
print(f"  {''.join('|' if a == b and a != '-' else ' ' for a, b in zip(aligned1, aligned2))}")
print(f"  {aligned2}")
print(f"\nScore: {score}")

# Calculate identity
matches = sum(1 for a, b in zip(aligned1, aligned2) if a == b and a != '-')
identity = matches / len(aligned1)
print(f"Identity: {identity:.2%} ({matches}/{len(aligned1)})")

Local Alignment (Smith-Waterman)
# Find best matching subsequences
# Allows alignment to start/end anywhere

def smith_waterman(seq1: str, seq2: str,
                   match_score: int = 2,
                   mismatch_score: int = -1,
                   gap_penalty: int = -2) -> tuple:
    """
    Smith-Waterman local alignment algorithm.
    
    Returns: (aligned_seq1, aligned_seq2, score, start1, start2)
    """
    n, m = len(seq1), len(seq2)
    
    # Initialize scoring matrix (with zeros for local alignment)
    F = np.zeros((n + 1, m + 1), dtype=int)
    
    max_score = 0
    max_pos = (0, 0)
    
    # Fill matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # Match/mismatch
            if seq1[i-1] == seq2[j-1]:
                diag = F[i-1, j-1] + match_score
            else:
                diag = F[i-1, j-1] + mismatch_score
            
            # Gap in seq2
            up = F[i-1, j] + gap_penalty
            
            # Gap in seq1
            left = F[i, j-1] + gap_penalty
            
            # Local alignment: never go below 0
            F[i, j] = max(0, diag, up, left)
            
            # Track maximum
            if F[i, j] > max_score:
                max_score = F[i, j]
                max_pos = (i, j)
    
    # Traceback from maximum
    aligned1, aligned2 = [], []
    i, j = max_pos
    
    while i > 0 and j > 0 and F[i, j] > 0:
        if seq1[i-1] == seq2[j-1]:
            score = match_score
        else:
            score = mismatch_score
        
        if F[i, j] == F[i-1, j-1] + score:
            aligned1.append(seq1[i-1])
            aligned2.append(seq2[j-1])
            i -= 1
            j -= 1
        elif F[i, j] == F[i-1, j] + gap_penalty:
            aligned1.append(seq1[i-1])
            aligned2.append('-')
            i -= 1
        else:
            aligned1.append('-')
            aligned2.append(seq2[j-1])
            j -= 1
    
    # Reverse
    aligned1 = ''.join(reversed(aligned1))
    aligned2 = ''.join(reversed(aligned2))
    
    # Calculate start positions
    start1 = i
    start2 = j
    
    return aligned1, aligned2, max_score, start1, start2

# Example: find conserved region
seq1 = "ACGTACGTACGTACGT"
seq2 = "GGGGACGTACGTTTTT"

aligned1, aligned2, score, start1, start2 = smith_waterman(seq1, seq2)

print("\n=== Smith-Waterman Local Alignment ===")
print(f"Seq1: {seq1}")
print(f"Seq2: {seq2}")
print(f"\nBest local alignment:")
print(f"  {aligned1}")
print(f"  {''.join('|' if a == b and a != '-' else ' ' for a, b in zip(aligned1, aligned2))}")
print(f"  {aligned2}")
print(f"\nScore: {score}")
print(f"Position in seq1: {start1}-{start1 + len(aligned1.replace('-', ''))}")
print(f"Position in seq2: {start2}-{start2 + len(aligned2.replace('-', ''))}")

Multiple Sequence Alignment
# Align 3+ sequences
# Progressive alignment (ClustalW-like)

def pairwise_distance(seq1: str, seq2: str) -> float:
    """Calculate distance between two sequences (1 - identity)."""
    aligned1, aligned2, _ = needleman_wunsch(seq1, seq2)
    
    matches = sum(1 for a, b in zip(aligned1, aligned2) if a == b and a != '-')
    total = len(aligned1)
    
    return 1.0 - (matches / total)

def build_distance_matrix(sequences: list) -> np.ndarray:
    """Build pairwise distance matrix."""
    n = len(sequences)
    D = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i+1, n):
            dist = pairwise_distance(sequences[i], sequences[j])
            D[i, j] = dist
            D[j, i] = dist
    
    return D

def progressive_alignment(sequences: list) -> list:
    """
    Simple progressive multiple sequence alignment.
    Aligns sequences in order of similarity.
    """
    n = len(sequences)
    
    if n == 0:
        return []
    if n == 1:
        return sequences
    
    # Build distance matrix
    D = build_distance_matrix(sequences)
    
    # Find closest pair
    min_dist = float('inf')
    min_i, min_j = 0, 1
    
    for i in range(n):
        for j in range(i+1, n):
            if D[i, j] < min_dist:
                min_dist = D[i, j]
                min_i, min_j = i, j
    
    # Align closest pair
    aligned_i, aligned_j, _ = needleman_wunsch(sequences[min_i], sequences[min_j])
    
    # Build alignment progressively
    alignment = [aligned_i, aligned_j]
    
    # Add remaining sequences
    for k in range(n):
        if k != min_i and k != min_j:
            # Align to consensus (simplified)
            consensus = ''.join(
                a if a == b else '-'
                for a, b in zip(aligned_i, aligned_j)
            )
            aligned_k, _, _ = needleman_wunsch(sequences[k], consensus)
            alignment.append(aligned_k)
    
    return alignment

# Example
sequences = [
    "GATTACA",
    "GCATGCU",
    "GATTA",
    "GCATG"
]

alignment = progressive_alignment(sequences)

print("\n=== Multiple Sequence Alignment ===")
for i, seq in enumerate(alignment):
    print(f"Seq{i+1}: {seq}")

# Calculate conservation
print("\nConservation:")
for pos in range(len(alignment[0])):
    column = [seq[pos] for seq in alignment]
    unique = len(set(column) - {'-'})
    symbol = '*' if unique == 1 else ':' if unique == 2 else ' '
    print(symbol, end='')
print()

Sequence Similarity Search (BLAST-like)
# Find similar sequences in a database
# Heuristic approach for speed

def blast_like_search(query: str, database: list, 
                      word_size: int = 3, threshold: int = 10) -> list:
    """
    Simplified BLAST-like sequence search.
    
    1. Break query into words
    2. Find exact matches in database
    3. Extend matches
    4. Report high-scoring pairs (HSPs)
    """
    hits = []
    
    # Generate all words from query
    words = [query[i:i+word_size] for i in range(len(query) - word_size + 1)]
    
    # Search database
    for db_id, db_seq in database.items():
        for word in words:
            # Find word in database sequence
            pos = db_seq.find(word)
            if pos != -1:
                # Extend alignment
                start = max(0, pos - 10)
                end = min(len(db_seq), pos + word_size + 10)
                
                db_region = db_seq[start:end]
                query_region = query[max(0, pos-10):min(len(query), pos+word_size+10)]
                
                # Score alignment
                aligned1, aligned2, score = needleman_wunsch(query_region, db_region)
                
                if score >= threshold:
                    hits.append({
                        'db_id': db_id,
                        'score': score,
                        'position': pos,
                        'alignment': (aligned1, aligned2)
                    })
    
    # Sort by score
    hits.sort(key=lambda x: x['score'], reverse=True)
    
    return hits

# Example
query = "GATTACA"
database = {
    'seq1': 'GGATTACATTT',
    'seq2': 'ACGTGATTAC',
    'seq3': 'TTTTTTTTTT',
    'seq4': 'GATTACAGATTACA',
}

hits = blast_like_search(query, database)

print("\n=== BLAST-like Search ===")
print(f"Query: {query}")
print(f"\nHits found: {len(hits)}")
for i, hit in enumerate(hits[:5]):
    print(f"\nHit {i+1}: {hit['db_id']} (score: {hit['score']})")
    print(f"  Position: {hit['position']}")
    print(f"  {hit['alignment'][0]}")
    print(f"  {hit['alignment'][1]}")

CHAPTER 3: PHYLOGENETICS
Distance-Based Methods (UPGMA)
# Build phylogenetic tree from distance matrix
# UPGMA: Unweighted Pair Group Method with Arithmetic Mean
# Assumes molecular clock (constant rate of evolution)

import numpy as np

def upgma(distance_matrix: np.ndarray, labels: list) -> dict:
    """
    UPGMA hierarchical clustering for phylogenetic tree.
    
    Returns: tree as nested dict
    """
    n = len(labels)
    
    # Initialize clusters
    clusters = {i: {'label': labels[i], 'size': 1, 'height': 0} 
                for i in range(n)}
    
    # Copy distance matrix
    D = distance_matrix.copy()
    active = set(range(n))
    
    tree = None
    
    while len(active) > 1:
        # Find minimum distance
        min_dist = float('inf')
        min_i, min_j = None, None
        
        active_list = sorted(active)
        for idx1, i in enumerate(active_list):
            for j in active_list[idx1+1:]:
                if D[i, j] < min_dist:
                    min_dist = D[i, j]
                    min_i, min_j = i, j
        
        # Merge clusters
        new_height = min_dist / 2
        
        new_cluster = {
            'left': clusters[min_i],
            'right': clusters[min_j],
            'height': new_height,
            'size': clusters[min_i]['size'] + clusters[min_j]['size']
        }
        
        # Update distance matrix
        new_idx = max(active) + 1
        D = np.pad(D, ((0, 1), (0, 1)), mode='constant')
        
        for k in active:
            if k != min_i and k != min_j:
                # Weighted average
                dist = (D[min_i, k] * clusters[min_i]['size'] + 
                       D[min_j, k] * clusters[min_j]['size']) / new_cluster['size']
                D[new_idx, k] = dist
                D[k, new_idx] = dist
        
        # Update clusters
        clusters[new_idx] = new_cluster
        active.remove(min_i)
        active.remove(min_j)
        active.add(new_idx)
        
        tree = new_cluster
    
    return tree

def print_tree(tree, indent=0):
    """Print tree structure."""
    if 'label' in tree:
        print("  " * indent + f"└─ {tree['label']}")
    else:
        print("  " * indent + f"└─ (height: {tree['height']:.3f})")
        print_tree(tree['left'], indent + 1)
        print_tree(tree['right'], indent + 1)

# Example: distance matrix for 4 species
# Human, Chimpanzee, Gorilla, Orangutan
species = ['Human', 'Chimp', 'Gorilla', 'Orangutan']

distance_matrix = np.array([
    [0.00, 0.01, 0.02, 0.05],  # Human
    [0.01, 0.00, 0.02, 0.05],  # Chimp
    [0.02, 0.02, 0.00, 0.05],  # Gorilla
    [0.05, 0.05, 0.05, 0.00],  # Orangutan
])

tree = upgma(distance_matrix, species)

print("=== UPGMA Phylogenetic Tree ===")
print_tree(tree)

Neighbor-Joining Method
# More accurate than UPGMA
# Does not assume molecular clock
# Produces unrooted tree

def neighbor_joining(distance_matrix: np.ndarray, labels: list) -> dict:
    """
    Neighbor-Joining algorithm for phylogenetic tree.
    """
    n = len(labels)
    
    if n == 2:
        return {
            'left': {'label': labels[0]},
            'right': {'label': labels[1]},
            'distance': distance_matrix[0, 1]
        }
    
    # Initialize
    D = distance_matrix.copy()
    active = list(range(n))
    nodes = {i: {'label': labels[i]} for i in range(n)}
    
    while len(active) > 2:
        # Calculate Q matrix
        r = len(active)
        Q = np.zeros((n, n))
        
        # Row sums
        row_sums = {}
        for i in active:
            row_sums[i] = sum(D[i, j] for j in active if j != i)
        
        # Fill Q matrix
        for i in active:
            for j in active:
                if i != j:
                    Q[i, j] = (r - 2) * D[i, j] - row_sums[i] - row_sums[j]
        
        # Find minimum Q
        min_Q = float('inf')
        min_i, min_j = None, None
        
        for idx1, i in enumerate(active):
            for j in active[idx1+1:]:
                if Q[i, j] < min_Q:
                    min_Q = Q[i, j]
                    min_i, min_j = i, j
        
        # Calculate distances to new node
        dist_to_new_i = 0.5 * D[min_i, min_j] + 0.5 * (row_sums[min_i] - row_sums[min_j]) / (r - 2)
        dist_to_new_j = D[min_i, min_j] - dist_to_new_i
        
        # Create new node
        new_node = {
            'left': nodes[min_i],
            'right': nodes[min_j],
            'left_dist': dist_to_new_i,
            'right_dist': dist_to_new_j
        }
        
        # Update distance matrix
        new_idx = max(nodes.keys()) + 1
        D = np.pad(D, ((0, 1), (0, 1)), mode='constant')
        
        for k in active:
            if k != min_i and k != min_j:
                dist = 0.5 * (D[min_i, k] + D[min_j, k] - D[min_i, min_j])
                D[new_idx, k] = dist
                D[k, new_idx] = dist
        
        # Update nodes
        nodes[new_idx] = new_node
        active.remove(min_i)
        active.remove(min_j)
        active.append(new_idx)
    
    # Final join
    i, j = active
    final_tree = {
        'left': nodes[i],
        'right': nodes[j],
        'distance': D[i, j]
    }
    
    return final_tree

# Example
tree_nj = neighbor_joining(distance_matrix, species)

print("\n=== Neighbor-Joining Tree ===")
print_tree(tree_nj)

Molecular Evolution Models
# Substitution models for DNA/protein evolution
# Jukes-Cantor: simplest model (equal rates)
# Kimura 2-parameter: different rates for transitions/transversions

def jukes_cantor_distance(p: float) -> float:
    """
    Jukes-Cantor distance correction.
    p: proportion of differences
    Returns: estimated number of substitutions per site
    """
    if p >= 0.75:
        return float('inf')
    
    return -0.75 * np.log(1 - 4/3 * p)

def kimura_2parameter(p: float, q: float) -> float:
    """
    Kimura 2-parameter distance.
    p: proportion of transitions
    q: proportion of transversions
    """
    term1 = 1 - 2*p - q
    term2 = 1 - 2*q
    
    if term1 <= 0 or term2 <= 0:
        return float('inf')
    
    return -0.5 * np.log(term1) - 0.25 * np.log(term2)

# Example
observed_diff = 0.15  # 15% differences
jc_dist = jukes_cantor_distance(observed_diff)

print("\n=== Molecular Evolution ===")
print(f"Observed differences: {observed_diff:.2%}")
print(f"Jukes-Cantor corrected distance: {jc_dist:.4f}")

CHAPTER 4: GENOMICS & VARIANT CALLING
SNP Analysis
# Single Nucleotide Polymorphisms
# Most common type of genetic variation

def find_snps(reference: str, sample: str) -> list:
    """Find SNPs between reference and sample sequences."""
    snps = []
    
    for i, (ref_base, samp_base) in enumerate(zip(reference, sample)):
        if ref_base != samp_base and ref_base != 'N' and samp_base != 'N':
            snps.append({
                'position': i,
                'reference': ref_base,
                'alternate': samp_base
            })
    
    return snps

def calculate_variant_density(snps: list, sequence_length: int) -> float:
    """Calculate SNP density (SNPs per kb)."""
    return len(snps) / (sequence_length / 1000)

# Example
reference = "ATCGATCGATCGATCGATCG"
sample =    "ATCGATCAATCGATCGGTCG"

snps = find_snps(reference, sample)

print("=== SNP Analysis ===")
print(f"Reference: {reference}")
print(f"Sample:    {sample}")
print(f"\nSNPs found: {len(snps)}")
for snp in snps:
    print(f"  Position {snp['position']}: {snp['reference']} → {snp['alternate']}")

density = calculate_variant_density(snps, len(reference))
print(f"\nVariant density: {density:.2f} SNPs/kb")

VCF File Parsing
# Variant Call Format (VCF)
# Standard format for storing genetic variants

def parse_vcf(vcf_content: str) -> list:
    """Parse VCF file content."""
    variants = []
    
    for line in vcf_content.strip().split('\n'):
        if line.startswith('#'):
            continue
        
        fields = line.split('\t')
        if len(fields) >= 8:
            variant = {
                'chrom': fields[0],
                'pos': int(fields[1]),
                'id': fields[2],
                'ref': fields[3],
                'alt': fields[4],
                'qual': float(fields[5]) if fields[5] != '.' else 0,
                'filter': fields[6],
                'info': fields[7]
            }
            variants.append(variant)
    
    return variants

def filter_variants(variants: list, min_qual: float = 30) -> list:
    """Filter variants by quality."""
    return [v for v in variants if v['qual'] >= min_qual]

# Example VCF content
vcf_data = """
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
chr1	100	rs123	A	T	50	PASS	DP=30
chr1	200	rs456	G	C	10	LOWQUAL	DP=5
chr2	150	.	C	G	45	PASS	DP=25
"""

variants = parse_vcf(vcf_data)
filtered = filter_variants(variants, min_qual=30)

print("\n=== VCF Parsing ===")
print(f"Total variants: {len(variants)}")
print(f"After filtering (QUAL >= 30): {len(filtered)}")
for v in filtered:
    print(f"  {v['chrom']}:{v['pos']} {v['ref']}→{v['alt']} (QUAL={v['qual']})")

Genome Assembly
# Assemble short reads into contigs
# De Bruijn graph approach

def build_de_bruijn_graph(reads: list, k: int = 3) -> dict:
    """
    Build De Bruijn graph from reads.
    k: k-mer size
    """
    graph = {}
    
    for read in reads:
        for i in range(len(read) - k + 1):
            kmer = read[i:i+k]
            prefix = kmer[:-1]
            suffix = kmer[1:]
            
            if prefix not in graph:
                graph[prefix] = []
            graph[prefix].append(suffix)
    
    return graph

def eulerian_path(graph: dict, start: str) -> str:
    """Find Eulerian path in De Bruijn graph (assembly)."""
    # Simple DFS-based approach
    path = [start]
    current = start
    
    while graph.get(current):
        next_node = graph[current].pop(0)
        path.append(next_node)
        current = next_node
    
    # Reconstruct sequence
    sequence = path[0]
    for node in path[1:]:
        sequence += node[-1]
    
    return sequence

# Example
reads = ["ATCG", "TCGA", "CGAT", "GATC"]
k = 3

graph = build_de_bruijn_graph(reads, k)

print("\n=== De Bruijn Graph Assembly ===")
print(f"Reads: {reads}")
print(f"k-mer size: {k}")
print(f"\nGraph edges:")
for node, edges in graph.items():
    print(f"  {node} → {edges}")

# Find start node (node with no incoming edges)
all_nodes = set(graph.keys())
all_targets = set()
for edges in graph.values():
    all_targets.update(edges)

start_nodes = all_nodes - all_targets
start = list(start_nodes)[0] if start_nodes else list(graph.keys())[0]

assembly = eulerian_path(graph, start)
print(f"\nAssembled sequence: {assembly}")

CHAPTER 5: PROTEIN STRUCTURE
Protein Sequence Analysis
# Analyze amino acid properties
# Hydrophobicity, charge, secondary structure prediction

def analyze_protein(sequence: str) -> dict:
    """Analyze protein sequence properties."""
    sequence = sequence.upper()
    
    # Amino acid properties
    hydrophobic = set("AILMFWV")
    polar = set("STNQYC")
    positive = set("KRH")
    negative = set("DE")
    
    # Count properties
    hydrophobic_count = sum(1 for aa in sequence if aa in hydrophobic)
    polar_count = sum(1 for aa in sequence if aa in polar)
    positive_count = sum(1 for aa in sequence if aa in positive)
    negative_count = sum(1 for aa in sequence if aa in negative)
    
    # Molecular weight (approximate)
    mw_table = {
        'A': 89, 'R': 174, 'N': 132, 'D': 133, 'C': 121,
        'E': 147, 'Q': 146, 'G': 75, 'H': 155, 'I': 131,
        'L': 131, 'K': 146, 'M': 149, 'F': 165, 'P': 115,
        'S': 105, 'T': 119, 'W': 204, 'Y': 181, 'V': 117
    }
    
    mw = sum(mw_table.get(aa, 0) for aa in sequence) - (len(sequence) - 1) * 18
    
    # Isoelectric point (simplified)
    pI = 6.0  # Placeholder
    if positive_count > negative_count:
        pI = 8.0
    elif negative_count > positive_count:
        pI = 4.0
    
    return {
        'length': len(sequence),
        'hydrophobic': hydrophobic_count / len(sequence),
        'polar': polar_count / len(sequence),
        'positive': positive_count / len(sequence),
        'negative': negative_count / len(sequence),
        'molecular_weight': mw,
        'isoelectric_point': pI
    }

# Kyte-Doolittle hydrophobicity scale
HYDROPHOBICITY = {
    'I': 4.5, 'V': 4.2, 'L': 3.8, 'F': 2.8, 'C': 2.5,
    'M': 1.9, 'A': 1.8, 'G': -0.4, 'T': -0.7, 'S': -0.8,
    'W': -0.9, 'Y': -1.3, 'P': -1.6, 'H': -3.2, 'E': -3.5,
    'Q': -3.5, 'D': -3.5, 'N': -3.5, 'K': -3.9, 'R': -4.5
}

def hydrophobicity_profile(sequence: str, window: int = 9) -> list:
    """Calculate sliding window hydrophobicity profile."""
    profile = []
    
    for i in range(len(sequence) - window + 1):
        window_seq = sequence[i:i+window]
        avg_hydro = sum(HYDROPHOBICITY.get(aa, 0) for aa in window_seq) / window
        profile.append(avg_hydro)
    
    return profile

# Example
protein = "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH"

analysis = analyze_protein(protein)

print("=== Protein Analysis ===")
print(f"Sequence: {protein}")
print(f"Length: {analysis['length']} amino acids")
print(f"Molecular weight: {analysis['molecular_weight']:.1f} Da")
print(f"Isoelectric point: {analysis['isoelectric_point']:.1f}")
print(f"Composition:")
print(f"  Hydrophobic: {analysis['hydrophobic']:.2%}")
print(f"  Polar: {analysis['polar']:.2%}")
print(f"  Positive: {analysis['positive']:.2%}")
print(f"  Negative: {analysis['negative']:.2%}")

profile = hydrophobicity_profile(protein, window=9)
print(f"\nHydrophobicity profile (first 10 windows):")
for i, h in enumerate(profile[:10]):
    bar = '+' * int(abs(h) * 5)
    sign = '+' if h > 0 else '-'
    print(f"  {i:2d}: {h:6.2f} {sign}{bar}")

Secondary Structure Prediction
# Chou-Fasman method (simplified)
# Predict alpha helix, beta sheet, coil

def chou_fasman(sequence: str) -> str:
    """
    Simplified Chou-Fasman secondary structure prediction.
    H: alpha helix, E: beta sheet, C: coil
    """
    # Propensity values (simplified)
    helix_propensity = {
        'A': 1.42, 'R': 0.98, 'N': 0.67, 'D': 1.01, 'C': 0.70,
        'Q': 1.11, 'E': 1.51, 'G': 0.57, 'H': 1.00, 'I': 1.08,
        'L': 1.21, 'K': 1.16, 'M': 1.45, 'F': 1.13, 'P': 0.57,
        'S': 0.77, 'T': 0.83, 'W': 1.08, 'Y': 0.69, 'V': 1.06
    }
    
    sheet_propensity = {
        'A': 0.83, 'R': 0.93, 'N': 0.89, 'D': 0.54, 'C': 1.19,
        'Q': 1.10, 'E': 0.37, 'G': 0.75, 'H': 0.87, 'I': 1.60,
        'L': 1.30, 'K': 0.74, 'M': 1.05, 'F': 1.38, 'P': 0.55,
        'S': 0.75, 'T': 1.19, 'W': 1.37, 'Y': 1.47, 'V': 1.70
    }
    
    # Calculate propensities
    structure = []
    
    for i, aa in enumerate(sequence):
        h_prop = helix_propensity.get(aa, 1.0)
        e_prop = sheet_propensity.get(aa, 1.0)
        
        if h_prop > 1.0 and h_prop > e_prop:
            structure.append('H')
        elif e_prop > 1.0:
            structure.append('E')
        else:
            structure.append('C')
    
    return ''.join(structure)

# Example
protein = "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSH"
structure = chou_fasman(protein)

print("\n=== Secondary Structure Prediction ===")
print(f"Sequence:  {protein}")
print(f"Structure: {structure}")

# Count elements
helix = structure.count('H')
sheet = structure.count('E')
coil = structure.count('C')

print(f"\nAlpha helix: {helix} ({helix/len(structure):.1%})")
print(f"Beta sheet:  {sheet} ({sheet/len(structure):.1%})")
print(f"Coil:        {coil} ({coil/len(structure):.1%})")

Protein Structure Visualization (PDB)
# Parse PDB file format

def parse_pdb_atom(pdb_line: str) -> dict:
    """Parse ATOM record from PDB file."""
    if not pdb_line.startswith(('ATOM', 'HETATM')):
        return None
    
    atom = {
        'type': pdb_line[0:6].strip(),
        'serial': int(pdb_line[6:11]),
        'name': pdb_line[12:16].strip(),
        'altLoc': pdb_line[16],
        'resName': pdb_line[17:20].strip(),
        'chainID': pdb_line[21],
        'resSeq': int(pdb_line[22:26]),
        'x': float(pdb_line[30:38]),
        'y': float(pdb_line[38:46]),
        'z': float(pdb_line[46:54]),
    }
    
    return atom

def calculate_distance(atom1: dict, atom2: dict) -> float:
    """Calculate distance between two atoms."""
    dx = atom1['x'] - atom2['x']
    dy = atom1['y'] - atom2['y']
    dz = atom1['z'] - atom2['z']
    
    return np.sqrt(dx**2 + dy**2 + dz**2)

# Example PDB line
pdb_line = "ATOM      1  N   MET A   1      27.340  24.430   2.614  1.00  9.67           N"

atom = parse_pdb_atom(pdb_line)

print("\n=== PDB Parsing ===")
print(f"Parsed atom: {atom}")

CHAPTER 6: RNA ANALYSIS
RNA Secondary Structure
# Predict base pairing (simplified Nussinov algorithm)

def nussinov(sequence: str, min_loop: int = 3) -> list:
    """
    Nussinov algorithm for RNA secondary structure prediction.
    Returns list of base pairs.
    """
    n = len(sequence)
    
    # Initialize DP table
    dp = np.zeros((n, n), dtype=int)
    
    # Complementarity
    def can_pair(i, j):
        pair = sequence[i] + sequence[j]
        return pair in ['AU', 'UA', 'GC', 'CG', 'GU', 'UG']
    
    # Fill DP table
    for length in range(min_loop + 1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            
            # Case 1: j unpaired
            dp[i, j] = dp[i, j-1]
            
            # Case 2: j paired with k
            for k in range(i, j - min_loop):
                if can_pair(k, j):
                    score = 1 + dp[i, k-1] + dp[k+1, j-1]
                    dp[i, j] = max(dp[i, j], score)
    
    # Traceback
    def traceback(i, j):
        if i >= j:
            return []
        
        if dp[i, j] == dp[i, j-1]:
            return traceback(i, j-1)
        
        for k in range(i, j - min_loop):
            if can_pair(k, j) and dp[i, j] == 1 + dp[i, k-1] + dp[k+1, j-1]:
                return [(k, j)] + traceback(i, k-1) + traceback(k+1, j-1)
        
        return []
    
    pairs = traceback(0, n-1)
    return sorted(pairs)

def visualize_rna_structure(sequence: str, pairs: list):
    """Visualize RNA structure in dot-bracket notation."""
    structure = ['.'] * len(sequence)
    
    for i, j in pairs:
        structure[i] = '('
        structure[j] = ')'
    
    return ''.join(structure)

# Example
rna_sequence = "GGGAAAUCC"

pairs = nussinov(rna_sequence)
structure = visualize_rna_structure(rna_sequence, pairs)

print("\n=== RNA Secondary Structure ===")
print(f"Sequence:  {rna_sequence}")
print(f"Structure: {structure}")
print(f"Base pairs: {len(pairs)}")
for i, j in pairs:
    print(f"  {rna_sequence[i]}{i} - {rna_sequence[j]}{j}")

Gene Expression Analysis
# Analyze RNA-seq data
# Count reads per gene, normalize

def normalize_counts(counts: dict, method: str = 'tpm') -> dict:
    """
    Normalize gene expression counts.
    TPM: Transcripts Per Million
    """
    if method == 'tpm':
        # Calculate reads per kilobase
        gene_lengths = {gene: 1000 for gene in counts}  # Placeholder
        
        rpk = {gene: counts[gene] / (gene_lengths[gene] / 1000) 
               for gene in counts}
        
        # Calculate per million scaling factor
        total_rpk = sum(rpk.values())
        scaling_factor = total_rpk / 1e6
        
        # TPM
        tpm = {gene: rpk[gene] / scaling_factor for gene in counts}
        
        return tpm
    
    elif method == 'cpm':
        # Counts Per Million
        total = sum(counts.values())
        cpm = {gene: (counts[gene] / total) * 1e6 for gene in counts}
        return cpm
    
    return counts

# Example
gene_counts = {
    'GENE1': 1000,
    'GENE2': 500,
    'GENE3': 2000,
    'GENE4': 100,
}

tpm = normalize_counts(gene_counts, method='tpm')
cpm = normalize_counts(gene_counts, method='cpm')

print("\n=== Gene Expression Normalization ===")
print(f"Raw counts: {gene_counts}")
print(f"\nTPM normalized:")
for gene, value in tpm.items():
    print(f"  {gene}: {value:.2f}")
print(f"\nCPM normalized:")
for gene, value in cpm.items():
    print(f"  {gene}: {value:.2f}")

CHAPTER 7: SYSTEMS BIOLOGY
Metabolic Pathway Analysis
# Analyze biochemical networks

def build_metabolic_network(reactions: list) -> dict:
    """Build metabolic network from reactions."""
    network = {
        'metabolites': set(),
        'reactions': [],
        'adjacency': {}
    }
    
    for reaction in reactions:
        substrates, products = reaction
        
        network['reactions'].append({
            'substrates': substrates,
            'products': products
        })
        
        # Add metabolites
        network['metabolites'].update(substrates)
        network['metabolites'].update(products)
        
        # Build adjacency
        for sub in substrates:
            if sub not in network['adjacency']:
                network['adjacency'][sub] = []
            network['adjacency'][sub].extend(products)
    
    return network

def find_pathways(network: dict, start: str, end: str) -> list:
    """Find metabolic pathways from start to end metabolite."""
    paths = []
    
    def dfs(current, path, visited):
        if current == end:
            paths.append(path.copy())
            return
        
        for neighbor in network['adjacency'].get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, path, visited)
                path.pop()
                visited.remove(neighbor)
    
    dfs(start, [start], {start})
    return paths

# Example: glycolysis-like pathway
reactions = [
    (['Glucose'], ['Glucose-6-P']),
    (['Glucose-6-P'], ['Fructose-6-P']),
    (['Fructose-6-P'], ['Fructose-1,6-BP']),
    (['Fructose-1,6-BP'], ['G3P', 'DHAP']),
    (['G3P'], ['1,3-BPG']),
    (['1,3-BPG'], ['3-PG']),
    (['3-PG'], ['2-PG']),
    (['2-PG'], ['PEP']),
    (['PEP'], ['Pyruvate']),
]

network = build_metabolic_network(reactions)
pathways = find_pathways(network, 'Glucose', 'Pyruvate')

print("\n=== Metabolic Pathway Analysis ===")
print(f"Metabolites: {len(network['metabolites'])}")
print(f"Reactions: {len(network['reactions'])}")
print(f"\nPathways from Glucose to Pyruvate:")
for i, path in enumerate(pathways[:3]):
    print(f"  Path {i+1}: {' → '.join(path)}")

ODE Models for Biological Systems
# Ordinary differential equations for dynamics

from scipy.integrate import odeint
import matplotlib.pyplot as plt

def lotka_volterra(y, t, alpha, beta, delta, gamma):
    """
    Lotka-Volterra predator-prey model.
    y = [prey, predator]
    """
    prey, predator = y
    
    dprey = alpha * prey - beta * prey * predator
    dpredator = delta * prey * predator - gamma * predator
    
    return [dprey, dpredator]

# Parameters
alpha = 1.0    # prey growth rate
beta = 0.1     # predation rate
delta = 0.075  # predator growth from prey
gamma = 1.5    # predator death rate

# Initial conditions
y0 = [10, 5]  # [prey, predator]

# Time points
t = np.linspace(0, 50, 1000)

# Solve ODE
solution = odeint(lotka_volterra, y0, t, args=(alpha, beta, delta, gamma))

prey = solution[:, 0]
predator = solution[:, 1]

print("\n=== Lotka-Volterra Model ===")
print(f"Initial: prey={y0[0]}, predator={y0[1]}")
print(f"Final: prey={prey[-1]:.2f}, predator={predator[-1]:.2f}")

# Plot
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(t, prey, label='Prey', linewidth=2)
plt.plot(t, predator, label='Predator', linewidth=2)
plt.xlabel('Time')
plt.ylabel('Population')
plt.title('Population Dynamics')
plt.legend()
plt.grid(alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(prey, predator, linewidth=2)
plt.xlabel('Prey')
plt.ylabel('Predator')
plt.title('Phase Portrait')
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('lotka_volterra.png', dpi=100)
plt.show()

CHAPTER 8: MACHINE LEARNING IN BIOINFORMATICS
Sequence Classification
# Classify DNA/protein sequences using ML

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def extract_kmer_features(sequence: str, k: int = 3) -> str:
    """Extract k-mer features from sequence."""
    kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
    return ' '.join(kmers)

# Example: classify promoters vs non-promoters
sequences = [
    ("ATGCGTACGATCGATCG", "promoter"),
    ("GCTAGCTAGCTAGCTAG", "promoter"),
    ("TTTTTTTTTTTTTTTTT", "non-promoter"),
    ("AAAAAAAAAAAAAAAAA", "non-promoter"),
] * 10  # Repeat for more data

# Extract features
X = [extract_kmer_features(seq, k=3) for seq, _ in sequences]
y = [label for _, label in sequences]

# Vectorize
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)

# Train classifier
clf = SVC(kernel='linear')
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n=== Sequence Classification ===")
print(f"Accuracy: {accuracy:.2%}")
print(f"\nClassification report:")
print(classification_report(y_test, y_pred))

Clustering Gene Expression
# Cluster genes with similar expression patterns

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Simulated gene expression data
np.random.seed(42)
n_genes = 100
n_samples = 10

# Generate data with 3 clusters
expression_data = np.vstack([
    np.random.randn(33, n_samples) + 2,   # Cluster 1: high expression
    np.random.randn(33, n_samples) - 2,   # Cluster 2: low expression
    np.random.randn(34, n_samples)        # Cluster 3: medium expression
])

# Standardize
scaler = StandardScaler()
expression_scaled = scaler.fit_transform(expression_data)

# K-means clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(expression_scaled)

print("\n=== Gene Expression Clustering ===")
print(f"Number of genes: {n_genes}")
print(f"Number of clusters: 3")
print(f"\nCluster sizes:")
for i in range(3):
    size = np.sum(clusters == i)
    print(f"  Cluster {i+1}: {size} genes")

# Visualize with PCA
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
expression_pca = pca.fit_transform(expression_scaled)

plt.figure(figsize=(10, 6))
scatter = plt.scatter(expression_pca[:, 0], expression_pca[:, 1], 
                     c=clusters, cmap='viridis', alpha=0.7)
plt.colorbar(scatter, label='Cluster')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('Gene Expression Clustering (PCA)')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('gene_clustering.png', dpi=100)
plt.show()

CHAPTER 9: STATISTICAL METHODS
Hidden Markov Models for Gene Prediction
# HMM for finding genes in DNA

class SimpleHMM:
    """Simple HMM for gene prediction."""
    
    def __init__(self):
        # States: exon, intron, intergenic
        self.states = ['exon', 'intron', 'intergenic']
        
        # Transition probabilities
        self.transition = {
            'intergenic': {'intergenic': 0.9, 'exon': 0.1, 'intron': 0.0},
            'exon': {'exon': 0.8, 'intron': 0.2, 'intergenic': 0.0},
            'intron': {'intron': 0.8, 'exon': 0.1, 'intergenic': 0.1}
        }
        
        # Emission probabilities (simplified)
        self.emission = {
            'exon': {'A': 0.25, 'T': 0.25, 'G': 0.25, 'C': 0.25},
            'intron': {'A': 0.3, 'T': 0.3, 'G': 0.2, 'C': 0.2},
            'intergenic': {'A': 0.2, 'T': 0.2, 'G': 0.3, 'C': 0.3}
        }
    
    def viterbi(self, sequence: str) -> list:
        """Viterbi algorithm for most likely state sequence."""
        n = len(sequence)
        
        # Initialize
        V = [{} for _ in range(n)]
        path = {state: [] for state in self.states}
        
        # Initial probabilities
        for state in self.states:
            V[0][state] = self.emission[state].get(sequence[0], 0.01)
            path[state] = [state]
        
        # Forward pass
        for t in range(1, n):
            new_path = {state: [] for state in self.states}
            
            for state in self.states:
                max_prob = -1
                best_prev = None
                
                for prev_state in self.states:
                    prob = (V[t-1][prev_state] * 
                           self.transition[prev_state][state] *
                           self.emission[state].get(sequence[t], 0.01))
                    
                    if prob > max_prob:
                        max_prob = prob
                        best_prev = prev_state
                
                V[t][state] = max_prob
                new_path[state] = path[best_prev] + [state]
            
            path = new_path
        
        # Find best final state
        max_prob = max(V[n-1][state] for state in self.states)
        best_state = max(V[n-1], key=V[n-1].get)
        
        return path[best_state]

# Example
hmm = SimpleHMM()
sequence = "ATGCGATCGATCGATCG"

states = hmm.viterbi(sequence)

print("\n=== HMM Gene Prediction ===")
print(f"Sequence: {sequence}")
print(f"States:   {''.join(s[0].upper() for s in states)}")
print(f"          (E=exon, I=intron, G=intergenic)")

Multiple Testing Correction
# Correct for multiple hypothesis testing
# Bonferroni, FDR (Benjamini-Hochberg)

def bonferroni_correction(p_values: list, alpha: float = 0.05) -> list:
    """Bonferroni correction for multiple testing."""
    n = len(p_values)
    corrected_alpha = alpha / n
    
    return [p < corrected_alpha for p in p_values]

def benjamini_hochberg(p_values: list, fdr: float = 0.05) -> list:
    """Benjamini-Hochberg FDR correction."""
    n = len(p_values)
    
    # Sort p-values
    sorted_indices = np.argsort(p_values)
    sorted_pvalues = [p_values[i] for i in sorted_indices]
    
    # Calculate thresholds
    thresholds = [(i + 1) / n * fdr for i in range(n)]
    
    # Find largest k where p(k) <= threshold
    significant = [False] * n
    
    for i in range(n - 1, -1, -1):
        if sorted_pvalues[i] <= thresholds[i]:
            for j in range(i + 1):
                significant[sorted_indices[j]] = True
            break
    
    return significant

# Example
p_values = [0.001, 0.04, 0.03, 0.05, 0.002, 0.1, 0.02]

bonf_sig = bonferroni_correction(p_values, alpha=0.05)
fdr_sig = benjamini_hochberg(p_values, fdr=0.05)

print("\n=== Multiple Testing Correction ===")
print(f"P-values: {[f'{p:.3f}' for p in p_values]}")
print(f"Bonferroni significant: {bonf_sig}")
print(f"FDR significant: {fdr_sig}")
print(f"\nBonferroni rejects: {sum(bonf_sig)} hypotheses")
print(f"FDR rejects: {sum(fdr_sig)} hypotheses")

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Single-Cell RNA Sequencing
# Analyze gene expression at single-cell level
# Dimensionality reduction, clustering, trajectory inference

def simulate_single_cell_data(n_cells: int = 100, n_genes: int = 50) -> np.ndarray:
    """Simulate single-cell RNA-seq data."""
    # Generate data with batch effects
    data = np.random.negative_binomial(5, 0.3, (n_cells, n_genes))
    
    # Add cell type effects
    cell_types = np.random.choice([0, 1, 2], n_cells)
    for i in range(n_cells):
        if cell_types[i] == 0:
            data[i, :10] *= 2  # Upregulate genes 0-10
        elif cell_types[i] == 1:
            data[i, 10:20] *= 2  # Upregulate genes 10-20
    
    return data, cell_types

# Example
sc_data, cell_types = simulate_single_cell_data(100, 50)

print("\n=== Single-Cell RNA-seq ===")
print(f"Cells: {sc_data.shape[0]}")
print(f"Genes: {sc_data.shape[1]}")
print(f"Cell types: {np.unique(cell_types)}")

Metagenomics
# Analyze microbial communities

def classify_taxonomy(sequence: str, database: dict) -> str:
    """Classify sequence using k-mer matching."""
    best_match = None
    best_score = 0
    
    # Extract k-mers
    kmers = set(sequence[i:i+8] for i in range(len(sequence) - 7))
    
    # Compare to database
    for taxon, taxon_kmers in database.items():
        overlap = len(kmers & taxon_kmers)
        score = overlap / len(kmers)
        
        if score > best_score:
            best_score = score
            best_match = taxon
    
    return best_match, best_score

# Example database
taxonomy_db = {
    'Bacteria_Ecoli': set(['ATCGATCG', 'GCTAGCTA', 'TTTTAAAA']),
    'Bacteria_Staph': set(['AAAATTTT', 'CCCCGGGG', 'ATATATAT']),
    'Archaea_Methano': set(['GGGGCCCC', 'ATATCGCG', 'TATATATA']),
}

sequence = "ATCGATCGGCTAGCTATTTTAAAA"
taxon, score = classify_taxonomy(sequence, taxonomy_db)

print("\n=== Metagenomics Classification ===")
print(f"Sequence: {sequence}")
print(f"Classified as: {taxon} (score: {score:.2%})")

CRISPR Guide RNA Design
# Design guide RNAs for CRISPR-Cas9

def design_grna(sequence: str, pam: str = "NGG") -> list:
    """
    Design CRISPR guide RNAs.
    Look for 20-nt sequences followed by PAM.
    """
    guides = []
    
    # Find PAM sites
    for i in range(len(sequence) - 23):
        if sequence[i+20:i+23] == pam or sequence[i+20:i+23][1:] == pam[1:]:
            grna = sequence[i:i+20]
            
            # Check GC content (40-60% optimal)
            gc_content = (grna.count('G') + grna.count('C')) / 20
            
            if 0.4 <= gc_content <= 0.6:
                guides.append({
                    'sequence': grna,
                    'position': i,
                    'gc_content': gc_content
                })
    
    return guides

# Example
target_sequence = "ATCGATCGATCGATCGATCGGGATCGATCGATCGATCGATCGGG"

guides = design_grna(target_sequence)

print("\n=== CRISPR Guide RNA Design ===")
print(f"Target: {target_sequence}")
print(f"Guides found: {len(guides)}")
for i, guide in enumerate(guides[:5]):
    print(f"  Guide {i+1}: {guide['sequence']} "
          f"(pos {guide['position']}, GC={guide['gc_content']:.2%})")

Recommended Reading
# - "Bioinformatics Algorithms" by Compeau & Pevzner
# - "Biological Sequence Analysis" by Durbin et al.
# - "Current Topics in Computational Biology" by Pevzner
# - "An Introduction to Bioinformatics Algorithms" by Jones & Pevzner

# Online Resources
# - NCBI: https://www.ncbi.nlm.nih.gov/
# - UniProt: https://www.uniprot.org/
# - Pfam: http://pfam.xfam.org/
# - RCSB PDB: https://www.rcsb.org/
# - Ensembl: https://www.ensembl.org/
# - Biopython documentation: https://biopython.org/

# End of Bioinformatics & Computational Biology Reference