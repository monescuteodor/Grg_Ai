Synthetic Biology & Bio-Computing Complete Reference
CHAPTER 1: GETTING STARTED WITH SYNTHETIC BIOLOGY
Remarks
Synthetic Biology (SynBio) applies engineering principles to biology. It involves designing and constructing new biological parts, devices, and systems, or re-designing existing natural biological systems for useful purposes. Bio-computing uses biological molecules (DNA, RNA, proteins) to perform computational tasks. Key concepts: Genetic Circuits, CRISPR-Cas9, DNA Storage, Metabolic Engineering, Xenobiology. Applications: Biosensors, Biofuels, Pharmaceutical production, Data storage, Molecular computing.
Tools: Python (Biopython), SBOL (Synthetic Biology Open Language), CellDesigner, Benchling, Ginkgo Bioworks API, NUPACK (nucleic acid design).
Hello Synthetic Biology
# hello_synbio.py
"""
First SynBio program: Transcribe DNA to mRNA and Translate to Protein.
"""
from Bio.Seq import Seq

def central_dogma(dna_sequence):
    """Simulate transcription and translation."""
    dna = Seq(dna_sequence)
    
    # Transcription: DNA -> mRNA
    mrna = dna.transcribe()
    
    # Translation: mRNA -> Protein
    protein = mrna.translate()
    
    return str(dna), str(mrna), str(protein)

# Example: GFP (Green Fluorescent Protein) start sequence
dna_seq = "ATGGCTAGCAAA" 
dna, mrna, protein = central_dogma(dna_seq)

print("=== Central Dogma Simulation ===")
print(f"DNA:     {dna}")
print(f"mRNA:    {mrna}")
print(f"Protein: {protein}")

Genetic Code Table
# Standard Genetic Code (Codon Table)
# UUU/F: Phe, UUA/A: Leu, etc.
# Start Codon: AUG (Met)
# Stop Codons: UAA, UAG, UGA

import pandas as pd

CODON_TABLE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}

def translate_manual(dna_seq):
    """Manual translation using codon table."""
    protein = []
    for i in range(0, len(dna_seq) - 2, 3):
        codon = dna_seq[i:i+3].upper()
        aa = CODON_TABLE.get(codon, 'X')
        if aa == '*':
            break
        protein.append(aa)
    return ''.join(protein)

print(f"\nManual Translation: {translate_manual('ATGGCTAGCAAA')}")

CHAPTER 2: GENETIC CIRCUITS
Logic Gates in Biology
# Biological logic gates use promoters, repressors, and activators.
# NOT Gate: Repressor inhibits expression.
# AND Gate: Two activators required for expression.
# OR Gate: Either activator triggers expression.

class GeneticGate:
    def __init__(self, gate_type):
        self.type = gate_type
        
    def evaluate(self, inputs):
        if self.type == 'NOT':
            return not inputs[0]
        elif self.type == 'AND':
            return all(inputs)
        elif self.type == 'OR':
            return any(inputs)
        elif self.type == 'NAND':
            return not all(inputs)
        elif self.type == 'NOR':
            return not any(inputs)
        elif self.type == 'XOR':
            return sum(inputs) == 1
        return False

# Example: Toggle Switch (Mutual Repression)
# Gene A represses Gene B, Gene B represses Gene A.
# Stable states: A=ON/B=OFF or A=OFF/B=ON.

def simulate_toggle_switch(steps=10):
    state_a = True
    state_b = False
    
    print("\n=== Toggle Switch Simulation ===")
    print(f"Step 0: A={state_a}, B={state_b}")
    
    for i in range(steps):
        # Mutual repression logic
        next_a = not state_b
        next_b = not state_a
        
        state_a = next_a
        state_b = next_b
        
        print(f"Step {i+1}: A={state_a}, B={state_b}")

simulate_toggle_switch(5)

SBOL (Synthetic Biology Open Language)
# Standard format for describing genetic designs.
# XML-based, machine-readable.

def generate_sbol_component(name, type_uri, roles):
    """Generate a simple SBOL-like dictionary structure."""
    return {
        'identity': f"http://examples.org/{name}",
        'type': type_uri,
        'roles': roles,
        'components': []
    }

promoter = generate_sbol_component(
    "Promoter_Lac", 
    "http://identifiers.org/so/SO:0000167", 
    ["regulatory"]
)
coding_seq = generate_sbol_component(
    "GFP_CDS", 
    "http://identifiers.org/so/SO:0000316", 
    ["coding"]
)

print(f"\nSBOL Component: {promoter['identity']}")

CHAPTER 3: DNA STORAGE
Encoding Data in DNA
# Digital data (0s and 1s) encoded into nucleotides (A, C, G, T).
# Challenges: Synthesis errors, sequencing errors, homopolymers.
# Encoding schemes: Binary-to-Quaternary, Huffman coding, Reed-Solomon error correction.

def binary_to_dna(binary_string):
    """Convert binary string to DNA sequence."""
    mapping = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}
    dna = []
    # Pad with zeros if length is odd
    if len(binary_string) % 2 != 0:
        binary_string += '0'
        
    for i in range(0, len(binary_string), 2):
        pair = binary_string[i:i+2]
        dna.append(mapping[pair])
    return ''.join(dna)

def dna_to_binary(dna_string):
    """Convert DNA sequence back to binary."""
    mapping = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}
    binary = []
    for base in dna_string:
        binary.append(mapping[base])
    return ''.join(binary)

# Example
text = "Hi"
binary = ''.join(format(ord(i), '08b') for i in text)
dna_seq = binary_to_dna(binary)
decoded_binary = dna_to_binary(dna_seq)
decoded_text = ''.join(chr(int(decoded_binary[i:i+8], 2)) for i in range(0, len(decoded_binary), 8))

