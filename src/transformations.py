from __future__ import annotations

from dictionary_builder import get_dictionary
from dataclasses import dataclass
from utils import Option, Transform
from typing import List, Dict

@dataclass
class KeyedTransform(Transform):
    key: str

@dataclass
class ReplacementTransform(KeyedTransform):
    value: str

@dataclass
class NumberTransform(ReplacementTransform):
    pass

@dataclass
class LetterTransform(ReplacementTransform):
    pass

@dataclass
class SubstringTransform(ReplacementTransform):
    pass

@dataclass
class RemoveVowelTransform(KeyedTransform):
    pass

@dataclass
class SynonymTransform(Transform):
    pass

consonants = [
    "B", "C", "D", "F", "G",
    "H", "J", "K", "L", "M",
    "N", "P", "Q", "R", "S",
    "T", "V", "W", "X", "Y", "Z",
]

transforms = [
    NumberTransform(1, "I", "1"),
    NumberTransform(1, "E", "3"),
    NumberTransform(1, "A", "4"),
    LetterTransform(1, "C", "K"),
    LetterTransform(1, "Y", "I"),
    LetterTransform(1, "S", "Z"),
    SubstringTransform(1, "TOO", "2"),
    SubstringTransform(1, "TWO", "2"),
    SubstringTransform(1, "TO" , "2"),
    SubstringTransform(1, "FOR", "4"),
    SubstringTransform(1, "FOUR", "4"),
    SubstringTransform(1, "TH", "D"),
    SubstringTransform(1, "PH", "F"),
    SubstringTransform(1, "QU", "KW"),
    RemoveVowelTransform(1, "A"),
    RemoveVowelTransform(1, "E"),
    RemoveVowelTransform(1, "I"),
    RemoveVowelTransform(1, "O"),
    RemoveVowelTransform(1, "U"),
    SynonymTransform(2),
    NumberTransform(2, "Z", "2"),
    NumberTransform(2, "T", "7"),
    NumberTransform(2, "L", "1"),
    NumberTransform(2, "S", "5"),
    NumberTransform(3, "B", "8"),
    NumberTransform(3, "G", "9"),
]

def get_keyed_transform(_class: type[KeyedTransform]) -> Dict[str, KeyedTransform]:
    return { x.key: x for x in transforms if isinstance(x, _class) }

def get_transform(_class: type[Transform]) -> Transform:
    return next((x for x in transforms if isinstance(x, _class)))

number_transforms = get_keyed_transform(NumberTransform)
letter_transforms = get_keyed_transform(LetterTransform)
substring_transforms = get_keyed_transform(SubstringTransform)
remove_vowel_transforms = get_keyed_transform(RemoveVowelTransform)
synonym_transform = get_transform(SynonymTransform)

def transform_single_character(option: Option, transforms: Dict[str, KeyedTransform]) -> List[Option]:
    to_ret = []
    for i, c in enumerate(option.word):
        if c in transforms.keys():
            t = transforms[c]
            new_word = option.word[:i] + t.value + option.word[i+1:]
            to_ret.append(option.jump(new_word, t))
    return to_ret

def transform_letters_to_numbers(option: Option) -> List[Option]:
    return transform_single_character(option, number_transforms)

def transform_substrings_to_numbers(option: Option) -> List[Option]:
    to_ret = []
    # This could be improved by using KMP or something, but time to build maps probably outweighs
    # n^2 here for now.
    for i in range(len(option.word)):
        for sub in substring_transforms.keys():
            if option.word[i:i+len(sub)] == sub:
                t = substring_transforms[sub]
                new_word = option.word[:i] + t.value + option.word[i+len(sub):]
                to_ret.append(option.jump(new_word, t))
    return to_ret

def remove_middle_vowels(option: Option) -> List[Option]:
    to_ret = []

    for idx, l in enumerate(option.word):
        t = remove_vowel_transforms.get(l, None)
        if t and idx != 0 and idx != len(option.word) - 1:
            new_word = option.word[:idx] + option.word[idx+1:]
            to_ret.append(option.jump(new_word, t))

    return to_ret

dictionary = get_dictionary()
def find_synonyms(option: Option) -> List[Option]:
    if not synonym_transform:
        return []

    to_ret = []

    if option.word in dictionary.keys():
        for syn in dictionary[option.word].synonyms:
            to_ret.append(option.jump(syn, synonym_transform))

    if len(option.word.split()) > 1:
        starting_phrase = option.word.split()
        for idx, sub_part in enumerate(starting_phrase):
            if not sub_part in dictionary.keys():
                continue
            for syn in dictionary[sub_part].synonyms:
                copy_starting_phrase = starting_phrase.copy()
                copy_starting_phrase[idx] = syn
                new_word = " ".join(copy_starting_phrase)
                to_ret.append(option.jump(new_word, synonym_transform))

    return to_ret

def remove_middle_consonent(option: Option) -> List[Option]:
    return []

def change_letters(option: Option) -> List[Option]:
    return transform_single_character(option, letter_transforms)

def remove_start_or_end(option: Option) -> List[Option]:
    return []

transformation_functions = [
    transform_letters_to_numbers,
    transform_substrings_to_numbers,
    remove_middle_vowels,
    find_synonyms,
    remove_middle_consonent,
    change_letters,
    remove_start_or_end,
]

def transform(option: Option) -> List[Option]:
    results = []
    for f in transformation_functions:
        results.extend(f(option))
    return results
