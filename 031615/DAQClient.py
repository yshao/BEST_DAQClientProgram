class DAQClient(object):
    def __init__(self,config):
        ""
        config=Config("config.xml")
        enc_ip=config.get("IP_ENCODER")
        rad_ip=config.get("IP_RADIOMETER_22-30")
        arch_ip=config.get("IP_ARCHIVAL")
        host_dir=config.get("LOCAL_DIR")
        user=config.get("REMOTE_USER")
        password=config.get("REMOTE_PASSWORD")

        self.config=config
        self.enc=ComputerClient(enc_ip,host_dir,user,password)
        self.arch=ComputerClient(arch_ip,host_dir,user,password)
        self.rad1=ComputerClient(rad_ip,host_dir,user,password)

    def send_home(self):
        self.arch.send("STOP")
        self.arch.send("STOP")
        self.arch.send("HOME")

    def send_forward(self):
        self.arch.send("STOP")
        self.arch.send("STOP")
        self.arch.send("FORWARD")

    def send_stop(self):
        self.arch.send("STOP")

    def send_startdaq(self):
        self.arch.send("DAQENC")
        self.rad.send("DAQRAD")

        self.arch.sync()
        self.enc.sync()

    def send_stopdaq(self):
        self.arch.send("DAQENC_STOP")
        self.rad.send("DAQRAD_STOP")