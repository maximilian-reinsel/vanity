import json
import os

from dataclasses import dataclass
from enum import Enum
from typing import List

dictionary_path = "counterfitted_neighbors.json"

@dataclass
class Entry:
    word: str
    synonyms: List[str]

def get_dictionary():
    entries = {}

    path = get_dictionary_path()
    with open(path) as f:
        full_syn_list = json.load(f)

    for word in full_syn_list.keys():
        entries[word.upper()] = Entry(word=word.strip().upper(), synonyms=[s.strip().upper() for s in full_syn_list[word]])

    return entries

def get_dictionary_path():
    script_dir = os.path.dirname(__file__) 
    return os.path.join(script_dir, dictionary_path)