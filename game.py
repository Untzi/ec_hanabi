from random import shuffle
colors = ['blue', 'red', 'yellow', 'white', 'green']
val_count = {1: 3, 2: 2, 3: 2, 4: 2, 5: 1}
known_status = ['color', 'val', 'color_and_val', 'none']

class Card:

    def __init__(self, color, val):
        self.val = val
        self.color = color

    def __str__(self):
        return self.color + '-' + str(self.val)

class Player:
    def __init__(self,player_num,hand):
        self.player_num = player_num
        self.hand = [{'card': card, 'status': 'none'} for card in hand]

    def __str__(self):
        ret_str = ''
        for card in self.hand:
            ret_str+=str(card['card']) + ':' + card['status'] + '|'
        return ret_str

class Game:
    def __init__(self, players_num):
        self.deck = self.create_deck()
        self.discards = []
        self.clues = 8
        self.strikes = 3
        self.turn = 0
        self.players = []
        self.inPlay = {color: 0 for color in colors}
        for player in range(players_num):
            hand = []
            for i in range(5):
                hand.append(self.deck.pop())
            player = Player(player, hand)
            self.players.append(player)

    def print_deck(self):
        print([str(card) for card in self.deck])

    def print_discards(self):
        print([str(card) for card in self.discards])

    def print_inPlay(self):
        print(self.inPlay)

    def raise_clues(self):
        self.clues = self.clues+1 if self.clues+1 < 9 else 8

    def place_card(self, card:Card):
        color = card.color
        if self.inPlay[color] == card.val-1:
            self.raise_clues()
            self.inPlay[color] = card.val
            print('legal card!! clues:'+ str(self.clues))
        else:
            self.strikes -= 1
            self.discards.append(card)
            if self.strikes == 0:
                self.endgame()
            print('ilegal card!! strikes:' + str(self.strikes))

    def endgame(self):
        pass

    def next_turn(self):
        self.turn = (self.turn+1) % len(self.players)
        return self.turn

    @staticmethod
    def create_deck():
        deck = []
        for color in colors:
            for val, count in val_count.items():
                cards = [Card(color, val) for i in range(count)]
                deck = deck + cards
        shuffle(deck)
        return deck

if __name__=='__main__':
    game = Game(2)
    game.print_inPlay()
    game.print_discards()
    game.place_card(Card('red',1))
    game.place_card(Card('red', 1))
    game.print_inPlay()
    game.print_discards()
