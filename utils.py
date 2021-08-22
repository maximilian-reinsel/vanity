from dataclasses import dataclass

def print_options_at_distance(d, words):
    print(f"DISTANCE {d}")
    
    for w in sorted(words, key=lambda e: e.word):
        if w.distance == d:
            print("\t", w)

@dataclass
class Option:
    word: str
    distance: int

    def __hash__(self):
        return hash(self.word)
    
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.word == other.word