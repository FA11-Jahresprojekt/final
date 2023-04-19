import time

import pygame
from pygame import mixer

from game import BauernSchach, Dame, MoveAction, MiniMaxKI, RandomKi

# Initialize pygame
pygame.init()

# Initialize fonts
pygame.font.init()
arial = pygame.font.SysFont('Arial', 24)
arialBold = pygame.font.SysFont('Arial Bold', 24)

# Global Variables
TITLE = "Bauernschach"
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
ROWS = 6
COLUMNS = 6
SQUARE_SIZE = 65
PADDING = 50
HELP_TEXT = ["Linie1", "Linie2", "Linie3"]
DAME_TEXTURES = False

# Sounds
MUSIC_BASE_DIR = "assets/sounds/"
mixer.music.load(MUSIC_BASE_DIR + "click.ogg")
mixer.music.set_volume(0.1)

# Images
IMAGE_BASE_DIR = "assets/image/"
IMAGE_WIN_LABEL = pygame.image.load(IMAGE_BASE_DIR + 'win_label.png')
IMAGE_LOSE_LABEL = pygame.image.load(IMAGE_BASE_DIR + 'lose_label.png')
IMAGE_FAVICON = pygame.image.load(IMAGE_BASE_DIR + 'favicon.png')
IMAGE_HEADING = pygame.image.load(IMAGE_BASE_DIR + 'heading.png')
IMAGE_ICON_HELP = pygame.image.load(IMAGE_BASE_DIR + 'question.png')
IMAGE_ICON_EXIT = pygame.image.load(IMAGE_BASE_DIR + 'exit.png')
IMAGE_BACKGROUND = pygame.image.load(IMAGE_BASE_DIR + 'background.png')
IMAGE_BUTTON = pygame.image.load(IMAGE_BASE_DIR + 'button.png')
IMAGE_WHITE_PAWN = pygame.image.load(IMAGE_BASE_DIR + 'pawn_white.png')
IMAGE_BLACK_PAWN = pygame.image.load(IMAGE_BASE_DIR + 'pawn_black.png')
IMAGE_HEADING_GRUPPE = pygame.image.load(IMAGE_BASE_DIR + 'heading_gruppe.png')
IMAGE_GAME_BACKGROUND = pygame.image.load(IMAGE_BASE_DIR + 'game_background.png')
IMAGE_STATS_BACKGROUND = pygame.image.load(IMAGE_BASE_DIR + 'stats_background.png')
IMAGE_LEADERBOARD_BACKGROUND = pygame.image.load(IMAGE_BASE_DIR + 'leaderboard_background.png')

# Setting up the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption(TITLE)
pygame.display.set_icon(IMAGE_FAVICON)

# Variables
selected_pawn = []
mark_pawns = []
disable_deselect = False

