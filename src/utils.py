from dataclasses import dataclass

def print_options_at_distance(d, words, width, max_length):
    print(f"DISTANCE {d}")
    filtered = (w.word for w in words if w.distance == d and len(w.word) <= max_length)
    print_grouped(sorted(filtered), width)

def print_grouped(words, width):
    grouped = [words[i:i+width] for i in range(0, len(words), width)]
    for g in grouped:
        print("\t", "".join("{:<10}".format(w) for w in g))

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