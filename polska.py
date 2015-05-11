__author__ = 'orps'

import re

class Stack():
	def __init__(self):
		self.stack = ['$']

	def push(self, element):
		self.stack.append(element)

	def pop(self):
		if self.isEmpty():
			raise NameError("stack is empty!")

		return self.stack.pop()

	def peak(self):
		return self.stack[-1]

	def isEmpty(self):
		return len(self.stack) < 2

def findBracketExpressionLength(expression, start):
	stack = ['(']
	pos = start
	while len(stack) > 0:
		pos = pos + 1
		if expression[pos] == '(':
			stack.append('(')
		if expression[pos] == ')':
			stack.pop()
	return pos - start + 1

priorities = {
	'0': 100,
	'1': 100,
	'other': 100,
	'*': 50,
	'.': 25,
	'+': 1,
	'$': -1
}

def getPrioritie(x):
	global priorities
	if x in priorities:
		return priorities[x]
	else:
		return priorities['other']


def transformToPolska(equation):
	stack = Stack()

	tmp = equation.split('=')[-1]

	regex_1 = r'([^()+.])([^*+.)])'
	regex_2 = r'([^(+.])([(])'

	tmp2 = tmp

	tmp = re.sub(regex_1, r'\1.\2', tmp)
	tmp = re.sub(regex_1, r'\1.\2', tmp)
	expression = re.sub(regex_2, r'\1.\2', tmp)

	pos = 0
	out = ''
	while len(expression) > pos:
		char = expression[pos]
		if char == '(':
			length = findBracketExpressionLength(expression, pos)
			bracketExpression = expression[pos+1:pos+length-1]

			out = out + transformToPolska(bracketExpression)
			pos = pos + length

			continue

		while getPrioritie(stack.peak()) >= getPrioritie(char):
			out = out + stack.pop()

		stack.push(char)
		pos = pos + 1

	while stack.isEmpty() is False:
		out = out + stack.pop()

	return out