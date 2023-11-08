import random


class Deck:
    def __init__(self):
        temp = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        temp_full = temp*4
        deck = temp_full*4
        random.shuffle(deck)
        self.deck = deck

    def shuffle(self):
        temp = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        temp_full = temp * 4
        deck = temp_full * 4
        random.shuffle(deck)
        self.deck = deck

    def getCard(self) -> str:
        return self.deck.pop()

    def getAmount(self):
        return len(self.deck)
