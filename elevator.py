import itertools, random, sys

class Card:
	valueOrder = "A23456789\u2491JQK"

	def __init__(self, value, suit):
		self.value = value
		self.suit = suit

	def __str__(self):
		return self.value + self.suit

	def __lt__(self, other):
		if type(other) == list:
			other = other[0]
		return Card.valueOrder.index(self.value) < Card.valueOrder.index(other.value)

	def __le__(self, other):
		if type(other) == list:
			other = other[0]
		return Card.valueOrder.index(self.value) <= Card.valueOrder.index(other.value)

	def __eq__(self, other):
		if type(other) == list:
			other = other[0]
		return Card.valueOrder.index(self.value) == Card.valueOrder.index(other.value)

	def __ge__(self, other):
		if type(other) == list:
			other = other[0]
		return Card.valueOrder.index(self.value) >= Card.valueOrder.index(other.value)

	def __gt__(self, other):
		if type(other) == list:
			other = other[0]
		return Card.valueOrder.index(self.value) > Card.valueOrder.index(other.value)

	def adjacent(self, other):
		if type(other) == list:
			other = other[0]
		sep = abs( Card.valueOrder.index(self.value) - Card.valueOrder.index(other.value) )
		return sep == 1 or sep == 12

class Deck:
	def __init__(self, cardList = None):
		if cardList:
			self.cards = cardList
		else:
			self.cards = [Card(value, suit) for value in "A23456789\u2491JQK" for suit in "\u2660\u2665\u2666\u2663"]

	def __str__(self):
		return str(list(map(str, self.cards)))

	def __len__(self):
		return len(self.cards)

	def shuffle(self):
		random.shuffle(self.cards)

	def deal(self, n):
		toDeal = []
		for _ in range(n):
			toDeal.append(self.cards.pop())
		return toDeal

class Game:
	def __init__(self, players, handSize):
		self.players = players
		# Check that players and handSize are valid, if not execute default case
		if players not in range(2,5):
			print("Error: Illegal number of players. Players set to 2")
			self.players = 2
		if handSize not in range(2, 8):
			print("Error: Illegal hand size. Hand size set to 5")
			handSize = 5

		# Initalize all the variable
		self.draw = Deck()
		self.draw.shuffle()
		self.hands = [self.draw.deal(handSize) for _ in range(players)]
		self.faceUp = self.draw.deal(1)
		self.turn = 0
		self.drawCount = 0
		self.winner = -1

	def playCard(self, player, card):
		if (self.turn % self.players != player):
			print("Error: not this player's turn")
		if self.faceUp[0].adjacent(card):
			self.faceUp.insert(0, card)
			self.hands[player].remove(card)
			self.turn += 1
		else:
			print("Not a valid card played.")
			return
		if len(self.hands[player]) == 0:
			self.winner = player
		self.drawCount = 0

	def drawCard(self, player):
		self.hands[player].append(self.draw.deal(1)[0])
		if len(self.draw) == 0:
			self.draw = Deck(self.faceUp)
			self.draw.shuffle()
			self.faceUp = self.draw.deal(1)
		self.drawCount += 1
		if self.drawCount == self.players:
			self.flipCard()
		self.turn += 1

	def flipCard(self):
		self.drawCount = 0
		self.faceUp.insert(0, self.draw.deal(1)[0])

	def printHand(self, player):
		self.hands[player].sort()
		print("CARD:\t" + "\t".join(list(map(str, self.hands[player]))) \
			+ "\t  " + str(self.faceUp[0]) \
			+ "\t  " + str(len(self.draw)) + " cards")

		print("INDEX:\t" + "\t".join(list(map(str, range(1,len(self.hands[player])+1)))) \
			+ "\tFACEUP" + "\tDRAW PILE SIZE" + "\tTURN " + str(self.turn))

	def botMove(self, player):
		for c in self.hands[player]:
			if c.adjacent(self.faceUp[0]):
				self.playCard(player, c)
				print("BOT MOVE: PLAYED " + str(c) + f"\tCARDS LEFT: {len(self.hands[player])}")
				return
		self.drawCard(player)
		print(f"BOT MOVE: DREW\t\tCARDS LEFT: {len(self.hands[player])}")

def playGame():
	print(chr(27) + "[2J")
	p_count = int(input("Enter player count [2,4]: "))
	h_size = int(input("Enter starting hand size [2,7]: "))
	print(chr(27) + "[2J")
	g = Game(p_count, h_size)
	while g.winner == -1:
		if g.turn % g.players == 0:
			g.printHand(0)
			raw_command = input(f"Enter move. Options: PLAY [INDEX], DRAW. ")
			commands = list(map(lambda s: s.upper(), raw_command.split()))
			if len(commands):
				if commands[0] == "DRAW":
					g.drawCard(0)
				elif commands[0] == "PLAY" and len(commands) == 2 and int(commands[1]) in range(len(g.hands[0])+1):
					g.playCard(0, g.hands[0][int(commands[1])-1])
				print(chr(27) + "[2J")
		else:
			g.botMove(g.turn % g.players)
	print("Player " + str(g.winner) + " WINS!")


if __name__ == "__main__":
	playGame()
