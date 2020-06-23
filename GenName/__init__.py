import random
import os

ADJECTIVES = os.path.join(os.path.dirname(__file__), 'adjective.txt')
NOUNS = os.path.join(os.path.dirname(__file__), 'noun.txt')


def generate():
    with open(ADJECTIVES) as f:
        adjectives = [adjective.rstrip('\n') for adjective in f]
    with open(NOUNS) as f:
        nouns = [noun.rstrip('\n') for noun in f]

    w1 = random.choice(adjectives).capitalize()
    w2 = random.choice(adjectives).capitalize()
    w3 = random.choice(nouns).capitalize()
    return "%s%s%s" % (w1, w2, w3)
