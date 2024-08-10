class StringBuilder:
    def __init__(self):
        self.pieces = []

    def append(self, piece: str):
        self.pieces.append(piece)

    def to_string(self) -> str:
        return "".join(self.pieces)

    def clear(self):
        self.pieces = []

    def size(self) -> int:
        return len(self.pieces)

    def is_empty(self) -> bool:
        return len(self.pieces) == 0
