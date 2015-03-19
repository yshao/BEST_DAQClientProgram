import os

__company__ = 'Boulder Environmental Sciences and Technology'
__project__ = ''
__author__ = 'Y. Shao'
__created__ = '3/17/2015' '1:46 PM'

PPATH=dict(
imu='/praco0/imu',
enc='/praco0/enc',
rad22='/praco0/rad22',
)

class PracoFileDriver():
    def start(self):
        ""

    def setup(self,opts):
        ""
        rate=5

    def decode_buffer(self):
        ""

    def add_file_index(self):
        ""
        ext=os.path.basename(f)[-3:]
        path=PPATH[ext]
        self.add(idx,)


def np_to_csv():
    ""

def csv_upload():
    ""


if __name__ == '__main__':
np_to_csv()
csv_upload()