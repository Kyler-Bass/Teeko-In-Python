import pygame
import math
import sys

class graphics_handler:
  def __init__(self, window, screen_surface):

    # load images here, use convert_alpha for images with transparent pixels
    error_color = '\033[93m'
    base_color = '\033[0m'
    try:
      self.board_image = pygame.image.load('images/board.png').convert()
      self.red_cir_image = pygame.image.load('images/redCircle.png').convert_alpha()
      self.black_cir_image = pygame.image.load('images/blackCircle.png').convert_alpha()
      self.start_bg = pygame.image.load("images/start_bg.png").convert()
      self.start_button = pygame.image.load("images/start_button.png").convert_alpha()
      self.instructions = pygame.image.load("images/instructions.png").convert()
      self.highlight_button = pygame.image.load("images/highlight.png").convert_alpha()
      self.black_turn = pygame.image.load("images/black_turn.png").convert_alpha()
      self.red_turn = pygame.image.load("images/red_turn.png").convert_alpha()
    except FileNotFoundError:
      print(f"{error_color}\nERROR: One or more Image Files Not Found, Run in base directory or restore image files\n{base_color}")
      sys.exit()

    # start menu button 
    self.start_button_rect = pygame.Rect(330, 380, 130, 60) # hitbox for start button

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

    # for bouncing border animation  
    self.upperbounce = False
    self.current_bounce = 100
    self.max_width = 0
    self.lowerbounce = False
    self.current_bounce_lower = 100
    self.max_width_lower = 0

    # for circle animation, starting degrees of the 24 points 
    self.points_degrees = [25,20,15,10,5,30,0,25,20,15,10,5,205,200,195,190,185,210,180,205,200,195,190,185]


  def display(self, board: list[list[str]], turn):
    """display the gameboard to the window, input the list representing the board"""

    # add background board to screen
    self.main_screen_surface.blit(self.board_image, (0, 0))

    # add turn indicator to screen
    if turn == "r":
      self.main_screen_surface.blit(self.red_turn, (720,50))
    elif turn == "b":
      self.main_screen_surface.blit(self.black_turn, (720,50))

    # add pieces to screen
    for y, row_list in enumerate(board): 
      for x, char in enumerate(row_list):
        if char == "b":
          self.main_screen_surface.blit(self.black_cir_image,(x * self.button_size + self.offset, y * self.button_size + self.offset))
        elif char == "r":
          self.main_screen_surface.blit(self.red_cir_image,(x * self.button_size + self.offset, y * self.button_size + self.offset))
        elif char == "h":
          self.main_screen_surface.blit(self.highlight_button,(x * self.button_size + self.offset, y * self.button_size + self.offset))

  def gameover(self, winner:str): 
    """Screen displayed when game is over, pass in the winner"""

    # color and borderwidth used for all animations 
    if winner == "red":
      color = (255,0,0)
      border_width = 0
    else:
      color = (255,255,255)
      border_width = 2

    # fill screen with black
    self.main_screen_surface.fill((0,0,0))

    # moving text animation
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

    if self.text == None:
      if winner == "red":
        self.text = pygame.image.load(f"images/red_wins.png").convert()
      elif winner == "black": 
        self.text = pygame.image.load(f"images/black_wins.png").convert() 

    if winner == "red":
      self.main_screen_surface.blit(self.text, (300,self.gameover_text_vertical))
    elif winner == "black":
      self.main_screen_surface.blit(self.text, (275,self.gameover_text_vertical))
    
    # bounce animation
    if self.upperbounce:
      current_width = self.max_width/self.current_bounce
      self.max_width = 200
      bounce_variable = self.current_bounce / 400
      bounce_rect = pygame.Rect(400 - current_width/2, 340, current_width, 10)
      pygame.draw.rect(self.main_screen_surface, color, bounce_rect, border_radius=6, width=border_width)
      self.current_bounce -= bounce_variable
      if self.current_bounce < 1:
        self.upperbounce = False
        self.current_bounce = 100
    if self.lowerbounce:
      current_width_lower = self.max_width_lower/self.current_bounce_lower
      self.max_width_lower = 200
      bounce_variable_lower = self.current_bounce_lower / 400
      bounce_rect_lower = pygame.Rect(400 - current_width_lower/2, 450, current_width_lower, 10)
      pygame.draw.rect(self.main_screen_surface, color, bounce_rect_lower, border_radius=6, width=border_width)
      self.current_bounce_lower -= bounce_variable_lower
      if self.current_bounce_lower < 1:
        self.lowerbounce = False
        self.current_bounce_lower = 100

    
    # circling shapes animation 
    points1,points2 = self.get_points()

    pygame.draw.polygon(self.main_screen_surface, color=color, points=points1, width=border_width)
    pygame.draw.polygon(self.main_screen_surface, color=color, points=points2, width=border_width)
      
  def start_menu(self, mouse_pos, mouse_pressed):
    """Displays the start screen, returns True when the start button is pressed"""

    # background and button 
    self.main_screen_surface.blit(self.start_bg, (0,0))  
    self.main_screen_surface.blit(self.start_button, (330,380)) 

    # click check
    if self.start_button_rect.collidepoint(mouse_pos) and mouse_pressed[0]:
      return True
    
  def instructions_menu(self):
    """Displays the instruction menu"""
    self.main_screen_surface.blit(self.instructions, (0,0))

  def get_points(self):
    """return the 24 points of the two shapes creating the circling animation around the winner text"""
    
    # radii
    inner_radius = 195
    middle_radius = 200
    outer_radius = 205

    # inner section of shape 1
    iX1,iY1 = math.cos(math.radians(self.points_degrees[0])) * inner_radius, math.sin(math.radians(self.points_degrees[0])) * inner_radius
    iX2,iY2 = math.cos(math.radians(self.points_degrees[1])) * inner_radius, math.sin(math.radians(self.points_degrees[1])) * inner_radius
    iX3,iY3 = math.cos(math.radians(self.points_degrees[2])) * inner_radius, math.sin(math.radians(self.points_degrees[2])) * inner_radius
    iX4,iY4 = math.cos(math.radians(self.points_degrees[3])) * inner_radius, math.sin(math.radians(self.points_degrees[3])) * inner_radius
    iX5,iY5 = math.cos(math.radians(self.points_degrees[4])) * inner_radius, math.sin(math.radians(self.points_degrees[4])) * inner_radius

    inner1 = [iX1 + 400,iY1 + 400]
    inner2 = [iX2 + 400,iY2 + 400]
    inner3 = [iX3 + 400,iY3 + 400]
    inner4 = [iX4 + 400,iY4 + 400]
    inner5 = [iX5 + 400,iY5 + 400]

    # middle section of shape 1
    mX1,mY1 = math.cos(math.radians(self.points_degrees[5])) * middle_radius, math.sin(math.radians(self.points_degrees[5])) * middle_radius
    mX2,mY2 = math.cos(math.radians(self.points_degrees[6])) * middle_radius, math.sin(math.radians(self.points_degrees[6])) * middle_radius

    middle1 = [mX1 + 400,mY1 + 400]
    middle2 = [mX2 + 400,mY2 + 400] 

    # outer section of shape 1
    oX1,oY1 = math.cos(math.radians(self.points_degrees[7])) * outer_radius, math.sin(math.radians(self.points_degrees[7])) * outer_radius
    oX2,oY2 = math.cos(math.radians(self.points_degrees[8])) * outer_radius, math.sin(math.radians(self.points_degrees[8])) * outer_radius
    oX3,oY3 = math.cos(math.radians(self.points_degrees[9])) * outer_radius, math.sin(math.radians(self.points_degrees[9])) * outer_radius
    oX4,oY4 = math.cos(math.radians(self.points_degrees[10])) * outer_radius, math.sin(math.radians(self.points_degrees[10])) * outer_radius
    oX5,oY5 = math.cos(math.radians(self.points_degrees[11])) * outer_radius, math.sin(math.radians(self.points_degrees[11])) * outer_radius

    outer1 = [oX1 + 400,oY1 + 400]
    outer2 = [oX2 + 400,oY2 + 400]
    outer3 = [oX3 + 400,oY3 + 400]
    outer4 = [oX4 + 400,oY4 + 400]
    outer5 = [oX5 + 400,oY5 + 400]

    # SHAPES SEPARATOR ------------------------------------------------------------------------------------------------------------------------------------

    # inner section of shape 2
    inner_radius = 195
    iX6,iY6 = math.cos(math.radians(self.points_degrees[12])) * inner_radius, math.sin(math.radians(self.points_degrees[12])) * inner_radius
    iX7,iY7 = math.cos(math.radians(self.points_degrees[13])) * inner_radius, math.sin(math.radians(self.points_degrees[13])) * inner_radius
    iX8,iY8 = math.cos(math.radians(self.points_degrees[14])) * inner_radius, math.sin(math.radians(self.points_degrees[14])) * inner_radius
    iX9,iY9 = math.cos(math.radians(self.points_degrees[15])) * inner_radius, math.sin(math.radians(self.points_degrees[15])) * inner_radius
    iX10,iY10 = math.cos(math.radians(self.points_degrees[16])) * inner_radius, math.sin(math.radians(self.points_degrees[16])) * inner_radius

    inner6 = [iX6 + 400,iY6 + 400]
    inner7 = [iX7 + 400,iY7 + 400]
    inner8 = [iX8 + 400,iY8 + 400]
    inner9 = [iX9 + 400,iY9 + 400]
    inner10 = [iX10 + 400,iY10 + 400]

    # middle section of shape 2
    middle_radius = 200
    mX3,mY3 = math.cos(math.radians(self.points_degrees[17])) * middle_radius, math.sin(math.radians(self.points_degrees[17])) * middle_radius
    mX4,mY4 = math.cos(math.radians(self.points_degrees[18])) * middle_radius, math.sin(math.radians(self.points_degrees[18])) * middle_radius

    middle3 = [mX3 + 400,mY3 + 400]
    middle4 = [mX4 + 400,mY4 + 400] 

    # outer section of shape 2
    outer_radius = 205
    oX6,oY6 = math.cos(math.radians(self.points_degrees[19])) * outer_radius, math.sin(math.radians(self.points_degrees[19])) * outer_radius
    oX7,oY7 = math.cos(math.radians(self.points_degrees[20])) * outer_radius, math.sin(math.radians(self.points_degrees[20])) * outer_radius
    oX8,oY8 = math.cos(math.radians(self.points_degrees[21])) * outer_radius, math.sin(math.radians(self.points_degrees[21])) * outer_radius
    oX9,oY9 = math.cos(math.radians(self.points_degrees[22])) * outer_radius, math.sin(math.radians(self.points_degrees[22])) * outer_radius
    oX10,oY10 = math.cos(math.radians(self.points_degrees[23])) * outer_radius, math.sin(math.radians(self.points_degrees[23])) * outer_radius

    outer6 = [oX6 + 400,oY6 + 400]
    outer7 = [oX7 + 400,oY7 + 400]
    outer8 = [oX8 + 400,oY8 + 400]
    outer9 = [oX9 + 400,oY9 + 400]
    outer10 = [oX10 + 400,oY10 + 400]


    # move the points around the circles 
    for i in range(24):
      self.points_degrees[i] += 0.1
      
    # specific return order for drawing the 2 shapes, can make any shapes
    return [middle2,inner5,inner4,outer3,inner2,inner1,middle1,outer1,outer2,inner3,outer4,outer5],[middle4,inner10,inner9,outer8,inner7,inner6,middle3,outer6,outer7,inner8,outer9,outer10]