class Engine:
    def __init__(self, mainMenu, difficulty, game):
        if game == 'Bauernschach':
            self.game = BauernSchach(difficulty)
            DAME_TEXTURES = False
        else:
            self.game = Dame(difficulty)
            DAME_TEXTURES = True

        if difficulty == 0:
            self.ki = RandomKi(self.game)
        else:
            self.ki = MiniMaxKI(self.game)

        self.mainMenu = mainMenu
        self.quit = False

    def draw_heading(self):
        leftover = SCREEN_HEIGHT - (COLUMNS * SQUARE_SIZE)
        offset = 15

        screen.blit(pygame.transform.scale(IMAGE_HEADING, (420, 46)), (PADDING - offset, leftover / 2 - offset))


    def draw_pawn(self, xField, yField, color):
        leftover = SCREEN_HEIGHT - (COLUMNS * SQUARE_SIZE)

        x = xField * SQUARE_SIZE + PADDING
        y = yField * SQUARE_SIZE + leftover / 2 + PADDING

        if color == "white":
            screen.blit(IMAGE_WHITE_PAWN, (x, y))
        elif color == "black":
            screen.blit(IMAGE_BLACK_PAWN, (x, y))


    def draw_help_button(self):
        leftover = SCREEN_HEIGHT - (COLUMNS * SQUARE_SIZE)
        x = PADDING + 380
        y = ROWS * SQUARE_SIZE + leftover / 2 + PADDING + 20

        help = screen.blit(IMAGE_ICON_HELP, (x, y))

        if help.collidepoint(pygame.mouse.get_pos()):
            minus_padding = (420 - SQUARE_SIZE * ROWS) / 2
            leftover = SCREEN_HEIGHT - (COLUMNS * SQUARE_SIZE)
            x = (SCREEN_WIDTH - 560) - PADDING / 2
            y = leftover / 2 + PADDING

            screen.blit(IMAGE_LEADERBOARD_BACKGROUND, (x - minus_padding, y - minus_padding))

            for i in range(len(HELP_TEXT)):
                helpText = arial.render(HELP_TEXT[i], True, (255, 255, 255))
                screen.blit(helpText, (x + 20, y + 20 + i * 30))


    def draw_quit_button(self):
        leftover = SCREEN_HEIGHT - (COLUMNS * SQUARE_SIZE)
        x = PADDING + 380
        y = ROWS * SQUARE_SIZE + leftover / 2 + PADDING + 20

        quitButton = screen.blit(IMAGE_ICON_EXIT, (x - 30, y))

        if quitButton.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                quit = True
                mixer.music.play()


    def draw_quit_warning(self):
        if self.quit == False:
            return

        self.draw_background()
        self.draw_loading()
        backBtn = self.draw_button(SCREEN_WIDTH / 2 - 500 / 2, SCREEN_HEIGHT / 2 - 67 / 2 + 80, "Zurück zum Spiel", 500, 67)
        quitBtn = self.draw_button(SCREEN_WIDTH / 2 - 500 / 2, SCREEN_HEIGHT / 2 - 67 / 2 + 150, "Spiel beenden", 500, 67)

        if backBtn.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.draw_background()
                self.draw_heading()
                self.draw_difficulty()
                mixer.music.play()
                quit = False

        if quitBtn.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.mainMenu.run()


    def draw_button(self, x, y, text, width=150, height=50):
        image = screen.blit(pygame.transform.scale(IMAGE_BUTTON, (width, height)), (x, y))
        buttonText = arial.render(text, True, (255, 255, 255))
        text_width, text_height = arial.size(text)

        screen.blit(buttonText, (x + width / 2 - text_width / 2, y + height / 2 - text_height / 2))
        return image


    def draw_losing_screen(self, score):
        global lose

        if not 'lose' in globals():
            lose = False
            return

        if lose == False:
            return

        self.draw_background()
        screen.blit(IMAGE_LOSE_LABEL, (SCREEN_WIDTH / 2 - 486 / 2, SCREEN_HEIGHT / 4))

        screen.blit(pygame.transform.scale(IMAGE_STATS_BACKGROUND, (300, 80)),
                    (SCREEN_WIDTH / 2 - 300 / 2, SCREEN_HEIGHT / 4 + 100))

        scoreText = arial.render("Destroyed Pawns: " + str(score), True, (255, 255, 255))
        screen.blit(scoreText, (SCREEN_WIDTH / 2 - 300 / 2 + 35, SCREEN_HEIGHT / 4 + 125))

        quitBtn = self.draw_button(SCREEN_WIDTH / 2 - 500 / 2, SCREEN_HEIGHT / 2 - 67 / 2 + 150, "Spiel beenden", 500, 67)

        if quitBtn.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.back_to_main()


    def draw_winning_screen(self, score):
        global win

        if not 'win' in globals():
            win = False
            return

        if win == False:
            return

        self.draw_background()
        screen.blit(IMAGE_WIN_LABEL, (SCREEN_WIDTH / 2 - 497 / 2, SCREEN_HEIGHT / 4))

        screen.blit(pygame.transform.scale(IMAGE_STATS_BACKGROUND, (300, 80)),
                    (SCREEN_WIDTH / 2 - 300 / 2, SCREEN_HEIGHT / 4 + 100))

        scoreText = arial.render("Destroyed Pawns: " + str(score), True, (255, 255, 255))
        screen.blit(scoreText, (SCREEN_WIDTH / 2 - 300 / 2 + 35, SCREEN_HEIGHT / 4 + 125))

        quitBtn = self.draw_button(SCREEN_WIDTH / 2 - 500 / 2, SCREEN_HEIGHT / 2 - 67 / 2 + 150, "Spiel beenden", 500, 67)

        if quitBtn.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                self.back_to_main()

    def back_to_main(self):
        self.mainMenu.run()


    def truncline(self, text, font, maxwidth):
        real = len(text)
        stext = text
        l = font.size(text)[0]
        cut = 0
        a = 0
        done = 1
        old = None
        while l > maxwidth:
            a = a + 1
            n = text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext = n[:-cut]
            else:
                stext = n
            l = font.size(stext)[0]
            real = len(stext)
            done = 0
        return real, done, stext


    def wrapline(self, text, font, maxwidth):
        done = 0
        wrapped = []

        while not done:
            nl, done, stext = self.truncline(text, font, maxwidth)
            wrapped.append(stext.strip())
            text = text[nl:]
        return wrapped


    def draw_board(self):
        global mark_pawns
        leftover = SCREEN_HEIGHT - (COLUMNS * SQUARE_SIZE)

        light_color = (196, 156, 126)
        dark_color = (114, 74, 44)

        minus_padding = (420 - SQUARE_SIZE * ROWS) / 2
        screen.blit(IMAGE_GAME_BACKGROUND, (PADDING - minus_padding, leftover / 2 + PADDING - minus_padding))

        for row in range(ROWS):
            for column in range(COLUMNS):
                x = column * SQUARE_SIZE + PADDING
                y = row * SQUARE_SIZE + leftover / 2 + PADDING

                if (row + column) % 2 == 0:
                    color = light_color
                else:
                    color = dark_color

                if pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE)).collidepoint(pygame.mouse.get_pos()):
                    self.draw_rect_alpha(screen, (0, 0, 0, 20), (x, y, SQUARE_SIZE, SQUARE_SIZE))

                    if pygame.mouse.get_pressed()[0]:
                        self.draw_rect_alpha(screen, (0, 0, 0, 50), (x, y, SQUARE_SIZE, SQUARE_SIZE))
                        self.on_click(column, row)

                if [column, row] in mark_pawns:
                    self.draw_rect_alpha(screen, (0, 100, 0, 60), (x, y, SQUARE_SIZE, SQUARE_SIZE))

                if selected_pawn == [column, row]:
                    self.draw_rect_alpha(screen, (0, 0, 0, 80), (x, y, SQUARE_SIZE, SQUARE_SIZE))


    def draw_difficulty(self):
        leftover = SCREEN_HEIGHT - (COLUMNS * SQUARE_SIZE)
        x = PADDING
        y = ROWS * SQUARE_SIZE + leftover / 2 + PADDING + 20

        difficulty = arialBold.render("Schwierigkeit: Einfach", True, (255, 255, 255))

        screen.blit(difficulty, (x, y))


    def on_click(self, column, row):
        global last_click, game, mark_pawns, selected_pawn, win, disable_deselect

        if not 'last_click' in globals():
            last_click = pygame.time.get_ticks() - 200

        if pygame.time.get_ticks() - last_click > 400:
            mixer.music.play()

            last_click = pygame.time.get_ticks()

            if selected_pawn == [column, row] and not disable_deselect:
                selected_pawn.clear()
                return

            if [column, row] in mark_pawns:
                print(f"Selected Pawn {column} {row}")
                pawn = self.game.gameField.getPawnForPos(column, row)
                oldPawn = None if len(selected_pawn) != 2 else self.game.gameField.getPawnForPos(selected_pawn[0], selected_pawn[1])
                if oldPawn is not None and pawn is None or (pawn is not None and oldPawn is not None and pawn.player != oldPawn.player):
                    print(f"Move Pawn {selected_pawn[0]} {selected_pawn[1]} to {column} {row}")
                    if self.game.movePawn(MoveAction(oldPawn, column, row)):
                        if self.game.checkIfWon("A"):
                            win = True
                            return
                        if disable_deselect:
                            disable_deselect = False
                        selected_pawn.clear()
                        mark_pawns.clear()
                        self.game.switchPlayer()
                        return
                    else:
                        if self.game.checkIfWon("A"):
                            win = True
                            return
                        selected_pawn.clear()
                        selected_pawn.append(column)
                        selected_pawn.append(row)
                        disable_deselect = True
                        mark_pawns = self.game.getPossiblePawnDestinationsForChosenPawn(oldPawn, True)
                        return

                else:
                    if pawn is not None:
                        mark_pawns = self.game.getPossiblePawnDestinationsForChosenPawn(pawn)
                    else:
                        mark_pawns = self.game.getPossiblePawnsForPlayer(self.game.currentPlayer)
            elif len(mark_pawns) != 0:
                return

            if len(selected_pawn) != 0:
                selected_pawn.clear()

            selected_pawn.append(column)
            selected_pawn.append(row)


    def draw_rect_alpha(self, surface, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)


    def get_leaderboard(self):
        return [{"username": "Alice", "score": 104}, {"username": "Bob", "score": 20}, {"username": "Charlie", "score": 15},
                {"username": "Alice", "score": 104}, {"username": "Bob", "score": 20}, {"username": "Charlie", "score": 15},
                {"username": "Alice", "score": 104}, {"username": "Bob", "score": 20}, {"username": "Charlie", "score": 15},
                {"username": "Alice", "score": 104}, {"username": "Bob", "score": 20}, {"username": "Charlie", "score": 15}]


    def draw_leaderboard(self):
        minus_padding = (420 - SQUARE_SIZE * ROWS) / 2
        leftover = SCREEN_HEIGHT - (COLUMNS * SQUARE_SIZE)
        x = (SCREEN_WIDTH - 560) - PADDING / 2
        y = leftover / 2 + PADDING

        screen.blit(IMAGE_LEADERBOARD_BACKGROUND, (x - minus_padding, y - minus_padding))

        leaderboard = self.get_leaderboard()

        for i in range(len(leaderboard)):
            if i > 10:
                break

            place = arialBold.render(str(i + 1) + ".", True, (255, 255, 255))
            username = arialBold.render(leaderboard[i]["username"], True, (255, 255, 255))
            score = arial.render(str(leaderboard[i]["score"]), True, (255, 255, 255))

            screen.blit(place, (x + 30, y + 35 + i * 30))
            screen.blit(username, (x + 55, y + 35 + i * 30))
            screen.blit(score, (x + 30 + 400, y + 35 + i * 30))


    def draw_stats(self):
        global score

        if not 'score' in globals():
            score = 0

        minus_padding = (420 - SQUARE_SIZE * ROWS) / 2
        leftover = SCREEN_HEIGHT - (COLUMNS * SQUARE_SIZE)
        x = (SCREEN_WIDTH - 560) - PADDING / 2
        y = leftover / 2 + PADDING

        screen.blit(IMAGE_STATS_BACKGROUND, (x - minus_padding, y - minus_padding - 150))

        scoreText = arial.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(scoreText, (x + 35, y - 110))


    def draw_background(self):
        screen.blit(IMAGE_BACKGROUND, (0, 0))


    def draw_loading(self):
        screen.blit(IMAGE_BACKGROUND, (0, 0))
        screen.blit(IMAGE_HEADING_GRUPPE, (SCREEN_WIDTH / 2 - 228, SCREEN_HEIGHT / 2 - 37.5))


    def draw_text(self, text, x, y, color):
        screen.blit(arial.render(text, True, color), (x, y))


    def game_loop(self):
        global IMAGE_HEADING, IMAGE_BLACK_PAWN, IMAGE_WHITE_PAWN, game, mark_pawns, lose, win

        if DAME_TEXTURES:
            IMAGE_HEADING = pygame.image.load(IMAGE_BASE_DIR + 'heading_dame.png')
            IMAGE_BLACK_PAWN = pygame.image.load(IMAGE_BASE_DIR + 'pawn_dame_black.png')
            IMAGE_WHITE_PAWN = pygame.image.load(IMAGE_BASE_DIR + 'pawn_dame_white.png')

        self.draw_loading()
        pygame.display.flip()
        # time.sleep(2)

        self.draw_background()
        self.draw_heading()
        self.draw_leaderboard()
        self.draw_difficulty()
        pygame.display.update()

        running = True

        while running:

            if self.game.currentPlayer == "A":
                if self.game.checkIfLose("A"):
                    lose = True
                if len(selected_pawn) == 0:
                    mark_pawns = self.game.getPossiblePawnsForPlayer("A")
                else:
                    pass
            else:
                if self.game.checkIfLose("B"):
                    win = True
                else:
                    action = self.ki.getAction("B")
                    self.game.movePawn(action)
                    if self.game.checkIfWon("B"):
                        lose = True
                    else:
                        self.game.switchPlayer()
            self.draw_board()
            self.draw_leaderboard()
            self.draw_help_button()
            self.draw_quit_button()
            self.draw_stats()

            for row in self.game.gameField.gameField:
                for field in row:
                    if field is not None:
                        self.draw_pawn(field.posX, field.posY, "white" if field.player == "A" else "black")


            self.draw_quit_warning()
            self.draw_winning_screen(self.game.gameField.destoryedPawns["A"])
            self.draw_losing_screen(self.game.gameField.destoryedPawns["A"])

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()