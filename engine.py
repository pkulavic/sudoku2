import random
from square import Square

class SudokuBoard:
    def __init__(self):
        # initialize a blank array with 81 values
        # self.array will store the puzzle
        self.array = [Square() for _ in range(81)]

        # Clues, an array of ints, stores the indices of all the clues 
        # in the puzzle. These indices are randomly generated. 
        self.clues = []

        self.is_valid: bool= True
        self.solution = []
    
    houses = {
        1: (0, 1, 2, 9, 10, 11, 18, 19, 20),
        2: (3, 4, 5, 12, 13, 14, 21, 22, 23),
        3: (6, 7, 8, 15, 16, 17, 24, 25, 26),
        4: (27, 28, 29, 36, 37, 38, 45, 46, 47),
        5: (30, 31, 32, 39, 40, 41, 48, 49, 50),
        6: (33, 34, 35, 42, 43, 44, 51, 52, 53),
        7: (54, 55, 56, 63, 64, 65, 72, 73, 74),
        8: (57, 58, 59, 66, 67, 68, 75, 76, 77),
        9: (60, 61, 62, 69, 70, 71, 78, 79, 80)
    }

    def find_row(self, pos: int):
        """
        find_row returns the starting index of the row that 'pos' belongs to.
        E.g. find_row(17) returns 9 because index 17 is in the second row, 
        which begins at index 9. 
        """
        if pos < 0 or pos > 80:
            raise IndexError(f"{pos} is invalid.")
        return ( pos // 9 ) * 9

    def num_is_in_row(self, pos: int, num: int):
        """
        Returns True if 'num' is in the row that contains 'pos'.
        Returns False otherwise.
        """
        for i in range(self.find_row(pos), self.find_row(pos) + 9 ):
            if self.array[i] == num:
                return True
        return False

    def find_col(self, pos):
        """
        """
        return pos % 9
    
    def num_is_in_col(self, pos: int, num: int):
        """
        Returns True if 'num' is in the column that pos belongs to. 
        Returns False otherwise.
        """
        col = pos % 9
        for row in range(0, 9):
            if self.array[row * 9 + col ] == num:
                return True
        return False
    
    def num_is_in_house(self, pos: int, num: int):
        """
        Returns True if value 'num' is found in the house that index 'pos' 
        belongs to.
        Returns False otherwise.
        """
        house = self.find_house(pos)
        for i in self.houses[house]:
            if self.array[i] == num:
                return True
        return False
       
    def find_house(self, pos: int):
        """
        Returns the the house (1 - 9) that the index 
        pos belongs to. 
        """
        for h in self.houses:
            if pos in self.houses[h]:
                return h
        return -1 # if the position does not have a house ... so sad 

    def get_random_position(self):
        rand = random.randint(0, 80)
        while rand in self.clues:
            rand = random.randint(0, 80)
        self.clues.append(rand)
        return rand

    def get_random_value(self):
        return random.randint(1, 9)
    
    def num_is_in_col_row_or_house(self, pos: int, num: int):
        return self.num_is_in_col(pos, num) or self.num_is_in_row(pos, num) \
            or self.num_is_in_house(pos, num)

    def fill_random_cell(self):
        pos = self.get_random_position()
        value = self.get_random_value()
        while self.num_is_in_col_row_or_house(pos, value):
            value = self.get_random_value() # reassign 'value' from the outer scope
        self.array[pos].value = value
#Square ^

    def generate_clues(self, level: int):
        """
        The level of difficulty is represented by 'level', which equals 
        the number of clues generated. The more clues there are, the easier 
        the puzzle is to solve.
        """
        count = 0
        while count < level:
            self.fill_random_cell()
            count += 1

    def find_negaters(self, pos: int):
        negaters = set()

        # check the row
        row = self.find_row(pos)
        for c in range(row, row+9):
            if self.array[c] != 0:
                negaters.add(self.array[c].value)

        # check the column
        col = self.find_col(pos)
        for r in range(0, 9):
            if self.array[r * 9 + col] != 0:
                negaters.add(self.array[r * 9 + col].value)
                
        # check house
        house = self.find_house(pos)
        for h in self.houses[house]:
            if self.array[h] != 0:
                negaters.add(self.array[h].value)

        return negaters

    def find_candidates(self, pos) -> set:
        negaters: set = self.find_negaters(pos)
        return {1, 2, 3, 4, 5, 6, 7, 8, 9} - negaters


    def find_relevant_region(self, pos) -> set:
        # Set is used here beccause we do not want duplicates, and order 
        # does not matter.
        relevant_region = set()

        # add all row indices
        row = self.find_row(pos)
        for i in range(row, row+9):
            relevant_region.add(i)

        # add all column indices
        col = self.find_col(pos)
        for c in range(col, col+73, 9):
            relevant_region.add(c)

        # add all house indices
        house = self.find_house(pos)
        for h in self.houses[house]:
            relevant_region.add(h)

        return relevant_region

    
    def update_candidates_new(self, pos, val) -> None:
        """
        When a value is added to the board, the squares in its relevant region
        should be checked to see if the added value is a candidate. If it is,
        it should be removed as a candidate from that square.
        """
        rel = self.find_relevant_region(pos)
        for i in rel:
            # using set.discard removes the value if it is present, 
            # and does nothing if it is not. 
            self.array[i].candidates.discard(val)

    def update_candidates_removal(self, pos, val) -> None:
        rel = self.find_relevant_region(pos)
        for i in rel:
            if not self.val_is_in_relevant_region(i, val):
                self.array[i].candidates.add(val)

    def val_is_in_relevant_region(self, pos, val) -> bool:
        rel = self.find_relevant_region(pos)
        for i in rel:
            if self.array[i] == val:
                return True
        return False


    def generate_candidates(self) -> None:
        """
        This method finds candidates for each square and adds those 
        candidates to the square. It does not remove existing candidates
        from the squares, so it should be used only on a board with no 
        candidates.
        """
        for i in range(81):
            self.array[i].candidates |= self.find_candidates(i)

    def clear_candidates(self) -> None:
        for square in self.array:
            square.candidates.clear()

    def __str__(self):
        return str(self.array)

    def update_validity_insertion(self, pos: int, val:int):
        relevant_indices = self.find_relevant_region(pos)
        for i in relevant_indices:
            if self.array[i] == val:
                self.is_valid = False
                return False
        return True

    def update_validity_removal(self, pos):
        """Check the relevant region given by pos. If it was formerly invalid,
        update it if it is no longer invalid. Otherwise, deletion will never
        make a board invalid."""
        if not self.is_valid:
            if self.region_is_valid(pos):
                self.is_valid = True

    
    def region_is_valid(self, pos: int):
        """Check if the relevant region given by pos contains duplicates. 
        Return True if there are no duplicates. False otherwise."""
        relevant_indices = self.find_relevant_region(pos)
        relevant_indices.remove(pos)
        for i in relevant_indices:
            if self.array[i] == self.array[pos]:
                return False
        return True

    def fill_puzzle(self):
        self.recursively_fill(0)
        self.solution = self.array # is this a shallow or deep copy? shallow copy

    def recursively_fill(self, i):
        if i == 81:
            return self.array[80].value
        else:
            self.array[i].candidates.clear()
            candidates = list(self.find_candidates(i))
            if len(candidates) == 0:
                return 0
            else:
                self.array[i].value = candidates.pop(random.randint(0, len(candidates)-1))
            while self.recursively_fill(i+1) == 0:
                if len(candidates) == 0:
                    self.array[i].value = 0
                    return 0
                else:
                    self.array[i].value = candidates.pop(random.randint(0, len(candidates)-1))
            return self.array[i].value

    def test_filled_puzzle_is_valid(self):
        for i in range(81):
            if not self.region_is_valid(i):
                print("Puzzle invalid; problem at index", i)
                return
        print("Valid puzzle")

    def remove_clues(self, holes: int):
        """Remove the number of clues specified by holes."""
        # get the indices for removal
        indices = random.sample(range(81), holes)
        for i in indices:
            self.array[i].value = 0
    
    def set_clue_array(self):
        """To be called immediately after poking holes. 
        Zips through the array, adds the index of any non-zero value
        to the self.clues array."""
        for i in range(len(self.array)):
            if self.array[i] != 0:
                self.clues.append(i)
    
    def remove_value(self, pos):
        """Remove the value from the array by setting it to zero."""
        self.array[pos].value = 0
    
    def set_value(self, pos, val):
        """Set the value at the given position."""
        self.array[pos].value = val




