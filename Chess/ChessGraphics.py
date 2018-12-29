import pygame
import numpy as np
import ChessBoard
import Piece


class ChessGraphics:
    def __init__(self):
        self.grid_s = 100
        self.board_white = (200, 200, 200)
        self.board_black = (10, 10, 10)
        self.piece_white = (220, 150, 130)
        self.piece_black = (20, 20, 10)
        self.selected_square_color = (20, 120, 20)
        self.legal_move_green = (20, 90, 20)
        self.legal_capture_red = (90, 20, 20)
        pygame.init()
        self.selected_square = None
        self.scr = pygame.display.set_mode((8 * self.grid_s, 8 * self.grid_s))
        self.font = pygame.font.SysFont("Calibri", 64, 4)

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
        self.draw_pieces(chessboard, bottom_player)
        if self.selected_square is not None: # If a square is selected
            self.draw_moves(chessboard, self.selected_square, bottom_player)
        pygame.display.flip()

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

    def draw_moves(self, chessboard, square, bottom_player):
        if chessboard.board[square] is None:
            return
        elif chessboard.board[square].color != chessboard.player_to_move:
            return
        moves, captures = chessboard.board[square].legal_moves(chessboard)
        radius = round(self.grid_s / 8)
        if bottom_player == "white":
            for move in moves:
                x = self.grid_s * move[0] + int(self.grid_s/2)
                y = self.grid_s * (7-move[1]) + int(self.grid_s/2)
                pygame.draw.circle(self.scr, self.legal_move_green, (x, y), radius)
            for cap in captures:
                x = self.grid_s * cap[0] + int(self.grid_s/2)
                y = self.grid_s * (7-cap[1]) + int(self.grid_s/2)
                pygame.draw.circle(self.scr, self.legal_capture_red, (x, y), radius)
        else:
            for move in moves:
                x = self.grid_s * (7-move[0]) + self.grid_s/2
                y = self.grid_s * move[1] + self.grid_s/2
                pygame.draw.circle(self.scr, self.legal_move_green, (x, y), radius)
            for cap in captures:
                x = self.grid_s * (7 - move[0]) + self.grid_s / 2
                y = self.grid_s * move[1] + self.grid_s / 2
                pygame.draw.circle(self.scr, self.legal_capture_red, (x, y), radius)
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
        if pressed:
            if gr.selected_square == gr.board_mouse_pos(bottom_player):     # If you pressed the already selected square
                gr.selected_square = None
            elif gr.selected_square is not None and b.board[gr.selected_square] is not None \
                    and b.board[tuple(gr.selected_square)].color == b.player_to_move:      # If you selected a piece of your own color
                legal_moves, legal_captures = b.board[gr.selected_square].legal_moves(b)
                found = False
                for cand in legal_moves:
                    if gr.board_mouse_pos(bottom_player)[0] == cand[0] \
                            and gr.board_mouse_pos(bottom_player)[1] == \
                            cand[1]:
                        found = True
                if found:
                    b.previous_board = b.board
                    b.board[gr.board_mouse_pos(bottom_player)] = b.board[gr.selected_square]
                    b.board[gr.board_mouse_pos(bottom_player)].pos = np.array(gr.board_mouse_pos(bottom_player))
                    b.board[gr.selected_square] = None
                    b.player_to_move = ChessBoard.n(b.player_to_move)
                else:
                    found = False
                    for cand in legal_captures:
                        if gr.board_mouse_pos(bottom_player)[0] == cand[0] \
                                and gr.board_mouse_pos(bottom_player)[1] == cand[1]:
                            found = True
                    if found:
                        b.previous_board = b.board
                        b.board[gr.board_mouse_pos(bottom_player)] = b.board[gr.selected_square]
                        b.board[gr.board_mouse_pos(bottom_player)].pos = np.array(gr.board_mouse_pos(bottom_player))
                        b.board[gr.selected_square] = None
                        b.player_to_move = ChessBoard.n(b.player_to_move)
            else:
                gr.selected_square = gr.board_mouse_pos(bottom_player)
