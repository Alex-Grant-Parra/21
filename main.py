from random import randint, choice

class cards:

    #  Avaliable number cards
    ALLCARDS = [str(num) for num in range (2, 11)] + ["J", "Q", "K", "A"]
    avaliableCards = ALLCARDS.copy()

    # Avaliable trump cards
    ALLTRUMPS = {
        "Draw" : [str(num) for num in range (2, 8)],
        "Go for" : ["17", "24", "27"],
        "Bet" : ["+1", "+2", "-1", "-2", "bloodshed"],
        "Token" : ["bless", "destroy", "friendship", "reincarnation"],
        "Deck" : ["hush", "perfectDraw", "refresh", "remove", "return", "exchange", "disservice"]
    }

    # Gets a random card from the avaliable, and returns it, then removes from avaliable cards
    @staticmethod
    def randomCard():
        if not cards.avaliableCards: raise ValueError("No more cards available!")
        else: return cards.avaliableCards.pop(randint(0, len(cards.avaliableCards) - 1))

    # Gets a random trump and returns it
    @staticmethod 
    def randomTrump():
        category = choice(list(cards.ALLTRUMPS.keys()))
        return choice(cards.ALLTRUMPS[category])
    
    def drawCard(self):
        self.deck.append(cards.randomCard())

    def drawTrump(self):
        self.trumps.append(cards.randomTrump())

    def __init__(self):
        self.deck, self.trumps = [], []

        # Deals starting items out to each player
        for i in range(0, 2):
            self.drawCard()
            self.drawTrump()



def gameloop(Players):
    # Check the game has the correct number of players

    if Players < 2: raise ValueError("Too few players to start the game! (2 <= Players <= 13)")
    elif Players > 13: raise ValueError("Too many players to start the game! (2 <= Players <= 13)")
        
    
    # Startup assignment
    player = [cards() for _ in range(Players)]
    currentBet = 1
    






gameloop(2)