# from __future__ import annotations
from card import Card, PlayerCard
from random import sample



colors = ['blue', 'red', 'yellow', 'white', 'green']
known_status = ['color', 'val', 'color_and_val', 'none']
values = [1,2,3,4,5]

class Player:
    def __init__(self,player_num,hand, game):
        self.player_num = player_num
        self.hand = [PlayerCard(card) for card in hand]
        self.game = game

    def __str__(self):
        ret_str = ''
        for card in self.hand:
            ret_str += str(card) + '\t: color_s: ' + card.color_status  + '\tval_s: ' + card.val_status
            ret_str += '\n'
        ret_str+= '--------------------------------------------------------\n'
        return ret_str

    def get_next_action(self, game):
        # action = sample(self.get_random_info(), self.discard_oldest_with_least_info(),self.get_random_info_from_player())
        # action()
        game.player_action_tree()

    def player_place_card(self, card: PlayerCard, game):
        print("player_place_card")
        game.place_card(card)
        if len(game.deck)> 0:
            new_card = game.deck.pop()
            self.hand.append(PlayerCard(new_card))
        self.hand.remove(card)


    def discard_card(self, card, game):
        print("discard_card")
        self.hand.remove(card)
        game.discards.append(Card(card.color, card.val))
        game.raise_clues()
        if len(game.deck) > 0:
            new_card = game.deck.pop()
            self.hand.append(PlayerCard(new_card))
        if len(game.deck) == 0:
            game.last_round = True


    def tell_info(self, player, info, game):
        print("tell_info")
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
                card.color_status = 'known' if len(set(colors) - set(card.negative_color)) == 1 else 'unknown'
                card.val_status = 'known' if len(set([1,2,3,4,5]) - set(card.negative_val)) == 1 else 'unknown'

        game.clues -= 1

    def get_playable_card_or_none(self,inPlay):
        for card in self.hand:
            for desk_card in inPlay: #type: Card
                if desk_card.val == card.val -1 and card.color == desk_card.color and \
                        card.color_status != 'unknown' and card.val_status != 'unknown':
                    return card
        return None

    def get_random_info(self):
        to_rand = sample(['val', 'color'])
        if to_rand == 'val':
            random_info = sample(values)
        else:
            random_info = sample(colors)
        return random_info

    def get_random_info_from_player(self, player_hand):
        sampled_Card = sample(player_hand)
        return sample([sampled_Card.color, sampled_Card.val])

    def discard_oldest_with_least_info(self):
        to_discard = sample(self.hand) #type: PlayerCard
        for card in self.hand:
            if (card.color_status == 'unknown' and card.val_status == 'unknown'
                    and (card.turns_with_no_info < to_discard.turns_with_no_info)):
                to_discard = card

    def raise_turns_with_no_info(self):
        for card in self.hand:
            card.turns_with_no_info += 1

