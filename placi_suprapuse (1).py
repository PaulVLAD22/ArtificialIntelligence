import logging
import re
import itertools as it
import threading
import sys

from heapq import heapify, heappop, heappush
from typing import List
from argparse import ArgumentParser
from copy import deepcopy
from time import time, ctime

def replaceInString(position: int, string: str, element: str) -> str:
	"""replaceInString

	Funcție ce va înlocui într-un șir de caractere elementul de pe o poziție dată cu un alt element.

	Args:
		position (int): poziția elementului care va fi înlocuit
		string (str): șirul de caractere
		element (str): elementul înlocuitor

	Returns:
		str: va întoarce string-ul care conține elementul înlocuit pe poziția dată
	"""
	return string[:position] + element + string[position + 1:]


class Plaque:
	"""Plaque

	Clasă ce reprezintă o placă dată în problemă. Se caracterizează prin poziție, litera care o identifică și lungime.
	"""
	column: int
	row: int
	letter: str
	length: int

	def __init__(self, row: int, column: int, letter: str, length: int):
		"""__init__
		Args:
			row (int): rândul pe care se află placa
			column (int): coloana pe care se află placa
			letter (str): litera prin care identificăm coloana
			length (int): lungimea coloanei
		"""
		self.row = row
		self.column = column
		self.letter = letter
		self.length = length

	def __str__(self):
		return f'Plaque: {["{} = {} ".format (key, val) for (key, val) in self.__dict__.items()]}'
	
	def __lt__(self, other):
		"""__lt__

		O placă poate fi comparată cu altă placă sau cu o bilă, comparându-se poziția celor două (mai întâi rândul, apoi coloana).

		Args:
			other (Plaque | Ball)

		Returns:
			bool: va întoarce True dacă self < other, False altfel.
		"""
		if self.row < other.row:
			return True
		elif self.row == other.row:
			if self.column < other.column:
				return True
		return False


class Ball:
	"""Ball

	Clasă ce reprezintă o bilă dată în problemă. Se caracterizează prin poziție. 
	"""
	column: int
	row: int

	def __init__(self, row: int, column: int):
		"""__init__
		Args:
			row (int): rândul pe care se află bila
			column (int): coloana pe care se află bila
		"""
		self.row = row
		self.column = column
	
	def __str__(self) -> str:
		return f'Ball: {["{} = {} ".format (key, val) for (key, val) in self.__dict__.items()]}'
	
	def __lt__(self, other) -> bool:
		"""__lt__

		O bilă poate fi comparată cu altă bilă sau cu o placă, comparându-se poziția celor două (mai întâi rândul, apoi coloana).

		Args:
			other (Plaque | Ball)

		Returns:
			bool: va întoarce True dacă self < other, False altfel.
		"""
		if self.row < other.row:
			return True
		elif self.row == other.row:
			if self.column < other.column:
				return True
		return False


class Node:
	def __init__(self, information: list, level: int, move_cost: int, additive_cost: int, heuristic_cost: int, parent):
		"""__init__

		Se inițializează un nod în graful soluției.

		Args:
			information (list): information[0] conține o matrice ce reprezintă vizualizarea configurației actuale, 
									iar următoarele elemente sunt elementele de tip Plaque și Ball din configurație.
			level (): [description]
			move_cost ([type]): [description]
			additive_cost ([type]): [description]
			heuristic_cost ([type]): [description]
			parent (Node | None): [description]
		"""
		self.information = information
		self.parent = parent
		self.level = level
		self.move_cost = move_cost
		self.additive_cost = additive_cost
		self.heuristic_cost = heuristic_cost
		self.last_move = None

	def getRoad(self) -> list:
		"""getRoad

		Alcătuiește drumul într-o listă pornind de la un nodul actual.

		Returns:
			List: drumul până la nodul actual.
		"""
		road = [self.information[0]]
		cost = [self.move_cost]
		node = self

		while node.parent is not None:
			road.insert(0, node.parent.information[0])
			cost.insert(0, node.parent.move_cost)
			node = node.parent
		return road, cost
		
	def showRoad(self) -> int:
		"""showRoad

		Afișează drumul și costul fiecărei mutări până la nodul actual și returnează lungimea acestuia.

		Returns:
			int: lungimea drumului
		"""
		road, cost = self.getRoad()
		total = 0

		print ('Prima mutare: ')
		for index, config in enumerate(road):
			print(f'{index})')
			for line in config:
				print (line)
			print(f'Cost mutare: {cost[index]}')
			total += cost[index]
			print()
		print (f'Costul total a fost {total}')
		return len(road)

	def isInRoad(self, information: list) -> bool:
		"""isInRoad

		Folosim această funcție pentru a verifica dacă un nod se află sau nu în drumul actual.

		Args:
			information (list): Informația despre care verificăm dacă se află în drum

		Returns:
			bool: True dacă informația se află în drum, False altfel.
		"""
		roadNode = self
		while roadNode is not None:
			if (roadNode.information[0] == information[0]):
				return True
			roadNode = roadNode.parent
		return False
		
	def __str__(self) -> str:
		ret = f'({self.move_cost}, {self.additive_cost}, {self.heuristic_cost}), {self.information[0]}'
		if self.parent is not None:
			return str(self.parent) + '\n' + ret
		else:
			return ret
	
	def __lt__(self, other) -> bool:
		"""__lt__

		Nodurile sunt comparate folosindu-se costul acestora.

		Args:
			other (Node)

		Returns:
			bool: va întoarce True dacă costul lui self < costul lui other, False altfel.
		"""
		return self.move_cost < other.move_cost

	def __eq__(self, other) -> bool:
		"""__eq__

		Două noduri sunt comparate folosindu-se doar matricea din information[0]

		Args:
			other (Node)

		Returns:
			[type]: dacă self și other au aceeași matrice a configurație se întoarce True, False altfel
		"""
		return self.information[0] == other.information[0]


