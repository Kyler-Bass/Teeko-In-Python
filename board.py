from graphics import graphics_handler
from buttons import button_class




# a manager class holding variables and functions and the objects for graphics and buttons 
class board_class:
    def __init__(self, board_list, window, screen_surface):
        # variables, objects, and lists 
        self.turn = "b" # "r" for red, "b" for black
        self.current_piece = '' # pos of current piece user is "holding" if they are holding one
        self.buttons = [] # list of all buttons 
        self.board_list = board_list # the list representing the board 
        self.graphics = graphics_handler(window, screen_surface) # the object for handling graphics 
        self.pieces_on_board = 0

        # add all the buttons to the list 
        for x,row in enumerate(self.board_list):
            for y,letter in enumerate(row):
                self.buttons.append(button_class((x,y), letter))

    def check_for_clicks(self, mouse_pos, mouse_pressed, current_time):
        """Check all buttons and call functions depending on state of the button clicked"""
        for button in self.buttons:
            # check if the button has been clicked 
            try_put = button.check_click(mouse_pos, mouse_pressed, current_time)

            # first 8 pieces 
            if try_put == 1 and self.pieces_on_board < 8:
                button.place(self.turn)
                self.board_list[button.pos[0]][button.pos[1]] = self.turn
                self.pieces_on_board += 1 
                self.next_turn()  
            # clicked on a piece that is not empty, pick it up 
            elif try_put == -1:
                self.current_piece = button
            # clicked on a piece that is empty, put piece down or do nothing
            elif try_put == 1:
                if self.current_piece != '':
                    if button.pos[0] in [self.current_piece.pos[0] - 1, self.current_piece.pos[0], self.current_piece.pos[0] + 1] and button.pos[1] in [self.current_piece.pos[1] - 1, self.current_piece.pos[1], self.current_piece.pos[1] + 1]:
                        self.change_piece_pos(button)
            elif try_put == 0: # either not clicked or already clicked this second 
                pass

    def check_win(self):
        """Check if either player won the game"""

        # get the positions of all the red pieces and black pieces 
        red_pieces = []
        black_pieces = []

        # the buttons will be in order from 0,0 to 4,4
        for button in self.buttons:
            if button.state == "r":
                red_pieces.append(button.pos)
            if button.state == "b":
                black_pieces.append(button.pos)

        # return values
        # 0 = no one won
        # 1 = red wins
        # 2 = black wins

        # win checks only work if the buttons are in order, ie. (0,0),(0,2),(1,3)....
        # red pieces win checks

        if len(red_pieces) < 4: # see if there are even 4 pieces, if not exit function 
            return 0
        
        # horizontal win - 4 in a row
        if red_pieces[0][0] == red_pieces[1][0] == red_pieces[2][0] == red_pieces[3][0] and red_pieces[0][1] + 1 == red_pieces[1][1] and red_pieces[1][1] + 1 == red_pieces[2][1] and red_pieces[2][1] + 1 == red_pieces[3][1]:
            return 1
        # vertical win - 4 in a column
        elif red_pieces[0][1] == red_pieces[1][1] == red_pieces[2][1] == red_pieces[3][1]:
            return 1
        # square win ['','','r','r',''],['','','r','r',''] 
        elif red_pieces[0][0] == red_pieces[1][0] and red_pieces[0][0] + 1 == red_pieces[2][0] and red_pieces[0][0] + 1 == red_pieces[3][0] and red_pieces[0][1] == red_pieces[2][1] and red_pieces[1][1] == red_pieces[3][1]:
            return 1
        # left to right diagonal win
        elif red_pieces[0][0] == red_pieces[1][0] - 1 == red_pieces[2][0] - 2 == red_pieces[3][0] - 3 and red_pieces[0][1] == red_pieces[1][1] - 1 == red_pieces[2][1] - 2 == red_pieces[3][1] - 3:
            return 1
        # right to left diagonal win
        elif red_pieces[0][0] == red_pieces[1][0] - 1 == red_pieces[2][0] - 2 == red_pieces[3][0] - 3 and red_pieces[0][1] == red_pieces[1][1] + 1 == red_pieces[2][1] + 2 == red_pieces[3][1] + 3:
            return 1


        # black pieces win checks

        if len(black_pieces) < 4: # see if there are even 4 pieces, if not exit function 
            return 0
        # horizontal win - 4 in a row
        if black_pieces[0][0] == black_pieces[1][0] == black_pieces[2][0] == black_pieces[3][0] and black_pieces[0][1] + 1 == black_pieces[1][1] and black_pieces[1][1] + 1 == black_pieces[2][1] and black_pieces[2][1] + 1 == black_pieces[3][1] and black_pieces[3][1] + 1 == black_pieces[4][1]: 
            return 2
        # vertical win - 4 in a column
        elif black_pieces[0][1] == black_pieces[1][1] == black_pieces[2][1] == black_pieces[3][1]:
            return 2
        # square win
        elif black_pieces[0][0] == black_pieces[1][0] and black_pieces[0][0] + 1 == black_pieces[2][0] and black_pieces[0][0] + 1 == black_pieces[3][0] and black_pieces[0][1] == black_pieces[2][1] and black_pieces[1][1] == black_pieces[3][1]:
            return 2
        # left to right diagonal win
        elif black_pieces[0][0] == black_pieces[1][0] - 1 == black_pieces[2][0] - 2 == black_pieces[3][0] - 3 and black_pieces[0][1] == black_pieces[0][1] - 1 == black_pieces[0][2] - 2 == black_pieces[0][3] - 3:
            return 2
        # right to left diagonal win
        elif black_pieces[0][0] == black_pieces[1][0] - 1 == black_pieces[2][0] - 2 == black_pieces[3][0] - 3 and black_pieces[0][1] == black_pieces[1][1] + 1 == black_pieces[2][1] + 2 == black_pieces[3][1] + 3:
            return 2
        # if no one won return 0
        else: 
            return 0

    def change_piece_pos(self, button):
        """"target is the location of where currently held piece"""
        self.board_list[self.current_piece.pos[0]][self.current_piece.pos[1]] = ""
        self.board_list[button.pos[0]][button.pos[1]] = self.current_piece.state
        button.state = self.current_piece.state
        self.current_piece.state = ''
        self.current_piece = ''
        self.next_turn()
    
    def next_turn(self):
        """Change the turn"""
        if self.turn == "r":
            self.turn = "b"
        elif self.turn == "b":
            self.turn = "r"