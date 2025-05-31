from random import randint, choice

class cards:

    #  Avaliable number cards
    SPECIALCARDS = {
        "J" : "11",
        # "Q" : 12,
        # "K" : 13,
        # "A" : 15,
    }
    ALLCARDS = [str(num) for num in range (2, 11)] + list(SPECIALCARDS)
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
    
    def drawCard(self, Hidden=False, card=None):
        if card is None:
            new_card = cards.randomCard()
        else:
            if card in cards.avaliableCards:
                new_card = card
                cards.avaliableCards.remove(str(card))
            else:
                return None

        self.deck.append(new_card)
        self.hiddenOrder.append(Hidden)  # This ensures order stays consistent

        # Ensure lengths always match
        while len(self.hiddenOrder) > len(self.deck):
            self.hiddenOrder.pop()



    def drawTrump(self):
        self.trumps.append(cards.randomTrump())

    def getTotalPlayerTotal(self):
        intDeck = []
        for card in self.deck:
            if card not in cards.SPECIALCARDS:
                intDeck.append(int(card))
            else:
                if card in cards.SPECIALCARDS:
                    intDeck.append(int(cards.SPECIALCARDS[card]))


        return sum(intDeck)

    def getVisiblePlayerTotal(player):
        intDeck = []
        for card in player.deck:
            if card not in cards.SPECIALCARDS:
                intDeck.append(int(card))
            else:
                if card in cards.SPECIALCARDS:
                    intDeck.append(int(cards.SPECIALCARDS[card]))
        
        hiddenOrder = player.hiddenOrder

        return sum(card for card, hidden in zip(intDeck, hiddenOrder) if not hidden)

    def playTrump(self, voidTrump, target = None):

        # Converts to dictionary if not already
        if str(type(voidTrump)) != "<class 'dict'>": trump = eval(voidTrump)
        else: trump = voidTrump

        # Checks if the trump card is really in the player's hand
        ensureTrumpInHand = False # Debug only
        if ensureTrumpInHand:
            if trump not in self.trumps:
                raise ValueError(f"{trump} is not in the player's hand, but was attempted to be played.")
                return
            
        # Trump card logic
        category = list(trump.keys()).pop()
        card = trump[category]
        
        def destroy():
            if target is not None and target.activeTrumps:
                removed = target.activeTrumps.pop()  # Remove last active trump
                category = list(removed.keys())[0]
                card = removed[category]




                if list(removed.keys())[0] == "Go for":
                    pass # Make it look at the last go for in the active trumps
                if category == "Bet":  # If it's a bet-related trump
                    if card == "bloodshed":
                        Game.currentBet += 1
                    else:
                        Game.currentBet -= int(card)
                elif list(removed.values())[0] == "bless":
                    pass # Nothing needs to happen, as bless is only counted when a person is knocked out.

        if category == "Draw": self.drawCard(card = card)

        elif category == "Go for": Game.currentGoal = int(card)

        elif category == "Bet":

            if card == "bloodshed":
                self.drawTrump
                Game.currentBet -= 1
            else:
                Game.currentBet = Game.currentBet + int(card)
                if Game.currentBet < 0:
                    Game.currentBet = 0

        elif category == "Token":

            if card == "bless":
                pass

            if card == "destroy":
                destroy()

            if card == "friendship":
                for p in Game.player:
                    p.drawTrump()
                    p.drawTrump()

            if card == "reincarnation":
                destroy()
                self.drawTrump()

        elif category == "Deck":

            if card == "hush":
                self.drawCard(Hidden = True)

            elif card == "perfectDraw":
                ideal = Game.currentGoal
                current = self.getPlayerTotal()
                difference = ideal - current

                avaliableCards = [cards.SPECIALCARDS[card] if card in cards.SPECIALCARDS else card for card in cards.avaliableCards]
                validCards = [int(card) for card in avaliableCards if int(card) <= difference]
                highestCard = str(max(validCards, default=None))
                
                reversedCards = {str(value): key for key, value in cards.SPECIALCARDS.items()}
                cardToAdd = reversedCards.get(highestCard, highestCard)
                
                self.drawCard(cardToAdd)
            
            elif card == "refresh":
                for c in range(0, len(self.deck)):
                    toReturn = self.deck.pop()
                    cards.avaliableCards.append(toReturn)
                self.drawCard()
                self.drawCard() 
                
            elif card == "remove":
                if len(target.deck) > 1:
                    toReturn = target.deck.pop()
                    cards.avaliableCards.append(toReturn)

            elif card == "return":
                if len(self.deck) > 1:
                    toReturn = self.deck.pop()
                    cards.avaliableCards.append(toReturn)

            elif card == "exchange":
                player1Card, player2Card = self.deck.pop(), target.deck.pop()
                self.deck.append(player2Card)
                target.deck.append(player1Card)

            elif card == "disservice":
                target.drawCard()

        
        

        if category in ["Go for", "Bet"] or card == "bless":
            self.activeTrumps.append(trump)

        if ensureTrumpInHand:
            self.trumps.remove(trump) 

    def getPlayerDeck(player):
        # Hides the areas that are suppost to be hidden before showing
        HIDDENIDENTIFIER = "XXX"

        deck = player.deck
        hiddenOrder = player.hiddenOrder
        return [HIDDENIDENTIFIER if hidden else card for card, hidden in zip(deck, hiddenOrder)]


    def __init__(self):
        self.deck, self.trumps, self.activeTrumps = [], [], []
        self.hiddenOrder = [True, False]

        # Deals starting items out to each player
        self.drawCard()
        self.drawCard()
        self.drawTrump()
        self.drawTrump()

class Game:
    
    currentBet = 1
    currentGoal = 21
    player = []

def gameloop(Players):

    # Check the game has the correct number of players

    if Players < 2: raise ValueError("Too few players to start the game! (2 <= Players <= 13)")
    elif Players > 13: raise ValueError("Too many players to start the game! (2 <= Players <= 13)")
        
    
    # Startup assignment
    g = Game()
    Game.player = [cards() for _ in range(Players)]


    Game.player[0].playTrump({"Deck" : "hush"})
    Game.player[0].drawCard()
    print(cards.getPlayerDeck(Game.player[0]))
    print(Game.player[0].hiddenOrder)
    print(cards.getVisiblePlayerTotal(Game.player[0]))
    




gameloop(2)