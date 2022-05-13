from utils import Option, PrioritizedItem
from utils import print_options
from queue import PriorityQueue
from typing import List

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

def transform(option: Option) -> List[Option]:
    results = []
    for f in transformation_functions.keys():
        new_distance = option.distance + transformation_functions[f]
        derived = f(option)
        results.extend(Option(word=d, distance=new_distance) for d in derived)
    return results

def search(input_word, max_distance):
    '''Just Dijkstra's algorithm'''
    word = input_word.strip().upper()
    queue = PriorityQueue()
    queue.put(Option(word=word, distance=0).to_priority())
    visited = set()

    while not queue.empty():
        current = queue.get().item
        if current in visited:
            continue
        visited.add(current)
        new_options = transform(current)
        for option in new_options:
            if option not in visited and option.distance <= max_distance:
                queue.put(option.to_priority())

    return visited

def explore(input_word, max_distance, output_width, max_length, dmv, use_emoji):
    options = search(input_word, max_distance)
    print_options(options, output_width, max_length, dmv, use_emoji)
