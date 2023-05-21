# More Meaningful Measurements: Effect Sizes and Confidence Intervals for Proportions using Python 📊

Last updated by Thomas J. Nicoletti on May 21, 2023

I would like to preface this document by stating this is my third published project using Python. Along my journey thus far, I  improved upon my understanding of Python and its endless capabilities; however, I still have a long road ahead of me as I continue to master the language. I strive to learn more and more with each project, and I hope this script provides some benefit to the greater social science community.

The purpose of this tool is to provide the user with both <ins>[effect sizes](https://en.wikipedia.org/wiki/effect_size)</ins> and optional <ins>[confidence intervals](https://en.wikipedia.org/wiki/confidence_interval)</ins> for an exhaustive set of boundless two-way group comparisons, where the data being compared are proportions on some variable (e.g., percent favorable scores on a given survey item). In psychology and related fields, there has been a movement towards the use of effect sizes either as the sole measure of meaningful differences or in conjunction with p-values yielded from tests of significance. For this tool, we focus on effect sizes for proportions, known as <ins>[Cohen's h](https://en.wikipedia.org/wiki/Cohen%27s_h)</ins>, and confidence intervals to guarantee robustness.

This tool will communicate with the user using simple inputs via the Command Prompt. Once all inputs are received, the analysis will run and deliver output to the source folder, including a summary column for quickly interpreting all two-way group comparisons. For accessibility, both an <ins>[example dataset](data.csv)</ins> and a <ins>[template](template.csv)</ins> are included in this repository as well.

## 💻 Installation and Preparation
Please note that all excerpts of code provided below are from the <ins>[effect_size.py](effect_size.py)</ins> script. As a self-taught programmer, I suggest reading through my comments here to gain insight into my programming decisions.

For this project, I used <ins>[Python 3.11](https://www.python.org/downloads/)</ins>, the Microsoft Windows operating system, and Microsoft Excel. As such, these components act as the prerequisites for utilizing this repository successfully without any additional troubleshooting. Going forward, please ensure everything you download or install for this project ends up in the correct location (e.g., the same source folder).

Use <ins>[pip](https://pip.pypa.io/en/stable/)</ins> to install relevant packages to the proper source folder using the Command Prompt and correct PATH. For example:

```bash
C:\Users\...
pip install numpy
pip install pandas
```

Please be sure to install each of the following packages: `easygui`, `itertools`, `math`, `numpy`, and `pandas`. If required, use the first section of the script to determine lacking dependencies, and proceed accordingly.

## 📑 Script Breakdown
The script begins by calling relevant libraries in Python, followed by asking the user to upload their dataset. If the user either escapes the process or uploads an incorrect file type (i.e., ".xlsx" instead of ".csv"), an error will be triggered.

```python
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
```

The following section cleans up the dataset by dropping the first column (i.e., row labels), as well as replacing empty cells with `NaN`. If values for group proportions are missing, or if there are more than two rows as designated in the template, an error will be triggered.

```python
df.drop(axis = 1, columns = df.columns[0], inplace = True)
df.replace(r'^s*$', float('NaN'), inplace = True, regex = True)

if df.iloc[0, :].isna().sum() > 0:
	print('\nError #2: Please ensure there are no missing proportions in your dataset. Afterwards, re-run this application.')
	quit()

if df.shape[0] >= 3:
	print('\nError #3: Please ensure your dataset is formatted using the provided template. Afterwards, re-run this application.')
	quit()
```

Assuming all goes smoothly up until this point, the next section asks the user whether they need confidence intervals computed as well. It will continue asking the user for their input if they do not type either "Yes" or "No".

```python
choice = []

while choice != 'Yes' or choice != 'No':
	choice = input('\nIn addition to computing effect sizes, do you also need to compute confidence intervals?\n\n' +
		'Please type only "Yes" or "No", and then press enter.\n\n')
	if choice == 'Yes' or choice == 'No':
		break
```

The next section is dedicated to the mathematics behind calculating both effect sizes and confidence intervals for proportions. Briefly, it starts by defining all possible two-way combinations of groups within the provided dataset. It also defines proportions and sample sizes for each group. The formula for Cohen's h is as follows:

###### h = 2 [ sin<sup>-1</sup> ( √ p<sub>1</sub> ) - sin<sup>-1</sup> ( √ p<sub>2</sub> ) ]
<br>
And for those curious about the minimum and maximum bounds of Cohen's h...

###### -3.14 <= h <= 3.14
<br>
This formula was recreated in Python within this section, and is used in bits and pieces frequently to determine not only Cohen's h, but also the lower and upper bounds of the confidence interval, assuming the user says "Yes" in the previous input. But first, when calculating the standard error, the critical z-score for a 95% confidence interval is used (i.e., 1.960). Assuming a "large enough" sample size, which is highly dependent on the greater research context, this will be satisfactory for most users. However, if the user knows their sample follows a different distribution, this value can be replaced within the script to ensure robustness.
<br><br>
The last part of this section swaps group labels and their respective proportions, (negative-transformed) bounds, and sample sizes. Essentially, this step takes the absolute values of both Cohen's h and its lower and upper bounds in a more complicated way to ensure confidence intervals that span zero are captured correctly. It then reorders all two-way group comparisons to ensure the first group is the higher scoring group, allowing for easier interpretation.

```python
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
```

The last section includes a step dedicated to defining the strength of the calculated effect sizes using Cohen's well-received thresholds (i.e., trivial, small, medium, or large). Depending on the strength and whether the user opted for confidence intervals, a different insight will be auto-generated with the appropriate information. The two-way group comparisons are then sorted in descending order using Cohen's h. This is helpful for users who need a quick view of which comparisons experienced the most meaningful differences. The <ins>[output](effect_size.csv)</ins> is then organized, artifacts are removed, and finally it is uploaded to the source folder.

```python
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
```

To run the script, use a batch file located in the source folder with only the following content:

```bash
python effect_size.py
PAUSE
```

This information should prove helpful in getting the user accustomed to what this script aims to achieve. If any additional information and / or explanations would prove beneficial, please reach out!

## 📋 Next Steps
One area of improvement would fall in the realm of optimizing the script and making it more "pythonic". Another opportunity would be adding user inputs for deciding which distribution critical values should be used. I am also quite interested in hearing feedback from users, including their field of practice, which variables they used for their analyses, and how satisfied they were with this tool overall.

## 💡 Community Contribution
Feedback, recommendations, and / or requests from anyone, especially new learners, are always appreciated. Please click <ins>[here](LICENSE.md)</ins> for information about the license for this project.

## ❔ Project Support
Please reach out if you plan on adapting the script to a project of your own interest. We can certainly collaborate if that would be helpful!

## 📚 Additional Resources
For easy-to-use text editing software, check out <ins>[Sublime Text](https://www.sublimetext.com/)</ins> for Python and <ins>[Visual Studio Code](https://code.visualstudio.com/)</ins> for Markdown.