import pygame


class button_class:
    def __init__(self, pos:list[int], state:str):
        # button variables
        self.pos = pos # [row,col]
        self.state = state # "r", "b", or ""
        self.last_click = 0 # last time this button was clicked, used for preventing multiple clicks being registered per time the user clicks 

        # button rectangle representing the hitbox, buttonsize is 100px by 100px
        self.rect = pygame.Rect(self.pos[1] * 140 + 70, self.pos[0] * 140 + 70, 100, 100)

    def check_click(self, mouse_pos, mouse_clicked, current_time):
        """check if given button is being clicked this frame, and return result"""
        if current_time - self.last_click > 0.2: # limit how often a button can be clicked
            if self.rect.collidepoint(mouse_pos) and mouse_clicked[0]:
                self.last_click = current_time
                # clicked and empty 
                if self.state == "":
                    return 1
                # clicked and not empty
                else:
                    return -1
        # not clicked or clicked too often
        else:
            return 0 
        
    def place(self, turn:str):
        """change the button's state to the given color"""
        self.state = turn



