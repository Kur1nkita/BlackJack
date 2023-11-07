class Hand:
    def __init__(self):
        self.cards = [[]]
        self.amount = [[0, 0]]
        self.hand_counts = 1
        self.split = [False]
        self.double = [False]
        self.bust = [False]
        self.bj = [False]

    def addCard(self, card: str, position: int):
        self.cards[position].append(card)
        self.count(position)
        # self.set_state(position)

    def get_info(self, position):
        return {
            "cards": self.cards[position],
            "amount": self.amount[position],
            "bust": self.bust[position],
            "bj": self.bj[position],
            "double": self.double[position],
            "split": self.split[position]
        }

    # def set_state(self, position):


    # TODO: Threat self.amount tuple as 0-index for ace == 11 only if the sum less than 10, otherwise ace == 1
    # TODO: For the 1-index, ace == 1 with no condition.
    def count(self, position):
        hand1 = 0
        hand2 = 0
        for x in self.cards[position]:
            if x in ["K", "Q", "J"]:
                hand1 += 10
                hand2 += 10
            elif x == "A":
                if hand1 > 10:
                    hand1 += 1
                else:
                    hand1 += 11
                hand2 += 1
            else:
                hand1 += int(x)
                hand2 += int(x)
        self.amount[position][0] = hand1
        self.amount[position][1] = hand2

    def __str__(self):
        return str(self.amount)