class Graph:
	start: Node
	nsol: int

	def __init__(self, filename: str, nsol: int):
		"""__init__

		Se va citi fișierul de input și se va forma matricea de reprezentare și obiectele care sunt în configurație.

		Args:
			filename (str): fișierul de input
			nsol (int): numărul de soluții căutate
		"""

		self.nsol = nsol
		def splitInput(line):
			return [list(el) for _, el in it.groupby(line)]

		with open(filename, 'r') as file:
			content = [line.strip() for line in file.readlines()]

			self.start = [[]]
			for row, line in enumerate(content):
				self.start[0].append(line)
				column = 0
				for _, elem in enumerate(splitInput(line)):
					if elem[0].isalpha():
						self.start.append(Plaque(row, column, elem[0], len(elem)))
					elif elem[0] == '*':
						for add, ball in enumerate(elem):
							self.start.append(Ball(row, column + add))
					column += len(elem)
				print (line)

		for elem in self.start:
			print(elem)

	def testGoal(self, information: list) -> bool:
		"""testGoal

		Funcția verifică ca în configurația actuală să nu mai existe elemente de tipul Ball.

		Args:
			information (list): informația din nodul pe care-l testăm.

		Returns:
			bool: Returnează True dacă au dispărut toate bilele, False altfel.
		"""
		for elem in information[1:]:
			if type(elem) is Ball:
				return False
		return True

	def checkValidity(self, information: list) -> (list, bool):
		"""checkValidity

		Se verifică validitatea unei mutări (să nu rămână plăci în aer, să nu cadă bile mai mult de un spațiu). De asemenea, coborâm și bilele care sunt în aer.

		Args:
			information (list): informația din nodul pe care-l verificăm.

		Returns:
			(list, bool): Primul element este informația nouă, al doilea element este un bool ce determină dacă s-a mutat vreo bilă.
		"""
		rows = len(information[0])
		matrix = information[0]
		
		movedBall = False
		for index, elem in enumerate(information[1:]):
			if type(elem) is Ball:
				row = elem.row + 1
				while row < rows and matrix[row][elem.column] == '.':
					movedBall = True
					row += 1
				diff = row - elem.row
				if diff > 2:
					return False, False
				elif diff == 2:
					row -= 1
					matrix[elem.row] = matrix[elem.row][:elem.column] + '.' + matrix[elem.row][elem.column + 1:]
					if row == rows - 1:
						information[index + 1].row = row
						matrix[elem.row] = matrix[elem.row][:elem.column] + '.' + matrix[elem.row][elem.column + 1:]
						information = information[:index + 1] + information[index + 2:]
					else:
						information[index + 1].row = row
						matrix[elem.row] = matrix[elem.row][:elem.column] + '*' + matrix[elem.row][elem.column + 1:]
		for index, elem in enumerate(information[1:]):
			if type(elem) is Plaque:
				plaque = information[index]
				if elem.row != (rows - 1):
					isStable = False
					for length in range(elem.length):
						if matrix[elem.row + 1][elem.column + length] != '.':
							isStable = True
					if not isStable:
						return False, movedBall
	
		return information, movedBall

	def generateSuccesors(self, currentNode, heuristic_type = 'default') -> list:
		"""generateSuccesors

		Se generează o listă cu mutările succesoare ale unui nod dat. Se mută elementele din information folosindu-se clasele (indecșii de la 1 încolo...).
		După actualizarea matricei și a instanțelor claselor din information se crează un nod nou ce îl are ca părinte pe cel actual.
		Pentru optimizare nu se mută elemente decât dacă acestea au 

		Args:
			currentNode (Node): nodul căruia vrem să-i generăm succesorii
			heuristic_type (str, optional): euristica folosită, cea predefinită este 'default'.
		
		Returns:
			list: O listă cu succesorii nodului dat ca parametru.
		"""
		def canMoveRight(matrix, elem):
			"""canMoveRight

			Se verifică dacă un element poate fi mutat către dreapta dându-se matricea configurației și elementul în cauză.

			Args:
				matrix (matrix): matricea care descrie configurația actuală.
				elem (Plaque): elementul a cărui poziție se verifică

			Returns:
				bool | list: returnează o listă cu bilele mișcate de placă dacă elementul se poate mișca spre dreapta, False altfel.
			"""
			ballPos = []
			for index in range(elem.column + elem.length, len(matrix[elem.row])):
				if matrix[elem.row][index] == '.':
					return ballPos
				elif matrix[elem.row][index] == '*':
					ballPos.append(index)
				else:
					return False
			return False
		def canMoveLeft(matrix, elem):
			"""canMoveLeft

			Se verifică dacă un element poate fi mutat către stânga dându-se matricea configurației și elementul în cauză.

			Args:
				matrix (matrix): matricea care descrie configurația actuală.
				elem (Plaque): elementul a cărui poziție se verifică

			Returns:
				bool | list: returnează o listă cu bilele mișcate de placă dacă elementul se poate mișca spre stânga, False altfel.
			"""
			ballPos = []
			for index in range(elem.column - 1, -1, (-1)):
				if matrix[elem.row][index] == '.':
					return ballPos
				elif matrix[elem.row][index] == '*':
					ballPos.append(index)
				else:
					return False
			return False
		def getMinBall(information):
			"""getMinBall

			Se caută bila poziționată cel mai sus.

			Args:
				information (list): listă cu matricea configurației actuale și elementele.

			Returns:
				int: se întoarce poziția bilei poziționate cel mai sus.
			"""
			minimum = len(information[0]) - 1
			for elem in information[1:]:
				if type(elem) is Ball:
					if elem.row < minimum:
						minimum = elem.row
			return minimum

		succesorList = []
		information = currentNode.information
		matrix = information[0]
		minMove = max(getMinBall(information) - 1, 0)
		maxMove = min(max(minMove + len(information[0]) / 2, 2), len(information[0]) + 1)

		for index, elem in enumerate(information[1:]):
			if type(elem) is Plaque:
				if elem.row < minMove or elem.row > maxMove:
					continue
				if (ballPos := canMoveLeft(matrix, elem)) != False:
					informationCopy = deepcopy(information)
					matrixCopy = informationCopy[0]
					ballRef = []
					for jndex, ball in enumerate(information[1:]):
						if type(ball) is Ball and ball.row == elem.row and ball.column in ballPos:
							ballRef.append(jndex)
					matrixCopy[elem.row] = replaceInString(elem.column - 1, matrixCopy[elem.row], matrixCopy[elem.row][elem.column])
					matrixCopy[elem.row] = replaceInString(elem.column + elem.length - 1, matrixCopy[elem.row], '.')
					informationCopy[index + 1].column -= 1
					for jndex in range(len(ballRef)):
						matrixCopy[elem.row] = replaceInString(elem.column - 2 - jndex, matrixCopy[elem.row], '*')
					for jndex in ballRef:
						informationCopy[jndex + 1].column -= 1
					informationCopy, movedBall = self.checkValidity(informationCopy)
					if informationCopy != False and not currentNode.isInRoad(informationCopy):
						if movedBall:
							cost = 1
						elif len(ballPos):
							cost = 2 * (1 + elem.length)
						else:
							cost = 1 + elem.length
						succesorList.append(Node(informationCopy, currentNode.level + 1, cost, currentNode.additive_cost + cost, self.heuristicCost(informationCopy, heuristic_type), currentNode))

				if (ballPos := canMoveRight(matrix, elem)) != False:
					informationCopy = deepcopy(information)
					matrixCopy = informationCopy[0]
					ballRef = []
					for jndex, ball in enumerate(information[1:]):
						if type(ball) is Ball and ball.row == elem.row and ball.column in ballPos:
							ballRef.append(jndex)
					matrixCopy[elem.row] = replaceInString(elem.column + elem.length, matrixCopy[elem.row], matrixCopy[elem.row][elem.column])
					matrixCopy[elem.row] = replaceInString(elem.column, matrixCopy[elem.row], '.')
					informationCopy[index + 1].column += 1
					for jndex in range(len(ballRef)):
						matrixCopy[elem.row] = replaceInString(elem.column + elem.length + 1 + jndex, matrixCopy[elem.row], '*')
					for jndex in ballRef:
						informationCopy[jndex + 1].column += 1
					informationCopy, movedBall = self.checkValidity(informationCopy)
					if informationCopy != False and not currentNode.isInRoad(informationCopy):
						if movedBall:
							cost = 1
						elif len(ballPos):
							cost = 2 * (1 + elem.length)
						else:
							cost = 1 + elem.length
						succesorList.append(Node(informationCopy, currentNode.level + 1, cost, currentNode.additive_cost + cost, self.heuristicCost(informationCopy, heuristic_type), currentNode))

		return succesorList

	def heuristicCost(self, nodeInformation, heuristic_type = "default"):
		"""heuristicCost

		Args:
			nodeInformation (list): informația care se găsește în nod
			heuristic_type (str, optional): euristica folosită, cea predefinită e 'default'.

		Returns:
			int: valoarea euristicii selectate
		"""
		moves = 0
		
		'''
			Euristica 'ok', se bazează pe o sumă alcătuită din diferențele de nivel dintre nivelul final și nivelul pe care se află fiecare bilă.
			Euristica 'improved' ia în calcul și numărul minim de mutări necesare până la căderea unei bile (caută spații disponibile între piese).
			Euristica 'avoid', caută cea mai îndepărtată cale liberă pentru o bilă, și o înmulțește cu numărul de bile și de plăci pe care-l avem la momentul respectiv.
			Euristica 'default' este euristica banală.
		'''
		if heuristic_type == 'ok':
			level = len(nodeInformation[0]) - 1
			for elem in nodeInformation[1:]:
				if type(elem) is Ball:
					row = elem.row
					moves += abs(row - level)
			return moves
		elif heuristic_type == 'improved':
			for elem in nodeInformation[1:]:
				if type(elem) is Ball:
					column = elem.column
					possibleFalls = []
					row = elem.row + 1
					for index in range(len(nodeInformation[0][row])):
						if nodeInformation[0][row][index] == '.' or (index < len(nodeInformation[0][row]) - 1 and '.' not in [nodeInformation[0][row][index], nodeInformation[0][row][index + 1]] and nodeInformation[0][row][index] != nodeInformation[0][row][index + 1]):
							possibleFalls.append(abs(column - index))
					if len(possibleFalls) != 0:
						moves += min(possibleFalls)
			level = len(nodeInformation[0]) - 1
			for elem in nodeInformation[1:]:
				if type(elem) is Ball:
					row = elem.row
					moves += abs(row - level)
			return moves
		elif heuristic_type == 'avoid':
			balls = 0
			plaques = 0
			for elem in nodeInformation[1:]:
				if type(elem) is Ball:
					balls += 1
				elif type(elem) is Plaque:
					plaques += 1
			for elem in nodeInformation[1:]:
				if type(elem) is Ball:
					column = elem.column
					possibleFalls = []
					for index in range(len(nodeInformation[0][elem.row])):
						if nodeInformation[0][elem.row][index] == '.':
							possibleFalls.append(abs(column - index))
					if len(possibleFalls) != 0:
						moves += max(possibleFalls) * balls * plaques + 1
			return moves
		else:
			if self.testGoal(nodeInformation):
				return 0
			else:
				return 1

	def __str__(self):
		ret = ''
		for (k, v) in self.__dict__.items():
			ret += '{} = {}\n'.format(k, v)
		return ret

