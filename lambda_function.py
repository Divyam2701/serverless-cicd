import json
import sys

# Optional: color support for CLI
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_X = Fore.RED + Style.BRIGHT
    COLOR_O = Fore.BLUE + Style.BRIGHT
    COLOR_RESET = Style.RESET_ALL
    COLORAMA_AVAILABLE = True
except ImportError:
    COLOR_X = COLOR_O = COLOR_RESET = ""
    COLORAMA_AVAILABLE = False

def check_winner(board):
    # Rows, columns and diagonals
    lines = [
        board[0:3], board[3:6], board[6:9],  # rows
        board[0:9:3], board[1:9:3], board[2:9:3],  # columns
        board[0:9:4], board[2:7:2]  # diagonals
    ]
    for line in lines:
        if line[0] != " " and line[0] == line[1] == line[2]:
            return line[0]
    if " " not in board:
        return "Draw"
    return None

def make_move(board, pos, player):
    if board[pos] == " ":
        board[pos] = player
        return True
    return False

def interact_lambda(event):
    # Expects JSON: { "board": [...], "move": pos, "player": "X" or "O" }
    data = event if isinstance(event, dict) else {}
    board = data.get("board", [" "] * 9)
    move = data.get("move")
    player = data.get("player", "X")
    if move is None or not (0 <= move < 9):
        return {"error": "Invalid move position"}
    if player not in ("X", "O"):
        return {"error": "Invalid player"}
    if not make_move(board, move, player):
        return {"error": "Cell already taken"}
    winner = check_winner(board)
    return {
        "board": board,
        "winner": winner,
        "next_player": "O" if player == "X" else "X"
    }

def lambda_handler(event, context):
    try:
        body = event.get('body')
        if body:
            data = json.loads(body)
        else:
            data = event
        result = interact_lambda(data)
        return {
            "statusCode": 200,
            "body": json.dumps(result),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"  # 🟢 Allow from browser
            }
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

def pretty_cell(cell):
    if cell == "X":
        return f"{COLOR_X}X{COLOR_RESET}"
    elif cell == "O":
        return f"{COLOR_O}O{COLOR_RESET}"
    else:
        return " "

def print_board(board):
    # Unicode box drawing for a nice board
    cells = [pretty_cell(c) if c != " " else str(i) for i, c in enumerate(board)]
    print("┏━━━┳━━━┳━━━┓")
    print(f"┃ {cells[0]} ┃ {cells[1]} ┃ {cells[2]} ┃")
    print("┣━━━╋━━━╋━━━┫")
    print(f"┃ {cells[3]} ┃ {cells[4]} ┃ {cells[5]} ┃")
    print("┣━━━╋━━━╋━━━┫")
    print(f"┃ {cells[6]} ┃ {cells[7]} ┃ {cells[8]} ┃")
    print("┗━━━┻━━━┻━━━┛")

if __name__ == "__main__":
    if not COLORAMA_AVAILABLE:
        print("(Tip: Install 'colorama' for colored output: pip install colorama)")
    print("Welcome to Tic-Tac-Toe!")
    print("Enter the number shown in each cell to make your move.")
    print_board([str(i) for i in range(9)])
    board = [" "] * 9
    current_player = "X"
    while True:
        print_board(board)
        move = input(f"Player {COLOR_X if current_player == 'X' else COLOR_O}{current_player}{COLOR_RESET}, enter your move (0-8): ")
        if not move.isdigit() or not (0 <= int(move) < 9):
            print("Invalid input. Try again.")
            continue
        move = int(move)
        if not make_move(board, move, current_player):
            print("Cell already taken. Try again.")
            continue
        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == "Draw":
                print("It's a draw!")
            else:
                print(f"Player {COLOR_X if winner == 'X' else COLOR_O}{winner}{COLOR_RESET} wins!")
            break
        current_player = "O" if current_player == "X" else "X"
