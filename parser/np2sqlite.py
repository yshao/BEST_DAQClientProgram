import sqlite3
import numpy
 
# Array of 4 columns and 100 rows                                                                                                                                              
data = numpy.random.rand(100, 4)
 
# Create a sample database                                                                                                                                                     
conn = sqlite3.connect('sample.db')
cursor = conn.cursor()
 
# Create a new table with four columns                                                                                                                                         
cursor.execute('''create table data (field1 real, field2 real, field3 real, field4 real)''')
conn.commit()
 
# Insert the data array into the 'data' table                                                                                                                                  
cursor.executemany('''insert into data values (?, ?, ?, ?)''', map(tuple, data.tolist()))
conn.commit()
cursor.close()
conn.close()