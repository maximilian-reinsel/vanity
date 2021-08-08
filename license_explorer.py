from utils import Option
from utils import print_options_at_distance

print("Initializing...")
# Because this parses the dictionary at import time, it takes some time, 
# but less than you'd expect.
from transformations import transform_letters_to_numbers
from transformations import transform_substrings_to_numbers
from transformations import remove_middle_vowels
from transformations import find_synonyms
from transformations import remove_middle_consinent
from transformations import change_letters
from transformations import remove_start_or_end

transformation_functions = {
    transform_letters_to_numbers: 1, 
    transform_substrings_to_numbers: 1,
    remove_middle_vowels: 1,
    find_synonyms: 1,
    remove_middle_consinent: 3,
    change_letters: 5,
    remove_start_or_end: 10,
}

word = input("Enter word to start:").strip().upper()
max_distance = int(input("Enter max distance to output: "))

distance_traveled = 0
word_set = set()
word_set.add(Option(word=word, distance=0))

while distance_traveled <= max_distance:
    print_options_at_distance(distance_traveled, word_set)
    new_words = []
    for existing_option in word_set:
        for f in transformation_functions.keys():
            distance_out = transformation_functions[f] + distance_traveled
            if distance_out > max_distance:
                continue
            derived = f(existing_option)
            for d in derived:
                new_words.append((d, distance_out))

    for w in new_words:
        word_set.add(Option(word=w[0], distance=w[1]))

    distance_traveled += 1
