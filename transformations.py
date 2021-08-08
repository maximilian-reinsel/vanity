from dictionary_builder import get_dictionary

vowels = ["A", "E", "I", "O", "U"]
consinents = [
    "B", "C", "D", "F", "G",
    "H", "J", "K", "L", "M",
    "N", "P", "Q", "R", "S",
    "T", "V", "W", "X", "Y", "Z", 
]

number_transforms = {
    "O": "0",
    "L": "1",
    "I": "1",
    "Z": "2",
    #"R": "2",
    "E": "3",
    "A": "4",
    "S": "5",
    #"G": "6",
    #"C": "6",
    "T": "7",
    #"Y": "7",
    "B": "8",
    "G": "9",
}

substring_transforms = {
    "TOO" : "2",
    "TWO" : "2",
    "TO"  : "2",
    "FOR" : "4",
    "FOUR": "4",
}

def transform_letters_to_numbers(w):
    to_ret = []
    for l in number_transforms.keys():
        if l in w.word:
            to_ret.append(w.word.replace(l, number_transforms[l], 1))
    return to_ret

def transform_substrings_to_numbers(w):
    to_ret = []
    for l in substring_transforms.keys():
        if l in w.word:
            to_ret.append(w.word.replace(l, substring_transforms[l], 1))
    return to_ret

def remove_middle_vowels(w):
    to_ret = []

    for idx, l in enumerate(w.word):
        if l in vowels and idx != 0 and idx != len(w.word) - 1:
            to_ret.append(w.word[:idx] + w.word[idx+1:])

    return to_ret

dictionary = get_dictionary()
def find_synonyms(w):
    if w.word in dictionary.keys():
        return dictionary[w.word].synonyms
    else:
        return []

def remove_middle_consinent(w):
    return []

def change_letters(w):
    return []

def remove_start_or_end(w):
    return []