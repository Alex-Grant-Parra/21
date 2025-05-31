from random import randint, choice

class cards:

    #  Avaliable number cards
    SPECIALCARDS = ["J", "Q", "K", "A"] # Full card deck for testing
    SPECIALCARDS = ["J"] # Only jack for real games
    ALLCARDS = [str(num) for num in range (2, 11)] + SPECIALCARDS
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
        card = choice(cards.ALLTRUMPS[category])
        return {category : card}
    
    def drawCard(self, card = 0):
        if card == 0:
            self.deck.append(cards.randomCard())
        else:
            if card in cards.avaliableCards:
                self.deck.append(card)
                cards.avaliableCards.remove(str(card))
            else:
                return -1

    def drawTrump(self):
        self.trumps.append(cards.randomTrump())

    def getPlayerTotal(self):
        intDeck = []
        for card in self.deck:
            if card not in cards.SPECIALCARDS:
                intDeck.append(int(card))
            else:
                if card == "J": intDeck.append(11)
                elif card == "Q": intDeck.append(12)
                elif card == "K": intDeck.append(13)
                elif card == "A": intDeck.append(15)

        return sum(intDeck)

    def playTrump(self, voidTrump):

        # Converts to dictionary if not already
        if str(type(voidTrump)) != "<class 'dict'>": trump = eval(voidTrump)
        else: trump = voidTrump

        # Checks if the trump card is really in the player's hand
        if trump not in self.trumps:
            raise ValueError(f"{trump} is not in the player's hand, but was attempted to be played.")
            return
            
        # Trump card logic
        category = list(trump.keys()).pop()
        card = trump[category]
        
        if category == "Draw": self.drawCard(card)
        elif category == "Go for": Game.currentGoal = int(card)
        elif category == "Bet": pass
        elif category == "Token": pass
        elif category == "Deck": pass
        
        self.trumps.remove(trump)


        

        
        



    def __init__(self):
        self.deck, self.trumps = [], []

        # Deals starting items out to each player
        self.drawCard()
        self.drawCard()
        self.drawTrump()
        self.drawTrump()

    
class Game:
    
    currentBet = 1
    currentGoal = 21

def gameloop(Players):

    # Check the game has the correct number of players

    if Players < 2: raise ValueError("Too few players to start the game! (2 <= Players <= 13)")
    elif Players > 13: raise ValueError("Too many players to start the game! (2 <= Players <= 13)")
        
    
    # Startup assignment
    game = Game()
    player = [cards() for _ in range(Players)]

    # player[0].playTrump(player[0].trumps[0])

    print(game.currentGoal)
    print(player[0].trumps)
    player[0].playTrump(player[0].trumps[0])
    
    print(game.currentGoal)
    print(player[0].trumps)









gameloop(2)