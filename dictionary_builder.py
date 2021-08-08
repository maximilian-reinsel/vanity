from dataclasses import dataclass
from enum import Enum
from typing import List

dictionary_path = "/home/maxreinsel/repos/license_plates/dictionary_sample"

@dataclass
class Entry:
    word: str
    synonyms: List[str]

class syn_state(Enum):
    NONE = 1
    OPEN = 2
    SEEN_LIST_START = 3
    SEEN_DESCRIPTION_START = 4

def get_syn_list_from_line(line):
    to_ret = []
    for w in line.strip(" -").split(";"):
        w = w.strip()
        if not w:
            continue
        idx = w.find(".")
        if idx == -1:
            to_ret.append(w.strip().upper())
        else:
            what_is_left =w[:idx].strip().upper() 
            if what_is_left:
                to_ret.append(what_is_left)
            break
    return to_ret

def get_dictionary():
    current_entry = None
    state = syn_state.NONE

    entries = {}

    with open("dictionary_only_words.txt") as f:
        for line in f:
            if line.strip() == "":
                continue
            # Only lines where all upper case are new words
            if line.upper() == line:
                # Sometimes multiple definitions? 
                if current_entry and line.strip() == current_entry.word:
                    state = syn_state.NONE
                    continue
                
                if current_entry:
                    entries[current_entry.word] = current_entry
                current_entry=Entry(word=line.strip().upper(), synonyms=[])
                state = syn_state.NONE
            elif line.strip() == "Syn.":
                state = syn_state.OPEN
            # Start of synonyms
            elif state == syn_state.OPEN and line.startswith(" -- "):
                state = syn_state.SEEN_LIST_START
                current_entry.synonyms.extend(get_syn_list_from_line(line))
            elif state == syn_state.SEEN_LIST_START and line.startswith(" -- "):
                state = syn_state.SEEN_DESCRIPTION_START
                continue
            elif state == syn_state.SEEN_LIST_START:
                current_entry.synonyms.extend(get_syn_list_from_line(line))
                continue
            else:
                continue
            
    entries[current_entry.word] = current_entry

    return entries