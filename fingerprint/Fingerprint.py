class Fingerprint:
    def __init__(self, time_1: int, time_2: int, freq_1: int, freq_2: int, origin: str):
        self.time_difference = time_2 - time_1
        self.time_1 = time_1
        self.freq_1 = freq_1
        self.freq_2 = freq_2
        self.origin = origin
