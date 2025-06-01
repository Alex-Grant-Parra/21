from random import randint, choice
from ast import literal_eval


class CardManager:
    SPECIALCARDS = {
        "J": "11",
        # "Q": "12",
        # "K": "13",
        # "A": "15",
    }
    ALLCARDS = [str(num) for num in range(2, 11)] + list(SPECIALCARDS)
    avaliableCards = ALLCARDS.copy()

    ALLTRUMPS = {
        "Draw": [str(num) for num in range(2, 8)],
        "Go for": ["17", "24", "27"],
        "Bet": ["+1", "+2", "-1", "-2", "bloodshed"],
        "Token": ["bless", "destroy", "friendship", "reincarnation"],
        "Deck": ["hush", "perfectDraw", "refresh", "remove", "return", "exchange", "disservice"]
    }

    @staticmethod
    def randomCard():
        if not CardManager.avaliableCards:
            raise ValueError("No more cards available!")
        return CardManager.avaliableCards.pop(randint(0, len(CardManager.avaliableCards) - 1))

    @staticmethod
    def randomTrump():
        category = choice(list(CardManager.ALLTRUMPS.keys()))
        card = choice(CardManager.ALLTRUMPS[category])
        return {category: card}


class Player:
    checkTrumpInHand = False  # Toggle for debug

    def __init__(self):
        self.__deck = []
        self.__trumps = []
        self.__activeTrumps = []
        self.__hiddenOrder = []

        self.drawCard()
        self.drawCard()
        self.drawTrump()
        self.drawTrump()

    def __repr__(self):
        return f"Deck: {self.__deck}, Trumps: {self.__trumps}, ActiveTrumps: {self.__activeTrumps}"

    def drawCard(self, hidden=False, card=None):
        if card is None:
            new_card = CardManager.randomCard()
        else:
            if card in CardManager.avaliableCards:
                new_card = card
                CardManager.avaliableCards.remove(str(card))
            else:
                return None

        self.__deck.append(new_card)
        self.__hiddenOrder.append(hidden)

        while len(self.__hiddenOrder) > len(self.__deck):
            self.__hiddenOrder.pop()

    def drawTrump(self):
        self.__trumps.append(CardManager.randomTrump())

    def getDeckInternal(self):
        return self.__deck.copy()

    def getDeckExternal(self):
        HIDDENIDENTIFIER = "XXX"
        return [HIDDENIDENTIFIER if hidden else card for card, hidden in zip(self.__deck, self.__hiddenOrder)]

    def getTrumpsInternal(self):
        return self.__trumps.copy()

    def getActiveTrumps(self):
        return self.__activeTrumps.copy()

    def getPlayerTotalInternal(self):
        intDeck = []
        for card in self.__deck:
            if card not in CardManager.SPECIALCARDS:
                intDeck.append(int(card))
            else:
                intDeck.append(int(CardManager.SPECIALCARDS[card]))
        return sum(intDeck)

    def getPlayerTotalExternal(self):
        intDeck = []
        for card in self.__deck:
            if card not in CardManager.SPECIALCARDS:
                intDeck.append(int(card))
            else:
                intDeck.append(int(CardManager.SPECIALCARDS[card]))

        return sum(card for card, hidden in zip(intDeck, self.__hiddenOrder) if not hidden)

    def __playTrump(self, voidTrump, target=None):
        if str(type(voidTrump)) != "<class 'dict'>":
            trump = literal_eval(voidTrump)
        else:
            trump = voidTrump

        if Player.checkTrumpInHand:
            if trump not in self.__trumps:
                raise ValueError(f"{trump} is not in the player's hand, but was attempted to be played.")

        category = list(trump.keys())[0]
        card = trump[category]

        def destroy():
            if target is not None and target.__activeTrumps:
                removed = target.__activeTrumps.pop()
                cat = list(removed.keys())[0]
                c = removed[cat]
                if cat == "Go for":
                    pass
                if cat == "Bet":
                    if c == "bloodshed":
                        Game.currentBet += 1
                    else:
                        Game.currentBet -= int(c)
                elif c == "bless":
                    pass

        if category == "Draw":
            self.drawCard(card=card)

        elif category == "Go for":
            Game.currentGoal = int(card)

        elif category == "Bet":
            if card == "bloodshed":
                self.drawTrump()
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
                for p in Game.players:
                    p.drawTrump()
                    p.drawTrump()
            if card == "reincarnation":
                destroy()
                self.drawTrump()

        elif category == "Deck":
            if card == "hush":
                self.drawCard(hidden=True)
            elif card == "perfectDraw":
                ideal = Game.currentGoal
                current = self.getPlayerTotalInternal()
                difference = ideal - current

                avaliableCards = [CardManager.SPECIALCARDS.get(c, c) for c in CardManager.avaliableCards]
                validCards = [int(c) for c in avaliableCards if int(c) <= difference]
                highestCard = str(max(validCards, default=None))

                reversedCards = {str(value): key for key, value in CardManager.SPECIALCARDS.items()}
                cardToAdd = reversedCards.get(highestCard, highestCard)

                self.drawCard(cardToAdd)

            elif card == "refresh":
                for _ in range(len(self.__deck)):
                    toReturn = self.__deck.pop()
                    CardManager.avaliableCards.append(toReturn)
                self.drawCard()
                self.drawCard()

            elif card == "remove":
                if target and len(target.__deck) > 1:
                    toReturn = target.__deck.pop()
                    CardManager.avaliableCards.append(toReturn)

            elif card == "return":
                if len(self.__deck) > 1:
                    toReturn = self.__deck.pop()
                    CardManager.avaliableCards.append(toReturn)

            elif card == "exchange":
                if target:
                    player1Card, player2Card = self.__deck.pop(), target.__deck.pop()
                    self.__deck.append(player2Card)
                    target.__deck.append(player1Card)

            elif card == "disservice":
                if target:
                    target.drawCard()

        if category in ["Go for", "Bet"] or card == "bless":
            self.__activeTrumps.append(trump)

        if Player.checkTrumpInHand:
            self.__trumps.remove(trump)


