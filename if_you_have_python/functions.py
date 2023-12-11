# file for any standalone functions 
import pygame
import time

def exit_event_check():
    """Check if user clicked the (x) exit button, and what to do when they clicked it"""
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return True
        
def pause():
    """Pause program for 0.2 seconds"""
    time.sleep(0.2)
        