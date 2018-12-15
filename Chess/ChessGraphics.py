import pygame
import numpy as np
from ChessBoard import ChessBoard


class ChessGraphics:
    def __init__(self):
        self.grid_s = 100
        self.board_white = (200, 200, 200)
        self.board_black = (10, 10, 10)
        self.piece_white = (220, 150, 130)
        self.piece_black = (20, 20, 10)
        pygame.init()
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
        self.draw_pieces(chessboard, bottom_player)
        pygame.display.flip()

    def draw_pieces(self, chessboard, bottom_player):   # TODO: se till så att pjäserna ritas rätt om brädet vänds.
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

    def board_mouse_pos(self, bottom_player):
        mouse_pos = np.array(pygame.mouse.get_pos()).astype(int)
        grid_pos = mouse_pos//self.grid_s
        if bottom_player == "white":
            return (grid_pos[0], 7-grid_pos[1])
        else:
            return (7-grid_pos[0], grid_pos[1])

if __name__ == "__main__":
    gr = ChessGraphics()
    b = ChessBoard()
    bottom_player = "black"
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
            print(gr.board_mouse_pos(bottom_player))
