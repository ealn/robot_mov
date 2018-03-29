# Robot Motion Planning
#
# Autors:
#
# - Efrain Adrian Luna Nevarez
# - Efrain Arrambide Barron
#
import random

## Contants
CIRCLE        = 'Circle'
SQUARE        = 'Square'
TRIANGLE      = 'Triangle'

NUMBER_PIECES = 10
NUMBER_COLUMS = 6
SUCCESS       = True
FAIL          = False

## Globals
g_grid_pieces     = []
g_list_pieces     = []
g_list_names      = []
g_invalid_columns = []

#####################################################################################
################################### Clases ##########################################
#####################################################################################

class Piece():
    top = None
    bottom = None
    column = None

class Shape(Piece):

    def __init__(self, shape_type, name):
        self.shape_type = shape_type
        self.name = name

    def draw_top(self):
        if self.shape_type == CIRCLE:
            print(" ---  ", end='', flush=True)
        elif self.shape_type == SQUARE:
            print("----- ", end='', flush=True)
        elif self.shape_type == TRIANGLE:
            print("  ^   ", end='', flush=True)

    def draw_med1(self):
        if self.shape_type == CIRCLE:
            print("/   \\ ", end='', flush=True)
        elif self.shape_type == SQUARE:
            print("|   | ", end='', flush=True)
        elif self.shape_type == TRIANGLE:
            print(" / \\  ", end='', flush=True)

    def draw_med2(self):
        if self.shape_type == CIRCLE:
            print("\\ {} / ".format(self.name), end='', flush=True)
        elif self.shape_type == SQUARE:
            print("| {} | ".format(self.name), end='', flush=True)
        elif self.shape_type == TRIANGLE:
            print("/ {} \\ ".format(self.name), end='', flush=True)

    def draw_botton(self):
        if self.shape_type == CIRCLE:
            print(" ---  ", end='', flush=True)
        elif self.shape_type == SQUARE:
            print("----- ", end='', flush=True)
        elif self.shape_type == TRIANGLE:
            print("----- ", end='', flush=True)

######################################### Draw #################################################

def draw():
    global g_list_pieces
    global g_grid_pieces
    max = 0
    i = 1

    #Find the max index of all columns
    for column in g_grid_pieces:
        len_column = len(column)
        if len_column > max:
            max = len_column

    while max > 0:
        #Draw all columns
        for column in g_grid_pieces:
            if len(column) >= max:
                piece = column[max - 1]
                piece.draw_top()
            else:
                print("      ", end='', flush=True)    #Print offset

        print()    #New Line

        for column in g_grid_pieces:
            if len(column) >= max:
                piece = column[max - 1]
                piece.draw_med1()
            else:
                print("      ", end='', flush=True)    #Print offset

        print()  # New Line

        for column in g_grid_pieces:
            if len(column) >= max:
                piece = column[max - 1]
                piece.draw_med2()
            else:
                print("      ", end='', flush=True)    #Print offset

        print()  # New Line

        for column in g_grid_pieces:
            if len(column) >= max:
                piece = column[max - 1]
                piece.draw_botton()
            else:
                print("      ", end='', flush=True)    #Print offset

        print()  # New Line
        max -= 1

    while i <= NUMBER_COLUMS:
        print("--{}-- ".format(i), end='', flush=True)
        i += 1

    print("\n")  # New Line

######################################### Algorithm ############################################

def put_on(piece_to_move, piece_target):
    #Prevent invalid movement
    ret = is_valid_movement(piece_target)

    if ret == SUCCESS:
        save_invalid_columns_to_move(piece_to_move, piece_target)
        column = get_space(piece_to_move, piece_target)

        if column != None:
            is_free_top = grasp(piece_to_move)

            if is_free_top == SUCCESS:
                move(piece_to_move, column)
                ungrasp(piece_to_move, column)

                print("\nPut {} on ".format(piece_to_move.name), end='')

                if piece_target != None:
                    print(piece_target.name)
                else:
                    if len(column) == 1:
                        print("Empty Space")
                    else:
                        prev_piece = column[-2]
                        print(prev_piece.name)

                draw()
            else:
                print("ERROR: Cannot free top of {}".format(piece_to_move.name))
        else:
            print("ERROR: There is not a valid space to move {}".format(piece_to_move.name))
            ret = FAIL
    else:
        print("ERROR: Cannot put {} on {}".format(piece_to_move.name, piece_target.name))
        ret = FAIL

    return ret

def get_space(piece_to_move, piece_target):
    column = None

    if piece_target == None:
        ret = SUCCESS

        if piece_to_move.top != None:
            ret = make_space(piece_to_move)

        if ret == SUCCESS:
            #Get empty space
            column = get_free_space()
    else:   #piece_target != None
        if piece_target.top != None:
            ret = make_space(piece_target)

            if ret == SUCCESS and piece_target.top == None:
                # Return the column of target piece
                column = piece_target.column
        else:
            # Return the column of target piece
            column = piece_target.column

    return column


