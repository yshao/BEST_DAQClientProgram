import pandas as pd
import matplotlib.pyplot as plt
from common.sqliteutils import DaqDB

df=pd.DataFrame()
conn=DaqDB("../daq.db")
counter=conn.load_pd_data("SELECt counter FROM rad LIMIT 100")

enc=conn.load_pd_data("SELECt encoder_count FROM rad LIMIT 100")

print conn.__dict__.keys()

counter=counter.interpolate()

print counter

# counter = range(100)
ax1 = plt.subplot(1, 1, 1)
ax1.plot(counter, enc)
plt.title('Motor')
plt.xlabel('Counter')
plt.ylabel('Raw Encoder')


plt.show()