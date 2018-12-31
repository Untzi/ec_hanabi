from __future__ import annotations
from card import Card, PlayerCard
# from game import Game


colors = ['blue', 'red', 'yellow', 'white', 'green']
known_status = ['color', 'val', 'color_and_val', 'none']


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

    def player_place_card(self, card: Card, game):
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
    # def get_playable_card_or_none(self,inPlay):
    #     for card in self.hand:
    #         c = card['card']  # type: Card
    #         card_value = c.val if card_value['color']
    #         card_color = c.color
    #         for desk_card in inPlay: #type: Card
    #             if desk_card.val == card_value -1 and desk_card.color == desk_card.color:
    #                 return c

    def raise_turns_with_no_info(self):
        for card in self.hand:
            card.turns_with_no_info += 1