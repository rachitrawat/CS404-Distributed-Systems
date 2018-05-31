import operator

with open("output2") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip().replace("\t", " ").split() for x in content]

dict = {}
for list in content:
    dict[list[0]] = int(list[1])

sorted_x = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)

# print([item[0] for item in sorted_x[:10]])

import matplotlib.pyplot as plt;

plt.rcdefaults()

import numpy as np
import matplotlib.pyplot as plt

word = tuple([item[0] for item in sorted_x[:50]])
y_pos = np.arange(len(word))
frequency = [item[1] for item in sorted_x[:50]]

plt.barh(y_pos, frequency, align='center', alpha=0.5)
plt.yticks(y_pos, word)
plt.xlabel('No of occurrences')
plt.title('Word Frequency')

plt.show()
