class RuleResult:
    name: str = ''
    error: str = ''
    resolution: str = ''

    def __init__(self, name: str, error: str, resolution: str):
        self.name = name
        self.error = error
        self.resolution = resolution
