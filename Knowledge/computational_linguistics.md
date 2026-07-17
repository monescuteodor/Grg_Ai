Computational Linguistics & Natural Language Understanding Complete Reference
CHAPTER 1: GETTING STARTED WITH COMPUTATIONAL LINGUISTICS
Remarks
Computational Linguistics (CL) is the interdisciplinary field concerned with the computational modeling of natural language. It bridges linguistics, computer science, and artificial intelligence. Key areas: Morphology, Syntax (Parsing), Semantics, Pragmatics, Discourse Analysis, and Machine Translation. Unlike modern NLP which often relies on statistical patterns in large datasets, CL focuses heavily on the structural rules and logical representations of language.
Tools: Python (NLTK, SpaCy, Stanza), Prolog (logic programming), Treebank corpora (Penn Treebank, Universal Dependencies), Hugging Face Transformers.
Hello Computational Linguistics
# hello_cl.py
"""
First CL program: Basic tokenization and Part-of-Speech tagging.
"""
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Download required data (run once)
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

sentence = "Computational linguistics is a fascinating field."

# Tokenization
tokens = word_tokenize(sentence)
print(f"Tokens: {tokens}")

# POS Tagging
tagged = pos_tag(tokens)
print(f"POS Tags: {tagged}")

# Explanation of tags:
# NN: Noun, singular
# NNS: Noun, plural
# VB: Verb, base form
# VBD: Verb, past tense
# JJ: Adjective
# RB: Adverb

Morphological Analysis
# Morphology: Study of word structure and formation.
# Stemming: Crude heuristic process (chopping off ends).
# Lemmatization: Vocabulary-based process (using dictionary).

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

words = ["running", "runs", "ran", "better", "best"]
for w in words:
    # POS hint helps lemmatizer (v for verb, a for adjective)
    print(f"{w:10s} -> {lemmatizer.lemmatize(w, pos='v')}")

CHAPTER 2: SYNTACTIC PARSING
Context-Free Grammars (CFG)
# CFGs define the syntax of a language using production rules.
# S -> NP VP
# NP -> Det N | PropN
# VP -> V NP | V

import nltk
from nltk import CFG

grammar = CFG.fromstring("""
S -> NP VP
NP -> Det N | 'John' | 'Mary'
VP -> V NP | V
Det -> 'the' | 'a'
N -> 'dog' | 'cat' | 'ball'
V -> 'chased' | 'saw'
""")

sentence_tokens = ['John', 'chased', 'the', 'dog']

# Chart Parser
parser = nltk.ChartParser(grammar)
trees = parser.parse(sentence_tokens)

print("\n=== Syntactic Parse Trees ===")
for tree in trees:
    print(tree)
    tree.draw() # Opens a window with the tree diagram

Dependency Parsing
# Dependency grammar focuses on relationships between words (head-dependent).
# No phrasal nodes (NP, VP), just words connected by labeled arcs.

import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("The quick brown fox jumps over the lazy dog.")

print("\n=== Dependency Parse ===")
for token in doc:
    print(f"{token.text:10s} -> {token.dep_:10s} (Head: {token.head.text})")

Constituency vs Dependency
# Constituency (Phrase Structure): Hierarchical grouping into phrases (NP, VP). Good for generation.
# Dependency: Binary relations between words. Good for information extraction.

CHAPTER 3: SEMANTICS
Word Sense Disambiguation (WSD)
# Determining the meaning of a word in context.
# Example: "Bank" (financial institution vs. river side).

from nltk.corpus import wordnet as wn

def get_synsets(word):
    return wn.synsets(word)

word = "bank"
synsets = get_synsets(word)
print(f"\n=== Senses of '{word}' ===")
for ss in synsets[:3]:
    print(f"Sense: {ss.name()}")
    print(f"Definition: {ss.definition()}")
    print(f"Example: {ss.examples()[0] if ss.examples() else 'None'}")
    print("-" * 40)

