from best.common.sqliteutils import DaqDB

db=DaqDB("../daq.db")
counter=db.load_pd_data("SELECT counter FROM rad")


counter=counter.interpolate()

counter.