stats = [1, 1, 0] # maxNodes, totalNodes, solutionsGenerated

def uniform_cost(graph, nsol: int = 1, heuristic: str = 'default'):
	"""uniform_cost (UCS)

	Algoritmul UCS caută un drum folosind un heap ordonat după costul mutărilor.
	Args:
		graph (Graph): graful pe care aplicăm algoritmul
		nsol (int, optional): numărul soluțiilor, valoarea default este 1.
	"""
	global stats 
	queue = [(0, Node(graph.start, 1, 0, 0, 0, None))]

	while len(queue) > 0:
		stats[0] = max(stats[0], len(queue))
		_, currentNode = heappop(queue)
		if graph.testGoal(currentNode.information):
			print (f'Am găsit soluția {graph.nsol - nsol + 1}: {ctime(time())}')
			currentNode.showRoad()
			nsol -= 1
			stats[2] += 1
			if nsol == 0:
				return
			else:
				continue
		succesors = graph.generateSuccesors(currentNode)
		stats[1] += len(succesors)
		for succesor in succesors:
			heappush(queue, (succesor.additive_cost, succesor))

def a_star(graph, nsol: int = 1, heuristic: str = 'default'):
	"""a_star (A*)

	Algoritmul A* caută un drum folosind un heap ordonat folosindu-se euristică + cost. Pentru euristică + cost egale ordonăm descrescător după cost.
	Args:
		graph (Graph): graful pe care aplicăm algoritmul
		nsol (int, optional): numărul soluțiilor, valoarea default este 1.
		heuristic (str, optional): euristica folosită.
	"""
	global stats

	queue = [(0, 0, Node(graph.start, 1, 0, 0, graph.heuristicCost(graph.start, heuristic), None))]

	while len(queue) > 0:
		_, _, currentNode = heappop(queue)
		stats[0] = max(stats[0], len(queue))
		if graph.testGoal(currentNode.information):
			print (f'Am găsit soluția {graph.nsol - nsol + 1}: {ctime(time())}')
			currentNode.showRoad()
			nsol -= 1
			stats[2] += 1
			if nsol == 0:
				return
			else:
				continue
		succesors = graph.generateSuccesors(currentNode, heuristic)
		stats[1] += len(succesors)
		for succesor in succesors:
			heappush(queue, (succesor.heuristic_cost + succesor.additive_cost, - succesor.additive_cost, succesor))

