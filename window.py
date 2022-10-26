import pygame
from engine import SudokuBoard
import time
import math


class Dimensions:
    def __init__(self, size: int = 8) -> None:
        self.size_multiple = size
    
    # Window dimensions
    @property
    def window_width(self):
        return self.margin * 2 + self.grid_width + \
            self.grid_input + self.input_width
    @property
    def window_height(self):
        return self.menu_height + self.menu_main + \
            self.grid_height + self.grid_bottom

    # Grid dimensions
    @property
    def grid_width(self):
        return self.size_multiple * 81
    @property
    def grid_height(self):
        return self.grid_width
    # Grid position
    @property
    def grid_x(self):
        return self.margin
    @property
    def grid_y(self):
        return self.menu_height + self.menu_main
    @property
    def main_box_thickness(self):
        return self.thick
    
    # Input widget dimensions
    @property
    def input_width(self):
        return self.grid_width / 3
    @property
    def input_height(self):
        return self.grid_height / 3

    # House dimensions
    @property
    def house_width(self):
        return self.grid_width / 3
    @property
    def house_height(self):
        return self.grid_height / 3
    
    # Cell dimensions
    @property
    def cell_width(self):
        return self.grid_width / 9
    @property
    def cell_height(self):
        return self.grid_height / 9
    
    # Menu bar dimensions
    @property
    def menu_width(self):
        return self.window_width
    @property
    def menu_height(self):
        return self.cell_height * 2 / 3
    
    # Spacers
    @property
    def grid_input(self):
        """The space between the grid and the input widgets."""
        return self.cell_width / 2
    @property
    def menu_main(self):
        """The space between the menu bar and the rest of the widgets."""
        return self.cell_height / 4
    @property
    def grid_bottom(self):
        """The space between the grid bottom and the edge of window."""
        return self.cell_height / 2
    @property
    def margin(self):
        """The left-most and right-most white space."""
        return self.house_width / 2
    
    # Colors
    @property
    def black(self):
        return (0, 0, 0)
    @property
    def white(self):
        return (255, 255, 255)
    @property
    def light_gray(self):
        return (230, 230, 230)
    @property
    def gray(self):
        return (149, 149, 149)
    @property
    def yellow(self):
        return (255, 221, 9)
    @property
    def dark_yellow(self):
        return (230, 199, 7)
    
    # Widths 
    @property
    def thick(self):
        return 5
    @property
    def thin(self):
        return 1
    
    # Font
    @property
    def font(self):
        return 'georgia'
    @property
    def font_size(self):
        return 48
    @property
    def custom_font_path(self):
        return "font/FranklinDemi.ttf"
    @property
    def franklin_font_size(self):
        return 37
    @property
    def font_height(self):
        return math.floor(self.cell_height * 0.45)
    @property
    def font_width(self):
        return math.floor(self.cell_width * 0.32)
    
    def cell_coordinates(self, cell_number):
        """Return the coordinates of the left-top corner of a cell.
        Cells are numbered from zero to 80, starting at the top-left corner
        and moving left to right, row to row."""
        row = cell_number // 9
        y = self.grid_y + row * self.cell_height
        col = cell_number % 9
        x = self.grid_x + col * self.cell_width
        return x, y
    
    def cell_coordinates_center(self, cell_number):
        """Return the coordinates of the center of a cell, to the 
        nearest pixel."""
        x, y = self.cell_coordinates(cell_number)
        return x + self.cell_width // 2, y + self.cell_height // 2
    
    def cell_coordinates_number(self, cell_number):
        x, y = self.cell_coordinates(cell_number)
        return x + 25, y + 9
    

    @property
    def icon_path(self):
        return "images/IMG_3263.jpeg"



