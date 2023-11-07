from gamefiles.player import Player
from gamefiles.deck import Deck
import datetime


def calculate_hand(hand: list) -> (int, bool, int):
    ace_count = 0
    count = 0
    for x in hand:
        if x == "A":
            ace_count += 1
        elif x in ["K", "Q", "J"]:
            count += 10
        else:
            count += int(x)
    if len(hand) == 2 and count == 10 and ace_count == 1:
        return 21, True, 0
    if not ace_count:
        return count, False, 0
    count2 = count
    while ace_count:
        if ace_count > 1:
            count += 1
            count2 += 1
            ace_count -= 1
            continue
        if count == 10:
            count += 11
            count2 = 0
            break
        elif count > 10:
            count += 1
            count2 += 1
            break
        else:
            count += 11
            count2 += 1
            break
    if count > 21:
        return count, False, 0
    return count, False, count2


def check_condition(dealer_value: tuple, calculated: tuple) -> str:
    if dealer_value[1]:
        if calculated[1]:
            condition = "PUSH"
        else:
            condition = "LOSE"
    elif calculated[1]:
        condition = "WIN"
    elif calculated[0] == dealer_value[0]:
        condition = "PUSH"
    elif calculated[0] > 21:
        condition = "BUST"
    elif calculated[0] < dealer_value[0]:
        condition = "LOSE"
    else:
        condition = "WIN"
    return condition


def calculate_win(condition: str, calculated: tuple, bet: list) -> int:
    bet = bet[0]
    if condition in ["LOSE", "BUST"]:
        return 0
    if condition == "PUSH":
        return bet
    if calculated[1]:
        return bet * 2 + int(bet * 0.5)
    return bet * 2


def check_bet(bet: list) -> str:
    if bet[1]:
        return f'{bet[0]} "DOUBLE"'
    return f'{bet[0]}'


class Table:
    def __init__(self, players: list[Player], hands=None, bets=None, date=None):
        if hands is None:
            hands = []
        self.players = players
        self.deck = Deck()
        self.hands = hands
        self.bets = bets
        self.date = date
        if date is None:
            temp = datetime.datetime.now()
            self.date = f'{temp.year}-{temp.month}-{temp.day}'

    def __str__(self):
        dealer_value = calculate_hand(self.hands[0])
        temp = (f'Playdate: {self.date}\n\n'
                f'Dealer Hand: {self.hands[0]} ({dealer_value[0]})')
        if dealer_value[1]:
            temp += " BLACKJACK"
        temp += "\n"
        i = 0
        y = 0
        y2 = 0
        for x in self.hands[1:]:
            if x is None:
                temp += f'\n{self.players[i].getName()}\n'
                i += 1
                y = 0
                continue
            calculated = calculate_hand(x)
            condition = check_condition(dealer_value, calculated)
            temp += (f'Hand {y + 1}: (Bet: {check_bet(self.bets[y2])}) {x} ({calculated[0]}) '
                     f'[{condition}]')
            if calculated[1]:
                temp += " [BLACKJACK]"
            temp += f' Reward: {calculate_win(condition, calculated, self.bets[y2])}'
            temp += "\n"
            y += 1
            y2 += 1
        return temp
