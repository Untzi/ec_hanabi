# from __future__ import annotations
from card import Card, PlayerCard
# from random import sample
import random



colors = ['blue', 'red', 'yellow', 'white', 'green']
known_status = ['color', 'val', 'color_and_val', 'none']
values = [1,2,3,4,5]

class Player:
    def __init__(self,player_num,hand, game):
        # random.seed(1)
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
        # action = random.sample(self.get_random_info(), self.discard_oldest_with_least_info(),self.get_random_info_from_player())
        # action()
        game.player_action_tree()
        for player in game.players:
            player.raise_turns_with_no_info()



    def player_place_card(self, card: PlayerCard, game):
        game.place_card(card)
        if len(game.deck) > 0:
            new_card = game.deck.pop()
            if len(game.deck) == 0:
                game.last_round = True
            self.hand.append(PlayerCard(new_card))
        self.hand.remove(card)

    def discard_card(self, card, game):
        if len(self.hand) < 5 and game.last_round:
            return
        self.hand.remove(card)
        game.discards.append(Card(card.color, card.val))
        game.raise_clues()
        if len(game.deck) > 0:
            new_card = game.deck.pop()
            self.hand.append(PlayerCard(new_card))
            if len(game.deck) == 0:
                game.last_round = True


    def tell_info(self, player, info, game):
        if game.clues == 0:
            # raise PermissionError('not allowed to give info')
            return
        if info in ["1", "2", "3", "4", "5"]:
            info = int(info)
        for card in player.hand:
            if card.color == info: #type:PlayerCard
                card.color_status = 'known'
                card.turns_with_no_info = -1
            elif card.val == info:
                card.val_status = 'known'
                card.turns_with_no_info = -1
            else:
                if info in colors:
                    card.negative_color.append(info)
                else:
                    card.negative_val.append(info)
                card.color_status = 'known' if len(set(colors) - set(card.negative_color)) == 1 else 'unknown'
                card.val_status = 'known' if len(set([1,2,3,4,5]) - set(card.negative_val)) == 1 else 'unknown'

        game.clues -= 1

    def get_playable_card_or_none(self, inPlay):
        for card in self.hand:
            for desk_card in inPlay: #type: Card
                if desk_card.val == card.val -1 and card.color == desk_card.color and \
                        card.color_status != 'unknown' and card.val_status != 'unknown':
                    return card
        return None

    def get_random_info(self):
        to_rand = random.sample(['val', 'color'])
        if to_rand == 'val':
            random_info = random.sample(values)
        else:
            random_info = random.sample(colors)
        return random_info

    def discard_oldest_with_least_info(self):
        if not self.game.last_round and len(self.hand)==0:
            print('problem')
        to_discard = random.sample(self.hand, 1)[0] #type: PlayerCard
        for card in self.hand:
            if (card.color_status == 'unknown' and card.val_status == 'unknown'
                    and (card.turns_with_no_info < to_discard.turns_with_no_info)):
                to_discard = card
        self.discard_card(to_discard, self.game)

    def raise_turns_with_no_info(self):
        for card in self.hand:
            card.turns_with_no_info += 1

    def deduction(self, return_card=None):
        counts = self.game.generate_counts()
        # removing cards from discards and inPlay
        for card in self.game.discards:
            counts[card.color].remove(card.val)
        for color in self.game.inPlay:
            for i in range(self.game.inPlay[color]):
                if i == 0:
                    continue
                counts[color].remove(i)
        # remove known cards from the players hand
        for p in self.game.players:  # type: Player
            for card in p.hand:  # type: PlayerCard
                if p.player_num == self.player_num:
                    if card.val_status != 'unknown' and card.color_status != 'unknown':
                        try:
                            counts[card.color].remove(card.val)
                        except ValueError:
                            print('value error')
                            continue
                else:
                    try:
                        counts[card.color].remove(card.val)
                    except ValueError:
                        print('value error')
                        continue
        # deducing if only one value is known about color
        for card in self.hand:
            if card.val_status == 'unknown' and card.color_status != 'unknown':
                if len(set(counts[card.color])) == 1:
                    card.val_status = 'known'
                    counts[card.color].remove(card.val)

        reverse_counts = Player.inverse_dict(counts)
        for card in self.hand:
            if card.val_status != 'unknown' and card.color_status == 'unknown':
                if len(set(reverse_counts[card.val])):
                    card.color_status = 'known'
                    counts[card.color].remove(card.val)
        return counts

    @staticmethod
    def inverse_dict(m):
        inv_map = {}
        for k, v in m.items():
            for val in v:
                inv_map[val] = inv_map.get(val, [])
                inv_map[val].append(k)
        return inv_map

    def update_safe_probabilities(self, counts):
        for card in self.hand:
            if card.color_status != 'unknown':
                next_val = self.game.get_next_playable(card.color)
                if len(counts[card.color]) != 0:
                    card.safe_to_play_prob = counts[card.color].count(next_val)//len(counts[card.color])

