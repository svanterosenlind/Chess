import pygame
import numpy as np
import ChessBoard
import Piece


class ChessGraphics:
    def __init__(self):
        self.grid_s = 100
        self.radius = round(self.grid_s / 8)
        self.board_white = (200, 200, 200)
        self.board_black = (10, 10, 90)
        self.piece_white = (220, 150, 130)
        self.piece_black = (50, 20, 10)
        self.selected_square_color = (20, 120, 20)
        self.legal_move_green = (20, 90, 20)
        self.legal_capture_red = (90, 20, 20)
        pygame.init()
        self.selected_square = None
        self.scr = pygame.display.set_mode((8 * self.grid_s, 8 * self.grid_s))
        self.font = pygame.font.SysFont("Calibri", 64, 4)
        self.promoting = False

    def draw_board(self, chessboard, bottom_player):
        for x in range(8):
            for y in range(8):
                rec = pygame.Rect((x*self.grid_s, y*self.grid_s), (self.grid_s, self.grid_s))
                if (x + y) % 2 == 0:
                    color = self.board_white
                else:
                    color = self.board_black
                pygame.draw.rect(self.scr, color, rec)
        if self.selected_square is not None:
            if bottom_player == "white":
                rec = pygame.Rect((self.selected_square[0] * self.grid_s, (7-self.selected_square[1]) * self.grid_s),
                                  (self.grid_s, self.grid_s))
            else:
                rec = pygame.Rect(((7-self.selected_square[0]) * self.grid_s, self.selected_square[1] * self.grid_s),
                                  (self.grid_s, self.grid_s))
            pygame.draw.rect(self.scr, self.selected_square_color, rec)

    def draw_pieces(self, chessboard, bottom_player):
        b = chessboard.board
        for x in range(8):
            for y in range(8):
                if b[(x, y)] is not None:
                    if b[(x, y)].color == "white":
                        text_color = self.piece_white
                    else:
                        text_color = self.piece_black
                    text = self.font.render(b[(x, y)].text, 0, text_color)
                    if bottom_player == "white":
                        self.scr.blit(text, (x * self.grid_s, (7 - y) * self.grid_s))
                    else:
                        self.scr.blit(text, ((7 - x) * self.grid_s, y * self.grid_s))

    # Draws the squares corresponding to the legal moves of the piece being selected
    def draw_moves(self, moves, bottom_player):
        if moves is None:
            return
        for m in moves:
            # If the move is a capture
            if m.move_type == "capture":
                color = self.legal_capture_red
            # If the move is not a capture
            else:
                color = self.legal_move_green

            x, y = m.move_square
            if bottom_player == "white":
                draw_x = self.grid_s * x + int(self.grid_s / 2)
                draw_y = self.grid_s * (7 - y) + int(self.grid_s / 2)
            else:
                draw_x = self.grid_s * (7 - x) + int(self.grid_s / 2)
                draw_y = self.grid_s * y + int(self.grid_s / 2)
            pygame.draw.circle(self.scr, color, (draw_x, draw_y), self.radius)

    def draw_promotion(self):
        outer_rec = pygame.rect.Rect((round(1.5*self.grid_s), round(3*self.grid_s)),
                                     (5*self.grid_s, 2*self.grid_s))
        inner_rec = pygame.rect.Rect((round(1.6*self.grid_s), round(3.1*self.grid_s)),
                                     (round(4.8*self.grid_s), round(1.8*self.grid_s)))
        pygame.draw.rect(self.scr, self.board_white, outer_rec)
        pygame.draw.rect(self.scr, self.board_black, inner_rec)
        for promotion in [Piece.Knight, Piece.Bishop, Piece.Rook, Piece.Queen]:
            pass

    def legal_moves(self, chess_board):
        pos = self.selected_square
        if pos is None:
            return []
        if chess_board.is_p(pos, color=chess_board.player_to_move):
            return chess_board.board[pos].legal_moves(chess_board)
        else:
            return []

    def board_mouse_pos(self, bottom_player):
        mouse_pos = np.array(pygame.mouse.get_pos()).astype(int)
        grid_pos = mouse_pos//self.grid_s
        if bottom_player == "white":
            return grid_pos[0], 7-grid_pos[1]
        else:
            return 7-grid_pos[0], grid_pos[1]


if __name__ == "__main__":
    gr = ChessGraphics()
    b = ChessBoard.ChessBoard()
    bottom_player = "white"
    running = True
    while running:
        pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressed = True
        gr.draw_board(b, bottom_player)
        possible_moves = gr.legal_moves(b)
        gr.draw_moves(possible_moves, bottom_player)
        gr.draw_pieces(b, bottom_player)
        pygame.display.flip()
        if pressed:
            mouse_square = gr.board_mouse_pos(bottom_player)
            # If you hadn't selected a square yet, select the one you clicked
            if gr.selected_square is None:
                gr.selected_square = mouse_square

            # If you clicked the one you had selected, unselect it
            elif gr.selected_square == mouse_square:
                gr.selected_square = None
            # If you had selected a square and then clicked another square
            else:
                # If you are making a move
                for move in possible_moves:
                    if np.array_equal(move.move_square, mouse_square):
                        print("moved")
                        b = move
                        # Check to see if this move ends the game
                        if not b.has_legal_moves():
                            if b.is_in_check():
                                print(f"{ChessBoard.n(b.player_to_move)} wins")
                            else:
                                print("Stalemate")
                            running = False
                        break
                # Otherwise just select the square you clicked on
                else:
                    gr.selected_square = mouse_square

