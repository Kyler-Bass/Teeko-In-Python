from board import board_class
from functions import exit_event_check
import pygame as pg
import time



def main():

  # initialize pygame module 
  pg.init()
  
  # create window and screen surface 
  SCREENSIZE = (800,800)
  window = pg.display
  screen_surface = window.set_mode(SCREENSIZE)  
  window.set_caption("Teeko")
  icon = pg.image.load("images/icon.png").convert_alpha()
  window.set_icon(icon)
  
  # variables
  winner = ''
  gameRunning = True
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
            gameRunning = False
            gameover_screen = False
            start_menu_running = False
            instructions_running = False
        
        mouse_pos = pg.mouse.get_pos()
        mouse_pressed = pg.mouse.get_pressed()
        start_clicked = board_obj.graphics.start_menu(mouse_pos,mouse_pressed)

        if start_clicked:
           start_menu_running = False

        window.update()

  
  # prevents clicking the button in the same instant as the screen switches to the gameboard
  time.sleep(0.2)
  
  # instructions menu
  while instructions_running:
        if exit_event_check():
            gameRunning = False
            gameover_screen = False
            start_menu_running = False
            instructions_running = False

        mouse_pressed = pg.mouse.get_pressed()
        board_obj.graphics.instructions_menu()

        if mouse_pressed[0]:
            instructions_running = False

        window.update()


  # prevent accidental button clicking 
  time.sleep(0.2)


  # gameloop 
  while gameRunning:
    # check if user presses exit (x in top right)
    if exit_event_check():
        gameRunning = False
        gameover_screen = False

    # check if someone won here
    win = board_obj.check_win()
    if win != 0:
        if win == 1:
           gameRunning = False
           winner = "red"
        elif win == 2:
           gameRunning = False
           winner = "black"

    # display board to user 
    board_obj.graphics.display(board_obj.board_list)

    # check if the user clicked and grab the mouse position
    mouse_pressed = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()

    # check if a button was clicked on, and 
    current_time = time.time()
    board_obj.check_for_clicks(mouse_pos, mouse_pressed, current_time)

    # update the frame 
    window.update() 


  # gameover screen
  while gameover_screen:
    if exit_event_check():
        gameover_screen = False
    board_obj.graphics.gameover(winner)
    window.update()
    window.flip()



if __name__ == "__main__":
    main()