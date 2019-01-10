# from __future__ import annotations
from card import Card
from player import Player , PlayerCard
# from game import Game


class RuleSet:
    def __init__(self):
        pass
    @staticmethod
    def is_card_playable(card,game):
        inPlay = game.inPlay
        return inPlay[card.color] == (card.val - 1)

    @staticmethod
    def has_playable_card(player, game = None, return_card = None):
        to_ret = None
        for card in player.hand: #type: PlayerCard
            if card.color_status != 'unknown' and card.val_status != 'unknown':
                if RuleSet.is_card_playable(card, game):
                        return (True, card) if (return_card != None) else True

        if to_ret == None:
            return False
        else:
            return False, False


    #
    # @staticmethod
    # def deduction(player:Player, game, return_card = None):
    #     counts = game.generate_counts()
    #     #removing cards from discards and inPlay
    #     for card in game.discards:
    #         counts[card.color].remove(card.val)
    #     for color in game.inPlay:
    #         for i in range(game.inPlay[color]+1):
    #             counts[color].remove(i)
    #     #remove known cards from the players hand
    #     for p in game.players: #type: Player
    #         for card in p.hand: #type: PlayerCard
    #             if p.player_num == player.player_num:
    #                 if card.val_status != 'unknown' and card.color_status != 'unknown':
    #                     try:
    #                         counts[card.color].remove(card.val)
    #                     except ValueError:
    #                         print('value error')
    #                         continue
    #             else:
    #                 try:
    #                     counts[card.color].remove(card.val)
    #                 except ValueError:
    #                     print('value error')
    #                     continue
    #     #deducing if only one value is known about color
    #     for card in player.hand:
    #         if card.val_status == 'unknown' and card.color_status != 'unknown':
    #             if len(set(counts[card.color])) == 1:
    #                 card.val_status = 'known'
    #                 counts[card.color].remove(card.val)
    #
    #     reverse_counts = RuleSet.inverse_dict(counts)
    #     for card in player.hand:
    #         if card.val_status != 'unknown' and card.color_status == 'unknown':
    #             if len(set(reverse_counts[card.val])):
    #                 card.color_status = 'known'
    #                 counts[card.color].remove(card.val)
    #     return counts