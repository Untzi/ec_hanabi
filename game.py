from __future__ import annotations
from random import shuffle
from card import Card, PlayerCard
from player import Player

colors = ['blue', 'red', 'yellow', 'white', 'green']
val_count = {1: 3, 2: 2, 3: 2, 4: 2, 5: 1}


class Game:
    def __init__(self, players_num):
        self.deck = self.create_deck()
        self.discards = []
        self.clues = 8
        self.strikes = 3
        self.turn = -1
        self.last_round = False
        self.players = []
        self.inPlay = {color: 0 for color in colors}
        for player in range(players_num):
            hand = []
            for i in range(5):
                hand.append(self.deck.pop())
            player = Player(player, hand)
            self.players.append(player)

    def raise_clues(self):
        self.clues = self.clues+1 if self.clues+1 < 9 else 8

    def place_card(self, card:Card):
        color = card.color
        if self.inPlay[color] == card.val-1:
            self.raise_clues()
            self.inPlay[color] = card.val
            print('legal card!! clues: '+ str(self.clues))
        else:
            self.strikes -= 1
            self.discards.append(card)
            if self.strikes == 0:
                self.endgame()
                return
            print('ilegal card!! strikes:' + str(self.strikes))

    def endgame(self):
        final_score = sum(self.inPlay.values())
        print('final ' + str(final_score))

    def next_turn(self):
        self.turn = (self.turn+1) % len(self.players)
        return self.turn

    def get_card_list_by_color(self,cards):
        ret = {color: [] for color in colors}
        for card in cards:
            ret[card.color].append(card.val)

    def get_card_list_by_val(self, cards):
        ret = {value: [] for value in [1,2,3,4,5]}
        for card in cards:
            ret[card.val].append(card.color)

    @staticmethod
    def create_deck():
        deck = []
        for color in colors:
            for val, count in val_count.items():
                cards = [Card(color, val) for _ in range(count)]
                deck = deck + cards
        shuffle(deck)
        return deck

    @staticmethod
    def generate_counts():
        to_ret = {}
        for color in colors:
            to_ret[color] = [1, 1, 1, 2, 2, 3, 3, 4, 4, 5]
        return to_ret

    def print_deck(self):
        print([str(card) for card in self.deck])

    def print_discards(self):
        print([str(card) for card in self.discards])

    def print_inPlay(self):
        print(self.inPlay)

    def run_game(self):
        while not self.last_round:
            self.next_turn()
            curr_player = self.players[self.turn] #type: Player
            curr_player.get_next_action(self.playersp[self.turn+1 % len(self.players)], self.discards, self.inPlay)

            if len(self.deck) == 0:
                self.last_round =True
        for i in range(len(self.players)):
            pass
        self.endgame()

if __name__=='__main__':
    game = Game(2)
    game.run_game()

    game.print_discards()
    game.print_inPlay()
    game.print_deck()
    game.place_card(Card('red',1))
    game.place_card(Card('red', 1))
    game.place_card(Card('red', 1))
    game.place_card(Card('red', 1))
    print(Game.generate_counts())