class Game:
    currentBet = 1
    currentGoal = 21
    players = []
    currentPlayer = None

    @staticmethod
    def nextTurn():
        try:
            Game.currentPlayer = next(Game.__playerIterator)
        except StopIteration:
            Game.__playerIterator = iter(Game.players)
            Game.currentPlayer = next(Game.__playerIterator)

    @staticmethod
    def playTrumpCard(playerObj, trumpCardName, target=None):
        matchingTrump = None
        if Player.checkTrumpInHand:
            for trump in playerObj.getTrumpsInternal():
                category = list(trump.keys())[0]
                card = trump[category]
                if card == trumpCardName:
                    matchingTrump = trump
                    break
            if not matchingTrump:
                raise ValueError(f"Trump card '{trumpCardName}' not found in player's hand.")
        else:
            categoryFound = None
            for category, cards in CardManager.ALLTRUMPS.items():
                if trumpCardName in cards:
                    categoryFound = category
                    break
            if not categoryFound:
                raise ValueError(f"Trump card '{trumpCardName}' not recognized in any category.")
            matchingTrump = {categoryFound: trumpCardName}

        playerObj._Player__playTrump(matchingTrump, target)

    @staticmethod
    def gameLoop(playerConfig):
        totalPlayers = sum(playerConfig.values())

        if totalPlayers < 2:
            raise ValueError("Too few players to start the game! (2 <= Players <= 13)")
        elif totalPlayers > 13:
            raise ValueError("Too many players to start the game! (2 <= Players <= 13)")

        Game.players = []
        playerTypeMap = {
            "AIPlayer": AIPlayer,
            "RemoteHumanPlayer": RemoteHumanPlayer,
            "LocalHumanPlayer": LocalHumanPlayer
        }

        for playerTypeName, count in playerConfig.items():
            playerClass = playerTypeMap.get(playerTypeName)
            if not playerClass:
                raise ValueError(f"Unknown player type: {playerTypeName}")
            for _ in range(count):
                Game.players.append(playerClass())

        Game.__playerIterator = iter(Game.players)
        Game.nextTurn()

        # Your test snippet
        player = Game.players[0]
        target = Game.players[1]

        Game.playTrumpCard(player, "+1")
        Game.playTrumpCard(player, "+2")
        Game.playTrumpCard(player, "bloodshed")
        Game.playTrumpCard(player, "-1")
        Game.playTrumpCard(player, "-2")
        


        print(Game.currentBet)

class LocalHumanPlayer(Player):
    pass


class RemoteHumanPlayer(Player):
    pass


class AIPlayer(Player):
    pass


# Example usage to start the game loop with 2 players
Game.gameLoop({
    "LocalHumanPlayer": 1,
    "AIPlayer": 1
})