def a_star_open_closed(graph, nsol: int = 1, heuristic: str = 'default'):
	"""a_star_open_closed (A* optimizat, cu listele open și closed)

	Algoritmul A* caută un drum folosind un heap ordonat folosindu-se euristică + cost. Pentru euristică + cost egale ordonăm descrescător după cost.
	Aici folosim open și closed pentru a nu expanda noduri în plus atunci când suntem sigur că ele nu ajung la soluție.
	Args:
		graph (Graph): graful pe care aplicăm algoritmul
		nsol (int, optional): numărul soluțiilor, valoarea default este 1.
		heuristic (str, optional): euristica folosită.
	"""
	global stats

	open =  [(0, 0, Node(graph.start, 1, 0, 0, graph.heuristicCost(graph.start, heuristic), None))]
	closed = []

	while len(open) > 0:
		stats[0] = max(stats[0], len(open) + len(closed))
		_, _, currentNode = heappop(open)
		heappush(closed, (currentNode.heuristic_cost + currentNode.additive_cost, currentNode.additive_cost, currentNode))

		if graph.testGoal(currentNode.information):
			print (f'Am găsit soluția {graph.nsol - nsol + 1}: {ctime(time())}')
			currentNode.showRoad()
			nsol -= 1
			stats[2] += 1
			if nsol == 0:
				return
			else:
				continue

		succesors = graph.generateSuccesors(currentNode, heuristic)
		stats[1] += len(succesors)
		for succesor in succesors:
			try:
				if index := [elem[2] for elem in open].index(succesor):
					openNode = open[index][2]
					if succesor.additive_cost + succesor.heuristic_cost < openNode.additive_cost + openNode.heuristic_cost:
						openNode.additive_cost = succesor.additive_cost
						openNode.heuristic_cost = succesor.heuristic_cost
						openNode.move_cost = succesor.move_cost
						openNode.parent = currentNode
						heapify(open)
			except ValueError:
				try:
					if index := [elem[2] for elem in closed].index(succesor):
						continue
						closedNode = closed[index][2]
						if succesor.additive_cost + succesor.heuristic_cost < openNode.additive_cost + openNode.heuristic_cost:
							closed = closed[:index] + closed[index + 1:]
							heappush(open, (succesor.heuristic_cost + succesor.additive_cost, succesor.additive_cost, succesor))
				except ValueError:
					heappush(open, (succesor.heuristic_cost + succesor.additive_cost, succesor.additive_cost, succesor))

