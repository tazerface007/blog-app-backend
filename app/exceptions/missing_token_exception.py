class MissingTokenException(Exception):
    """
    Exception raised when GITHUB_TOKEN is missing.
    """
    def __init__(self, var_name, message="Environment variable is missing."):
        self.var_name = var_name
        self.message = f'{message}: {var_name}'
        super().__init__(self.message)


    