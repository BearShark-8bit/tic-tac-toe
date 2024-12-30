from enum import Enum
from typing import Self, Type
import pygame
import logging
from copy import deepcopy as c

logging.basicConfig(
    filename="tictactoe.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(levelname)s - %(message)s",
)


class Move(Enum):
    CROSS = "X"
    CIRCLE = "O"


class Board:
    def __init__(self) -> None:
        self.___board = [[" " for _ in range(3)] for _ in range(3)]

    @property
    def board(self) -> list[list[Type[Move]]]:
        return c(self.___board)

    def is_available(self, pos: tuple[int, int]) -> bool:
        """
        Check if the position is available for a move
        :param pos: tuple[int, int]
        :return: bool
        """
        x, y = pos
        return self.___board[y][x] == " "

    def check_winner(self) -> Type[Move]:
        """
        Check if there is a winner
        :return: Type[Move]
        """
        for i in range(3):
            if self.___board[i][0] == self.___board[i][1] == self.___board[i][2] != " ":
                return self.___board[i][0]
            if self.___board[0][i] == self.___board[1][i] == self.___board[2][i] != " ":
                return self.___board[0][i]
        if self.___board[0][0] == self.___board[1][1] == self.___board[2][2] != " ":
            return self.___board[0][0]
        if self.___board[0][2] == self.___board[1][1] == self.___board[2][0] != " ":
            return self.___board[0][2]
        return False

    def is_full(self) -> bool:
        """
        Check if the board is full
        :return: bool
        """
        return all(all(cell != " " for cell in row) for row in self.___board)

    def make_move(self, move: Move, pos: tuple[int, int]) -> Self:
        """
        Make a move on the board
        :param move: Move
        :param pos: tuple[int, int]
        :return: Board
        """
        if not self.is_available(pos):
            raise ValueError(f"Position {pos} is not available")
        logging.info("Adding %s to %s", move.value, pos)
        x, y = pos
        self.___board[y][x] = move
        return self

    def __str__(self) -> str:
        formatted_board = [
            *map(
                lambda l: [el.value if isinstance(el, Move) else " " for el in l],
                self.___board,
            )
        ]
        result_string = "\n      ".join(map(str, formatted_board))
        return f"Board({ result_string })"

    __repr__ = __str__


scale = pygame.transform.scale
load = pygame.image.load


class TicTacToe(pygame.sprite.Sprite):
    board: Board = Board()
    board_size: int = 300

    image: pygame.Surface = pygame.Surface((board_size, board_size))
    rect: pygame.Rect = image.get_rect()
    move_size: int = 81
    board_texture: pygame.Surface = scale(
        load("./img/tic-tac-toe.png"), (board_size, board_size)
    )
    cross_texture: pygame.Surface = scale(
        load("./img/cross.png"), (move_size, move_size)
    )
    circle_texture: pygame.Surface = scale(
        load("./img/circle.png"), (move_size, move_size)
    )

    def update(self):
        self.image.fill((255, 255, 255))
        self.image.blit(self.board_texture, (0, 0))
        offset = 9
        for y, row in enumerate(self.board.board):
            for x, cell in enumerate(row):
                if cell == Move.CROSS:
                    self.image.blit(
                        self.cross_texture, (x * 100 + offset, y * 100 + offset)
                    )
                elif cell == Move.CIRCLE:
                    self.image.blit(
                        self.circle_texture, (x * 100 + offset, y * 100 + offset)
                    )


def main():

    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption("Tic Tac Toe")
    clock = pygame.time.Clock()
    running = True
    ttt = TicTacToe()
    tictactoe = pygame.sprite.GroupSingle(ttt)
    state = Move.CROSS

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x //= 100
                y //= 100
                try:
                    ttt.board.make_move(state, (x, y))
                    state = Move.CROSS if state == Move.CIRCLE else Move.CIRCLE
                except ValueError as e:
                    logging.error(e)

        tictactoe.update()
        if winner := ttt.board.check_winner():
            logging.info("Winner is %s", winner.value)
            running = False
        if ttt.board.is_full():
            logging.info("It's a tie")
            running = False

        tictactoe.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
