"""Freecell game."""

import types
from cards import *


def cleanup_tableau(tableau):
    """Clear the last 4 cells of the last row upon game setup."""
    del tableau[4][6]
    del tableau[5][6]
    del tableau[6][6]
    del tableau[7][6]
    return tableau


def setup():
    """Create game structures."""
    # paramaters: None (deck can be created within this function)
    # returns:
    # - a foundation (list of 4 empty lists)
    # - cell (list of 4 empty lists)
    # - a tableau (a list of 8 lists, the dealt cards)
    foundation = [[], [], [], []]
    cell = [[], [], [], []]
    tableau = [[], [], [], [], [], [], [], []]

    # Instantiate an instance of Deck and shuffle the deck
    deck = Deck()
    deck.shuffle()

    while deck.cards_count() > 0:
        for i in tableau:
            i.append(deck.deal())

    cleanup_tableau(tableau)
    return foundation, tableau, cell


def tableau_to_foundation(foundation, tableau, cell, t_col, f_col):
    """Move a card from the tableau to the foundation."""
    # parameters: a tableau, a foundation, column of tableau, column of foundation
    # returns: Boolean (True if the move is valid, False otherwise)
    # moves a card at the end of a column of tableau to a column of foundation
    # This function can also be used to move a card from cell to foundation

    # Grab the last card of the selected column

    card = tableau[t_col - 1][-1]

    # Delete the last card of the selected column
    del tableau[t_col - 1][-1]

    # Add that card to the selected location in the foundation
    foundation = foundation[f_col - 1].append(card)

    return tableau, foundation


def tableau_to_cell(tableau, cell, t_col, c_col):
    """Move a card from the tableau to the cell."""
    # parameters: a tableau, a cell, column of tableau, column of cell
    # returns: Boolean (True if the move is valid, False otherwise)
    # moves a card at the end of a column of tableau to a cell

    # Grab the last card of the selected column
    card = tableau[t_col - 1][-1]

    # Delete the last card of the selected column
    del tableau[t_col - 1][-1]

    # Add that card to the selected location in the foundation
    cell = cell[c_col - 1].append(card)

    return tableau, cell


def tableau_to_tableau(foundation, tableau, cell, t_col, tdest_col):
    """Move a card from one column of the tableau to another column of the tableau."""
    # parameters: a tableau, a cell, column of tableau, a cell
    # returns: Boolean (True if the move is valid, False otherwise)
    # moves a card in the cell to a column of tableau
    # remember to check validity of move
    if t_col == tdest_col:
        print("INVALID MOVE:\n You cannot move a card into the same column")
        play(foundation, tableau, cell)
    else:
        # Grab the last card of the selected column
        card = tableau[t_col - 1][-1]

        # Delete the last card of the selected column
        del tableau[t_col - 1][-1]

        # Add that card to the selected location in the foundation
        tableau = tableau[tdest_col - 1].append(card)

        return tableau


def cell_to_tableau(foundation, tableau, cell, c_col, t_col):
    """Move a card from the cell to the tableau."""
    # Grab the last card of the selected column
    card = cell[c_col - 1][-1]

    # Delete the last card of the selected column
    del cell[c_col - 1][-1]

    # Add that card to the selected location in the foundation
    tableau = tableau[t_col - 1].append(card)

    return tableau, cell


def cell_to_foundation(foundation, tableau, cell, c_col, f_col):
    """Move a card from the cell to the foundation."""
    # Grab the last card of the selected column
    card = cell[c_col - 1][-1]

    # Delete the last card of the selected column
    del cell[c_col - 1][-1]

    # Add that card to the selected location in the foundation
    foundation = foundation[f_col - 1].append(card)

    return foundation, cell


def print_game(foundation, tableau, cell):
    """Print the current state of the game."""
    # parameters: a tableau, a foundation and a cell
    # returns: Nothing
    # prints the game, i.e, print all the info user can see.
    # Includes:
    #     a) print tableau
    #     b) print foundation ( can print the top card only)
    #     c) print cells
    print()
    print("                 Cells:                           Foundation:")
    # print cell and foundation labels in one line
    for i in range(4):
        print("{:8d}".format(i + 1), end="")
    print("    ", end="")
    for i in range(4):
        print("{:8d}".format(i + 1), end="")
    print()  # carriage return at the end of the linefoundation

    # print cell and foundation cards in one line; foundation is only top card
    for c in cell:
        # print if there is a card there; if not, exception prints spaces.
        try:
            print("    {:8s}".format(c[0]), end="")
        except IndexError:
            print("{:8s}".format(""), end="")

    print("    ", end="")
    for stack in foundation:
        # print if there is a card there; if not, exception prints spaces.
        try:
            print("    {:8s}".format(stack[-1]), end="")
        except IndexError:
            print("{:8s}".format(""), end="")

    print()  # carriage return at the end of the line
    print("----------")

    print("\n                                Tableau")
    for i in range(len(tableau)):  # print tableau headers
        print("{:8d}".format(i + 1), end="")
    print("\n")  # carriage return at the end of the line

    # Find the length of the longest stack
    max_length = max([len(stack) for stack in tableau])

    # print tableau stacks row by row
    for i in range(max_length):  # for each row
        print(" " * 7, end="")  # indent each row
        for stack in tableau:
            # print if there is a card there; if not, exception prints spaces.
            try:
                print("{:8s}".format(stack[i]), end="")
            except IndexError:
                print("{:8s}".format(""), end="")
        print()  # carriage return at the end of the line
    print("----------")


