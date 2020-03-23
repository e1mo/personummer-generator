import string
from random import randint, choice

print(verbosity)

def randomCompliantString(length=9, letters = None):
	output = ""

	if letters is None:	
		letters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'C', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'T', 'V', 'W', 'X', 'Y', 'Z']

	for i in range(length):
		output += choice(letters)
	
	# print(output)
	return(output)

def generateChecksum(text, weightSequence = [7,3,1]):
	# print(text)
	numbers = []
	weights = []

	for letter in str(text).lower():
		if letter in string.digits:
			numbers.append(int(letter))
		else:
			numbers.append(string.ascii_lowercase.index(letter) + 10)

	# print(numbers)


	if weightSequence is None:
		weightSequence = [7,3,1]
	
	sum = 0
	sums = []
	i = 0

	for number in numbers:
		weight = weightSequence[i % len(weightSequence)]
		product = number * weight
		weights.append(weight)
		# lastNumber = product % 10
		lastNumber = product
		sums.append(lastNumber)
		sum += lastNumber
		# print('{} * {} = {} => {}'.format(number, weight, product, lastNumber))
		i += 1

	# print(weights)
	# print(sums)
	
	# print(sum, sum % 10, str(sum % 10))
	return(sum % 10)

