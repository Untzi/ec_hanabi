from __future__ import annotations
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


class PlayerCard(Card):
    def __init__(self, color_or_card, val=None):
        if isinstance(color_or_card,Card):
            super().__init__(color_or_card.color,color_or_card.val)
        else:
            super().__init__(color_or_card, val)

        self.color_status = 'unknown'
        self.val_status = 'unknown'
        self.turns_with_no_info = 0
        self.negative_val = []
        self.negative_color = []


class Player:
    def __init__(self,player_num,hand):
        self.player_num = player_num
        self.hand = [PlayerCard(card) for card in hand]

    def __str__(self):
        ret_str = ''
        for card in self.hand:
            ret_str += str(card) + '\t: color_s: ' + card.color_status  + '\tval_s: ' + card.val_status
            ret_str += '\n'
        ret_str+= '--------------------------------------------------------\n'
        return ret_str

    def get_next_action(self, other_players_hands, discards, inPlay):
        pass

    def player_place_card(self, card: Card, game: Game):
        game.place_card(card)
        new_card = game.deck.pop()
        self.hand.append(PlayerCard(new_card))

    def discard_card(self, card, game):
        self.hand.remove(card)
        game.discards.append(Card(card.color, card.val))
        game.raise_clues()
        new_card = game.deck.pop()
        if len(game.deck) == 0:
            pass #TODO: see how to treat this
        self.hand.append(PlayerCard(new_card))

    def tell_info(self, player:Player, info, game:Game):
            if game.clues == 0:
                raise PermissionError('not allowed to give info')

            for card in player.hand:
                if card.color == info: #type:PlayerCard
                    card.color_status = 'known'
                    card.turns_with_no_info = 0
                elif card.val == info:
                    card.val_status = 'known'
                    card.turns_with_no_info = 0
                else:
                    if info in colors:
                        card.negative_color.append(info)
                    else:
                        card.negative_val.append(info)
            game.clues -= 1


    def raise_turns_with_no_info(self):
        for card in self.hand:
            card.turns_with_no_info += 1

    # def get_playable_card_or_none(self,inPlay):
    #     for card in self.hand:
    #         c = card['card']  # type: Card
    #         card_value = c.val if card_value['color']
    #         card_color = c.color
    #         for desk_card in inPlay: #type: Card
    #             if desk_card.val == card_value -1 and desk_card.color == desk_card.color:
    #                 return c








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

    @staticmethod
    def create_deck():
        deck = []
        for color in colors:
            for val, count in val_count.items():
                cards = [Card(color, val) for i in range(count)]
                deck = deck + cards
        shuffle(deck)
        return deck

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



        for i in range(len(self.players)):
            pass
        self.endgame()
if __name__=='__main__':
    game = Game(2)
    game.print_discards()
    game.print_inPlay()
    game.print_deck()
    game.place_card(Card('red',1))
    game.place_card(Card('red', 1))
    game.place_card(Card('red', 1))
    game.place_card(Card('red', 1))
    

