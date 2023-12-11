from board import board_class
from functions import exit_event_check,pause
import pygame 
import time



def main(): 

  # initialize pygame module 
  pygame.init()
  
  # create window and screen surface, configuring settings 
  SCREENSIZE = (800,800)
  window = pygame.display
  screen_surface = window.set_mode(SCREENSIZE)  
  window.set_caption("Teeko")
  
  # set icon 
  error_color = '\033[93m'
  base_color = '\033[0m'
  try:
    window.set_icon(pygame.image.load("images/icon.png").convert_alpha())
  except FileNotFoundError:
    print(f"{error_color}\nERROR: Icon Image Not Found, Run in base directory or restore image file\n{base_color}")
  
  # variables
  winner = ''
  game_running = True
  gameover_screen = True
  start_menu_running = True
  instructions_running = True
  board_list = [
            ["","","","",""],
            ["","","","",""],
            ["","","","",""],
            ["","","","",""],
            ["","","","",""]]
  

  # initialize board that holds everything
  board_obj = board_class(board_list, window, screen_surface)
    
  # start menu
  while start_menu_running: 
    if exit_event_check():
      return 0
        
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    start_clicked = board_obj.graphics.start_menu(mouse_pos,mouse_pressed)

    if start_clicked:
      start_menu_running = False

    window.update()

  pause()
  
  # instructions menu
  while instructions_running:
    if exit_event_check():
      return 0

    mouse_pressed = pygame.mouse.get_pressed()
    board_obj.graphics.instructions_menu()

    if mouse_pressed[0]:
      instructions_running = False

    window.update()

  pause()

  # main gameloop 
  while game_running:
    if exit_event_check():
        return 0

    win = board_obj.check_win()
    if win != 0:
      if win == 1:
        game_running = False
        winner = "red"
      elif win == 2:
        game_running = False
        winner = "black"

    board_obj.graphics.display(board_obj.board_list, board_obj.turn)

    mouse_pressed = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    current_time = time.time()
    board_obj.check_for_clicks(mouse_pos, mouse_pressed, current_time)

    window.update() 

  # gameover screen
  while gameover_screen:
    if exit_event_check():
        return 0
    board_obj.graphics.gameover(winner)
    window.update()
    window.flip()

if __name__ == "__main__":
  main()