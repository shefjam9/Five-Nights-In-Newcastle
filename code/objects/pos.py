class Pos:
    """Position class"""
    x: int
    y: int

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def to_tuple(self) -> tuple:
        """Return position as tuple"""
        return (self.x, self.y)
    
    def to_dict(self) -> dict:
        """Return position as dict"""
        return {"x": self.x, "y": self.y}