def make_space(piece):
    return get_and_of(piece.top)

def grasp(piece):
    ret = SUCCESS

    if piece.top != None:
        ret = clear_top(piece)

    if piece.top == None:
        column = piece.column
        column.remove(piece)
        piece.column = None
        bottom_piece = piece.bottom

        if bottom_piece != None:
            bottom_piece.top = None
            piece.bottom = None

    return ret

def clear_top(piece):
    return get_and_of(piece.top)

def get_and_of(piece):
    return put_on(piece, None)

def move(piece, column):
    column.append(piece)

def ungrasp(piece, column):
    piece.column = column

    if len(column) > 1:
        prev_element = column[-2]  #Get prev element inserted

        if prev_element != None:
            # Ungrap Piece
            prev_element.top = piece
            piece.bottom = prev_element

############################################### Utils ##########################################
def save_invalid_columns_to_move(piece_to_move, piece_target):
    global g_invalid_columns

    # If this is the main movement
    if piece_to_move != None and piece_target != None:
        g_invalid_columns = []
        g_invalid_columns.append(piece_to_move.column)
        g_invalid_columns.append(piece_target.column)

def is_valid_column(column):
    ret = True
    global g_invalid_columns

    for col in g_invalid_columns:
        if col == column:
            ret = False
            break

    return ret

def is_valid_movement(piece_target):
    ret = SUCCESS

    if piece_target != None and piece_target.shape_type != SQUARE:
        ret = FAIL

    return ret


def get_free_space():
    global g_grid_pieces
    free_column = None

    # Search first the empty columns
    for column in g_grid_pieces:
        if len(column) == 0:
            free_column = column
            break

    # If there was not empty space
    if free_column == None:
        # Search valid columns
        for column in g_grid_pieces:
            if is_valid_column(column) and can_insert_piece(column):
                free_column = column
                break

    return free_column

def can_insert_piece(column):
    ret = True

    if len(column) > 0:
        top = column[-1] #Get last element

        if top != None and top.shape_type != SQUARE:
            ret = False

    return ret

########################################## Console Utils #######################################

def get_console_input(str, list_valid_entries):
    is_invalid = True
    inp = None

    while is_invalid:
        inp = input(str)

        #Search if input is valid
        for value in list_valid_entries:
            if value == inp:
                is_invalid = False        # Valid input, break loops
                break

        if is_invalid:
            print("Invalid entry, Try again")

    return inp

def get_piece_to_move():
    global g_list_names
    global g_list_pieces
    piece_to_move = None
    piece_target = None

    name_piece_to_move = get_console_input("Put-on first piece {}: ".format(g_list_names), g_list_names)
    name_piece_target  = get_console_input("Put-on second piece {}: ".format(g_list_names), g_list_names)

    for piece in g_list_pieces:
        if piece.name == name_piece_to_move:
            piece_to_move = piece
        elif piece.name == name_piece_target:
            piece_target = piece

        if piece_to_move != None and piece_target != None:
            break

    return piece_to_move, piece_target


############################################### Init ###########################################

def create_list_pieces():
    global g_list_pieces
    global g_list_names
    choices = [SQUARE, SQUARE, SQUARE, CIRCLE, TRIANGLE, SQUARE, SQUARE]
    name = 'A'
    i = 0

    while i < NUMBER_PIECES:
        shape_type = random.choice(choices)
        g_list_names.append(name)
        piece = Shape(shape_type, name)
        g_list_pieces.append(piece)
        name = chr(ord(name) + 1)
        i += 1

def create_grid():
    global g_grid_pieces
    i = 0

    while i < NUMBER_COLUMS:
        list_empty = []
        g_grid_pieces.append(list_empty)
        i += 1

def init_piece_position():
    global g_list_pieces
    global g_grid_pieces

    copy_grid_piece = g_grid_pieces[:]   #Copy list

    for piece in g_list_pieces:
        loop = True

        while loop:
            if len(copy_grid_piece) > 0:
                column = random.choice(copy_grid_piece)
                if can_insert_piece(column):
                    move(piece, column)
                    ungrasp(piece, column)
                    loop = False
                else:
                    copy_grid_piece.remove(column)
            else:
                loop = False

def start():
    loop = True

    while loop:
        piece_to_move, piece_target = get_piece_to_move()
        put_on(piece_to_move, piece_target)


def main():
    create_list_pieces()
    create_grid()
    init_piece_position()
    draw()
    start()

#When this script is called as main, run the main function
if __name__ == '__main__':
    main()