__author__ = 'orps'

from polska import Stack

count = 0

class TransitionTable():
	def __init__(self):
		self.table = {}

	def addTable(self, table):
		self.table.update(table.table)

	def addTransition(self, start, finish, char='e'):
		if start in self.table.keys():
			d = self.table[start]
			if char in d.keys():
				d[char].append(finish)
			else:
				d[char] = [finish]
		else:
			self.table[start] = {char: [finish]}

	def getTransitions(self, id, char):
		transitions = []
		if id in self.table.keys():
			t1 = self.table[id]
			if char in t1.keys():
				t2 = t1[char]
				transitions = map(lambda x: {'id': x, 'char': char}, t2)

		if char != 'e':
			transitions = transitions + self.getTransitions(id, 'e')

		return transitions

class NKA():

	def __init__(self, char):
		global count
		self.start = count
		self.finish = count + 1
		self.tlist = []
		self.expr = ''
		count = count + 2
		self.table = TransitionTable()
		self.table.addTransition(self.start, self.finish, char)

	def point(self, other):
		self.table.addTable(other.table)
		self.table.addTransition(self.finish, other.start)
		self.finish = other.finish

	def asterisk(self):
		global count

		finish = count
		count = count + 1

		self.table.addTransition(self.finish, self.start)
		self.table.addTransition(self.start, finish)
		self.table.addTransition(self.finish, finish)

		self.finish = finish

	def plus(self, other):
		global count

		start = count
		finish = count + 1
		count = count + 2

		self.table.addTable(other.table)
		self.table.addTransition(start, self.start)
		self.table.addTransition(start, other.start)
		self.table.addTransition(self.finish, finish)
		self.table.addTransition(other.finish, finish)

		self.start = start
		self.finish = finish

	def newTransition(self, id, curChar=None):

		list = {
			'id': id,
			#'prevId': prevId,
			'char': curChar,
			't': None
		}

		return list

	def rollback(self):
		if len(self.tlist) == 1:
			print "ERRRROROROROROROOROROR trying rollback list with one element"
			return

		element = self.tlist[-1]
		self.tlist = self.tlist[0:-1]
		if element['char'] != 'e':
			self.expr = element['char'] + self.expr

	def isLambdaCycle(self, id):
		for element in reversed(self.tlist):
			if element['id'] == id and element['char'] == 'e':
				return True

			if element['char'] != 'e':
				break

		return False

	def solve(self, _expression):
		self.expr = _expression
		self.tlist = [self.newTransition(self.start)]

		while True:
			# check if there is may be more transitions
			if len(self.tlist) == 1 \
					and self.tlist[0]['t'] is not None \
					and len(self.tlist[0]['t']) == 0:
				return False, []

			# check if there is end
			if self.expr == '' \
					and self.tlist[-1]['id'] == self.finish:
				return True, self.tlist

			# get possible transitions for last element
			if self.tlist[-1]['t'] is None:
				char = 'e'
				if len(self.expr) > 0:
					char = self.expr[0]
				self.tlist[-1]['t'] = self.table.getTransitions(self.tlist[-1]['id'], char)
				continue

			# rollback if there is no transitions from last state
			if len(self.tlist[-1]['t']) == 0:
				self.rollback()
				continue

			# transition
			t = self.tlist[-1]['t']
			self.tlist[-1]['t'] = t[:-1]
			vertex = t[-1]['id']
			char = t[-1]['char']

			if char == 'e' and self.isLambdaCycle(vertex):
				continue

			if char != 'e':
				self.expr = self.expr[1:]

			self.tlist.append(self.newTransition(vertex, char))

def makeNKA(expression):
	stack = Stack()

	for char in expression:
		if char == '.':
			b = stack.pop()
			a = stack.peak()
			a.point(b)
		elif char == '*':
			a = stack.peak()
			a.asterisk()
		elif char == '+':
			b = stack.pop()
			a = stack.peak()
			a.plus(b)
		else:
			nka = NKA(char)
			stack.push(nka)

	return stack.pop()