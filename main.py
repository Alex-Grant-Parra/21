from random import randint

class cards:

    # Assigns the avaliable cards
    ALLCARDS = [str(num) for num in range (2, 11)] + ["J", "Q", "K", "A"]
    avaliableCards = ALLCARDS.copy()

    # Gets a random card from the avaliable, and returns it
    @staticmethod
    def randomCard():
        if not cards.avaliableCards:
            raise ValueError("No more cards available!")
        return cards.avaliableCards.pop(randint(0, len(cards.avaliableCards) - 1))

    def __init__(self):
        # Deals starting card out to each player
        self.deck = [cards.randomCard()]
        # Starting card cannot be repeated


    def drawCard(self):
        self.deck.append(cards.randomCard())


def gameloop(Players):
    # Check the game has the correct number of players
    if Players < 2: raise ValueError("Too few players to start the game! (2 <= Players <= 13)")
    elif Players > 13: raise ValueError("Too many players to start the game! (2 <= Players <= 13)")
        
    
    # Startup dealing
    player = [cards() for _ in range(Players)]










gameloop(2)