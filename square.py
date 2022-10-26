"""
A Square class to represent each square on the board.
A square must be able to store two things:
    1. Its value; 0 (blank) or an int [1, 9]
    2. The set of candidates. That is, the set of values that could 
        feasibly be placed in that square without causing a 
        duplicate in its row, column, or house. In other words, the set of
        integers from 1 to 9 minus the set of values found in the square's 
        relevant region. 

Def. relevant region:
    The row, column, and house that a square belongs to. 
"""

class Square:
    def __init__(self, value=0):
        self._value = value
        # the candidates will be stored in a python set to prohibit duplicates
        self.candidates = set()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if not isinstance(val, int):
            raise TypeError("Value must be an integer")
        if val < 0 or val > 9:
            raise ValueError("Value must be within [0, 9]")
        self._value = int(val)

    def __eq__(self, other):
        return other == self.value

    def __ne__(self, other):
        return other != self.value
    
    def __int__(self):
        return self.value




