import vincent
import pandas as pd
import pandas.io.data as web

#All of the following import code comes from Python for Data Analysis
all_data = {}

for ticker in ['AAPL', 'GOOG']:
    all_data[ticker] = web.get_data_yahoo(ticker, '1/1/2010', '1/1/2013')

price = pd.DataFrame({tic: data['Adj Close']
                      for tic, data in all_data.iteritems()})

#Create line graph, with monthly plotting on the axes
line = vincent.Line()
line.tabular_data(price, columns=['AAPL'], axis_time='month')
# line.to_json(path)

#Play with the axes labels a bit
line + ({'labels': {'angle': {'value': 25}}}, 'axes', 0, 'properties')
line + ({'value': 22}, 'axes', 0, 'properties', 'labels', 'dx')
line.update_vis(width=800, height=300)
line.axis_label(y_label='AAPL Price', title='AAPL Stock Price 1/1/2010-1/1/2013')
line.update_vis(padding={'bottom': 50, 'left': 60, 'right': 30, 'top': 30})
# line.to_json(path)