from engine import SudokuBoard

def main():
    level: int = 45
    b = SudokuBoard()
    b.fill_puzzle()
    b.test_filled_puzzle_is_valid()
    


if __name__ == "__main__":
    main()

