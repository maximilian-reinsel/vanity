from dataclasses import dataclass

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
    return []

def find_synonyms(w):
    return []

def remove_middle_consinent(w):
    return []

def change_letters(w):
    return []

def remove_start_or_end(w):
    return []

def print_options_at_distance(d, words):
    print(f"DISTANCE {d}")
    for w in words:
        if w.distance == d:
            print("\t", w)

transformation_constants = {
    transform_letters_to_numbers: 1, 
    transform_substrings_to_numbers: 1,
    remove_middle_vowels: 1,
    find_synonyms: 1,
    remove_middle_consinent: 3,
    #change_letters: 5,
    #remove_start_or_end: 10,
}

@dataclass
class Option:
    word: str
    distance: int

    def __hash__(self):
        return word.__hash__()
    
    def __eq__(self, other):
        if not isinstance(other, type(Option)):
            return False
        return self.word == other.word

    

print("Initializing...")

dictionary = get_dictionary()

word = input("Enter word to start:").strip().upper()
max_distance = int(input("Enter max distance to output: "))

distance_traveled = 0
word_set = set()
word_set.add(Option(word=word, distance=0))

while distance_traveled <= max_distance:
    print_options_at_distance(distance_traveled, word_set)
    new_words = []
    for existing_option in word_set:
        for f in transformation_constants.keys():
            distance_out = transformation_constants[f] + distance_traveled
            if distance_out > max_distance:
                continue
            derived = f(existing_option)
            for d in derived:
                new_words.append((d, distance_out))

    for w in new_words:
        word_set.add(Option(word=w[0], distance=w[1]))

    distance_traveled += 1
