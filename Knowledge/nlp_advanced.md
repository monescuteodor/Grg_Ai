Natural Language Processing Advanced Complete Reference
CHAPTER 1: GETTING STARTED WITH NLP
Remarks
Natural Language Processing (NLP) enables machines to understand, interpret, and generate human language. Evolution: rule-based → statistical → neural → transformer-based LLMs. Key tasks: tokenization, POS tagging, NER, parsing, sentiment analysis, machine translation, text generation, question answering, summarization. Modern breakthrough: Transformer architecture (2017), BERT (2018), GPT series (2018-2024), LLaMA, Mistral, Claude.
Tools: Python, NLTK, spaCy, Hugging Face Transformers, PyTorch, TensorFlow, SentencePiece, tiktoken, LangChain, LlamaIndex.
Hello NLP
# hello_nlp.py
"""
First NLP program: tokenize, analyze, and visualize text.
"""
import re
from collections import Counter
import numpy as np

def simple_tokenizer(text):
    """Basic word tokenizer."""
    # Lowercase and split on non-alphanumeric
    tokens = re.findall(r'\b\w+\b', text.lower())
    return tokens

def compute_ngrams(tokens, n=2):
    """Generate n-grams from tokens."""
    return [' '.join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

def compute_tf(tokens):
    """Compute term frequency."""
    counts = Counter(tokens)
    total = len(tokens)
    return {token: count / total for token, count in counts.items()}

def compute_idf(documents):
    """Compute inverse document frequency."""
    n_docs = len(documents)
    term_doc_count = {}
    
    for doc in documents:
        unique_terms = set(doc)
        for term in unique_terms:
            term_doc_count[term] = term_doc_count.get(term, 0) + 1
    
    return {term: np.log(n_docs / (count + 1)) for term, count in term_doc_count.items()}

# Example
text = """Natural language processing is a subfield of linguistics, 
computer science, and artificial intelligence concerned with the 
interactions between computers and human language."""

tokens = simple_tokenizer(text)
bigrams = compute_ngrams(tokens, n=2)
trigrams = compute_ngrams(tokens, n=3)

print(f"Text length: {len(text)} chars")
print(f"Tokens: {len(tokens)}")
print(f"Unique tokens: {len(set(tokens))}")
print(f"Bigrams: {len(bigrams)}")
print(f"Trigrams: {len(trigrams)}")

print(f"\nMost common tokens:")
for token, count in Counter(tokens).most_common(10):
    print(f"  {token}: {count}")

print(f"\nSample bigrams: {bigrams[:5]}")
print(f"Sample trigrams: {trigrams[:5]}")

# Vocabulary size analysis
print(f"\nVocabulary statistics:")
print(f"  Type-token ratio: {len(set(tokens)) / len(tokens):.3f}")
print(f"  Hapax legomena: {sum(1 for t, c in Counter(tokens).items() if c == 1)}")

NLP Pipeline Overview
# Standard NLP processing pipeline:
# 1. Text Acquisition: raw text collection
# 2. Preprocessing: cleaning, normalization
# 3. Tokenization: split into tokens
# 4. Morphological Analysis: stemming, lemmatization
# 5. Syntactic Analysis: POS tagging, parsing
# 6. Semantic Analysis: NER, word sense disambiguation
# 7. Discourse Analysis: coreference, relations
# 8. Pragmatic Analysis: intent, context

# Modern LLM pipeline:
# 1. Tokenization (BPE, WordPiece, SentencePiece)
# 2. Embedding (learned embeddings)
# 3. Transformer layers (self-attention + FFN)
# 4. Output projection (logits over vocabulary)
# 5. Decoding (greedy, beam search, sampling)

# NLP paradigms:
# - Symbolic: rules, grammars (1950s-1980s)
# - Statistical: HMMs, CRFs, n-grams (1990s-2010s)
# - Neural: RNNs, CNNs, attention (2013-2017)
# - Transformer: BERT, GPT, T5 (2017-present)
# - LLMs: GPT-4, Claude, LLaMA (2023-present)

CHAPTER 2: TEXT PREPROCESSING & REPRESENTATION
Text Cleaning
import re
import unicodedata

class TextCleaner:
    """Comprehensive text cleaning pipeline."""
    
    def __init__(self, lowercase=True, remove_accents=True, 
                 normalize_whitespace=True, remove_urls=True,
                 remove_emails=True, remove_html=True):
        self.lowercase = lowercase
        self.remove_accents = remove_accents
        self.normalize_whitespace = normalize_whitespace
        self.remove_urls = remove_urls
        self.remove_emails = remove_emails
        self.remove_html = remove_html
    
    def clean(self, text):
        """Apply all cleaning steps."""
        if not isinstance(text, str):
            return ""
        
        # Remove HTML tags
        if self.remove_html:
            text = re.sub(r'<[^>]+>', '', text)
        
        # Remove URLs
        if self.remove_urls:
            text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # Remove emails
        if self.remove_emails:
            text = re.sub(r'\S+@\S+', '', text)
        
        # Remove accents
        if self.remove_accents:
            text = unicodedata.normalize('NFKD', text)
            text = ''.join(c for c in text if not unicodedata.combining(c))
        
        # Lowercase
        if self.lowercase:
            text = text.lower()
        
        # Remove special characters (keep alphanumeric and basic punctuation)
        text = re.sub(r'[^\w\s.,!?\'-]', ' ', text)
        
        # Normalize whitespace
        if self.normalize_whitespace:
            text = re.sub(r'\s+', ' ', text).strip()
        
        return text

# Example
dirty_text = """
<html><body>Check out https://example.com and email me at test@example.com!
Café résumé naïve   multiple   spaces...
Special chars: ©®™ €£¥</body></html>
"""

cleaner = TextCleaner()
clean_text = cleaner.clean(dirty_text)
print(f"Original: {dirty_text[:100]}...")
print(f"Cleaned:  {clean_text}")

Tokenization Methods
# Types of tokenization:
# 1. Word-level: split on whitespace/punctuation
# 2. Character-level: each character is a token
# 3. Subword: BPE, WordPiece, SentencePiece
# 4. Byte-level: GPT-2 style

import re

class WordTokenizer:
    """Simple word tokenizer with options."""
    
    def __init__(self, language='english'):
        self.language = language
        # Contractions for English
        self.contractions = {
            "n't": " not", "'re": " are", "'s": " is",
            "'d": " would", "'ll": " will", "'t": " not",
            "'ve": " have", "'m": " am"
        }
    
    def tokenize(self, text):
        """Tokenize text into words."""
        # Handle contractions
        for contraction, expansion in self.contractions.items():
            text = text.replace(contraction, expansion)
        
        # Split on word boundaries
        tokens = re.findall(r'\b\w+(?:[-\']\w+)*\b|[.,!?;:]', text)
        return tokens
    
    def detokenize(self, tokens):
        """Join tokens back into text."""
        text = ' '.join(tokens)
        # Fix punctuation spacing
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        return text

class CharacterTokenizer:
    """Character-level tokenizer."""
    
    def __init__(self, vocab=None):
        self.vocab = vocab or {}
        self.inv_vocab = {}
    
    def build_vocab(self, texts):
        """Build vocabulary from texts."""
        chars = set()
        for text in texts:
            chars.update(text)
        
        # Special tokens
        self.vocab = {'<PAD>': 0, '<UNK>': 1, '<BOS>': 2, '<EOS>': 3}
        idx = 4
        for char in sorted(chars):
            if char not in self.vocab:
                self.vocab[char] = idx
                idx += 1
        
        self.inv_vocab = {v: k for k, v in self.vocab.items()}
    
    def encode(self, text):
        """Encode text to character IDs."""
        return [self.vocab.get(c, self.vocab['<UNK>']) for c in text]
    
    def decode(self, ids):
        """Decode IDs back to text."""
        return ''.join(self.inv_vocab.get(i, '') for i in ids)

# Byte Pair Encoding (BPE)
class BPETokenizer:
    """Byte Pair Encoding tokenizer."""
    
    def __init__(self, vocab_size=10000):
        self.vocab_size = vocab_size
        self.vocab = {}
        self.merges = {}
    
    def _get_word_freqs(self, corpus):
        """Get word frequencies from corpus."""
        freqs = {}
        for text in corpus:
            for word in text.split():
                # Add end-of-word symbol
                word_freq = tuple(word) + ('</w>',)
                freqs[word_freq] = freqs.get(word_freq, 0) + 1
        return freqs
    
    def _get_pair_freqs(self, word_freqs):
        """Get frequencies of adjacent pairs."""
        pair_freqs = {}
        for word, freq in word_freqs.items():
            for i in range(len(word) - 1):
                pair = (word[i], word[i+1])
                pair_freqs[pair] = pair_freqs.get(pair, 0) + freq
        return pair_freqs
    
    def _merge_pair(self, word_freqs, pair):
        """Merge the most frequent pair."""
        new_word_freqs = {}
        for word, freq in word_freqs.items():
            new_word = []
            i = 0
            while i < len(word):
                if i < len(word) - 1 and word[i:i+2] == pair:
                    new_word.append(pair[0] + pair[1])
                    i += 2
                else:
                    new_word.append(word[i])
                    i += 1
            new_word_freqs[tuple(new_word)] = freq
        return new_word_freqs
    
    def train(self, corpus):
        """Train BPE tokenizer on corpus."""
        word_freqs = self._get_word_freqs(corpus)
        
        # Initialize vocabulary with characters
        for word in word_freqs:
            for char in word:
                if char not in self.vocab:
                    self.vocab[char] = len(self.vocab)
        
        # Learn merges
        for i in range(self.vocab_size - len(self.vocab)):
            pair_freqs = self._get_pair_freqs(word_freqs)
            if not pair_freqs:
                break
            
            best_pair = max(pair_freqs, key=pair_freqs.get)
            new_token = best_pair[0] + best_pair[1]
            
            self.vocab[new_token] = len(self.vocab)
            self.merges[best_pair] = new_token
            
            word_freqs = self._merge_pair(word_freqs, best_pair)
    
    def encode(self, text):
        """Encode text using learned merges."""
        tokens = []
        for word in text.split():
            word_tokens = list(word) + ['</w>']
            
            # Apply merges
            while len(word_tokens) > 1:
                pair_freqs = {}
                for i in range(len(word_tokens) - 1):
                    pair = (word_tokens[i], word_tokens[i+1])
                    if pair in self.merges:
                        pair_freqs[i] = pair
                
                if not pair_freqs:
                    break
                
                # Apply first merge
                i = min(pair_freqs)
                pair = pair_freqs[i]
                word_tokens = (word_tokens[:i] + 
                              [self.merges[pair]] + 
                              word_tokens[i+2:])
            
            tokens.extend(word_tokens)
        
        return [self.vocab.get(t, self.vocab.get('<UNK>', 0)) for t in tokens]

# Example
tokenizer = WordTokenizer()
text = "I can't believe it's already 2024! Don't you agree?"
tokens = tokenizer.tokenize(text)
print(f"\nWord tokenization: {tokens}")
print(f"Detokenized: {tokenizer.detokenize(tokens)}")

# Character tokenizer
char_tokenizer = CharacterTokenizer()
char_tokenizer.build_vocab(["hello world", "test text"])
encoded = char_tokenizer.encode("hello")
print(f"\nCharacter encoding of 'hello': {encoded}")
print(f"Decoded: {char_tokenizer.decode(encoded)}")

Stemming and Lemmatization
import re

class SimpleStemmer:
    """Porter-like stemmer (simplified)."""
    
    def __init__(self):
        self.rules = [
            # Step 1a
            (r'sses$', 'ss'),
            (r'ies$', 'i'),
            (r'ss$', 'ss'),
            (r's$', ''),
            # Step 1b
            (r'eed$', 'ee'),
            (r'ed$', ''),
            (r'ing$', ''),
            # Step 1c
            (r'y$', 'i'),
            # Step 2
            (r'ational$', 'ate'),
            (r'tional$', 'tion'),
            (r'enci$', 'ence'),
            (r'anci$', 'ance'),
            (r'izer$', 'ize'),
            # Step 3
            (r'icate$', 'ic'),
            (r'ative$', ''),
            (r'alize$', 'al'),
            # Step 4
            (r'al$', ''),
            (r'ence$', ''),
            (r'ance$', ''),
            (r'er$', ''),
            (r'ic$', ''),
            (r'able$', ''),
            (r'ible$', ''),
            (r'ment$', ''),
            (r'ion$', ''),
            (r'ous$', ''),
            (r'ive$', ''),
            (r'ize$', ''),
        ]
    
    def stem(self, word):
        """Apply stemming rules."""
        word = word.lower()
        for pattern, replacement in self.rules:
            if re.search(pattern, word):
                word = re.sub(pattern, replacement, word)
                break
        return word

class Lemmatizer:
    """Simple lemmatizer using lookup dictionary."""
    
    def __init__(self):
        # Irregular forms
        self.irregular = {
            'am': 'be', 'is': 'be', 'are': 'be', 'was': 'be', 'were': 'be',
            'been': 'be', 'being': 'be',
            'have': 'have', 'has': 'have', 'had': 'have', 'having': 'have',
            'do': 'do', 'does': 'do', 'did': 'do', 'doing': 'do',
            'go': 'go', 'goes': 'go', 'went': 'go', 'gone': 'go',
            'say': 'say', 'says': 'say', 'said': 'say',
            'get': 'get', 'gets': 'get', 'got': 'get', 'gotten': 'get',
            'make': 'make', 'makes': 'make', 'made': 'make',
            'know': 'know', 'knows': 'know', 'knew': 'know', 'known': 'know',
            'think': 'think', 'thinks': 'think', 'thought': 'think',
            'take': 'take', 'takes': 'take', 'took': 'take', 'taken': 'take',
            'see': 'see', 'sees': 'see', 'saw': 'see', 'seen': 'see',
            'come': 'come', 'comes': 'come', 'came': 'come',
            'want': 'want', 'wants': 'want', 'wanted': 'want',
            'use': 'use', 'uses': 'use', 'used': 'use', 'using': 'use',
            'find': 'find', 'finds': 'find', 'found': 'find',
            'give': 'give', 'gives': 'give', 'gave': 'give', 'given': 'give',
            'tell': 'tell', 'tells': 'tell', 'told': 'tell',
            'work': 'work', 'works': 'work', 'worked': 'work', 'working': 'work',
            'call': 'call', 'calls': 'call', 'called': 'call',
        }
    
    def lemmatize(self, word, pos='v'):
        """Lemmatize word given POS tag."""
        word = word.lower()
        
        # Check irregular forms
        if word in self.irregular:
            return self.irregular[word]
        
        # Apply POS-specific rules
        if pos == 'v':  # Verb
            if word.endswith('ing'):
                if len(word) > 4 and word[-4] == word[-5]:
                    return word[:-4]  # running → run
                return word[:-3] + 'e' if len(word) > 4 else word[:-3]
            elif word.endswith('ed'):
                if word.endswith('ied'):
                    return word[:-3] + 'y'
                return word[:-2] if word.endswith('eed') else word[:-1]
            elif word.endswith('s') and not word.endswith('ss'):
                return word[:-1]
        
        return word

# Example
stemmer = SimpleStemmer()
lemmatizer = Lemmatizer()

words = ["running", "ran", "runs", "better", "studies", "studying", 
         "computational", "computing", "computed", "computes"]

print("\n=== Stemming vs Lemmatization ===")
print(f"{'Word':<15} {'Stem':<15} {'Lemma':<15}")
print("-" * 45)
for word in words:
    stem = stemmer.stem(word)
    lemma = lemmatizer.lemmatize(word, pos='v')
    print(f"{word:<15} {stem:<15} {lemma:<15}")

TF-IDF Representation
import numpy as np
from collections import Counter
import math

class TFIDFVectorizer:
    """TF-IDF vectorization from scratch."""
    
    def __init__(self, max_features=10000, min_df=1, max_df=1.0):
        self.max_features = max_features
        self.min_df = min_df
        self.max_df = max_df
        self.vocabulary = {}
        self.idf = {}
    
    def _tokenize(self, text):
        """Simple tokenization."""
        return re.findall(r'\b\w+\b', text.lower())
    
    def fit(self, documents):
        """Fit vectorizer on documents."""
        # Count document frequencies
        doc_freq = Counter()
        n_docs = len(documents)
        
        for doc in documents:
            tokens = self._tokenize(doc)
            unique_tokens = set(tokens)
            for token in unique_tokens:
                doc_freq[token] += 1
        
        # Filter by min_df and max_df
        min_count = self.min_df
        max_count = int(self.max_df * n_docs)
        
        filtered_tokens = [
            token for token, count in doc_freq.items()
            if min_count <= count <= max_count
        ]
        
        # Sort by frequency and take top max_features
        filtered_tokens.sort(key=lambda t: doc_freq[t], reverse=True)
        filtered_tokens = filtered_tokens[:self.max_features]
        
        # Build vocabulary
        self.vocabulary = {token: idx for idx, token in enumerate(filtered_tokens)}
        
        # Compute IDF
        for token in self.vocabulary:
            df = doc_freq[token]
            self.idf[token] = math.log((1 + n_docs) / (1 + df)) + 1
    
    def transform(self, documents):
        """Transform documents to TF-IDF matrix."""
        n_docs = len(documents)
        n_features = len(self.vocabulary)
        
        tfidf_matrix = np.zeros((n_docs, n_features))
        
        for i, doc in enumerate(documents):
            tokens = self._tokenize(doc)
            tf = Counter(tokens)
            
            # L2 normalize TF
            total = sum(tf.values())
            if total > 0:
                for token, count in tf.items():
                    if token in self.vocabulary:
                        idx = self.vocabulary[token]
                        tfidf_matrix[i, idx] = (count / total) * self.idf[token]
            
            # L2 normalize row
            norm = np.linalg.norm(tfidf_matrix[i])
            if norm > 0:
                tfidf_matrix[i] /= norm
        
        return tfidf_matrix
    
    def fit_transform(self, documents):
        """Fit and transform in one step."""
        self.fit(documents)
        return self.transform(documents)
    
    def get_feature_names(self):
        """Return feature names (tokens)."""
        return list(self.vocabulary.keys())

# Example
documents = [
    "The cat sat on the mat",
    "The dog chased the cat",
    "The cat and dog are friends",
    "Machine learning is fascinating",
    "Deep learning uses neural networks",
]

vectorizer = TFIDFVectorizer(max_features=20)
tfidf_matrix = vectorizer.fit_transform(documents)

print("\n=== TF-IDF Vectorization ===")
print(f"Vocabulary size: {len(vectorizer.vocabulary)}")
print(f"Matrix shape: {tfidf_matrix.shape}")

# Show top features
feature_names = vectorizer.get_feature_names()
print(f"\nTop features: {feature_names[:10]}")

# Compute similarity
from numpy.linalg import norm

def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    return np.dot(a, b) / (norm(a) * norm(b) + 1e-10)

# Similarity between documents
print("\nDocument similarities:")
for i in range(len(documents)):
    for j in range(i+1, len(documents)):
        sim = cosine_similarity(tfidf_matrix[i], tfidf_matrix[j])
        print(f"  Doc {i} vs Doc {j}: {sim:.3f}")

Word Embeddings (Word2Vec-style)
import numpy as np
from collections import Counter, defaultdict

class SimpleWord2Vec:
    """Simplified Word2Vec (Skip-gram with negative sampling)."""
    
    def __init__(self, vector_size=100, window_size=5, 
                 learning_rate=0.025, n_negative=5):
        self.vector_size = vector_size
        self.window_size = window_size
        self.learning_rate = learning_rate
        self.n_negative = n_negative
        
        self.vocab = {}
        self.word_counts = Counter()
        self.W_in = None  # Input weights
        self.W_out = None  # Output weights
    
    def _sigmoid(self, x):
        """Numerically stable sigmoid."""
        return np.where(x >= 0, 
                       1 / (1 + np.exp(-x)),
                       np.exp(x) / (1 + np.exp(x)))
    
    def build_vocab(self, sentences, min_count=5):
        """Build vocabulary from sentences."""
        for sentence in sentences:
            self.word_counts.update(sentence)
        
        # Filter by min_count
        self.vocab = {
            word: idx for idx, (word, count) in 
            enumerate(self.word_counts.most_common())
            if count >= min_count
        }
        
        vocab_size = len(self.vocab)
        
        # Initialize weights
        np.random.seed(42)
        self.W_in = np.random.uniform(-0.5/vector_size, 0.5/vector_size, 
                                      (vocab_size, self.vector_size))
        self.W_out = np.random.uniform(-0.5/vector_size, 0.5/vector_size,
                                       (vocab_size, self.vector_size))
        
        print(f"Vocabulary size: {vocab_size}")
    
    def _generate_negative_samples(self, target_idx, n_samples):
        """Generate negative samples using unigram distribution."""
        # Simple uniform sampling (real W2Vec uses unigram^0.75)
        negatives = []
        while len(negatives) < n_samples:
            idx = np.random.randint(0, len(self.vocab))
            if idx != target_idx:
                negatives.append(idx)
        return negatives
    
    def train(self, sentences, epochs=5):
        """Train Word2Vec model."""
        vocab_size = len(self.vocab)
        
        for epoch in range(epochs):
            total_loss = 0
            n_examples = 0
            
            # Shuffle sentences
            np.random.shuffle(sentences)
            
            for sentence in sentences:
                # Convert to indices
                indices = [self.vocab[w] for w in sentence if w in self.vocab]
                
                for i, target_idx in enumerate(indices):
                    # Context window
                    window_start = max(0, i - self.window_size)
                    window_end = min(len(indices), i + self.window_size + 1)
                    
                    for j in range(window_start, window_end):
                        if i == j:
                            continue
                        
                        context_idx = indices[j]
                        
                        # Positive sample
                        hidden = self.W_in[target_idx]
                        score = np.dot(hidden, self.W_out[context_idx])
                        grad = self._sigmoid(score) - 1
                        loss = -np.log(self._sigmoid(score) + 1e-10)
                        total_loss += loss
                        n_examples += 1
                        
                        # Update
                        grad_out = grad * hidden
                        grad_in = grad * self.W_out[context_idx]
                        
                        self.W_out[context_idx] -= self.learning_rate * grad_out
                        self.W_in[target_idx] -= self.learning_rate * grad_in
                        
                        # Negative samples
                        negatives = self._generate_negative_samples(
                            context_idx, self.n_negative
                        )
                        
                        for neg_idx in negatives:
                            score = np.dot(hidden, self.W_out[neg_idx])
                            grad = self._sigmoid(score)
                            loss = -np.log(1 - self._sigmoid(score) + 1e-10)
                            total_loss += loss
                            n_examples += 1
                            
                            grad_out = grad * hidden
                            grad_in = grad * self.W_out[neg_idx]
                            
                            self.W_out[neg_idx] -= self.learning_rate * grad_out
                            self.W_in[target_idx] -= self.learning_rate * grad_in
            
            avg_loss = total_loss / max(n_examples, 1)
            print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")
    
    def get_vector(self, word):
        """Get word vector."""
        if word not in self.vocab:
            return None
        return self.W_in[self.vocab[word]]
    
    def most_similar(self, word, top_n=10):
        """Find most similar words."""
        if word not in self.vocab:
            return []
        
        vec = self.get_vector(word)
        similarities = []
        
        for other_word, idx in self.vocab.items():
            if other_word == word:
                continue
            other_vec = self.W_in[idx]
            sim = np.dot(vec, other_vec) / (np.linalg.norm(vec) * 
                                            np.linalg.norm(other_vec) + 1e-10)
            similarities.append((other_word, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_n]

# Example usage (with synthetic data)
sentences = [
    ["the", "cat", "sat", "on", "the", "mat"],
    ["the", "dog", "chased", "the", "cat"],
    ["the", "cat", "and", "dog", "are", "friends"],
    ["a", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"],
] * 100  # Repeat for training

w2v = SimpleWord2Vec(vector_size=50, window_size=2)
w2v.build_vocab(sentences, min_count=2)
w2v.train(sentences, epochs=3)

print("\n=== Word2Vec Results ===")
print("Most similar to 'cat':")
for word, sim in w2v.most_similar('cat', top_n=5):
    print(f"  {word}: {sim:.3f}")

CHAPTER 3: CLASSICAL NLP METHODS
N-gram Language Models
import numpy as np
from collections import defaultdict, Counter

class NGramLM:
    """N-gram language model with smoothing."""
    
    def __init__(self, n=2, smoothing='kneser_ney'):
        self.n = n
        self.smoothing = smoothing
        self.ngram_counts = defaultdict(Counter)
        self.context_counts = Counter()
        self.vocab = set()
    
    def _get_ngrams(self, tokens):
        """Extract n-grams from token sequence."""
        # Add start/end tokens
        tokens = ['<s>'] * (self.n - 1) + tokens + ['</s>']
        ngrams = []
        for i in range(len(tokens) - self.n + 1):
            ngram = tuple(tokens[i:i+self.n])
            ngrams.append(ngram)
        return ngrams
    
    def fit(self, sentences):
        """Fit model on sentences."""
        for sentence in sentences:
            ngrams = self._get_ngrams(sentence)
            for ngram in ngrams:
                context = ngram[:-1]
                word = ngram[-1]
                self.ngram_counts[context][word] += 1
                self.context_counts[context] += 1
                self.vocab.add(word)
    
    def probability(self, word, context):
        """Compute P(word | context) with smoothing."""
        context = tuple(context)
        
        if self.smoothing == 'laplace':
            # Add-one smoothing
            count = self.ngram_counts[context].get(word, 0) + 1
            total = self.context_counts[context] + len(self.vocab)
            return count / total
        
        elif self.smoothing == 'kneser_ney':
            # Simplified Kneser-Ney
            count = self.ngram_counts[context].get(word, 0)
            total = self.context_counts[context]
            
            if total == 0:
                return 1.0 / len(self.vocab)
            
            # Discount
            discount = 0.75
            if count > 0:
                return max(count - discount, 0) / total
            else:
                # Backoff
                return discount * len(self.ngram_counts[context]) / (total * len(self.vocab))
        
        else:  # No smoothing
            count = self.ngram_counts[context].get(word, 0)
            total = self.context_counts[context]
            return count / total if total > 0 else 0
    
    def perplexity(self, sentences):
        """Compute perplexity on test sentences."""
        log_prob = 0
        n_words = 0
        
        for sentence in sentences:
            ngrams = self._get_ngrams(sentence)
            for ngram in ngrams:
                context = ngram[:-1]
                word = ngram[-1]
                prob = self.probability(word, context)
                log_prob += np.log(prob + 1e-10)
                n_words += 1
        
        return np.exp(-log_prob / n_words)
    
    def generate(self, max_length=20, context=None):
        """Generate text from the model."""
        if context is None:
            context = ['<s>'] * (self.n - 1)
        else:
            context = list(context[-(self.n-1):])
        
        generated = list(context)
        
        for _ in range(max_length):
            # Sample next word
            probs = []
            words = []
            for word in self.vocab:
                prob = self.probability(word, context)
                probs.append(prob)
                words.append(word)
            
            # Normalize
            probs = np.array(probs)
            probs = probs / probs.sum()
            
            # Sample
            next_word = np.random.choice(words, p=probs)
            generated.append(next_word)
            
            if next_word == '</s>':
                break
            
            context = generated[-(self.n-1):]
        
        return [w for w in generated if w not in ['<s>', '</s>']]

# Example
training_sentences = [
    ["the", "cat", "sat", "on", "the", "mat"],
    ["the", "dog", "chased", "the", "cat"],
    ["the", "cat", "slept", "on", "the", "bed"],
    ["a", "dog", "ran", "in", "the", "park"],
] * 10

lm = NGramLM(n=2, smoothing='laplace')
lm.fit(training_sentences)

print("=== N-gram Language Model ===")
print(f"Vocabulary size: {len(lm.vocab)}")
print(f"Perplexity: {lm.perplexity(training_sentences):.2f}")

print("\nGenerated sentences:")
for _ in range(5):
    generated = lm.generate(max_length=10)
    print(f"  {' '.join(generated)}")

Hidden Markov Models (HMM) for POS Tagging
import numpy as np
from collections import defaultdict

class HMMPOSTagger:
    """Hidden Markov Model for POS tagging."""
    
    def __init__(self):
        self.tags = set()
        self.words = set()
        
        # Transition probabilities: P(tag_i | tag_{i-1})
        self.transition_counts = defaultdict(Counter)
        self.tag_counts = Counter()
        
        # Emission probabilities: P(word | tag)
        self.emission_counts = defaultdict(Counter)
        
        # Initial probabilities: P(tag_0)
        self.initial_counts = Counter()
    
    def fit(self, sentences):
        """
        Fit HMM on tagged sentences.
        sentences: list of [(word, tag), ...]
        """
        for sentence in sentences:
            prev_tag = '<START>'
            
            for word, tag in sentence:
                self.words.add(word)
                self.tags.add(tag)
                
                # Initial
                if prev_tag == '<START>':
                    self.initial_counts[tag] += 1
                
                # Transition
                self.transition_counts[prev_tag][tag] += 1
                self.tag_counts[prev_tag] += 1
                
                # Emission
                self.emission_counts[tag][word] += 1
                
                prev_tag = tag
            
            # End transition
            self.transition_counts[prev_tag]['<END>'] += 1
            self.tag_counts[prev_tag] += 1
    
    def _transition_prob(self, prev_tag, tag):
        """Compute P(tag | prev_tag)."""
        count = self.transition_counts[prev_tag].get(tag, 0)
        total = self.tag_counts[prev_tag]
        
        # Laplace smoothing
        return (count + 1) / (total + len(self.tags) + 1)
    
    def _emission_prob(self, tag, word):
        """Compute P(word | tag)."""
        count = self.emission_counts[tag].get(word, 0)
        total = sum(self.emission_counts[tag].values())
        
        # Laplace smoothing
        return (count + 1) / (total + len(self.words) + 1)
    
    def _initial_prob(self, tag):
        """Compute P(tag_0 = tag)."""
        count = self.initial_counts[tag]
        total = sum(self.initial_counts.values())
        return (count + 1) / (total + len(self.tags) + 1)
    
    def viterbi(self, sentence):
        """
        Viterbi algorithm for most likely tag sequence.
        sentence: list of words
        """
        n = len(sentence)
        tags = list(self.tags)
        
        # Viterbi table
        V = [{} for _ in range(n)]
        backpointer = [{} for _ in range(n)]
        
        # Initialization
        for tag in tags:
            V[0][tag] = (self._initial_prob(tag) * 
                        self._emission_prob(tag, sentence[0]))
            backpointer[0][tag] = '<START>'
        
        # Recursion
        for t in range(1, n):
            for tag in tags:
                best_prob = -1
                best_prev = None
                
                for prev_tag in tags:
                    prob = (V[t-1][prev_tag] * 
                           self._transition_prob(prev_tag, tag) *
                           self._emission_prob(tag, sentence[t]))
                    
                    if prob > best_prob:
                        best_prob = prob
                        best_prev = prev_tag
                
                V[t][tag] = best_prob
                backpointer[t][tag] = best_prev
        
        # Termination
        best_prob = -1
        best_tag = None
        
        for tag in tags:
            prob = V[n-1][tag] * self._transition_prob(tag, '<END>')
            if prob > best_prob:
                best_prob = prob
                best_tag = tag
        
        # Backtrack
        tags_sequence = [best_tag]
        for t in range(n-1, 0, -1):
            best_tag = backpointer[t][best_tag]
            tags_sequence.insert(0, best_tag)
        
        return tags_sequence

# Example
training_data = [
    [("The", "DT"), ("cat", "NN"), ("sat", "VBD"), ("on", "IN"), 
     ("the", "DT"), ("mat", "NN")],
    [("The", "DT"), ("dog", "NN"), ("chased", "VBD"), ("the", "DT"), 
     ("cat", "NN")],
    [("A", "DT"), ("big", "JJ"), ("dog", "NN"), ("ran", "VBD")],
] * 20

hmm = HMMPOSTagger()
hmm.fit(training_data)

test_sentence = ["The", "big", "cat", "sat"]
tags = hmm.viterbi(test_sentence)

print("\n=== HMM POS Tagging ===")
for word, tag in zip(test_sentence, tags):
    print(f"  {word:10s} → {tag}")

Conditional Random Fields (CRF) - Conceptual
class CRFConceptual:
    """Conceptual CRF implementation."""
    
    def __init__(self):
        self.feature_weights = {}
        self.transition_weights = {}
    
    def describe(self):
        """Describe CRF concepts."""
        print("=== Conditional Random Fields ===")
        print("\nCRF is a discriminative model for sequence labeling.")
        print("\nKey differences from HMM:")
        print("  • Discriminative (models P(Y|X)) vs Generative (P(X,Y))")
        print("  • Can use arbitrary features of observation sequence")
        print("  • Avoids independence assumptions")
        print("  • Better for NLP tasks (NER, POS, chunking)")
        
        print("\nFeature types:")
        print("  • State features: f(y_t, x, t)")
        print("  • Transition features: f(y_{t-1}, y_t, x, t)")
        
        print("\nTraining:")
        print("  • Maximize conditional log-likelihood")
        print("  • L-BFGS or gradient descent")
        print("  • L1/L2 regularization")
        
        print("\nInference:")
        print("  • Viterbi algorithm (most likely sequence)")
        print("  • Forward-backward (marginals)")
        
        print("\nPopular libraries:")
        print("  • sklearn-crfsuite")
        print("  • pycrfsuite")
        print("  • MALLET")

crf = CRFConceptual()
crf.describe()

CHAPTER 4: NEURAL NETWORKS FOR NLP
RNN for Sequence Modeling
import numpy as np

class SimpleRNN:
    """Simple RNN for sequence classification."""
    
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Initialize weights
        scale = np.sqrt(1.0 / input_size)
        self.W_xh = np.random.randn(input_size, hidden_size) * scale
        self.W_hh = np.random.randn(hidden_size, hidden_size) * scale
        self.W_hy = np.random.randn(hidden_size, output_size) * scale
        
        self.b_h = np.zeros(hidden_size)
        self.b_y = np.zeros(output_size)
    
    def forward(self, x_sequence):
        """
        Forward pass through RNN.
        x_sequence: shape (seq_len, input_size)
        """
        seq_len = len(x_sequence)
        h = np.zeros(self.hidden_size)
        hidden_states = []
        
        for t in range(seq_len):
            x_t = x_sequence[t]
            h = np.tanh(x_t @ self.W_xh + h @ self.W_hh + self.b_h)
            hidden_states.append(h.copy())
        
        # Use final hidden state for classification
        y = hidden_states[-1] @ self.W_hy + self.b_y
        
        return y, hidden_states
    
    def predict(self, x_sequence):
        """Predict class."""
        y, _ = self.forward(x_sequence)
        return np.argmax(y)

# Example: sentiment classification
rnn = SimpleRNN(input_size=10, hidden_size=20, output_size=2)

# Dummy input (sequence of word embeddings)
seq_len = 5
x_sequence = np.random.randn(seq_len, 10)

y, hidden_states = rnn.forward(x_sequence)
print(f"\n=== Simple RNN ===")
print(f"Input shape: {x_sequence.shape}")
print(f"Hidden states: {len(hidden_states)} × {hidden_states[0].shape}")
print(f"Output logits: {y}")
print(f"Predicted class: {np.argmax(y)}")

LSTM Implementation
class LSTMCell:
    """Long Short-Term Memory cell."""
    
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size
        
        # Combined weights for all gates
        scale = np.sqrt(1.0 / (input_size + hidden_size))
        
        # Forget gate
        self.W_f = np.random.randn(input_size + hidden_size, hidden_size) * scale
        self.b_f = np.ones(hidden_size)  # Initialize to 1 (helps gradient flow)
        
        # Input gate
        self.W_i = np.random.randn(input_size + hidden_size, hidden_size) * scale
        self.b_i = np.zeros(hidden_size)
        
        # Cell candidate
        self.W_c = np.random.randn(input_size + hidden_size, hidden_size) * scale
        self.b_c = np.zeros(hidden_size)
        
        # Output gate
        self.W_o = np.random.randn(input_size + hidden_size, hidden_size) * scale
        self.b_o = np.zeros(hidden_size)
    
    def forward(self, x, h_prev, c_prev):
        """
        Forward pass through LSTM cell.
        x: input (input_size,)
        h_prev: previous hidden state (hidden_size,)
        c_prev: previous cell state (hidden_size,)
        """
        # Concatenate input and previous hidden state
        combined = np.concatenate([x, h_prev])
        
        # Gates
        f = 1 / (1 + np.exp(-(combined @ self.W_f + self.b_f)))  # Forget
        i = 1 / (1 + np.exp(-(combined @ self.W_i + self.b_i)))  # Input
        c_tilde = np.tanh(combined @ self.W_c + self.b_c)        # Candidate
        o = 1 / (1 + np.exp(-(combined @ self.W_o + self.b_o)))  # Output
        
        # Cell state update
        c = f * c_prev + i * c_tilde
        
        # Hidden state
        h = o * np.tanh(c)
        
        return h, c

class LSTM:
    """LSTM for sequence processing."""
    
    def __init__(self, input_size, hidden_size):
        self.cell = LSTMCell(input_size, hidden_size)
        self.hidden_size = hidden_size
    
    def forward(self, x_sequence):
        """
        Process entire sequence.
        x_sequence: shape (seq_len, input_size)
        """
        seq_len = x_sequence.shape[0]
        
        h = np.zeros(self.hidden_size)
        c = np.zeros(self.hidden_size)
        
        hidden_states = []
        cell_states = []
        
        for t in range(seq_len):
            h, c = self.cell.forward(x_sequence[t], h, c)
            hidden_states.append(h.copy())
            cell_states.append(c.copy())
        
        return np.array(hidden_states), np.array(cell_states)

# Example
lstm = LSTM(input_size=10, hidden_size=20)
x_sequence = np.random.randn(5, 10)

hidden_states, cell_states = lstm.forward(x_sequence)
print(f"\n=== LSTM ===")
print(f"Input shape: {x_sequence.shape}")
print(f"Hidden states shape: {hidden_states.shape}")
print(f"Cell states shape: {cell_states.shape}")

GRU Implementation
class GRUCell:
    """Gated Recurrent Unit cell."""
    
    def __init__(self, input_size, hidden_size):
        self.hidden_size = hidden_size
        scale = np.sqrt(1.0 / (input_size + hidden_size))
        
        # Reset gate
        self.W_r = np.random.randn(input_size + hidden_size, hidden_size) * scale
        self.b_r = np.zeros(hidden_size)
        
        # Update gate
        self.W_z = np.random.randn(input_size + hidden_size, hidden_size) * scale
        self.b_z = np.zeros(hidden_size)
        
        # Candidate
        self.W_h = np.random.randn(input_size + hidden_size, hidden_size) * scale
        self.b_h = np.zeros(hidden_size)
    
    def forward(self, x, h_prev):
        """Forward pass through GRU cell."""
        combined = np.concatenate([x, h_prev])
        
        # Gates
        z = 1 / (1 + np.exp(-(combined @ self.W_z + self.b_z)))  # Update
        r = 1 / (1 + np.exp(-(combined @ self.W_r + self.b_r)))  # Reset
        
        # Candidate with reset gate applied to previous hidden state
        combined_h = np.concatenate([x, r * h_prev])
        h_tilde = np.tanh(combined_h @ self.W_h + self.b_h)
        
        # New hidden state
        h = (1 - z) * h_prev + z * h_tilde
        
        return h

class GRU:
    """GRU for sequence processing."""
    
    def __init__(self, input_size, hidden_size):
        self.cell = GRUCell(input_size, hidden_size)
        self.hidden_size = hidden_size
    
    def forward(self, x_sequence):
        """Process sequence."""
        seq_len = x_sequence.shape[0]
        h = np.zeros(self.hidden_size)
        
        hidden_states = []
        
        for t in range(seq_len):
            h = self.cell.forward(x_sequence[t], h)
            hidden_states.append(h.copy())
        
        return np.array(hidden_states)

# Example
gru = GRU(input_size=10, hidden_size=20)
x_sequence = np.random.randn(5, 10)

hidden_states = gru.forward(x_sequence)
print(f"\n=== GRU ===")
print(f"Hidden states shape: {hidden_states.shape}")

Bidirectional RNN
class BiRNN:
    """Bidirectional RNN."""
    
    def __init__(self, input_size, hidden_size):
        self.forward_rnn = LSTM(input_size, hidden_size)
        self.backward_rnn = LSTM(input_size, hidden_size)
        self.hidden_size = hidden_size
    
    def forward(self, x_sequence):
        """Process sequence in both directions."""
        # Forward pass
        forward_states, _ = self.forward_rnn.forward(x_sequence)
        
        # Backward pass (reverse sequence)
        backward_states, _ = self.backward_rnn.forward(x_sequence[::-1])
        backward_states = backward_states[::-1]  # Reverse back
        
        # Concatenate
        combined = np.concatenate([forward_states, backward_states], axis=1)
        
        return combined

# Example
birnn = BiRNN(input_size=10, hidden_size=20)
x_sequence = np.random.randn(5, 10)

combined_states = birnn.forward(x_sequence)
print(f"\n=== Bidirectional RNN ===")
print(f"Combined states shape: {combined_states.shape}")
print(f"Expected: (5, {2 * 20}) = (5, 40)")

CHAPTER 5: ATTENTION MECHANISM
Scaled Dot-Product Attention
import numpy as np

def softmax(x, axis=-1):
    """Numerically stable softmax."""
    e_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e_x / np.sum(e_x, axis=axis, keepdims=True)

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Scaled dot-product attention.
    Q, K, V: shape (..., seq_len, d_k)
    mask: optional mask for padding/causal attention
    """
    d_k = Q.shape[-1]
    
    # Compute attention scores
    scores = Q @ K.transpose(0, 2, 1) / np.sqrt(d_k)
    
    # Apply mask
    if mask is not None:
        scores = np.where(mask == 0, -1e9, scores)
    
    # Softmax over keys
    weights = softmax(scores, axis=-1)
    
    # Weighted sum of values
    output = weights @ V
    
    return output, weights

# Example
batch_size = 2
seq_len = 5
d_k = 8

Q = np.random.randn(batch_size, seq_len, d_k)
K = np.random.randn(batch_size, seq_len, d_k)
V = np.random.randn(batch_size, seq_len, d_k)

output, weights = scaled_dot_product_attention(Q, K, V)
print("=== Scaled Dot-Product Attention ===")
print(f"Q, K, V shape: {Q.shape}")
print(f"Output shape: {output.shape}")
print(f"Attention weights shape: {weights.shape}")
print(f"Weights sum to 1: {np.allclose(weights.sum(axis=-1), 1.0)}")

Multi-Head Attention
class MultiHeadAttention:
    """Multi-head attention mechanism."""
    
    def __init__(self, d_model, num_heads):
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Projection matrices
        scale = np.sqrt(2.0 / d_model)
        self.W_q = np.random.randn(d_model, d_model) * scale
        self.W_k = np.random.randn(d_model, d_model) * scale
        self.W_v = np.random.randn(d_model, d_model) * scale
        self.W_o = np.random.randn(d_model, d_model) * scale
    
    def forward(self, Q, K, V, mask=None):
        """
        Forward pass through multi-head attention.
        Q, K, V: shape (batch, seq_len, d_model)
        """
        batch_size, seq_len, _ = Q.shape
        
        # Linear projections
        Q_proj = Q @ self.W_q
        K_proj = K @ self.W_k
        V_proj = V @ self.W_v
        
        # Reshape to (batch, num_heads, seq_len, d_k)
        Q_proj = Q_proj.reshape(batch_size, seq_len, self.num_heads, self.d_k)
        Q_proj = Q_proj.transpose(0, 2, 1, 3)
        
        K_proj = K_proj.reshape(batch_size, seq_len, self.num_heads, self.d_k)
        K_proj = K_proj.transpose(0, 2, 1, 3)
        
        V_proj = V_proj.reshape(batch_size, seq_len, self.num_heads, self.d_k)
        V_proj = V_proj.transpose(0, 2, 1, 3)
        
        # Scaled dot-product attention
        attn_output, attn_weights = scaled_dot_product_attention(
            Q_proj, K_proj, V_proj, mask
        )
        
        # Concatenate heads: (batch, num_heads, seq, d_k) → (batch, seq, d_model)
        attn_output = attn_output.transpose(0, 2, 1, 3)
        attn_output = attn_output.reshape(batch_size, seq_len, self.d_model)
        
        # Final linear projection
        output = attn_output @ self.W_o
        
        return output, attn_weights

# Example
mha = MultiHeadAttention(d_model=64, num_heads=8)
X = np.random.randn(2, 10, 64)

output, weights = mha.forward(X, X, X)
print(f"\n=== Multi-Head Attention ===")
print(f"Input shape: {X.shape}")
print(f"Output shape: {output.shape}")
print(f"Attention weights shape: {weights.shape}")

Self-Attention Visualization
def visualize_attention(text, attention_weights):
    """Visualize attention weights for a sentence."""
    words = text.split()
    n = len(words)
    
    print("\n=== Attention Visualization ===")
    print(f"{'':15s}", end="")
    for word in words:
        print(f"{word:10s}", end="")
    print()
    
    for i, word in enumerate(words):
        print(f"{word:15s}", end="")
        for j in range(n):
            weight = attention_weights[i, j]
            # Represent weight with asterisks
            n_stars = int(weight * 20)
            print(f"{'*' * n_stars:10s}", end="")
        print()

# Example
text = "the cat sat on the mat"
words = text.split()
n = len(words)

# Simulate attention weights (higher for nearby words)
attention_weights = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        distance = abs(i - j)
        attention_weights[i, j] = np.exp(-distance / 2)
    attention_weights[i] /= attention_weights[i].sum()

visualize_attention(text, attention_weights)

Positional Encoding
class PositionalEncoding:
    """Sinusoidal positional encoding."""
    
    def __init__(self, d_model, max_len=5000):
        self.d_model = d_model
        
        # Compute positional encodings
        pe = np.zeros((max_len, d_model))
        position = np.arange(max_len)[:, np.newaxis]
        div_term = np.exp(np.arange(0, d_model, 2) * (-np.log(10000.0) / d_model))
        
        pe[:, 0::2] = np.sin(position * div_term)
        pe[:, 1::2] = np.cos(position * div_term)
        
        self.pe = pe[np.newaxis, :, :]  # (1, max_len, d_model)
    
    def forward(self, x):
        """Add positional encoding to input."""
        seq_len = x.shape[1]
        return x + self.pe[:, :seq_len, :]

# Example
pe = PositionalEncoding(d_model=64, max_len=100)
x = np.random.randn(2, 10, 64)
x_encoded = pe.forward(x)

print(f"\n=== Positional Encoding ===")
print(f"Input shape: {x.shape}")
print(f"Encoded shape: {x_encoded.shape}")

# Visualize positional encoding
plt.figure(figsize=(10, 5))
plt.imshow(pe.pe[0, :50, :].T, aspect='auto', cmap='viridis')
plt.xlabel('Position')
plt.ylabel('Dimension')
plt.title('Positional Encoding Matrix')
plt.colorbar()
plt.tight_layout()
plt.savefig('positional_encoding.png', dpi=100)
plt.show()

CHAPTER 6: TRANSFORMER ARCHITECTURE
Transformer Encoder Layer
class LayerNorm:
    """Layer normalization."""
    
    def __init__(self, d_model, eps=1e-5):
        self.eps = eps
        self.gamma = np.ones((1, 1, d_model))
        self.beta = np.zeros((1, 1, d_model))
    
    def forward(self, x):
        mean = np.mean(x, axis=-1, keepdims=True)
        var = np.var(x, axis=-1, keepdims=True)
        x_norm = (x - mean) / np.sqrt(var + self.eps)
        return self.gamma * x_norm + self.beta

class FeedForward:
    """Position-wise feed-forward network."""
    
    def __init__(self, d_model, d_ff):
        scale1 = np.sqrt(2.0 / d_model)
        scale2 = np.sqrt(2.0 / d_ff)
        
        self.W1 = np.random.randn(d_model, d_ff) * scale1
        self.b1 = np.zeros(d_ff)
        self.W2 = np.random.randn(d_ff, d_model) * scale2
        self.b2 = np.zeros(d_model)
    
    def forward(self, x):
        # GELU activation
        h = x @ self.W1 + self.b1
        h = 0.5 * h * (1 + np.tanh(np.sqrt(2/np.pi) * (h + 0.044715 * h**3)))
        return h @ self.W2 + self.b2

class TransformerEncoderLayer:
    """Single transformer encoder layer."""
    
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)
        self.ff = FeedForward(d_model, d_ff)
        self.dropout = dropout
    
    def forward(self, x, mask=None):
        # Self-attention + residual + layer norm
        attn_output, _ = self.attention.forward(x, x, x, mask)
        x = self.norm1.forward(x + attn_output)
        
        # Feed-forward + residual + layer norm
        ff_output = self.ff.forward(x)
        x = self.norm2.forward(x + ff_output)
        
        return x

class TransformerDecoderLayer:
    """Single transformer decoder layer."""
    
    def __init__(self, d_model, num_heads, d_ff):
        self.self_attention = MultiHeadAttention(d_model, num_heads)
        self.cross_attention = MultiHeadAttention(d_model, num_heads)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)
        self.norm3 = LayerNorm(d_model)
        self.ff = FeedForward(d_model, d_ff)
    
    def forward(self, x, encoder_output, src_mask=None, tgt_mask=None):
        # Masked self-attention
        self_attn_output, _ = self.self_attention.forward(x, x, x, tgt_mask)
        x = self.norm1.forward(x + self_attn_output)
        
        # Cross-attention
        cross_attn_output, _ = self.cross_attention.forward(
            x, encoder_output, encoder_output, src_mask
        )
        x = self.norm2.forward(x + cross_attn_output)
        
        # Feed-forward
        ff_output = self.ff.forward(x)
        x = self.norm3.forward(x + ff_output)
        
        return x

# Example
encoder_layer = TransformerEncoderLayer(d_model=64, num_heads=8, d_ff=256)
decoder_layer = TransformerDecoderLayer(d_model=64, num_heads=8, d_ff=256)

src = np.random.randn(2, 10, 64)
tgt = np.random.randn(2, 8, 64)

encoder_output = encoder_layer.forward(src)
decoder_output = decoder_layer.forward(tgt, encoder_output)

print("=== Transformer Layers ===")
print(f"Encoder output shape: {encoder_output.shape}")
print(f"Decoder output shape: {decoder_output.shape}")

Full Transformer
class Transformer:
    """Complete Transformer model."""
    
    def __init__(self, src_vocab_size, tgt_vocab_size, 
                 d_model=512, num_heads=8, num_layers=6, 
                 d_ff=2048, max_len=5000):
        self.d_model = d_model
        self.num_layers = num_layers
        
        # Embeddings
        scale = np.sqrt(2.0 / d_model)
        self.src_embed = np.random.randn(src_vocab_size, d_model) * scale
        self.tgt_embed = np.random.randn(tgt_vocab_size, d_model) * scale
        
        # Positional encoding
        self.pos_enc = PositionalEncoding(d_model, max_len)
        
        # Encoder and decoder stacks
        self.encoder_layers = [
            TransformerEncoderLayer(d_model, num_heads, d_ff)
            for _ in range(num_layers)
        ]
        self.decoder_layers = [
            TransformerDecoderLayer(d_model, num_heads, d_ff)
            for _ in range(num_layers)
        ]
        
        # Output projection
        self.output_proj = np.random.randn(d_model, tgt_vocab_size) * scale
    
    def encode(self, src_tokens, src_mask=None):
        """Encode source sequence."""
        # Embed + scale + positional encoding
        x = self.src_embed[src_tokens] * np.sqrt(self.d_model)
        x = self.pos_enc.forward(x)
        
        # Pass through encoder layers
        for layer in self.encoder_layers:
            x = layer.forward(x, src_mask)
        
        return x
    
    def decode(self, tgt_tokens, encoder_output, src_mask=None, tgt_mask=None):
        """Decode target sequence."""
        x = self.tgt_embed[tgt_tokens] * np.sqrt(self.d_model)
        x = self.pos_enc.forward(x)
        
        for layer in self.decoder_layers:
            x = layer.forward(x, encoder_output, src_mask, tgt_mask)
        
        # Project to vocabulary
        logits = x @ self.output_proj
        return logits
    
    def forward(self, src_tokens, tgt_tokens):
        """Full forward pass."""
        encoder_output = self.encode(src_tokens)
        
        # Causal mask for decoder
        seq_len = tgt_tokens.shape[1]
        tgt_mask = np.tril(np.ones((seq_len, seq_len)))
        
        logits = self.decode(tgt_tokens, encoder_output, tgt_mask=tgt_mask)
        return logits

# Example
transformer = Transformer(
    src_vocab_size=10000,
    tgt_vocab_size=10000,
    d_model=64,
    num_heads=4,
    num_layers=2,
    d_ff=256
)

src = np.random.randint(0, 10000, (2, 10))
tgt = np.random.randint(0, 10000, (2, 8))

logits = transformer.forward(src, tgt)
print(f"\n=== Full Transformer ===")
print(f"Source tokens shape: {src.shape}")
print(f"Target tokens shape: {tgt.shape}")
print(f"Logits shape: {logits.shape}")

BERT-style Model
class BERTStyleModel:
    """Simplified BERT-style model (encoder-only)."""
    
    def __init__(self, vocab_size, d_model=768, num_heads=12, 
                 num_layers=12, max_len=512):
        self.d_model = d_model
        self.num_layers = num_layers
        
        # Token and position embeddings
        scale = np.sqrt(2.0 / d_model)
        self.token_embed = np.random.randn(vocab_size, d_model) * scale
        self.pos_embed = np.random.randn(max_len, d_model) * scale
        self.segment_embed = np.random.randn(2, d_model) * scale
        
        # Encoder layers
        self.encoder_layers = [
            TransformerEncoderLayer(d_model, num_heads, d_model * 4)
            for _ in range(num_layers)
        ]
        
        # MLM head
        self.mlm_head = np.random.randn(d_model, vocab_size) * scale
        
        # NSP head
        self.nsp_head = np.random.randn(d_model, 2) * scale
    
    def forward(self, input_ids, token_type_ids=None, attention_mask=None):
        """
        Forward pass.
        input_ids: (batch, seq_len)
        token_type_ids: (batch, seq_len) - segment IDs
        attention_mask: (batch, seq_len) - padding mask
        """
        batch_size, seq_len = input_ids.shape
        
        # Embeddings
        x = self.token_embed[input_ids]
        x = x + self.pos_embed[:seq_len]
        
        if token_type_ids is not None:
            x = x + self.segment_embed[token_type_ids]
        
        # Create attention mask
        if attention_mask is not None:
            mask = attention_mask[:, np.newaxis, np.newaxis, :]
        else:
            mask = None
        
        # Encoder layers
        for layer in self.encoder_layers:
            x = layer.forward(x, mask)
        
        # MLM logits
        mlm_logits = x @ self.mlm_head
        
        # NSP logits (use [CLS] token)
        cls_output = x[:, 0, :]
        nsp_logits = cls_output @ self.nsp_head
        
        return mlm_logits, nsp_logits

# Example
bert = BERTStyleModel(
    vocab_size=30000,
    d_model=128,
    num_heads=4,
    num_layers=2
)

input_ids = np.random.randint(0, 30000, (2, 20))
token_type_ids = np.zeros((2, 20), dtype=int)
token_type_ids[:, 10:] = 1

mlm_logits, nsp_logits = bert.forward(input_ids, token_type_ids)

print(f"\n=== BERT-style Model ===")
print(f"Input shape: {input_ids.shape}")
print(f"MLM logits shape: {mlm_logits.shape}")
print(f"NSP logits shape: {nsp_logits.shape}")

GPT-style Model
class GPTStyleModel:
    """Simplified GPT-style model (decoder-only)."""
    
    def __init__(self, vocab_size, d_model=768, num_heads=12, 
                 num_layers=12, max_len=1024):
        self.d_model = d_model
        self.num_layers = num_layers
        self.vocab_size = vocab_size
        
        # Embeddings
        scale = np.sqrt(2.0 / d_model)
        self.token_embed = np.random.randn(vocab_size, d_model) * scale
        self.pos_embed = np.random.randn(max_len, d_model) * scale
        
        # Decoder layers
        self.decoder_layers = [
            TransformerDecoderLayer(d_model, num_heads, d_model * 4)
            for _ in range(num_layers)
        ]
        
        # Output projection (tied with embeddings)
        self.output_proj = self.token_embed.T
    
    def _causal_mask(self, seq_len):
        """Create causal attention mask."""
        mask = np.tril(np.ones((seq_len, seq_len)))
        return mask[np.newaxis, np.newaxis, :, :]
    
    def forward(self, input_ids):
        """
        Forward pass.
        input_ids: (batch, seq_len)
        """
        batch_size, seq_len = input_ids.shape
        
        # Embeddings
        x = self.token_embed[input_ids]
        x = x + self.pos_embed[:seq_len]
        
        # Causal mask
        mask = self._causal_mask(seq_len)
        
        # Decoder layers (no cross-attention for GPT)
        for layer in self.decoder_layers:
            # Simplified: use self-attention only
            x = layer.self_attention.forward(x, x, x, mask)[0]
            x = layer.norm1.forward(x + x)  # Residual + norm
            x = layer.norm2.forward(x + layer.ff.forward(x))
        
        # Logits
        logits = x @ self.output_proj
        
        return logits
    
    def generate(self, input_ids, max_new_tokens=50, temperature=1.0):
        """Generate text autoregressively."""
        generated = input_ids.copy()
        
        for _ in range(max_new_tokens):
            # Forward pass
            logits = self.forward(generated)
            
            # Get logits for last token
            next_token_logits = logits[:, -1, :] / temperature
            
            # Sample from distribution
            probs = softmax(next_token_logits, axis=-1)
            next_token = np.array([
                np.random.choice(self.vocab_size, p=p)
                for p in probs
            ])
            
            # Append
            generated = np.concatenate([
                generated, next_token[:, np.newaxis]
            ], axis=1)
        
        return generated

# Example
gpt = GPTStyleModel(
    vocab_size=30000,
    d_model=128,
    num_heads=4,
    num_layers=2
)

input_ids = np.random.randint(0, 30000, (2, 10))
logits = gpt.forward(input_ids)

print(f"\n=== GPT-style Model ===")
print(f"Input shape: {input_ids.shape}")
print(f"Logits shape: {logits.shape}")

# Generate
generated = gpt.generate(input_ids, max_new_tokens=5)
print(f"Generated shape: {generated.shape}")

CHAPTER 7: MODERN LLMS
LLM Training Pipeline
class LLMTrainer:
    """Conceptual LLM training pipeline."""
    
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
    
    def describe_pipeline(self):
        """Describe LLM training pipeline."""
        print("=== LLM Training Pipeline ===\n")
        
        print("1. Data Collection:")
        print("   • Common Crawl (web text)")
        print("   • Books, Wikipedia, code repositories")
        print("   • Filtering and deduplication")
        print("   • Quality filtering (heuristics, classifiers)")
        
        print("\n2. Tokenization:")
        print("   • BPE (GPT-2, GPT-3/4)")
        print("   • SentencePiece (LLaMA, T5)")
        print("   • tiktoken (OpenAI)")
        print("   • Vocabulary size: 32K-100K tokens")
        
        print("\n3. Pre-training:")
        print("   • Objective: next token prediction (causal LM)")
        print("   • Compute: thousands of GPUs for weeks/months")
        print("   • Data: trillions of tokens")
        print("   • Techniques: gradient checkpointing, mixed precision")
        
        print("\n4. Fine-tuning:")
        print("   • Supervised Fine-Tuning (SFT)")
        print("   • Instruction tuning (Alpaca, FLAN)")
        print("   • RLHF (Reinforcement Learning from Human Feedback)")
        print("   • DPO (Direct Preference Optimization)")
        
        print("\n5. Evaluation:")
        print("   • Perplexity on held-out data")
        print("   • Benchmarks: MMLU, HellaSwag, ARC, TruthfulQA")
        print("   • Human evaluation")
        print("   • Red teaming (safety)")
    
    def describe_scaling_laws(self):
        """Describe neural scaling laws."""
        print("\n=== Neural Scaling Laws ===\n")
        
        print("Kaplan et al. (2020) discovered power-law relationships:")
        print("  • Loss ∝ N^(-α)  (model parameters)")
        print("  • Loss ∝ D^(-β)  (dataset size)")
        print("  • Loss ∝ C^(-γ)  (compute budget)")
        
        print("\nChinchilla (Hoffmann et al., 2022):")
        print("  • Optimal: model size ∝ dataset size")
        print("  • 70B model needs ~1.4T tokens")
        print("  • LLaMA 2: 7B/13B/70B with 2T tokens")
        
        print("\nEmergent abilities (Wei et al., 2022):")
        print("  • Capabilities appear suddenly at scale")
        print("  • Chain-of-thought reasoning")
        print("  • In-context learning")
        print("  • Instruction following")

trainer = LLMTrainer(None, None)
trainer.describe_pipeline()
trainer.describe_scaling_laws()

RLHF (Reinforcement Learning from Human Feedback)
class RLHFConceptual:
    """Conceptual RLHF implementation."""
    
    def describe(self):
        """Describe RLHF process."""
        print("=== RLHF Process ===\n")
        
        print("Stage 1: Supervised Fine-Tuning (SFT)")
        print("  • Fine-tune base model on instruction-response pairs")
        print("  • High-quality human demonstrations")
        print("  • Result: SFT model")
        
        print("\nStage 2: Reward Model Training")
        print("  • Collect human preferences: (prompt, response_A, response_B)")
        print("  • Train reward model to predict preference")
        print("  • Loss: Bradley-Terry model")
        print("  • Result: reward model R(x, y)")
        
        print("\nStage 3: PPO Optimization")
        print("  • Optimize policy π_θ to maximize reward")
        print("  • KL penalty to stay close to SFT model")
        print("  • Objective: E[R(x,y)] - β * KL(π_θ || π_SFT)")
        print("  • Result: RLHF model")
        
        print("\nDPO Alternative (Rafailov et al., 2023):")
        print("  • Directly optimize policy from preferences")
        print("  • No separate reward model needed")
        print("  • Loss: -log σ(β * (log π(y_w|x)/π_ref(y_w|x) - log π(y_l|x)/π_ref(y_l|x)))")
        print("  • Simpler and more stable than PPO")

rlhf = RLHFConceptual()
rlhf.describe()

Inference Optimization
class InferenceOptimizer:
    """LLM inference optimization techniques."""
    
    def describe_techniques(self):
        """Describe optimization techniques."""
        print("=== LLM Inference Optimization ===\n")
        
        print("1. KV-Cache:")
        print("   • Cache key/value tensors from previous tokens")
        print("   • Avoid recomputation during generation")
        print("   • Memory: O(batch * seq_len * num_layers * d_model)")
        
        print("\n2. Flash Attention:")
        print("   • IO-aware attention implementation")
        print("   • Reduces memory from O(N²) to O(N)")
        print("   • 2-4x speedup, same accuracy")
        
        print("\n3. Quantization:")
        print("   • FP16 → INT8 → INT4")
        print("   • GPTQ, AWQ, GGUF")
        print("   • 2-4x memory reduction, minimal accuracy loss")
        
        print("\n4. Speculative Decoding:")
        print("   • Small draft model proposes tokens")
        print("   • Large model verifies in parallel")
        print("   • 2-3x speedup for generation")
        
        print("\n5. PagedAttention (vLLM):")
        print("   • Virtual memory for KV-cache")
        print("   • Reduces memory fragmentation")
        print("   • 2-4x throughput improvement")
        
        print("\n6. Continuous Batching:")
        print("   • Dynamic batching of requests")
        print("   • No waiting for longest sequence")
        print("   • Higher GPU utilization")

optimizer = InferenceOptimizer()
optimizer.describe_techniques()

CHAPTER 8: PROMPT ENGINEERING
Prompt Engineering Techniques
class PromptEngineer:
    """Prompt engineering techniques."""
    
    def zero_shot(self, task):
        """Zero-shot prompting."""
        return f"{task}"
    
    def few_shot(self, task, examples):
        """Few-shot prompting with examples."""
        prompt = ""
        for ex_in, ex_out in examples:
            prompt += f"Input: {ex_in}\nOutput: {ex_out}\n\n"
        prompt += f"Input: {task}\nOutput:"
        return prompt
    
    def chain_of_thought(self, task):
        """Chain-of-thought prompting."""
        return f"{task}\n\nLet's think step by step."
    
    def self_consistency(self, task, n_samples=5):
        """Self-consistency: sample multiple reasoning paths."""
        prompts = [
            f"{task}\n\nLet's think step by step."
            for _ in range(n_samples)
        ]
        return prompts
    
    def role_prompting(self, task, role):
        """Assign a role to the model."""
        return f"You are {role}.\n\n{task}"
    
    def demonstrate(self):
        """Demonstrate prompt engineering techniques."""
        print("=== Prompt Engineering Techniques ===\n")
        
        # Zero-shot
        print("1. Zero-shot:")
        print(f"   {self.zero_shot('Classify this review as positive or negative: Great movie!')}\n")
        
        # Few-shot
        print("2. Few-shot:")
        examples = [
            ("I love this!", "Positive"),
            ("This is terrible.", "Negative"),
            ("It was okay.", "Neutral"),
        ]
        print(f"   {self.few_shot('Amazing experience!', examples)}\n")
        
        # Chain-of-thought
        print("3. Chain-of-thought:")
        print(f"   {self.chain_of_thought('If I have 5 apples and buy 3 more, then eat 2, how many do I have?')}\n")
        
        # Role prompting
        print("4. Role prompting:")
        print(f"   {self.role_prompting('Explain quantum computing', 'a physics professor teaching undergraduates')}\n")

prompt_eng = PromptEngineer()
prompt_eng.demonstrate()

Retrieval-Augmented Generation (RAG)
class SimpleRAG:
    """Simplified RAG implementation."""
    
    def __init__(self, documents):
        self.documents = documents
        self.embeddings = None
        self._build_index()
    
    def _simple_embed(self, text):
        """Simple bag-of-words embedding."""
        words = text.lower().split()
        return np.array([hash(w) % 1000 for w in words[:10]], dtype=float)
    
    def _build_index(self):
        """Build simple retrieval index."""
        self.embeddings = [self._simple_embed(doc) for doc in self.documents]
    
    def retrieve(self, query, top_k=3):
        """Retrieve relevant documents."""
        query_emb = self._simple_embed(query)
        
        similarities = []
        for i, doc_emb in enumerate(self.embeddings):
            # Cosine similarity
            sim = np.dot(query_emb, doc_emb) / (
                np.linalg.norm(query_emb) * np.linalg.norm(doc_emb) + 1e-10
            )
            similarities.append((i, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [self.documents[idx] for idx, _ in similarities[:top_k]]
    
    def generate_answer(self, query, context):
        """Generate answer with context (simulated)."""
        return f"Based on the context: {context}\n\nAnswer to '{query}': [Generated response]"
    
    def query(self, question, top_k=2):
        """Full RAG pipeline."""
        # Retrieve
        relevant_docs = self.retrieve(question, top_k)
        context = "\n\n".join(relevant_docs)
        
        # Generate
        answer = self.generate_answer(question, context)
        
        return answer, relevant_docs

# Example
documents = [
    "Python is a high-level programming language created by Guido van Rossum in 1991.",
    "Machine learning is a subset of artificial intelligence that learns from data.",
    "Neural networks are inspired by biological neural networks in the brain.",
    "Transformers revolutionized NLP with the attention mechanism.",
    "BERT introduced bidirectional training for language models.",
]

rag = SimpleRAG(documents)
question = "Who created Python?"
answer, context = rag.query(question)

print("\n=== RAG Example ===")
print(f"Question: {question}")
print(f"\nRetrieved context:")
for i, doc in enumerate(context, 1):
    print(f"  {i}. {doc}")
print(f"\nAnswer: {answer}")

CHAPTER 9: NLP APPLICATIONS
Named Entity Recognition (NER)
import re

class SimpleNER:
    """Simple rule-based NER."""
    
    def __init__(self):
        # Patterns for different entity types
        self.patterns = {
            'PERSON': [
                r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # First Last
                r'\bDr\. [A-Z][a-z]+\b',
                r'\bMr\. [A-Z][a-z]+\b',
                r'\bMs\. [A-Z][a-z]+\b',
            ],
            'ORGANIZATION': [
                r'\b[A-Z][a-z]+ (Inc|Corp|LLC|Ltd)\b',
                r'\b(Amazon|Google|Microsoft|Apple|Facebook|Meta)\b',
                r'\b(IBM|HP|Intel|NVIDIA)\b',
            ],
            'LOCATION': [
                r'\b(New York|Los Angeles|San Francisco|London|Paris|Tokyo)\b',
                r'\b(USA|UK|France|Germany|Japan|China)\b',
                r'\b(California|Texas|Florida)\b',
            ],
            'DATE': [
                r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
                r'\b(January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2},? \d{4}\b',
                r'\b\d{4}\b',
            ],
            'MONEY': [
                r'\$\d+(?:,\d{3})*(?:\.\d{2})?',
                r'\d+(?:,\d{3})*(?:\.\d{2})? (dollars|USD|EUR)',
            ],
        }
    
    def extract_entities(self, text):
        """Extract entities from text."""
        entities = []
        
        for entity_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    entities.append({
                        'text': match.group(),
                        'type': entity_type,
                        'start': match.start(),
                        'end': match.end(),
                    })
        
        # Sort by position
        entities.sort(key=lambda x: x['start'])
        
        # Remove duplicates
        seen = set()
        unique_entities = []
        for entity in entities:
            key = (entity['text'], entity['type'])
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)
        
        return unique_entities

# Example
ner = SimpleNER()
text = """
Elon Musk founded SpaceX in 2002. The company, headquartered in 
 Hawthorne, California, has raised over $5 billion. On January 1, 2024, 
 Dr. Smith from MIT announced a new partnership with Google.
"""

entities = ner.extract_entities(text)

print("=== Named Entity Recognition ===")
print(f"Text: {text.strip()}\n")
print("Entities found:")
for entity in entities:
    print(f"  [{entity['type']:12s}] {entity['text']}")

Sentiment Analysis
import re
from collections import Counter

class SimpleSentimentAnalyzer:
    """Lexicon-based sentiment analysis."""
    
    def __init__(self):
        # Sentiment lexicon
        self.positive_words = {
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'awesome', 'love', 'best', 'happy', 'beautiful', 'perfect',
            'enjoy', 'pleased', 'delighted', 'brilliant', 'outstanding',
            'superb', 'magnificent', 'incredible', 'marvelous'
        }
        
        self.negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate',
            'disgusting', 'poor', 'disappointing', 'sad', 'ugly',
            'boring', 'annoying', 'frustrating', 'pathetic', 'dreadful',
            'miserable', 'useless', 'worthless', 'disgusted', 'angry'
        }
        
        # Intensifiers
        self.intensifiers = {
            'very': 1.5, 'really': 1.5, 'extremely': 2.0, 'absolutely': 2.0,
            'incredibly': 2.0, 'totally': 1.5, 'completely': 1.5
        }
        
        # Negations
        self.negations = {'not', "n't", 'no', 'never', 'neither', 'nor'}
    
    def analyze(self, text):
        """Analyze sentiment of text."""
        words = re.findall(r'\b\w+\b', text.lower())
        
        score = 0
        word_scores = []
        
        for i, word in enumerate(words):
            word_score = 0
            
            # Check sentiment
            if word in self.positive_words:
                word_score = 1
            elif word in self.negative_words:
                word_score = -1
            
            # Check for intensifier before
            if i > 0 and words[i-1] in self.intensifiers:
                word_score *= self.intensifiers[words[i-1]]
            
            # Check for negation before
            if i > 0 and words[i-1] in self.negations:
                word_score *= -1
            
            if word_score != 0:
                score += word_score
                word_scores.append((word, word_score))
        
        # Normalize
        if len(word_scores) > 0:
            normalized_score = score / len(word_scores)
        else:
            normalized_score = 0
        
        # Determine label
        if normalized_score > 0.2:
            label = 'POSITIVE'
        elif normalized_score < -0.2:
            label = 'NEGATIVE'
        else:
            label = 'NEUTRAL'
        
        return {
            'label': label,
            'score': normalized_score,
            'word_scores': word_scores
        }

# Example
analyzer = SimpleSentimentAnalyzer()

texts = [
    "This movie is absolutely amazing! I loved every minute of it.",
    "The service was terrible and the food was cold. Very disappointing.",
    "It's not bad, but it's not great either. Just okay.",
    "I'm extremely happy with my purchase. Best decision ever!",
    "The product is not good at all. I hate it.",
]

print("\n=== Sentiment Analysis ===")
for text in texts:
    result = analyzer.analyze(text)
    print(f"\nText: {text}")
    print(f"  Label: {result['label']} (score: {result['score']:.2f})")
    print(f"  Key words: {result['word_scores'][:5]}")

Text Summarization (Extractive)
import re
import numpy as np
from collections import Counter

class ExtractiveSummarizer:
    """Extractive text summarization using TextRank-like algorithm."""
    
    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'can'
        }
    
    def _tokenize_sentences(self, text):
        """Split text into sentences."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 20]
    
    def _tokenize_words(self, sentence):
        """Tokenize sentence into words."""
        words = re.findall(r'\b\w+\b', sentence.lower())
        return [w for w in words if w not in self.stop_words]
    
    def _compute_similarity(self, sent1, sent2):
        """Compute similarity between two sentences."""
        words1 = set(self._tokenize_words(sent1))
        words2 = set(self._tokenize_words(sent2))
        
        if len(words1) == 0 or len(words2) == 0:
            return 0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
    
    def _build_graph(self, sentences):
        """Build similarity graph."""
        n = len(sentences)
        similarity_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    similarity_matrix[i, j] = self._compute_similarity(
                        sentences[i], sentences[j]
                    )
        
        return similarity_matrix
    
    def _text_rank(self, similarity_matrix, damping=0.85, iterations=100):
        """Apply TextRank algorithm."""
        n = similarity_matrix.shape[0]
        scores = np.ones(n) / n
        
        for _ in range(iterations):
            new_scores = np.zeros(n)
            for i in range(n):
                for j in range(n):
                    if i != j:
                        # Normalize by out-degree
                        out_degree = np.sum(similarity_matrix[j])
                        if out_degree > 0:
                            new_scores[i] += (similarity_matrix[j, i] / out_degree) * scores[j]
                new_scores[i] = (1 - damping) + damping * new_scores[i]
            scores = new_scores
        
        return scores
    
    def summarize(self, text, ratio=0.3):
        """Summarize text."""
        sentences = self._tokenize_sentences(text)
        
        if len(sentences) <= 3:
            return text
        
        # Build similarity graph
        similarity_matrix = self._build_graph(sentences)
        
        # Compute scores
        scores = self._text_rank(similarity_matrix)
        
        # Select top sentences
        n_sentences = max(1, int(len(sentences) * ratio))
        top_indices = np.argsort(scores)[-n_sentences:]
        top_indices = sorted(top_indices)  # Keep original order
        
        summary = ' '.join([sentences[i] for i in top_indices])
        
        return summary

# Example
text = """
Natural language processing (NLP) is a subfield of linguistics, computer science, 
and artificial intelligence concerned with the interactions between computers and 
human language. The goal is to enable computers to understand, interpret, and 
generate human language in a valuable way. NLP combines computational linguistics 
with statistical, machine learning, and deep learning models.

The history of NLP dates back to the 1950s, when Alan Turing proposed the Turing 
test as a criterion for intelligence. Early NLP systems used rule-based approaches, 
but these were limited in scope and scalability. The statistical revolution in the 
1990s brought significant improvements, with models like hidden Markov models and 
conditional random fields.

The neural network revolution began in the 2010s with word embeddings like Word2Vec 
and GloVe. The transformer architecture, introduced in 2017, revolutionized the field 
by enabling parallel processing and capturing long-range dependencies. Models like BERT 
and GPT demonstrated unprecedented performance on various NLP tasks.

Modern large language models (LLMs) like GPT-4, Claude, and LLaMA have shown remarkable 
capabilities in text generation, reasoning, and instruction following. These models are 
trained on massive datasets and can perform few-shot and zero-shot learning. However, 
they also present challenges in terms of bias, hallucination, and computational cost.

The future of NLP includes multimodal models that combine text, images, and audio, 
more efficient architectures, better alignment with human values, and applications in 
healthcare, education, and scientific research. Ethical considerations and responsible 
AI development remain critical priorities for the field.
"""

summarizer = ExtractiveSummarizer()
summary = summarizer.summarize(text, ratio=0.3)

print("\n=== Text Summarization ===")
print(f"Original length: {len(text)} chars")
print(f"Summary length: {len(summary)} chars")
print(f"Compression ratio: {len(summary)/len(text):.2f}")
print(f"\nSummary:\n{summary}")

Machine Translation (Attention-based)
class SimpleTranslator:
    """Conceptual attention-based translation."""
    
    def __init__(self, src_vocab_size, tgt_vocab_size, d_model=64):
        self.encoder = TransformerEncoderLayer(d_model, num_heads=4, d_ff=128)
        self.decoder = TransformerDecoderLayer(d_model, num_heads=4, d_ff=128)
        
        # Embeddings
        scale = np.sqrt(2.0 / d_model)
        self.src_embed = np.random.randn(src_vocab_size, d_model) * scale
        self.tgt_embed = np.random.randn(tgt_vocab_size, d_model) * scale
        self.output_proj = np.random.randn(d_model, tgt_vocab_size) * scale
    
    def translate(self, src_tokens, max_length=50):
        """Translate source to target (greedy decoding)."""
        # Encode
        src_embedded = self.src_embed[src_tokens]
        encoder_output = self.encoder.forward(src_embedded[np.newaxis, :, :])
        
        # Decode
        tgt_tokens = [0]  # <BOS>
        
        for _ in range(max_length):
            tgt_embedded = self.tgt_embed[tgt_tokens]
            decoder_output = self.decoder.forward(
                tgt_embedded[np.newaxis, :, :],
                encoder_output
            )
            
            # Get next token
            logits = decoder_output[0, -1, :] @ self.output_proj
            next_token = np.argmax(logits)
            
            tgt_tokens.append(next_token)
            
            if next_token == 1:  # <EOS>
                break
        
        return tgt_tokens

# Example
translator = SimpleTranslator(src_vocab_size=1000, tgt_vocab_size=1000)
src_tokens = np.random.randint(0, 1000, 10)
tgt_tokens = translator.translate(src_tokens)

print("\n=== Machine Translation ===")
print(f"Source tokens: {src_tokens}")
print(f"Translated tokens: {tgt_tokens}")

CHAPTER 10: ADVANCED TOPICS AND RESOURCES
Modern NLP Architectures
# Recent developments:
# - Mixture of Experts (MoE): Mixtral, GPT-4
# - Long context: 100K+ tokens (Claude, Gemini)
# - Multimodal: GPT-4V, Gemini, LLaVA
# - Reasoning: Chain-of-thought, Tree-of-thought
# - Agents: AutoGPT, LangChain, LlamaIndex
# - Code generation: Codex, CodeLlama, StarCoder

# Evaluation benchmarks:
# - MMLU: Multi-task language understanding
# - HellaSwag: Commonsense reasoning
# - ARC: Science questions
# - TruthfulQA: Factuality
# - HumanEval: Code generation
# - GSM8K: Math reasoning

Tokenization Comparison
class TokenizerComparison:
    """Compare different tokenization methods."""
    
    def compare(self):
        """Compare tokenization approaches."""
        print("=== Tokenization Methods ===\n")
        
        print("1. BPE (Byte Pair Encoding):")
        print("   • Used by: GPT-2, GPT-3/4, LLaMA")
        print("   • Merges frequent byte pairs")
        print("   • Good balance of vocab size and coverage")
        
        print("\n2. WordPiece:")
        print("   • Used by: BERT, DistilBERT")
        print("   • Maximizes likelihood of training data")
        print("   • ## prefix for subword continuation")
        
        print("\n3. SentencePiece:")
        print("   • Used by: T5, ALBERT, many multilingual models")
        print("   • Language-agnostic")
        print("   • Treats text as raw byte sequence")
        
        print("\n4. tiktoken (OpenAI):")
        print("   • Used by: GPT-3.5, GPT-4")
        print("   • Optimized for speed")
        print("   • ~100K vocabulary")
        
        print("\n5. Unigram LM:")
        print("   • Used by: T5 (alternative)")
        print("   • Probabilistic subword segmentation")
        print("   • Can compute tokenization probability")

tokenizer_comp = TokenizerComparison()
tokenizer_comp.compare()

Safety and Alignment
class SafetyConcepts:
    """LLM safety and alignment concepts."""
    
    def describe(self):
        """Describe safety concepts."""
        print("=== LLM Safety & Alignment ===\n")
        
        print("Alignment problem:")
        print("  • Making AI systems pursue intended goals")
        print("  • Avoiding unintended harmful behaviors")
        print("  • Ensuring AI benefits humanity")
        
        print("\nSafety techniques:")
        print("  • RLHF / DPO (preference learning)")
        print("  • Constitutional AI (self-supervised)")
        print("  • Red teaming (adversarial testing)")
        print("  • Guardrails (input/output filtering)")
        print("  • Interpretability (mechanistic)")
        
        print("\nChallenges:")
        print("  • Reward hacking (gaming the reward model)")
        print("  • Sycophancy (telling users what they want)")
        print("  • Hallucination (generating false information)")
        print("  • Bias amplification")
        print("  • Jailbreaks (bypassing safety)")
        
        print("\nResearch directions:")
        print("  • Scalable oversight")
        print("  • Mechanistic interpretability")
        print("  • Formal verification")
        print("  • AI governance and policy")

safety = SafetyConcepts()
safety.describe()

Recommended Reading
# Foundational:
# - "Speech and Language Processing" by Jurafsky & Martin
# - "Foundations of Statistical NLP" by Manning & Schütze
# - "Neural Network Methods for NLP" by Goldberg

# Deep Learning:
# - "Deep Learning" by Goodfellow, Bengio, Courville
# - "Dive into Deep Learning" (d2l.ai)
# - "Attention Is All You Need" (Vaswani et al., 2017)

# Transformers & LLMs:
# - "The Annotated Transformer" (Harvard NLP)
# - "The Illustrated Transformer" (Jay Alammar)
# - Hugging Face course: https://huggingface.co/learn

# Modern LLMs:
# - "A Survey of Large Language Models" (Zhao et al., 2023)
# - "Sparks of AGI" (OpenAI, 2023)
# - "LLaMA 2" paper (Touvron et al., 2023)

# Online Resources
# - Hugging Face: https://huggingface.co/
# - Papers with Code: https://paperswithcode.com/
# - NLPLand: https://nlpland.com/
# - Stanford CS224N: https://web.stanford.edu/class/cs224n/
# - fast.ai NLP course: https://www.fast.ai/

# End of NLP Advanced Reference