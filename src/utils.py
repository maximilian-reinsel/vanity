from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Any, Iterable, TypeVar, Callable
from collections import defaultdict

SYMBOLS = {
    False: {
        None: "?",
        False: "_",
        True: "*",
    },
    True: {
        None: "❔",
        False: "🚫",
        True: "✅",
    },
}

@dataclass
class Transform:
    cost: int

@dataclass(order=True, frozen=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

@dataclass(order=True, frozen=True)
class Option:
    word: str
    distance: int=field(compare=False)

    def to_priority(self) -> PrioritizedItem:
        return PrioritizedItem(priority = self.distance, item = self)

    def jump(self, new_word: str, transform: Transform) -> Option:
        return Option(word = new_word, distance = self.distance + transform.cost)

def print_options(options: List[Option], width: int, max_length: int, dmv, use_emoji: bool):
    grouped = group_by(options, lambda x: x.distance, lambda x: x.word)
    by_distance = sorted(grouped.items(), key=lambda x: x[0])
    for distance, words in by_distance:
        print_words_at_distance(distance, words, width, max_length, dmv, use_emoji)

def print_words_at_distance(d: int, words: List[str], width: int, max_length: int, dmv, use_emoji: bool):
    print(f"DISTANCE {d}")
    words = sorted(w for w in words if len(w) <= max_length)
    if dmv:
        words = (with_result(w, dmv.check_plate(w), use_emoji) for w in words)
    print_grouped(words, width)

def print_grouped(words: List[Option], width: int):
    grouped = [words[i:i+width] for i in range(0, len(words), width)]
    for g in grouped:
        print("\t", "".join("{:<11}".format(w) for w in g))

def with_result(word: str, result: bool, use_emoji: bool) -> str:
    symbol = SYMBOLS[use_emoji][result]
    return word + " " + symbol

T = TypeVar("T")

def group_by(iterable: Iterable[T], key: Callable[[T], Any], value: Callable[[T], Any] = None):
    if not value:
        value = lambda x: x
    result = defaultdict(list)
    for item in iterable:
        result[key(item)].append(value(item))
    return result