import pygame as pg
import os

class graphics_handler:

  def __init__(self, window, screen_surface):

    # load images here, use convert_alpha for images with transparent pixels
    self.board_image = pg.image.load('images/board.png').convert()
    self.red_cir_image = pg.image.load('images/redCircle.png').convert_alpha()
    self.black_cir_image = pg.image.load('images/blackCircle.png').convert_alpha()
    self.start_bg = pg.image.load("images/start_bg.png").convert()
    self.start_button = pg.image.load("images/start_button.png").convert_alpha()
    self.instructions = pg.image.load("images/instructions.png").convert()

    # start menu objects # 
    self.start_button_rect = pg.Rect(330, 380, 130, 60) # hitbox for start button

    # window and screen surface objects
    self.window = window
    self.main_screen_surface = screen_surface

    # variables
    self.offset = 70  # how much x and y padding to add to the circle images when placing them onto the screen
    self.button_size = 140

    # for animation of gameover text 
    self.gameover_text_vertical = 351
    self.travelling_down = False
    self.text = None

    # for upper bounce animation  
    self.upperbounce = False
    self.current_bounce = 100
    self.max_width = 0

    # for lower bounce animation 
    self.lowerbounce = False
    self.current_bounce_lower = 100
    self.max_width_lower = 0


  def display(self, board: list[list[str]]):
    """display the gameboard to the window, input the list representing the board"""

    # add background board to screen
    self.main_screen_surface.blit(self.board_image, (0, 0))

    # board size = 800x800 px
    # button size = 140x140 px
    # padding = 70x70 px

    # add pieces to box
    for y, row_list in enumerate(board): # y pos in list
      for x, char in enumerate(row_list): # x pos in list
        if char == "b":
          self.main_screen_surface.blit(self.black_cir_image,(x * self.button_size + self.offset, y * self.button_size + self.offset))
        elif char == "r":
          self.main_screen_surface.blit(self.red_cir_image,(x * self.button_size + self.offset, y * self.button_size + self.offset))
        elif char == "":
          pass
        else:
          pass

  
  def gameover(self, winner:str): 
    """Screen displayed when game is over, pass in the winner"""

    # fill screen with black
    self.main_screen_surface.fill((0,0,0))

    # label sizes:
    # 50 px vertical, 200(red)-250(black) px wide

    # for animation
    if self.gameover_text_vertical <= 350:
      self.travelling_down = True
      self.upperbounce = True
      self.max_width = 0
    elif self.gameover_text_vertical >= 400:
      self.travelling_down = False
      self.lowerbounce = True
      self.max_width_lower = 0

    if self.travelling_down:
      self.gameover_text_vertical += 0.05
    elif not self.travelling_down:
      self.gameover_text_vertical -= 0.05
    
    # color and borderwidth for bounce animation
    if winner == "red":
      color = (255,0,0)
      border_width = 0
    else:
      color = (255,255,255)
      border_width = 2

    # bounce animation
    if self.upperbounce:
      current_width = self.max_width/self.current_bounce
      self.max_width = 200
      bounce_variable = self.current_bounce / 400
      bounce_rect = pg.Rect(400 - current_width/2, 340, current_width, 10)
      pg.draw.rect(self.main_screen_surface, color, bounce_rect, border_radius=6, width=border_width)
      self.current_bounce -= bounce_variable
      if self.current_bounce < 1:
        self.upperbounce = False
        self.current_bounce = 100
    if self.lowerbounce:
      current_width_lower = self.max_width_lower/self.current_bounce_lower
      self.max_width_lower = 200
      bounce_variable_lower = self.current_bounce_lower / 400
      bounce_rect_lower = pg.Rect(400 - current_width_lower/2, 450, current_width_lower, 10)
      pg.draw.rect(self.main_screen_surface, color, bounce_rect_lower, border_radius=6, width=border_width)
      self.current_bounce_lower -= bounce_variable_lower
      if self.current_bounce_lower < 1:
        self.lowerbounce = False
        self.current_bounce_lower = 100


    # text
    if self.text == None:
      if winner == "red":
        self.text = pg.image.load(f"images/red_wins.png").convert()
      elif winner == "black": 
        self.text = pg.image.load(f"images/black_wins.png").convert() 

    if winner == "red":
      self.main_screen_surface.blit(self.text, (300,self.gameover_text_vertical))
    elif winner == "black":
      self.main_screen_surface.blit(self.text, (275,self.gameover_text_vertical))
      
  def start_menu(self, mouse_pos, mouse_pressed):
    """Displays the start screen, returns True when the start button is pressed"""

    self.main_screen_surface.blit(self.start_bg, (0,0)) # 800x800 px 
    self.main_screen_surface.blit(self.start_button, (330,380)) # 65x30 px

    if self.start_button_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
      return True
    
  def instructions_menu(self):
    self.main_screen_surface.blit(self.instructions, (0,0))

