class Player:

    def __init__(self, user_id: int, username: str, money: int):
        self.user_id = user_id
        self.username = username
        self.money = money

    def getName(self):
        return self.username

    def getMoney(self):
        return self.money
