# Operations and calculations of the game
from random import randint, shuffle

def shuffle_cards(cards):
    shuffle(cards)

# shows player their hand
def player_pov(hand):
    print("Here is your hand:\n")
    for card in hand:
        print(card.name(), end=', ')
    print("\n")

# deals cards by adding to player's hand and deleting from deck
def deal_cards(deck, player_hand, npc_hand):
    while len(player_hand) < 6:
        player_hand.append(deck.pop(randint(0, len(deck) - 1)))
    while len(npc_hand) < 6:
        npc_hand.append(deck.pop(randint(0, len(deck) - 1)))
    player_pov(player_hand)

# gets trunp suit from player or npc
def set_trump_suit(hand, player_won_bid):
    while player_won_bid:
        try:
            trump_suit = input("Which suit would you like to bid in?: ").title()
            for card in hand:
                if card.suit == trump_suit:
                    return trump_suit
            print("You must have at least one card in the suit you bid in.")
        except:
            print("Invalid entry (ops line 32)")
    else:
        qlist = [card.suit for card in hand]
        trump_suit = max(qlist, key=qlist.count)
        return trump_suit

# gets sensible player bid
def get_player_bid():
    while True:
        try:
            player_bid_amount = int(input("How much would you like to bid? (0-4): "))
            if 4 >= player_bid_amount >= 0:
                return player_bid_amount
            print("That number is out of range :(")
        except ValueError:
            print("If you want to pass on bidding try entering 0")
            pass

# gets the winning bid, who won the bid, and which suit is trump
def bids(bid_precedence, player_hand, npc_hand):
    # when the player bids first
    if bid_precedence == 1:
        player_bid_amount = get_player_bid()
        print(f"You bid {player_bid_amount}")
        npc_bid_amount = randint(0, 4)
        # if npc loses the bid (conservative strategy <=)
        if npc_bid_amount <= player_bid_amount:
            print("Your opponent Passes. You won the bid!")
            trump_suit = set_trump_suit(player_hand, True)
            return 1, player_bid_amount, trump_suit
        # if npc wins the bid
        npc_bid_amount = player_bid_amount + 1
        trump_suit = set_trump_suit(npc_hand, False)
        print(f"Your opponent bids {npc_bid_amount} in {trump_suit}.")
        return 2, npc_bid_amount, trump_suit

    # when the npc bids first
    if bid_precedence == 2:
        npc_bid_amount = randint(1, 4)
        print(f"Your opponent bid {npc_bid_amount}")
        player_bid_amount = get_player_bid()
        # if npc wins the bid
        if player_bid_amount <= npc_bid_amount:
            trump_suit = set_trump_suit(npc_hand, False)
            print(f"Your opponent won the bid. Your opponent decided to bid {npc_bid_amount} in {trump_suit}.")
            return 2, npc_bid_amount, trump_suit
        # if npc loses the bid
        print(f"You win the bid!")
        trump_suit = set_trump_suit(player_hand, True)
        return 1, player_bid_amount, trump_suit

# auto discards all non-trump cards
def auto_discard(hand, trump):
    hand_index = [hand.index(card) for card in hand if card.suit != trump]
    hand_index.reverse()
    for index in hand_index:
        hand.pop(index)
    return len(hand_index)

# discards unwanted cards from player's and npc's hands
def discard(player_hand, npc_hand, trump):
    # auto discard for npc
    npc_dis_counter = auto_discard(npc_hand, trump)

    choice = input("Would you like to Discard? (yes/no): ")
    # auto discard for player
    if choice[0].lower() == 'y' and input("Auto or Manual? (Auto only keeps trump cards): ")[0].lower() == 'a':
        player_dis_counter = auto_discard(player_hand, trump)

    # manual discard
    elif choice[0].lower() != 'n':
        dis_card = input("Which card would you like to discard? "
                         "(ex: 'Ace of Hearts' or 'Done' to finish): ")
        player_dis_counter = 0
        while dis_card.lower() != 'done':
            opt_phrase = "No card with that name was found. "
            for card in player_hand:
                if card.name().title() == dis_card.title():
                    opt_phrase = ""
                    print(f"{player_hand.pop(player_hand.index(card)).name()} has been discarded.")
                    player_dis_counter += 1
            dis_card = input(f"{opt_phrase}Which card would you like to "
                             f"discard? (ex: 'Ace of Hearts' or 'Done' to finish): ")
            
    print(f"You discarded {player_dis_counter} cards.")
    print(f"Your opponent discarded {npc_dis_counter} cards.")

