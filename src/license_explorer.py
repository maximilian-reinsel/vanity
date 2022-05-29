from utils import Option
from utils import print_options
from queue import PriorityQueue
from typing import List

from transformations import transform

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
