"""
    Base abstract recorder class.
    Keeps track of menaces created and outcomes.
    Can have different classes based on what to store and where to store.
"""


class Recorder:
    def __init__(self, debug):
        self.debug = debug

    def record(self):
        pass

