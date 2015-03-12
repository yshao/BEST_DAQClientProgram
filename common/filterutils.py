class MovingAverageFilter(object):
	"""Simple moving average filter"""
 
	@property
	def avg(self):
		"""Returns current moving average value"""
		return self.__avg
 
	def __init__(self, n = 8, initial_value = 0):
		"""Inits filter with window size n and initial value"""
		self.__n = n
		self.__buffer = [initial_value/n]*n
		self.__avg = initial_value
		self.__p = 0
 
	def __call__(self, value):
		"""Consumes next input value"""
		self.__avg -= self.__buffer[self.__p]
		self.__buffer[self.__p] = value/self.__n
		self.__avg += self.__buffer[self.__p]
		self.__p = (self.__p  + 1) % self.__n
		return self.__avg


class KalmanFilter(object):

    def __init__(self, process_variance, estimated_measurement_variance):
        self.process_variance = process_variance
        self.estimated_measurement_variance = estimated_measurement_variance
        self.posteri_estimate = 0.0
        self.posteri_error_estimate = 1.0

    def input_latest_noisy_measurement(self, measurement):
        priori_estimate = self.posteri_estimate
        priori_error_estimate = self.posteri_error_estimate + self.process_variance

        blending_factor = priori_error_estimate / (priori_error_estimate + self.estimated_measurement_variance)
        self.posteri_estimate = priori_estimate + blending_factor * (measurement - priori_estimate)
        self.posteri_error_estimate = (1 - blending_factor) * priori_error_estimate

    def get_latest_estimated_measurement(self):
        return self.posteri_estimate