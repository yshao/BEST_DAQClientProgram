### plot legends

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(np.random.randn(10,2), columns=['col1','col2'])
df['col3'] = np.arange(len(df))**2 * 100 + 100

plt.scatter(df.col1, df.col2, s=df.col3)

colors = np.where(df.col3 > 300, 'r', 'k')
plt.scatter(df.col1, df.col2, s=120, c=colors)

cond = df.col3 > 300
subset_a = df[cond].dropna()
subset_b = df[~cond].dropna()
plt.scatter(subset_a.col1, subset_a.col2, s=120, c='b', label='col3 > 300')
plt.scatter(subset_b.col1, subset_b.col2, s=60, c='r', label='col3 <= 300')
plt.legend()

df['subset'] = np.select([df.col3 < 150, df.col3 < 400, df.col3 < 600],
                         [0, 1, 2], -1)
for color, label in zip('bgrm', [0, 1, 2, -1]):
    subset = df[df.subset == label]
    plt.scatter(subset.col1, subset.col2, s=120, c=color, label=str(label))
plt.legend()



plt.show()