class Window:
    def __init__(self) -> None:
        self.dimensions = Dimensions()
        self.display = Display(self.dimensions.window_width, self.dimensions.window_height)
        self.display.fill_background_white()
        self.display.set_caption("Sudoku")
        # self.font = pygame.font.SysFont(self.dimensions.font, self.dimensions.font_size)
        self.font = pygame.font.Font(self.dimensions.custom_font_path, self.dimensions.franklin_font_size)
    
    def draw_grid(self):
        self.draw_main_box()
        self.draw_houses()
        self.draw_cells()
        
    def draw_main_box(self):
        self.display.draw_rectangle(
            x=self.dimensions.grid_x,
            y=self.dimensions.grid_y,
            width=self.dimensions.grid_width,
            height=self.dimensions.grid_height,
            color=(0, 0, 0),
            thickness=self.dimensions.main_box_thickness
        )
    
    def draw_houses(self):
        self.draw_house_lines_vertical()
        self.draw_house_lines_horizontal()

    def draw_house_lines_vertical(self):
        for n in range(1, 3):
            self.display.draw_vertical_line(
                start_x=self.dimensions.grid_x + n * self.dimensions.house_width,
                start_y=self.dimensions.grid_y + self.dimensions.main_box_thickness,
                length=self.dimensions.grid_height - 2 * self.dimensions.main_box_thickness - 1,
                color=self.dimensions.gray,
                thickness=self.dimensions.thick
            )
    
    def draw_house_lines_horizontal(self):
        for n in range(1, 3):
            self.display.draw_horizontal_line(
                start_x=self.dimensions.grid_x + self.dimensions.main_box_thickness,
                start_y=self.dimensions.grid_y + n * self.dimensions.house_height,
                length=self.dimensions.grid_height - 2 * self.dimensions.main_box_thickness - 1,
                color=self.dimensions.gray,
                thickness=self.dimensions.thick
            )
    
    def draw_cells(self):
        self.draw_cell_lines_vertical()
        self.draw_cell_lines_horizontal()
    
    def draw_cell_lines_vertical(self):
        for n in [i for i in range(1, 9) if i not in (3, 6)]:
            self.display.draw_vertical_line(
                start_x=self.dimensions.grid_x + n * self.dimensions.cell_width,
                start_y=self.dimensions.grid_y + self.dimensions.main_box_thickness,
                length=self.dimensions.grid_height - 2 * self.dimensions.main_box_thickness - 1,
                color=self.dimensions.gray,
                thickness=self.dimensions.thin
            )
    
    def draw_cell_lines_horizontal(self):
        for n in [i for i in range(1, 9) if i not in (3, 6)]:
            self.display.draw_horizontal_line( 
                start_x=self.dimensions.grid_x + self.dimensions.main_box_thickness,
                start_y=self.dimensions.grid_y + n * self.dimensions.cell_height,
                length=self.dimensions.grid_height - 2 * self.dimensions.main_box_thickness - 1,
                color=self.dimensions.gray,
                thickness=self.dimensions.thin
            )
    
    def draw_number(self, number, cell):
        number = self.font.render(str(number), True, self.dimensions.black)
        pygame.display.get_surface().blit(number, self.dimensions.cell_coordinates_number(cell))
    
    def color_cell(self, cell_number, color):
        x, y, = self.dimensions.cell_coordinates(cell_number)
        self.display.draw_rectangle(
            x=x,
            y=y,
            width=self.dimensions.cell_width,
            height=self.dimensions.cell_height,
            color=color,
            thickness=0
        )

    def highlight_cell(self, cell_number):
        self.color_cell(cell_number, self.dimensions.yellow )
    
    def erase_highlight(self, cell_number):
        self.color_cell(cell_number, self.dimensions.white)
    
    def make_cell_gray(self, cell_number):
        self.color_cell(cell_number, self.dimensions.light_gray)
    
    def highlight_clue_cell(self, cell_number):
        self.color_cell(cell_number, self.dimensions.dark_yellow)


class Display:
    """An interface for a PyGame display object."""
    def __init__(self, window_width, window_height) -> None:
        self.display = pygame.display.set_mode((window_width, window_height))
    
    def set_background(self, color):
        pygame.display.get_surface().fill(color)
    
    def fill_background_white(self):
        self.set_background((255, 255, 255))
    
    def set_caption(self, caption: str):
        pygame.display.set_caption(caption)
    
    def draw_rectangle(self, x, y, width, height, color, thickness):
        pygame.draw.rect(self.display, color, pygame.Rect(x, y, width, height), width=thickness)
    
    def draw_vertical_line(self, start_x, start_y, length, color, thickness):
        pygame.draw.line(
            surface=self.display, 
            color=color, 
            start_pos=(start_x, start_y),
            end_pos=(start_x, start_y + length),
            width=thickness
        )
    
    def draw_horizontal_line(self, start_x, start_y, length, color, thickness):
        pygame.draw.line(
            surface=self.display, 
            color=color, 
            start_pos=(start_x, start_y),
            end_pos=(start_x + length, start_y),
            width=thickness
        )



