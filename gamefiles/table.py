import time
from player import Player
from deck import Deck
from os import system
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
    elif dealer_value[0] > 21:
        condition = "WIN"
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
    def __init__(self, players: list[Player], bets=None, hands=None, date=None,deck=Deck()):
        if hands is None:
            hands = []
        self.players = players
        self.deck = deck
        self.hands = hands
        self.bets = bets
        self.date = date
        if date is None:
            temp = datetime.datetime.now()
            self.date = f'{temp.year}-{temp.month}-{temp.day}'

    def __str__(self):
        system("cls")
        dealer_value = calculate_hand(self.hands[-1])
        temp = (f'Playdate: {self.date}\n\n'
                f'Dealer Hand: {self.hands[-1]} ({dealer_value[0]})')
        if dealer_value[0] > 21:
            temp += " [BUST]"
        if dealer_value[1]:
            temp += " BLACKJACK"
        temp += "\n"
        i = 0
        y = 0
        y2 = 0
        for x in self.hands[:-1]:
            if x is None:
                temp += f'\nSeat {i+1} "{self.players[i].getName()}"\n'
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

    def get_data(self):
        return self.players, self.bets, self.hands, self.date

    def game_start(self):
        temp_hands = []
        for _ in range(len(self.players)):
            temp = []
            temp_hands.append([temp])
        temp = []
        temp_hands.append(temp)
        for x in temp_hands[:-1]:
            x[0].append(self.deck.getCard())
        temp_hands[-1].append(self.deck.getCard())
        for x in temp_hands[:-1]:
            x[0].append(self.deck.getCard())

        hand_count = 0
        print()
        for x, player_hand in enumerate(temp_hands[:-1]):
            system("cls")
            count = 1
            dealer_calculated = calculate_hand(temp_hands[-1])
            dealer_hand_str = f"\nDealer Hand: {temp_hands[-1]} ({dealer_calculated[0]}"
            if dealer_calculated[0] != dealer_calculated[2]:
                dealer_hand_str += f'/{dealer_calculated[2]}'
            dealer_hand_str += f')\n'
            print(dealer_hand_str)
            print(f'Seat {hand_count + 1} "{self.players[x].getName()}" Money: {self.players[x].getMoney()}\n')
            i = 1
            while i > 0:
                hand = player_hand[count - 1]
                state = True
                sleep_state = False
                while state:
                    calculated = calculate_hand(hand)
                    length = len(hand)
                    if calculated[0] > 21:
                        print("BUST")
                        hand_count += 1
                        count += 1
                        sleep_state = True
                        break
                    if length == 2 and calculated[0] == 21:
                        print("BLACKJACK")
                        hand_count += 1
                        count += 1
                        sleep_state = True
                        break
                    if calculated[0] == 21:
                        print("PERFECT")
                        hand_count += 1
                        count += 1
                        sleep_state = True
                        break
                    command = "Hit, Stand"
                    if length == 2 and (hand[0] == hand[1] or (
                            hand[0] in ["K", "Q", "J", "10"] and hand[1] in ["K", "Q", "J", "10"])) \
                            and self.players[x].getMoney() >= self.bets[hand_count][0]:
                        command += ", Split"
                    if length == 2 and (calculated[0] in [9, 10, 11] or calculated[2] in [9, 10, 11]) \
                            and self.players[x].getMoney() >= self.bets[hand_count][0] and not self.bets[hand_count][1]:
                        command += ", Double"
                    temp = f'Hand {count}: (Bet: {self.bets[hand_count][0]}) {hand} ({calculated[0]}'
                    if calculated[0] != calculated[2]:
                        temp += f'/{calculated[2]}'
                    temp += f')\n{command}'
                    print(temp)
                    hand_count += 1
                    count += 1
                    while True:
                        answer = input().lower().strip()
                        if answer == "stand":
                            state = False
                            sleep_state = True
                            break
                        if answer == "split":
                            self.bets.insert(hand_count, [self.bets[hand_count - 1][0], False])
                            self.players[x].money -= self.bets[hand_count - 1][0]
                            card = hand.pop()
                            hand.append(self.deck.getCard())
                            player_hand.insert(count - 1, [card, self.deck.getCard()])
                            i += 1
                            count -= 1
                            hand_count -= 1
                            print()
                            break
                        elif answer == "double":
                            state = False
                            self.bets[hand_count - 1][0] *= 2
                            self.bets[hand_count - 1][1] = True
                            hand.append(self.deck.getCard())
                            sleep_state = True
                            break
                        elif answer == "hit":
                            hand.append(self.deck.getCard())
                            hand_count -= 1
                            count -= 1
                            break
                        else:
                            print("Not a command")
                print(f'Hand {count-1}: (Bet: {self.bets[hand_count-1][0]}) {hand} ({calculate_hand(hand)[0]})\n')
                if sleep_state:
                    time.sleep(1)
                i -= 1
        system("cls")
        print('\n"Dealer Round"')
        while True:
            calculated = calculate_hand(temp_hands[-1])
            temp = f'Dealer Hand: {temp_hands[-1]} ({calculated[0]}'
            if calculated[0] != calculated[2]:
                temp += f'/{calculated[2]}'
            temp += f')'
            print(temp, end="\r")
            if calculated[0] > 21 and calculated[2] > 21:
                print("BUST")
                break
            if len(temp_hands[-1]) == 2 and calculated[0] == 21:
                print("BLACKJACK")
                break
            if calculated[0] < 17 and calculated[1] < 17:
                temp_hands[-1].append(self.deck.getCard())
                time.sleep(1.5)
            else:
                break

        for x in temp_hands[:-1]:
            self.hands.append(None)
            for y in x:
                self.hands.append(y)
        self.hands.append(temp_hands[-1])
        time.sleep(1.5)
        print(self)

        dealer_value = calculate_hand(self.hands[-1])
        i = -1
        y = 0
        for x in self.hands[:-1]:
            if x is None:
                i += 1
                continue
            calculated = calculate_hand(x)
            reward = calculate_win(check_condition(dealer_value, calculated), calculated, self.bets[y])
            self.players[i].money += reward
            y += 1

# TODO: Edit dealer second card. Should be EU rules. No second card