def print_rules():
    """Print the rules of freecell."""
    # parameters: none
    # returns: nothing
    # prints the rules
    print("Rules of FreeCell")

    print("Goal")
    print("\tMove all the cards to the Foundations")

    print("Foundation")
    print("\tBuilt up by rank and by suit from Ace to King")

    print("Tableau")
    print("\tBuilt down by rank and by alternating color")
    print("\tThe bottom card of any column may be moved")
    print("\tAn empty spot may be filled with any card ")

    print("Cell")
    print("\tCan only contain 1 card")
    print("\tThe card may be moved")


def show_help():
    """Show user help menus."""
    # parameters: none
    # returns: nothing
    # prints the supported commands
    print("Responses are: ")
    print("\t t2f #T #F - move from Tableau to Foundation")  # X
    print("\t t2t #T1 #T2 - move card from one Tableau column to another")  # X
    print("\t t2c #T #C - move from Tableau to Cell")  # X
    print("\t c2t #C #T - move from Cell to Tableau")
    print("\t c2f #C #F - move from Cell to Foundation")
    print("\t 'h' for help")
    print("\t 'q' to quit")


def get_cols(source_name, dest_name):
    """Get the columns for choosing where you will move cards."""
    while True:
        try:
            source = int(
                input("Please enter the source column from %s: " % (source_name))
            )
            dest = int(
                input("Please enter the destination column from %s: " % (dest_name))
            )
            break
        except:
            print("Please only enter the column numbers you see on screen!")

    return source, dest


def empty_foundation(foundation):
    """Check if the foundation is empty."""
    for i in range(4):
        if len(foundation[i]) == 0:
            return True
        else:
            return False


def convert_to_int(card):
    """Convert a card into an integer."""
    return int(card)


def check_foundation_move(desired, foundation, tableau, cell, source, dest):
    """Check if a given move into foundation is complient with game rules."""
    card = desired[source - 1][-1]
    card_val = convert_to_int(card.get_value())
    card_suit = card.get_suit()

    # If destination column in Foundation is a list with len=0, we know its empty
    # Therefore the first move must be an ace
    if len(foundation[dest - 1]) == 0:
        if card_val == 1:
            print("VALID MOVE: CARD IS ACE")
            return True
        else:
            print("INVALID MOVE: FIRST CARD MUST BE AN ACE!")
            return False
    else:
        foundation_value = foundation[dest - 1][-1].get_value()
        foundation_suit = foundation[dest - 1][-1].get_suit()

        if card_val == foundation_value + 1 and card_suit == foundation_suit:
            print(
                "TABLEAU CARD IS GREATER THAN FOUNDATION CARD AND CARDS SHARE SAME SUIT"
            )
            return True
        elif card_val > foundation_value + 1 or card_suit != foundation_suit:
            print("CARD IS GREATER THAN FOUNDATION VALUE + 1")
            return False
        elif card_val <= foundation_value:
            print("TABLEAU CARD IS LESS THAN FOUNDATION CARD")
            return False


def check_winner(foundation):
    """Check if the player has won the game."""
    win_cols = [0, 0, 0, 0]
    if empty_foundation(foundation) == False:
        try:
            for i in range(len(foundation)):
                if foundation[i][-1].get_rank() == 13:
                    win_cols[i] = 1
                elif foundation[i][-1].get_rank() != 13:
                    win_cols[i] = 0
        except:
            print("")

    if sum(win_cols) == 4:
        return True
    else:
        return False


def play(foundation, tableau, cell):
    """Play Freecell. Does error checking on the user input."""
    while True:
        # Uncomment this next line. It is commented out because setup doesn't
        # do anything so printing doesn't work.

        print_game(foundation, tableau, cell)

        response = input("Command (type 'h' for help): ")
        response = response.strip()
        response_list = response.split()

        if len(response_list) > 0:
            r = response_list[0]
            if r == "t2f":
                source, dest = get_cols("Tableau", "Foundation")
                # Check move
                if (
                    check_foundation_move(
                        tableau, foundation, tableau, cell, source, dest
                    )
                    == True
                ):
                    print("VALID")
                    tableau_to_foundation(foundation, tableau, cell, source, dest)
                else:
                    print("INVALID MOVE!")
                # Check win
                if check_winner(foundation) == True:
                    print("CONGRATS! YOU WIN!")
                    break

            elif r == "t2t":
                source, dest = get_cols("Tableau", "Tableau")
                tableau_to_tableau(foundation, tableau, cell, source, dest)
                # Check win
                if check_winner(foundation) == True:
                    print("CONGRATS! YOU WIN!")
                    break

            elif r == "t2c":
                source, dest = get_cols("Tableau", "Cell")
                tableau_to_cell(tableau, cell, source, dest)
                # Check win
                if check_winner(foundation) == True:
                    print("CONGRATS! YOU WIN!")
                    break

            elif r == "c2t":
                source, dest = get_cols("Cell", "Tableau")
                cell_to_tableau(foundation, tableau, cell, source, dest)
                # Check win
                if check_winner(foundation) == True:
                    print("CONGRATS! YOU WIN!")
                    break

            elif r == "c2f":
                source, dest = get_cols("Tableau", "Foundation")
                # Check move
                if (
                    check_foundation_move(
                        tableau, foundation, tableau, cell, source, dest
                    )
                    == True
                ):
                    print("VALID")
                    cell_to_foundation(foundation, tableau, cell, source, dest)
                else:
                    print("INVALID MOVE!")
                # Check win
                if check_winner(foundation) == True:
                    print("CONGRATS! YOU WIN!")
                    break

            elif r == "q":
                break

            elif r == "h":
                show_help()

            else:
                print("Unknown command:", r)

        else:
            print("Unknown Command:", response)

    print("Thanks for playing")


def start():
    """Startup function that initiates game."""
    foundation, tableau, cell = setup()
    play(foundation, tableau, cell)
    print_rules()
    show_help()


start()
