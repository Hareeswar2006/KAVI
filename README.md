# KAVI PoetBot: A Hybrid NLP Chatbot for Poetry Analysis & Generation

## Project Overview

This project is a Python-based interactive chatbot designed to analyze and generate poetry. It stands out by using a **hybrid architecture**, combining the power of modern deep learning (Transformers) with classic NLP techniques (Markov Chains, Word2Vec) and rule-based systems.

The bot operates in two modes:
1.  **Analyze Mode:** Provides a multi-layered analysis of a poem, including its predicted emotion, key terms, technical rhyme scheme, and alliteration.
2.  **Generate Mode:** Creates new, original poem snippets based on the statistical style learned from a corpus of poetry.

## Core Features & How They Work

This project is built from several distinct components that work together.

### 1. Emotion Prediction (Fine-Tuned Transformer)
The core of the "explainer" is a **fine-tuned DistilBERT transformer model**.
* **Model:** `distilbert-base-uncased` (from Hugging Face).
* **Data:** Fine-tuned on a custom dataset (`final_df_emotions(remove-bias).csv`) containing poems labeled with 7 distinct emotions (e.g., sadness, joy, anger).
* **Process:** The bot feeds the user's poem to this fine-tuned model, which predicts the single most likely emotion for the entire stanza.

### 2. Human-Like Explanation Engine (Rule-Based + Word2Vec)
Instead of just stating the emotion, the bot generates a more nuanced explanation using:
* **Keyword Extraction:** Uses **NLTK (Natural Language Toolkit)** for Part-of-Speech (POS) tagging to identify key nouns and adjectives (e.g., 'cloud', 'heavy', 'golden').
* **Semantic Similarity:** Uses a pre-trained **`gensim` Word2Vec model** (Google News 300) to find words semantically similar to the identified keywords (e.g., 'heavy' -> 'weighty', 'burdensome').
* **Rule-Based Templates:** A custom Python script combines the predicted emotion, a key word, and its similar words into a natural-sounding explanation.

### 3. Technical Analysis Engine (Phonetics & Rules)
For a deeper technical analysis, the bot uses:
* **Phonetic Rhyme Scheme:** A custom-built function that uses the **CMU Pronouncing Dictionary (CMUDict)** to look up the phonetic sounds of the last word of each line. It compares sounds from the last stressed vowel onwards to find rhymes (e.g., ABABCC).
* **Alliteration Finder:** A rule-based function that scans each line for words starting with the same letter, while intelligently skipping over common "stop words" ('a', 'the', 'of', etc.).

### 4. Poetry Generation (Markov Chain)
The "generate" feature is powered by a classic NLP model built from scratch.
* **Model:** A **Markov Chain** model.
* **Training:** It was trained on the cleaned text of Emily Dickinson's poems.
* **Process:** The model learns the statistical probability of which words are likely to follow other words. It then generates new text by "walking" this probability chain, resulting in new text that mimics the original author's style.

## Technologies Used

* **Python 3**
* **Machine Learning:** PyTorch, Hugging Face `transformers` (DistilBERT, Trainer), `datasets`
* **NLP:** `gensim` (Word2Vec), `nltk` (POS Tagging, Tokenization), `re` (Regex)
* **Data Handling:** Pandas, NumPy
* **Environment:** Google Colab (for GPU-accelerated fine-tuning)

## How to Run
1.  Clone this repository: `git clone ...`
2.  Install required libraries: `pip install -r requirements.txt`.
3.  Download necessary data files (`cmudict.txt`, `word2vec-google-news-300` model - can be loaded via `gensim.downloader`).
4.  Run the main Jupyter Notebook (`.ipynb`) cells in sequential order to load data, train the models (or load pre-trained weights), and start the interactive chatbot loop.
