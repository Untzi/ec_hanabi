class Card:

    def __init__(self, color, val):
        self.val = val
        self.color = color

    def __str__(self):
        return self.color + '-' + str(self.val)

    def __eq__(self, other):
        return other.val == self.val and other.color == self.color

    def __ne__(self, other):
        return not self.__eq__(other)


class PlayerCard(Card):
    def __init__(self, color_or_card, val=None):
        if isinstance(color_or_card, Card):
            super().__init__(color_or_card.color, color_or_card.val)
        else:
            super().__init__(color_or_card, val)

        self.color_status = 'unknown'
        self.val_status = 'unknown'
        self.turns_with_no_info = 0
        self.negative_val = []
        self.negative_color = []
        self.safe_to_play_prob = 0
    def __eq__(self, other):
        if isinstance(other, PlayerCard):
            color_and_val_equals = super().__eq__(other)
            return (other.turns_with_no_info == self.turns_with_no_info
                    and other.val_status == self.val_status
                    and other.color_status == self.color_status
                    and other.negative_color == self.negative_color
                    and other.negative_val == self.negative_color
                    and color_and_val_equals)
        else:
            return other.val == self.val and other.color == self.color

    def __ne__(self, other):
        return not self.__eq__(other)
