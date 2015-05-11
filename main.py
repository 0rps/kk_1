__author__ = 'orps'
import re
from polska import transformToPolska
from module_nka import NKA, makeNKA

gramma = [
	'S->0A|1S|e',
	'A->0B|1A',
	'B->0S|1B'
]

class Nonterminal:
	def __init__(self, rawstr=''):
		self.value = rawstr

	def __repr__(self):
		return self.value

	def __eq__(self, other):
		if self.isNone():
			return False
		return self.value == other.value

	def isNone(self):
		return self.value == ''

class Token:
	def __init__(self, rawstr):
		search = re.search('([A-Z])', rawstr)

		if search:
			self.nonterminal = Nonterminal(search.group(0))
			rawstr = rawstr.replace(self.nonterminal.value, '')
			if rawstr == 'e':
				rawstr = ''
		else:
			self.nonterminal = Nonterminal()

		self.expression = rawstr

	def isTerminals(self):
		return self.nonterminal.isNone()


	def replaceNonterminal(self, equation):
		if self.nonterminal == equation.head:
			return map(lambda x: Token(self.expression + str(x)), equation.tokens)
		return [self]

	def join(self, str):
		if self.expression == "e":
			self.expression = ''
		self.expression = str + self.expression

	def __repr__(self):
		return self.expression + (str(self.nonterminal) if self.isTerminals() is False else '')


class Equation:
	def __init__(self, rawstr):
		rawstr = rawstr.replace(' ', '')

		(head, tail) = rawstr.split('->')
		self.head = Nonterminal(head)
		self.tokens = map(lambda x: Token(x), tail.split('|'))

	def replaceNonterminal(self, equation):
		if equation == self:
			return None

		tokens = []
		for token in self.tokens:
			tokens = tokens + token.replaceNonterminal(equation)

		self.tokens = tokens

	def isFinal(self):
		for token in self.tokens:
			if token.isTerminals() is False:
				return False
		return True

	def trysolve(self):
		nonTerminalTokens = []
		terminalTokens = []

		for token in self.tokens:
			if token.nonterminal == self.head:
				nonTerminalTokens.append(token)
			else:
				terminalTokens.append(token)

		if len(nonTerminalTokens) == 0:
			return False

		if len(nonTerminalTokens) > 1:
			expression = '({0})*'
		else:
			expression = '{0}*'

		nonNullTokens = filter(lambda x: x.expression != '', nonTerminalTokens)
		if len(nonNullTokens) > 0:
			expression = expression.format('+'.join(map(lambda x: x.expression, nonNullTokens)))

			for token in terminalTokens:
				token.join(expression)

		self.tokens = terminalTokens

		return True


	def __repr__(self):
		return '{0}={1}'.format(
			self.head,
			reduce(
				lambda x,y: '{0}+{1}'.format(x, y),
				map(lambda x: str(x), self.tokens)
			)
		)

class EquationSystem:
	def __init__(self, rawEquations):
		self.equations = map(lambda x: Equation(x), rawEquations)

	def solve(self):
		print str(self)
		print
		flag = True
		for eq in self.equations:
			if eq.isFinal() is False:
				flag = False
				break

		if flag:
			return

		equation = None

		for i in self.equations:
			if i.trysolve():
				equation = i
				break

		print 'equation {0} is solved\n{1}\n\n'.format(equation.head, equation)

		for i in self.equations:
			i.replaceNonterminal(equation)

		print 'replacing:'

		return self.solve()

	def __repr__(self):
		return reduce(lambda x, y: '{0}\n{1}'.format(x, y), map(lambda x: str(x), self.equations))

system = EquationSystem(gramma)
system.solve()

for i in system.equations:
	if i.head.value == 'S':
		e = 'S=0*'
		#expression = transformToPolska(e)
		expression = transformToPolska(str(i))
		print expression
		break

nka = makeNKA(expression)
print nka.solve("0")