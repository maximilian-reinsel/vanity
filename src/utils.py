from dataclasses import dataclass

EMOJI_YES = "✅"
EMOJI_NO = "🚫"
ASCII_YES = "*"
ASCII_NO = "_"

def print_options_at_distance(d, words, width, max_length, dmv, use_emoji):
    print(f"DISTANCE {d}")
    filtered = (w.word for w in words if w.distance == d and len(w.word) <= max_length)
    if dmv:
        filtered = (with_result(w, dmv.check_plate(w), use_emoji) for w in filtered)
    print_grouped(sorted(filtered), width)

def print_grouped(words, width):
    grouped = [words[i:i+width] for i in range(0, len(words), width)]
    for g in grouped:
        print("\t", "".join("{:<11}".format(w) for w in g))

def with_result(word, result, use_emoji):
    yes_symbol = EMOJI_YES if use_emoji else ASCII_YES
    no_symbol = EMOJI_NO if use_emoji else ASCII_NO
    return word + " " + (yes_symbol if result else no_symbol)

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