Distributional Semantics
# "You shall know a word by the company it keeps." (Firth, 1957)
# Words with similar contexts have similar meanings.
# Basis for Word2Vec, GloVe, BERT.

Semantic Role Labeling (SRL)
# Identifying who did what to whom, when, and where.
# Predicate: "sold"
# Agent: "John"
# Theme: "the car"
# Recipient: "Mary"

CHAPTER 4: PRAGMATICS & DISCOURSE
Coreference Resolution
# Linking pronouns to their antecedents.
# "John said he would come." -> he = John.

import neuralcoref
# Note: neuralcoref is deprecated in newer Spacy versions, but concept remains.
# Modern approach: CorefQA, SpanBERT.

Discourse Relations
# Rhetorical Structure Theory (RST).
# Relations: Elaboration, Contrast, Cause, Condition.
# Example: "It rained [Cause] so we stayed inside [Effect]."

Sentiment Analysis (Pragmatic Level)
# Beyond positive/negative: Sarcasm detection, intent recognition.

CHAPTER 5: MACHINE TRANSLATION
Statistical Machine Translation (SMT)
# Older approach based on phrase tables and language models.
# IBM Models 1-5.
# Largely replaced by Neural MT.

Neural Machine Translation (NMT)
# Encoder-Decoder architecture with Attention.
# Transformer model is the state-of-the-art.

# Sequence-to-Sequence (Seq2Seq)
# Input: Source Sentence (e.g., French)
# Output: Target Sentence (e.g., English)

# BLEU Score (Bilingual Evaluation Understudy)
# Metric for evaluating translation quality.
# Compares n-gram overlap with reference translations.

from nltk.translate.bleu_score import sentence_bleu

reference = [["the", "cat", "is", "on", "the", "mat"]]
candidate = ["the", "cat", "is", "on", "the", "mat"]
score = sentence_bleu(reference, candidate)
print(f"\nBLEU Score (Perfect Match): {score:.2f}")

candidate_bad = ["the", "dog", "is", "in", "the", "car"]
score_bad = sentence_bleu(reference, candidate_bad)
print(f"BLEU Score (Bad Match): {score_bad:.2f}")

CHAPTER 6: FORMAL GRAMMARS & AUTOMATA
Chomsky Hierarchy
# Type 0: Recursively Enumerable (Turing Machine)
# Type 1: Context-Sensitive (Linear Bounded Automaton)
# Type 2: Context-Free (Pushdown Automaton) -> Most programming languages, natural language syntax.
# Type 3: Regular (Finite State Automaton) -> Lexical analysis, simple patterns.

Regular Expressions in Linguistics
# Used for morphological parsing, tokenization.
# Example: Pluralization rule s?

import re
pattern = r'^\w+s?$' # Matches singular or plural nouns roughly
print(re.match(pattern, "cats")) # Match
print(re.match(pattern, "cat"))  # Match

Finite State Transducers (FST)
# Used for morphological analysis.
# Input: "cats" -> Output: "cat +N +Pl"
# Two-tape automaton.

CHAPTER 7: ADVANCED TOPICS AND RESOURCES
Universal Grammar (Chomsky)
# Hypothesis that humans are born with innate linguistic structures.
# Controversial in modern computational linguistics, which favors data-driven approaches.

Frame Semantics
# Meaning is understood in terms of structured frames (scenarios).
# FrameNet database.

Construction Grammar
# Grammar consists of form-meaning pairs (constructions).
# Idioms are constructions.

Recommended Reading
# - "Speech and Language Processing" by Jurafsky & Martin (The Bible of CL/NLP)
# - "Foundations of Statistical Natural Language Processing" by Manning & Schütze
# - "Computational Linguistics: An Introduction" by Webber & Joshi
# - Universal Dependencies: https://universaldependencies.org/
# - Penn Treebank: https://catalog.ldc.upenn.edu/LDC99T42

# End of Computational Linguistics Reference