# get player input for plays
def player_plays(hand, trump_suit, req_suit):
    opt_phrase = f"{req_suit} or {trump_suit}"
    # avoids redundancy if the required suit is the same as the trump suit
    if trump_suit == req_suit:
        opt_phrase = req_suit
    # ensures valid play from player
    while True:
        choice = input("Enter which card you want to play or type 'pov' to see your hand again: ").lower()
        suits_in_hand = [card.suit for card in hand]

        if choice == 'pov':
            player_pov(hand)
            continue
        elif req_suit in suits_in_hand:
            try:
                # returns chosen card if its suit matches the leading card or is trump
                return hand.pop(hand.index(next(card for card in hand if card.name().lower() == choice
                                                and (card.suit == req_suit or card.suit == trump_suit))))
            except:
                print(f"You must play a card of {opt_phrase}.")
                continue
        else:
            try:
                return hand.pop(hand.index(next(card for card in hand if card.name().lower() == choice)))
            except:
                print("Invalid entry. Try again.")

# npc strategy for plays
def npc_plays(hand, trump_suit, req_suit):

    valid_plays = [card for card in hand if card.suit == req_suit]
    # checks if there is a required suit and if it can match that suit
    if req_suit == 'Any' or len(valid_plays) == 0:
        return hand.pop(randint(0, len(hand) - 1))
    else:
        # random play using only cards of matching suit or trump suit
        valid_plays += [card for card in hand if card.suit == trump_suit]
        return hand.pop(hand.index(valid_plays.pop(randint(0, len(valid_plays) - 1))))

# find who wins and who loses each play
def compare_plays(precedence, trump_suit, player_card, npc_card, player_pile, npc_pile):
    # if player and npc play the same suit, the winner has the higher card (ex: 3 beats 2, Ace beats King)
    if player_card.suit == npc_card.suit:
        if player_card.value > npc_card.value:
            player_pile += player_card, npc_card
            winner = 1
        elif player_card.value < npc_card.value:
            npc_pile += npc_card, player_card
            winner = 2
    #
    elif player_card.suit != trump_suit != npc_card.suit:
        if precedence == 1:
            player_pile += player_card, npc_card
            winner = 1
        elif precedence == 2:
            npc_pile += npc_card, player_card
            winner = 2

    elif player_card.suit == trump_suit != npc_card.suit:
        player_pile += player_card, npc_card
        winner = 1
    elif player_card.suit != trump_suit == npc_card.suit:
        npc_pile += npc_card, player_card
        winner = 2

    if winner == 1:
        print("You take the cards!\n")
    elif winner == 2:
        print("Your opponent takes the cards!\n")

    return winner

# 
def process_scores_pre(trump_suit, player_hand, npc_hand):
    player_trump_cards = [card.value for card in player_hand if card.suit == trump_suit]
    npc_trump_cards = [card.value for card in npc_hand if card.suit == trump_suit]

    # determines who has the highest trump card
    if len(npc_trump_cards) == 0 or max(player_trump_cards) > max(npc_trump_cards):
        high = next(card for card in player_hand if card.value == max(player_trump_cards))
        high_winner = "you"
    elif len(player_trump_cards) == 0 or max(player_trump_cards) < max(npc_trump_cards):
        high = next(card for card in npc_hand if card.value == max(npc_trump_cards))
        high_winner = "your opponent"


    if len(npc_trump_cards) == 0 or min(player_trump_cards) < min(npc_trump_cards):
        low = next(card for card in player_hand if card.value == min(player_trump_cards))
        low_winner = "you"
    elif len(player_trump_cards) == 0 or min(player_trump_cards) > min(npc_trump_cards):
        low = next(card for card in npc_hand if card.value == min(npc_trump_cards))
        low_winner = "your opponent"

    return high, high_winner, low, low_winner

