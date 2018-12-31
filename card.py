class Card:

    def __init__(self, color, val):
        self.val = val
        self.color = color

    def __str__(self):
        return self.color + '-' + str(self.val)


class PlayerCard(Card):
    def __init__(self, color_or_card, val=None):
        if isinstance(color_or_card, Card):
            super().__init__(color_or_card.color,color_or_card.val)
        else:
            super().__init__(color_or_card, val)

        self.color_status = 'unknown'
        self.val_status = 'unknown'
        self.turns_with_no_info = 0
        self.negative_val = []
        self.negative_color = []