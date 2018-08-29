class BasePage():
    def __init__(self, driver, user):
        self.driver = driver
        self.user = user

    def authenticate_if_needed(self):
        if not self.user.is_authenticated:
            self.user.authenticate()
