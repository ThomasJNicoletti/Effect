# Last updated by Thomas J. Nicoletti on May 21, 2023

from itertools import combinations
import easygui
import math
import numpy as np
import pandas as pd

print('\nPlease attach your dataset using the pop-up file explorer.')

try:
	df = pd.read_csv(easygui.fileopenbox())
except:
	print('\nError #1: Your dataset was not uploaded. Please re-run this application and try again.')
	quit()

df.drop(axis = 1, columns = df.columns[0], inplace = True)
df.replace(r'^s*$', float('NaN'), inplace = True, regex = True)

if df.iloc[0, :].isna().sum() > 0:
	print('\nError #2: Please ensure there are no missing proportions in your dataset. Afterwards, re-run this application.')
	quit()

if df.shape[0] >= 3:
	print('\nError #3: Please ensure your dataset is formatted using the provided template. Afterwards, re-run this application.')
	quit()

choice = []

while choice != 'Yes' or choice != 'No':
	choice = input('\nIn addition to computing effect sizes, do you also need to compute confidence intervals?\n\n' + 
		'Please type only "Yes" or "No", and then press enter.\n\n')
	if choice == 'Yes' or choice == 'No':
		break

output = []

for a, b in combinations(list(df), 2):
	proportion1 = df.loc[0, a]
	proportion2 = df.loc[0, b]
	difference = np.arcsin(math.sqrt(proportion1)) - np.arcsin(math.sqrt(proportion2))
	effect_size = str(round(difference * 2, 2)).ljust(4, '0')

	if choice == 'Yes':

		if pd.isnull(df.loc[1, a]):
			print('\nError #4: Please ensure sample sizes were provided for all groups. Afterwards, re-run this application.')
			quit()
		else:
			n1 = df.loc[1, a]
			n2 = df.loc[1, b]
			standard_error = 1.960 * math.sqrt(((proportion1 * (1 - proportion1)) / n1) + (((proportion2 * (1 - proportion2)) / n2)))
			lower_bound = str(round((difference - standard_error) * 2, 2)).ljust(4, '0')
			upper_bound = str(round((difference + standard_error) * 2, 2)).ljust(4, '0')

	if difference * 2 < 0:
		effect_size = str(abs(round(difference * 2, 2))).ljust(4, '0')
		a, b = b, a
		proportion1, proportion2 = proportion2, proportion1

		if choice == 'Yes':
			lower_bound = str(-1 * (round((difference - standard_error) * 2, 2))).ljust(4, '0')
			upper_bound = str(-1 * (round((difference + standard_error) * 2, 2))).ljust(4, '0')
			lower_bound, upper_bound = upper_bound, lower_bound
			n1, n2 = n2, n1

	if abs(difference * 2) < 0.20:
		strength = 'Trivial'
	elif abs(difference * 2) < 0.50:
		strength = 'Small'
	elif abs(difference * 2) < 0.80:
		strength = 'Medium'
	else:
		strength = 'Large'

	if strength == 'Trivial':
		result = f'There was no meaningful difference in score between {a} and {b}.'
	elif choice == 'Yes':
		result = f'{a} had a meaningfully higher score than {b} [Cohen\'s h = {effect_size}, 95% Confidence Interval ({lower_bound}, {upper_bound})].'
	else:
		result = f'{a} had a meaningfully higher score than {b} (Cohen\'s h = {effect_size}).'

	if choice == 'Yes':
		output.append([a, proportion1, n1, b, proportion2, n2, strength, effect_size, lower_bound, upper_bound, result])
		output.sort(reverse = True, key = lambda x: x[7])
	else:
		output.append([a, proportion1, b, proportion2, strength, effect_size, result])
		output.sort(reverse = True, key = lambda x: x[5])

if choice == 'Yes':
	df = pd.DataFrame(output, columns = ['Group A', 'Group A - Proportion', 'Group A - Sample Size', 'Group B', 'Group B - Proportion', 'Group B - Sample Size', 
		'Effect Strength', 'Cohen\'s h', 'Lower Bound', 'Upper Bound', 'Summary'])
else:
	df = pd.DataFrame(output, columns = ['Group A', 'Group A - Proportion', 'Group B', 'Group B - Proportion', 'Effect Strength', 'Cohen\'s h', 'Summary'])

df.replace('nan0', '', inplace = True, regex = True)
df.to_csv('effect_size.csv', index = False)

print('\nThe output can be found in your source folder. Thank you for using this application, and have a great day!')