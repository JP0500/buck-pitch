# Main Module
import ops
from deck import create_cards
from random import randint

def main():
    # one time welcome message
    print("\nWelcome to Buck Pitch the card game!")

    # randomly chooses who gets precedence to bid first
    bid_precedence = randint(1, 2)

    # players start from 0 points
    player_points = 0
    npc_points = 0

    # reaching at least 7 points is the goal of the entire game, each loop is a pitch
    while player_points < 7 > npc_points:

        # assembles deck/list of cards
        deck = create_cards()

        # creates hands of 6 cards each for players
        player_hand = []
        npc_hand = []

        # shuffles deck
        print("\nShuffling...")
        ops.shuffle_cards(deck)

        # deals cards from deck to hands of players
        print("Dealing Cards...\n")
        ops.deal_cards(deck, player_hand, npc_hand)

        # switches bidding order after each pitch, 
        if bid_precedence == 2:
            bid_precedence = 1
        elif bid_precedence == 1:
            bid_precedence = 2

        # takes bids, id of bid winner, and trump suit(eg: diamonds, spades...)
        precedence, bid_amount, trump_suit = ops.bids(bid_precedence, player_hand, npc_hand)

        # record bid winner to check if they buck
        bid_winner = precedence

        # allows player to choose which cards to discard; auto discards non trump-suit cards from npc's hand
        ops.discard(player_hand, npc_hand, trump_suit)

        # restores 6 cards to each hand before play starts
        ops.deal_cards(deck, player_hand, npc_hand)

        # process high and low points before the cards get mixed into piles
        high, high_winner, low, low_winner = ops.process_scores_pre(trump_suit, player_hand, npc_hand)

        # piles are where the cards a player has won go
        player_pile = []
        npc_pile = []
        # play starts
        precedence = ops.main_play(precedence, trump_suit, player_hand, npc_hand, player_pile, npc_pile)

        # process jack and game points after pitch
        jack, jack_winner, game_score, game_point_winner = ops.process_scores_post(trump_suit, player_pile, npc_pile)

        # list of who won each point
        winners = [high_winner, low_winner, jack_winner, game_point_winner]
        # add up the scores at the end of the pitch
        player_points, npc_points = ops.sum_scores(player_points, npc_points, winners, bid_amount, bid_winner)

        # announce who won high and low points
        print(f"Tallying the score...\n\n{high_winner.title()} won the High point with the {high.name()}!\n"
              f"{low_winner.title()} won the Low point with the {low.name()}!")
        # announce who won the jack point
        if jack:
            print(f"{jack_winner.title()} won Jack by capturing the Jack of {trump_suit}!")
        else:
            print(f"There was no Jack of {trump_suit} so {jack_winner.lower()} won the Jack point.")
        # announce who won the game point
        if game_point_winner.lower() != "no one":
            print(f"And with a captured value of {game_score}, {game_point_winner} won the Game point!")
        else:
            print(f"And since each of you have a captured value of {game_score}, "
                  f"{game_point_winner.lower()} wins the Game point!")

        # show overall score
        ps = "s"
        ns = "s"
        if player_points == 1:
            ps = ""
        elif npc_points == 1:
            ns = ""
        print(f"\nThe score is {player_points} point{ps} to you, {npc_points} point{ns} to your opponent!")


    if npc_points < 7:
        final_winner = "You"
    elif player_points < 7:
        final_winner = "Your opponent"
    elif player_points > 7 < npc_points:
        if bid_precedence == 1:
            final_winner = "You"
        elif bid_precedence == 2:
            final_winner = "Your opponent"

    print(f"\n\n{final_winner} went out!!!\n\n\nGame over")


if __name__ == "__main__":
    main()