# tally the game score
def calc_game_score(pile):
    score = 0
    # only face cards and tens give game scores
    for card in [face_card for face_card in pile if face_card.value >= 10]:
        score += card.value
        # 10's are worth 10, jacks 1, queens 2... aces 4
        if card.value > 10:
            score -= 10
    return score

def process_scores_post(trump_suit, player_pile, npc_pile):
    # check for a trump jack and find who captured it
    if (jack := any([card for card in player_pile if card.value == 11 and card.suit == trump_suit])):
        jack_winner = "you"
    elif (jack := any([card for card in npc_pile if card.value == 11 and card.suit == trump_suit])):
        jack_winner = "your opponent"
    else:
        jack_winner = "no one"

    # get game score
    player_game_score = calc_game_score(player_pile)
    npc_game_score = calc_game_score(npc_pile)

    # find out who won the game point
    if player_game_score > npc_game_score:
        winning_game_score = player_game_score
        game_point_winner = "you"
    elif npc_game_score > player_game_score:
        winning_game_score = npc_game_score
        game_point_winner = "your opponent"
    elif player_game_score == npc_game_score:
        winning_game_score = npc_game_score
        game_point_winner = "no one"

    return jack, jack_winner, winning_game_score, game_point_winner

# a pitch
def main_play(precedence, trump_suit, player_hand, npc_hand, player_pile, npc_pile):
    # 6 turns in each pitch
    for turn in range(1, 7):
        req_suit = "Any"
        # a trump card is required for the first play
        if turn == 1:
            req_suit = trump_suit
        # if player goes first
        if precedence == 1:
            player_card = player_plays(player_hand, trump_suit, req_suit)
            print(f"You played your {player_card.name()}")
            npc_card = npc_plays(npc_hand, trump_suit, player_card.suit)
            print(f"\nYour opponent plays their {npc_card.name()} against your {player_card.name()}")
            precedence = compare_plays(precedence, trump_suit, player_card, npc_card, player_pile, npc_pile)
        # if npc goes first
        elif precedence == 2:
            npc_card = npc_plays(npc_hand, trump_suit, req_suit)
            print(f"Your opponent played their {npc_card.name()}")
            player_card = player_plays(player_hand, trump_suit, npc_card.suit)
            print(f"\nYou play your {player_card.name()} against the opponent's {npc_card.name()}")
            precedence = compare_plays(precedence, trump_suit, player_card, npc_card, player_pile, npc_pile)

    return precedence

# add up points
def sum_scores(player_pts, npc_pts, winners, threshold, bid_winner):
    # points from the pitch
    bid_pts = 0
    for winner in winners:
        if winner.title() == "You":
            player_pts += 1
            if bid_winner == 1:
                bid_pts += 1
        elif winner.title() == "Your Opponent":
            npc_pts += 1
            if bid_winner == 2:
                bid_pts += 1
    # if the bid isn't met, you buck
    if bid_pts < threshold:
        if bid_winner == 1:
            player_pts -= threshold + bid_pts
            print(f"Uh oh! You Bucked! You lose {threshold + bid_pts} points!")
        elif bid_winner == 2:
            npc_pts -= threshold + bid_pts
            print(f"Uh oh! Your Opponent Bucked! Your Opponent loses {threshold + bid_pts} points!")
    # points can't go into the negatives
    if player_pts < 0:
        player_pts = 0
    elif npc_pts < 0:
        npc_pts == 0

    return player_pts, npc_pts