def ida_star(graph, nsol: int = 1, heuristic: str = 'default'):
	startNode = Node(graph.start, 1, 0, 0, graph.heuristicCost(graph.start, heuristic), None)
	bound = startNode.additive_cost + startNode.heuristic_cost

	while True:
		nsol, rez = search(graph, startNode, bound, nsol, heuristic)
		if rez == True:
			break
		if rez == float('inf'):
			break
		bound = rez

def search(graph, currentNode, bound, nsol: int = 1, heuristic: str = 'default', maxNodesLast: int = 1):
	global stats

	if currentNode.additive_cost + currentNode.heuristic_cost > bound:
		return nsol, currentNode.additive_cost + currentNode.heuristic_cost

	if graph.testGoal(currentNode.information) and currentNode.additive_cost + currentNode.heuristic_cost == bound:
		print (f'Am găsit soluția {graph.nsol - nsol + 1}: {ctime(time())}')
		currentNode.showRoad()
		nsol -= 1
		stats[2] += 1
		if nsol == 0:
			return 0, True

	succesors = graph.generateSuccesors(currentNode, heuristic)
	stats[1] += len(succesors)
	stats[0] = max(stats[0], len(succesors) + maxNodesLast)
	minimum = float('inf')
	for succesor in succesors:
		nsol, rez = search(graph, succesor, bound, nsol, heuristic, stats[0])
		if rez == True:
			return 0, True
		if rez < minimum:
			minimum = rez
	return nsol, minimum

