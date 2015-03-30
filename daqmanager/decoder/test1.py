import sqlite3
import numpy as np
import io

def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    # http://stackoverflow.com/a/3425465/190597 (R. Hill)
    return buffer(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


# Converts np.array to TEXT when inserting
sqlite3.register_adapter(np.ndarray, adapt_array)

# Converts TEXT to np.array when selecting
sqlite3.register_converter("array", convert_array)

x = np.arange(12).reshape(2,6)

print x

con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()
cur.execute("create table test (arr array)")

cur.execute("insert into test (arr) values (?)", (x, ))

cur.execute("select arr from test")
data = cur.fetchone()[0]

print(data)
# print(data)
# [[ 0  1  2  3  4  5]
#  [ 6  7  8  9 10 11]]
# print(type(data))
# <type 'numpy.ndarray'>