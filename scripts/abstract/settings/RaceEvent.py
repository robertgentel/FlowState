class RaceEvent:
    LAP = 0
    CHECKPOINT = 1
    def __init__(self, channel, timeStamp, type):
        self.channel = channel
        self.timeStamp = timeStamp
        self.eventType = eventType
