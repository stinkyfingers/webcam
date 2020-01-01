class StatusBar():
    def __init__(self, window):
        self.window = window
        self.status_bar = window.statusBar()

    def set(self, msg):
        self.status_bar.showMessage(msg)

    def clear(self):
        self.status_bar.clearMessage()