class Game:
    def __init__(self) -> None:
        self.highlighted_cell = 0
        self.directional_keys = [
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_RIGHT, 
            pygame.K_LEFT
        ]
        self.number_keys = [
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
            pygame.K_4,
            pygame.K_5,
            pygame.K_6,
            pygame.K_7,
            pygame.K_8,
            pygame.K_9,
        ]
        self.edit_keys = self.number_keys + [pygame.K_BACKSPACE]
        
    def setup(self):
        self.engine = SudokuBoard()
        self.engine.fill_puzzle()

        self.engine.test_filled_puzzle_is_valid()
        self.engine.remove_clues(50)
        self.engine.set_clue_array()

        pygame.init()
        self.window = Window()
        icon = pygame.image.load(self.window.dimensions.icon_path)
        self.draw()
        pygame.display.set_icon(icon)
        self.draw_exp()
    
    def run(self):
        self.setup()
        running = True
        self.draw()
        while running:
            # self.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    self.key_input(event.key)
                    # time.sleep(0.5)
            # self.check_pressed()
            pygame.display.update()
    
    def draw(self):
        self.window.display.fill_background_white()
        self.make_clues_gray()
        self.set_highlight()
        self.window.draw_grid()
        self.draw_numbers()
        
    def draw_numbers(self):
        for i in range(len(self.engine.array)):
            if self.engine.array[i] != 0:
                self.window.draw_number(self.engine.array[i].value, i)
    
    def make_clues_gray(self):
        for i in range(len(self.engine.array)):
            if i in self.engine.clues:
                if i == self.highlighted_cell:
                    self.window.highlight_clue_cell(i)
                else:
                    self.window.make_cell_gray(i)

    def draw_exp(self):
        self.window.highlight_cell(0)

    def check_pressed(self):
        keys = pygame.key.get_pressed()
        for key in self.directional_keys:
            if keys[key]:
                self.directional_input(key)

    def directional_input(self, direction):
        self.move_highlight(direction)
        pygame.display.update()

    def move_highlight(self, direction):
        if self.highlighted_cell % 9 == 0:
            if direction == pygame.K_LEFT:
                return
        if self.highlighted_cell // 9 == 0:
            if direction == pygame.K_UP:
                return
        if self.highlighted_cell % 9 == 8:
            if direction == pygame.K_RIGHT:
                return
        if self.highlighted_cell // 9 == 8:
            if direction == pygame.K_DOWN:
                return
        # self.window.erase_highlight(self.highlighted_cell)
        self.window.display.fill_background_white()
        if direction == pygame.K_UP:
            self.highlighted_cell -= 9
        if direction == pygame.K_DOWN:
            self.highlighted_cell += 9
        if direction == pygame.K_RIGHT:
            self.highlighted_cell += 1
        if direction == pygame.K_LEFT:
            self.highlighted_cell -= 1
        if self.highlighted_cell in self.engine.clues:
            self.window.highlight_clue_cell(self.highlighted_cell)
        else:
            self.window.highlight_cell(self.highlighted_cell)  
        self.draw()      

    def key_input(self, key):
        if self.is_directional(key):
            self.directional_input(key)
        if key in self.edit_keys:
            self.edit_input(key)
    
    def is_directional(self, key):
        return (
            key == pygame.K_UP or
            key == pygame.K_DOWN or
            key == pygame.K_RIGHT or
            key == pygame.K_LEFT
        )
    
    def edit_input(self, key):
        if key == pygame.K_BACKSPACE:
            self.remove_number()
        elif key in self.number_keys:
            self.add_number(key)

    def remove_number(self):
        if self.highlighted_cell not in self.engine.clues:
            self.engine.remove_value(self.highlighted_cell)
            self.draw()

    def add_number(self, key):
        if self.highlighted_cell not in self.engine.clues:
            for i in range(len(self.number_keys)):
                if key == self.number_keys[i]:
                    self.engine.set_value(self.highlighted_cell, i+1)
            self.draw()
    
    def set_highlight(self):
        if self.highlighted_cell in self.engine.clues:
            self.window.highlight_clue_cell(self.highlighted_cell)
        else:
            self.window.highlight_cell(self.highlighted_cell)  
    

            



