# Interactive Tic-Tac-Toe Lambda Project

This project implements a simple interactive Tic-Tac-Toe game that can be played locally in the terminal or via AWS Lambda + API Gateway.

## Local Testing

Run:
```
python lambda_function.py
```
Follow the prompts to play Tic-Tac-Toe in your terminal. Players take turns entering positions (0-8):

```
 0 | 1 | 2
---+---+---
 3 | 4 | 5
---+---+---
 6 | 7 | 8
```

## Deploy to AWS Lambda

1. Zip `lambda_function.py`.
2. Create a Lambda function in AWS Console.
3. Upload the zip file.
4. Set the handler to `lambda_function.lambda_handler`.
5. Create an API Gateway (HTTP API or REST API) and connect it to your Lambda.
6. Send POST requests with JSON body as shown below.

## Example API Request

```
POST /your-api-endpoint
Content-Type: application/json

{
  "board": ["X", "O", "X", " ", "O", " ", " ", " ", " "],
  "move": 3,
  "player": "X"
}
```
Response:
```
{
  "board": ["X", "O", "X", "X", "O", " ", " ", " ", " "],
  "winner": null,
  "next_player": "O"
}
```

- `board`: Current board state as a list of 9 strings ("X", "O", or " ").
- `move`: Position (0-8) where the player wants to move.
- `player`: "X" or "O".
- `winner`: "X", "O", "Draw", or null if the game is ongoing.
- `next_player`: The player who should play next.

You can use this API to build a web or mobile front-end, or play programmatically.