def main():
	parser = ArgumentParser(usage=__file__ + ' '
											 '[--input FIȘIER_INPUT] '
											 '[--output FIȘIER_OUTPUT] '
											 '[--nsol NUMĂR_SOLUȚII] '
											 '[--timeout TIMP_TIMEOUT] '
											 '[--algorithm ALGORITM]'
											 '[--euristic EURISTICĂ]'
											 '[--help]',				 
							description='Problema plăcilor suprapuse')

	parser.add_argument('-i', '--input',
						dest='input',
						default='input.txt',
						help='Fișierul de input',
						type=str)
						

	parser.add_argument('-o', '--output',
						dest='output',
						default=None,
						help='Fișierul de output',
						type=str)

	
	parser.add_argument('-n', '--nsol',
						dest='nsol',
						default='1',
						help='Numărul de soluții de calculat',
						type=int)

	parser.add_argument('-t', '--timeout',
						dest='timeout',
						default='32',
						help='Timpul de timeout',
						type=int)
	
	parser.add_argument('-a', '--algorithm',
						dest='alg',
						default='ucs',
						choices=['a-star', 'a-star-optimised', 'ida-star', 'ucs'],
						help='Algoritmul folosit pentru generarea soluțiilor',
						type=str)
	
	parser.add_argument('-e', '--euristic',
						dest='e',
						default='default',
						choices=['default', 'avoid', 'ok', 'improved'],
						help='Euristica folosită în cazul algoritmilor A-star',
						type=str)

	print (f'Start time: {ctime(time())}')

	args = vars(parser.parse_args())

	i_file = args['input']
	o_file = args['output']
	original_stdout = sys.stdout 
	graf = Graph(i_file, args['nsol'])

	if o_file != None:
		out = open(o_file, 'w', encoding='utf-8')
		sys.stdout = out

	if args['alg'] == 'a-star':
		target = a_star
	elif args['alg'] == 'a-star-optimised':
		target = a_star_open_closed
	elif args['alg'] == 'ida-star':
		target = ida_star
	elif args['alg'] == 'ucs':
		target = uniform_cost

	p = threading.Thread(target=target, args=(graf, args['nsol'], args['e']))
	p.start()
	p.join(args['timeout'])

	sys.stdout = original_stdout 

	if p.is_alive():
		print ('Timpul de timeout a expirat')
		sys.exit()

	print (f'Stop time: {ctime(time())}')
	print ('Statistici:')
	print (f'Am calculat în total {stats[1]} noduri.')
	print (f'Numărul maxim de noduri din memorie a fost {stats[0]}.')

	if (args['nsol'] - stats[2] != 0):
		print (f'Au rămas {args["nsol"] - stats[2]} soluții necalculate.')

if __name__ == '__main__':
	main()