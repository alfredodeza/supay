class MockSys(object):
    """Can grab messages sent to stdout or stderr"""
    def __init__(self):
        self.message = []

    def write(self, string):
        self.message.append(string)
        pass

    def captured(self):
        return ''.join(self.message)

