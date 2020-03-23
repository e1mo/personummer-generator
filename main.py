"""
Generate a valid number for the German Personalausweis
"""

import argparse
import datetime
import string
from random import randint, choice
from pandas import Timestamp

parser = argparse.ArgumentParser(description='Generate a valid number for the German Personalausweise')

parser.add_argument('--verbose', '-v', nargs='*', help='Verbose output')

parser.add_argument('--authority', '-a', help='Code for the authority')
parser.add_argument('--number', '-n', help='Running number')

parser.add_argument('--birth_date', '-b', help='The date of birth. Defaults to random over the age of 18. Is exclusive to the birth_year, birth_month and birth_day')
parser.add_argument('--birth_year', '-y', help='The year of birth.', type=int)
parser.add_argument('--birth_month', '-m', help='The month of birth.', type=int)
parser.add_argument('--birth_day', '-d', help='The day of birth.', type=int)

parser.add_argument('--expiry', '-e', help='Date of expiry. Defaults to random within 5 Years')

parser.add_argument('--nationality', help='Nationality, defaults to D', default='D')

args = parser.parse_args()

verbosity = 0

if args.verbose is not None:
	verbosity = 1

	if len(args.verbose) > 0:
		verbosity += len(args.verbose[0])

	print('Running with Verbosity {}'.format(verbosity))
	print('')


def randomCompliantString(length=9, letters = None):
	output = ""

	if letters is None:	
		letters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'C', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'T', 'V', 'W', 'X', 'Y', 'Z']
	
	if verbosity > 2:
		print('Letters used for random strings: "{}"'.format(letters))

	for i in range(length):
		output += choice(letters)
	
	# print(output)
	return(output)

def generateChecksum(text, weightSequence = [7,3,1]):
	if verbosity > 1:
		print('Generating checksum for "{}"'.format(text))

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
	
	if verbosity > 2:
		print('Using weights "{}"'.format(weightSequence))

	sum = 0
	sums = []
	i = 0

	for number in numbers:
		weight = weightSequence[i % len(weightSequence)]
		product = number * weight
		weights.append(weight)
		lastNumber = product
		sums.append(lastNumber)
		sum += lastNumber
		i += 1
	
		if verbosity > 2:
			print('{} * {} = {} => {}'.format(number, weight, product, lastNumber))

	if verbosity > 2:
		print(weights)
		print(sums)
		print(sum, sum % 10, str(sum % 10))

	return(sum % 10)


authority = args.authority
number = args.number
expiry = args.expiry
nationality = args.nationality
birth_date = args.birth_date
birth_year = args.birth_year
birth_month = args.birth_month
birth_day = args.birth_day
expiry = args.expiry

if authority is None:
	authority = randomCompliantString(4)

	if verbosity > 1:
		print('No authority given, random generated authority is "{}" '.format(authority))

if number is None:
	number = randomCompliantString(5)
	# number = str(randint(1, 99999)).zfill(5)

	if verbosity > 1:
		print('No number given, random generated number is "{}" '.format(number))

if birth_year is None and birth_date is None:
	year = Timestamp.today().year
	birth_year = year - randint(19, 99)
 
	if verbosity > 1:
		print('No birth_year and birth_date given, random generated birth_year is "{}" '.format(birth_year))
	
if birth_month is None and birth_date is None:
	birth_month = randint(1, 12)
 
	if verbosity > 1:
		print('No birth_month and birth_date given, random generated birth_month is "{}" '.format(birth_month))
	
if birth_day is None and birth_date is None:
	daysInMonth = Timestamp(1990, birth_month, 1).daysinmonth
	birth_day = randint(1, daysInMonth)
 
	if verbosity > 1:
		print('No birth_day and birth_date given, random generated birth_day is "{}" '.format(birth_day))

if birth_date is not None:
	birth_date_ts = Timestamp(birth_date)

	if verbosity > 1:
		print('birth_date given, birth_date is "{}" '.format(birth_date_ts))

else:
	birth_date_ts = Timestamp(year=birth_year, month=birth_month, day=birth_day)

	if verbosity > 1:
		print('Generated birth_date is "{}" '.format(birth_date_ts))


if expiry is not None:
	expiry_date_ts = Timestamp(expiry)

	if verbosity > 1:
		print('expiry_date given, expiry_date_ts is "{}" '.format(expiry_date_ts))

else:
	expiry_year = Timestamp.today().year + randint(1, 5)
	expiry_month = randint(1, 12)
	daysInMonth = Timestamp(1990, expiry_month, 1).daysinmonth
	expiry_day = randint(1, daysInMonth)
	expiry_date_ts = Timestamp(expiry_year, expiry_month, expiry_day)

	if verbosity > 1:
		print('no expiry_date given, generated expiry_date_ts is "{}" '.format(expiry_date_ts))

if verbosity > 1:
	print('')

if verbosity > 0:
	print('Authority is {}.'.format(authority))
	print('Number is {}'.format(number))
	print('Date of birth is {}'.format(birth_date_ts.date()))
	print('Date of expiry is {}'.format(expiry_date_ts.date()))
	print('Nationality is {}'.format(nationality))
	print('')

blocks = [
	authority + number,
	birth_date_ts.strftime('%y%m%d'),
	expiry_date_ts.strftime('%y%m%d'),
	nationality
]

#blocks = ['T220001293', '6408125', '2010315', 'D']

for i,block in enumerate(blocks):
	if len(block) > 3:
		blocks[i] += str(generateChecksum(block))


totalCode = ""

for block in blocks:
	if len(block) > 1:
		totalCode += block

totalChecksum = generateChecksum(totalCode)
totalCode += blocks[3]
totalCode += str(totalChecksum)
# print(totalCode, blocks)

print('IDD<<{}<<<<<<<<<<<<<<<<'.format(blocks[0]))
print('{}<{}<<<<<<<<<<<<<<{}'.format(blocks[1], blocks[2] + blocks[3], totalChecksum))



