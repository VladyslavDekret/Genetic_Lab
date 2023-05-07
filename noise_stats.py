class NoiseStats:
    def __init__(self):
        self.NI = None
        self.conv_to = None
        self.reproduction_stats = None

    def __str__(self):
        return "\nNI: " + str(self.NI) + "\nConv to: " + str(self.conv_to) + str(self.reproduction_stats)

    def as_dict(self):
        return {"NI": [self.NI], "Conv to": [self.conv_to], **self.reproduction_stats.as_dict()}
