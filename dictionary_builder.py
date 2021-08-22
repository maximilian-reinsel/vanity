import json

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

    with open(dictionary_path) as f:
        full_syn_list = json.load(f)

    for word in full_syn_list.keys():
        entries[word.upper()] = Entry(word=word.strip().upper(), synonyms=[s.strip().upper() for s in full_syn_list[word]])

    return entries