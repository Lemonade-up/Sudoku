def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j) #row and column
    return None

def valid(board, number, position):
    #Check row
    for i in range(len(board[0])):
        if board[position[0]][i] == number and position[1] != i:
            return False
    
    #Check column
    for i in range(len(board)):
        if board[i][position[1]] == number and position[0] != i:
            return False

    #Check box
    box_x = position[1] // 3
    box_y = position[0] // 3
        
    for i in range(box_y * 3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if board[i][j] == number and (i, j) != position:
                return False

    return True

def solve(board):
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True
            
            board[row][col] = 0

    return False
