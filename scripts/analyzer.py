import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt
import re
import os
import sys
import string

def calculate_stats(poem_text):
    cleaned_text=poem_text.replace("--"," ")
    words=cleaned_text.lower().split()
    word_count=len(words)
    total_chars=sum(len(word) for word in words)
    if word_count > 0:
        average_word_length = total_chars/ word_count
    else:
        average_word_length = 0
    return {
        "word_count": word_count,
        "average_word_length": average_word_length
    }

try:
    with open("../data/clean_poems.txt", "r", encoding="utf-8") as f:
        poem_text = f.read()
    stats = calculate_stats(poem_text)
    print(f"Total Word Count: {stats['word_count']}")
    print(f"Average Word Length: {stats['average_word_length']:.2f} characters")

except FileNotFoundError:
    print("Error: The file was not found.")

def load_cmudict(filepath="../data/cmudict.txt"):
    print(f"Loading phonetic dictionary from {filepath}...")
    pronunciations = {}
    variant_regex = re.compile(r'\(\d+\)$')
    allowed_chars_regex = re.compile(r"[^A-Z']") 
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip() 
                if line.startswith(';;;') or not line: 
                    continue
                parts = line.split(maxsplit=1) 
                if len(parts) < 2: 
                    continue
                word = parts[0].strip()
                word = variant_regex.sub('', word)
                word = word.upper()
                word = allowed_chars_regex.sub('', word) 
                if not word:
                    continue
                    
                phonemes_str = parts[1].strip() 
                phonemes = phonemes_str.split() 
                if word not in pronunciations:
                    pronunciations[word] = phonemes
                    
        if not pronunciations:
             print("Warning: The dictionary appears empty after loading. Check the file format.")
             return None
        print(f"Dictionary loaded successfully. {len(pronunciations)} words found.")
        return pronunciations
        
    except FileNotFoundError:
        print(f"Error: The dictionary file '{filepath}' was not found.")
        return None
    
def detect_rhyme_scheme(stanza, pronunciation_dict):
    if not pronunciation_dict:
        return "Error: Dictionary not loaded."
    lines = stanza.strip().split('\n')
    last_word_sounds = []

    for line in lines:
        words = line.split()
        if words:
            clean_word = words[-1].upper().strip(string.punctuation)
            if clean_word in pronunciation_dict:
                phonemes = pronunciation_dict[clean_word]
                last_stress_index = -1
                for i in range(len(phonemes) - 1, -1, -1):
                    if phonemes[i][-1] in ('1', '2'):
                        last_stress_index = i
                        break
                if last_stress_index != -1:
                    rhyming_part = tuple(phonemes[last_stress_index:])
                    last_word_sounds.append(rhyming_part)
                else:
                    last_word_sounds.append(tuple(phonemes))
            else:
                last_word_sounds.append(None)
        else:
             last_word_sounds.append(None)

    rhyme_groups = {}
    scheme = []
    next_rhyme_label = 'A'

    for sounds in last_word_sounds:
        if sounds is None:
            scheme.append('X')
            continue
        if sounds in rhyme_groups:
            scheme.append(rhyme_groups[sounds])
        else:
            rhyme_groups[sounds] = next_rhyme_label
            scheme.append(next_rhyme_label)
            next_rhyme_label = chr(ord(next_rhyme_label) + 1)
            
    return "".join(scheme)

cmudict = load_cmudict()

#Testing phonetics
if cmudict:
    try:
        sample_stanza="""
        Because I could not stop for Death,
        He kindly stopped for me;
        The carriage held but just ourselves
        And Immortality.
        """
        rhyme_scheme = detect_rhyme_scheme(sample_stanza, cmudict)
        print(f"The rhyme scheme of the sample stanza is: {rhyme_scheme}")

    except FileNotFoundError:
        print("Error: 'clean_poems.txt' was not found.")
else:
    print("Exiting because the phonetic dictionary could not be loaded.")


def find_alliteration(line):
    stop_words = set([
        'a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'of', 
        'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
        'and', 'or', 'but', 'if', 'as', 'by', 'with', 'from',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 
        'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their' 
    ])
    translator = str.maketrans('', '', string.punctuation)
    cleaned_line = line.lower().translate(translator)
    words = cleaned_line.split()
    alliterations = []
    num_words = len(words)
    for i in range(num_words - 1):
        current_word = words[i]
        if not current_word or current_word in stop_words:
            continue
        for j in range(i + 1, num_words):
            next_word = words[j]
            if not next_word:
                continue
            if next_word in stop_words:
                continue
            if current_word[0] == next_word[0]:
                alliterations.append((current_word, next_word))
            break 
    return alliterations

# Testing find_alliterations
try:
    sample_line = "Success is counted sweetest by those who ne'er succeed."
    alliterative_pairs = find_alliteration(sample_line)
            
    if alliterative_pairs:
        print(f"Found alliteration in the line: '{sample_line}'")
        for pair in alliterative_pairs:
            print(f"  - {pair[0]} / {pair[1]}")
    else:
        print(f"No simple alliteration found in the line: '{sample_line}'")

except FileNotFoundError:
        print("Error: 'clean_poems.txt' was not found.")