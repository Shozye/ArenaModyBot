from Bot import Bot


class TestBot(Bot):
    def testAllFunctions(self):
        self.start_bot()
        self.login()
        self.update_status()
        self.make_emerald_action()
        self.update_status()
        self.make_emerald_action(hard=True)
