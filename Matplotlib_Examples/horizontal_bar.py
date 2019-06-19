# https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.barh.html
# https://glowingpython.blogspot.com/2014/02/terms-selection-with-chi-square.html

import os
import numpy as np
import matplotlib.pyplot as plt

x = [u'INFO', u'CUISINE', u'TYPE_OF_PLACE', u'DRINK', u'PLACE', u'MEAL_TIME', u'DISH', u'NEIGHBOURHOOD']
y = [160, 167, 137, 18, 120, 36, 155, 130]

fig, ax = plt.subplots()
width = 0.75 # the width of the bars


ind = np.arange(len(y))  # the x locations for the groups
ax.barh(ind, y, width, color="blue")
ax.set_yticks(ind+width/2)
ax.set_yticklabels(x, minor=False)

for i, v in enumerate(y):
    ax.text(v + 3, i + .25, str(v), color='blue', fontweight='bold')

plt.title('title')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
#plt.savefig(os.path.join('test.png'), dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures