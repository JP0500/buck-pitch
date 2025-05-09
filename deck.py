# Creates Cards

class Cards:

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def name(self):
        if self.value <= 10:
            return f"{self.value} of {self.suit}"
        else:
            face_cards = {11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}
            return f"{face_cards[self.value]} of {self.suit}"

def create_cards():

    suits = ('Diamonds', 'Spades', 'Hearts', 'Clubs')
    card_values = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)

    deck = []
    for suit in suits:
        for value in card_values:
            deck.append(Cards(suit, value))

    return deck