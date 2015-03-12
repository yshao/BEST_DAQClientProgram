import pandas as pd
from best.common.sqliteutils import *

df=pd.DataFrame(columns=ENC_COL)

print df

df.loc[0]=(["1" "2" "3" "4"])

rdf=pd.DataFrame(columns=RAD_COL)
db=DaqDB("daq.db")

# print rdf.read_sql_query("select * from rad",db.get_connection())




###
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# dataframe = pd.DataFrame({'Col': np.random.uniform(size=1000)})
# plt.scatter(dataframe.index, dataframe['Col'])

# plt.show()




rdf= pd.read_sql_query("select top 12 from rad",db.get_connection())




### rolling window ###
import pandas as pd
import numpy as np

# data = pd.DataFrame([
#     ['12/02/2007 23:23:00', 1443.75,  1444.00, 1443.75, 1444.00],
#     ['12/02/2007 23:25:00', 1444.00,  1444.00, 1444.00, 1444.00],
#     ['12/02/2007 23:26:00', 1444.25,  1444.25, 1444.25, 1444.25],
#     ['12/02/2007 23:27:00', 1444.25,  1444.25, 1444.25, 1444.25],
#     ['12/02/2007 23:28:00', 1444.25,  1444.25, 1444.25, 1444.25],
#     ['12/02/2007 23:29:00', 1444.25,  1444.25, 1444.00, 1444.00],
#     ['12/02/2007 23:30:00', 1444.25,  1444.25, 1444.00, 1444.00],
#     ['12/02/2007 23:31:00', 1444.25,  1444.25, 1443.75, 1444.00],
#     ['12/02/2007 23:32:00', 1444.00,  1444.00, 1443.75, 1443.75],
#     ['12/02/2007 23:33:00', 1444.00,  1444.00, 1443.50, 1443.50]
# ])

# window_size = 6
#
# # Prime the DataFrame using the date as the index
# result = pd.DataFrame(
#     [data.iloc[0:window_size, 1:].values.flatten()],
#     [data.iloc[window_size - 1, 0]])
#
# for t in data.iloc[window_size:, 1:].itertuples(index=True):
#     # drop the oldest values and append the new ones
#     new_features = result.tail(1).iloc[:, 4:].values.flatten()
#     new_features = np.append(new_features, list(t[1:]), 0)
#     # turn it into a DataFrame and append it to the ongoing result
#     new_df = pd.DataFrame([new_features], [t[0]])
#     result = result.append(new_df)


### try it on df ###
window_size = 4

result = pd.DataFrame(
    [rdf.iloc[0:window_size, 1:].values.flatten()],
    [rdf.iloc[window_size - 1, 0]])

for t in rdf.iloc[window_size:, 1:].itertuples(index=True):
    # drop the oldest values and append the new ones
    new_features = result.tail(1).iloc[:, 4:].values.flatten()
    new_features = np.append(new_features, list(t[1:]), 0)
    # turn it into a DataFrame and append it to the ongoing result
    new_df = pd.DataFrame([new_features], [t[0]])
    result = result.append(new_df)



plt.plot(rdf['counter'],rdf['ch1'],'b')
plt.plot(rdf['counter'],rdf['ch2'],'g')
plt.plot(rdf['counter'],rdf['ch3'],'r')
plt.plot(rdf['counter'],rdf['ch4'],'c')
plt.plot(rdf['counter'],rdf['ch5'],'m')
plt.plot(rdf['counter'],rdf['ch6'],'y')
plt.plot(rdf['counter'],rdf['ch7'],'k')
plt.plot(rdf['counter'],rdf['ch8'],'w')
plt.plot(rdf['counter'],rdf['ch9'],'b')
plt.plot(rdf['counter'],rdf['ch10'],'g')
plt.plot(rdf['counter'],rdf['ch11'],'r')
plt.plot(rdf['counter'],rdf['ch12'],'c')
plt.plot(rdf['counter'],rdf['ch13'],'m')
plt.plot(rdf['counter'],rdf['ch14'],'y')
plt.plot(rdf['counter'],rdf['ch15'],'k')
plt.plot(rdf['counter'],rdf['ch16'],'w')
plt.plot(rdf['counter'],rdf['ch17'],'b')
plt.plot(rdf['counter'],rdf['ch18'],'g')
plt.plot(rdf['counter'],rdf['ch19'],'r')
plt.plot(rdf['counter'],rdf['ch20'],'c')
plt.plot(rdf['counter'],rdf['ch21'],'m')
plt.plot(rdf['counter'],rdf['ch22'],'y')
plt.plot(rdf['counter'],rdf['ch23'],'k')
plt.plot(rdf['counter'],rdf['ch24'],'w')
# plt.plot(rdf.index,rdf['ch24'],'b',axes=False,xlab="",ylab="")
plt.show()
