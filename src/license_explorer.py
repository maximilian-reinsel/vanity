from utils import Option
from utils import print_options_at_distance

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

def explore(input_word, max_distance, output_width, max_length, dmv, use_emoji):
    word = input_word.strip().upper()
    distance_traveled = 0
    word_set = set()
    word_set.add(Option(word=word, distance=0))

    all_options_processed = False
    while distance_traveled <= max_distance and not all_options_processed:
        print_options_at_distance(distance_traveled, word_set, output_width, max_length, dmv, use_emoji)
        new_words = []
        all_options_processed = True
        for existing_option in word_set:
            if existing_option.distance < distance_traveled:
                continue
            all_options_processed = False
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