print("\n=== DNA Storage Encoding ===")
print(f"Text:      {text}")
print(f"Binary:    {binary}")
print(f"DNA:       {dna_seq}")
print(f"Decoded:   {decoded_text}")

Error Correction in DNA
# Reed-Solomon codes are commonly used.
# Add redundancy to recover data from synthesis/sequencing errors.

import reed_solomon

def encode_with_ecc(data_bytes):
    """Encode data with Reed-Solomon error correction."""
    rs = reed_solomon.ReedSolomon(10, 5) # 10 data symbols, 5 parity
    encoded = rs.encode(data_bytes)
    return encoded

def decode_with_ecc(encoded_bytes):
    """Decode data with error correction."""
    rs = reed_solomon.ReedSolomon(10, 5)
    try:
        decoded = rs.decode(encoded_bytes)
        return decoded
    except reed_solomon.Error:
        return None

CHAPTER 4: METABOLIC ENGINEERING
Pathway Optimization
# Designing metabolic pathways to produce valuable compounds.
# Tools: Flux Balance Analysis (FBA), Kinetic Modeling.

def flux_balance_analysis(stoichiometry_matrix, bounds, objective_vector):
    """Simplified FBA using linear programming concept."""
    # In practice, use COBRApy or similar libraries
    # Maximize Z = c^T * v
    # Subject to S * v = 0, lb <= v <= ub
    pass

# Example: Ethanol production pathway
# Glucose -> Pyruvate -> Acetaldehyde -> Ethanol

class MetabolicPathway:
    def __init__(self):
        self.reactions = {}
        
    def add_reaction(self, name, substrates, products, rate_constant):
        self.reactions[name] = {
            'substrates': substrates,
            'products': products,
            'k': rate_constant
        }
        
    def simulate_step(self, concentrations):
        """Simple kinetic simulation step."""
        changes = {met: 0 for met in concentrations}
        
        for rxn_name, rxn_data in self.reactions.items():
            # Mass action kinetics: Rate = k * [S1] * [S2]...
            rate = rxn_data['k']
            for sub in rxn_data['substrates']:
                if sub in concentrations:
                    rate *= concentrations[sub]
                    
            for sub in rxn_data['substrates']:
                if sub in changes:
                    changes[sub] -= rate
            for prod in rxn_data['products']:
                if prod in changes:
                    changes[prod] += rate
                    
        # Update concentrations
        new_conc = {}
        for met, conc in concentrations.items():
            new_conc[met] = max(0, conc + changes.get(met, 0))
            
        return new_conc

pathway = MetabolicPathway()
pathway.add_reaction('R1', ['Glucose'], ['Pyruvate'], 0.1)
pathway.add_reaction('R2', ['Pyruvate'], ['Ethanol'], 0.2)

conc = {'Glucose': 10.0, 'Pyruvate': 0.0, 'Ethanol': 0.0}
for i in range(5):
    conc = pathway.simulate_step(conc)
    print(f"Step {i+1}: {conc}")

CHAPTER 5: CRISPR & GENOME EDITING
Guide RNA Design
# CRISPR-Cas9 requires a guide RNA (gRNA) complementary to the target DNA.
# Specificity is crucial to avoid off-target effects.

def design_grna(target_sequence, pam_sequence="NGG"):
    """Identify potential gRNA targets near PAM sites."""
    targets = []
    for i in range(len(target_sequence) - 23):
        # Check for PAM site downstream
        potential_pam = target_sequence[i+20:i+23]
        if potential_pam.endswith("GG"): # Simplified PAM check
            grna_seq = target_sequence[i:i+20]
            targets.append({
                'position': i,
                'grna': grna_seq,
                'pam': potential_pam
            })
    return targets

target_dna = "ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG"
grnas = design_grna(target_dna)
print(f"\n=== CRISPR gRNA Design ===")
for g in grnas[:3]:
    print(f"Pos: {g['position']}, gRNA: {g['grna']}, PAM: {g['pam']}")

Off-Target Analysis
# Check for similar sequences elsewhere in the genome.
# Use BLAST or specialized tools like Cas-OFFinder.

CHAPTER 6: MOLECULAR COMPUTING
DNA Computing
# Using DNA hybridization to perform computations.
# Adleman's experiment: Solving Hamiltonian Path problem.

def dna_hybridization(strand1, strand2):
    """Check if two strands complement each other."""
    comp_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    if len(strand1) != len(strand2):
        return False
    for b1, b2 in zip(strand1, strand2):
        if comp_map[b1] != b2:
            return False
    return True

strand_a = "ATCG"
strand_b = "TAGC"
print(f"\nHybridization Test: {dna_hybridization(strand_a, strand_b)}")

DNA Origami
# Folding long DNA strands into specific shapes using short staple strands.
# Used for nanotechnology, drug delivery vehicles.

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Xenobiology
# Creating organisms with expanded genetic alphabets (e.g., XNA).
# Semi-synthetic organisms with non-canonical amino acids.

Biosensors
# Engineered cells that detect environmental pollutants or pathogens.
# Output: Fluorescence, color change, electrical signal.

Biosecurity
# Risks of dual-use research.
# Screening DNA synthesis orders for dangerous sequences.
# Ethical guidelines for gain-of-function research.

Recommended Reading
# - "Synthetic Biology: A Primer" by Paul S. Freemont
# - "Regenesis" by Syd Moore
# - "DNA Computing and Nanobiotechnology"
# - Nature Reviews Genetics (Synthetic Biology section)

# Online Resources
# - Addgene: https://www.addgene.org/
# - Benchling: https://benchling.com/
# - SnapGene: https://snapgene.com/
# - Biopython Documentation: https://biopython.org/

# End of Synthetic Biology & Bio-Computing Reference