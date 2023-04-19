import time

import pygame
from pygame import mixer

import Util
import Variables
from Database import Database
from GuiGameMenu import GuiGameMenu
from GuiLogin import GuiLogin
from GuiUserProfile import GuiUserProfile
from Renderer import Renderer

pygame.init()

clock = pygame.time.Clock()

# SCREEN
SCREEN = pygame.display.set_mode((Variables.SCREEN_WIDTH, Variables.SCREEN_HEIGHT))
pygame.display.set_caption(Variables.LAUNCHER_TITLE)
pygame.display.set_icon(pygame.image.load(Variables.DIR_IMAGES + "favicon.png"))

# Sounds
MUSIC_BASE_DIR = "assets/sounds/"
mixer.music.load(MUSIC_BASE_DIR + "click.ogg")
mixer.music.set_volume(0.1)

# FONT
pygame.font.init()

# IMAGE
BAUERNSCHACH_IMAGE = pygame.image.load(Variables.DIR_IMAGES + "games/bauernschach.png")
BAUERNSCHACH_HEADER_IMAGE = pygame.image.load(Variables.DIR_IMAGES + "headings/bauernschach.png")

DAME_IMAGE = pygame.image.load(Variables.DIR_IMAGES + "games/dame.png")
DAME_HEADER_IMAGE = pygame.image.load(Variables.DIR_IMAGES + "headings/dame.png")

IMAGE_GROUP = pygame.image.load(Variables.DIR_IMAGES + "group.png")

class GuiMainMenu:
    def __init__(self):
        self.db = Database.getInstance()
        self.renderer = Renderer(SCREEN)
        self.splash = True
        self.running = True

        self.buttons = []
        self.gui_login = None

        self.dame_difficulty = 3
        self.bauernschach_difficulty = 3

        if Variables.PLAYER_ID == None:
            self.gui_login = GuiLogin(self)
            self.gui_login.runLoginScreen()
            self.running = False

    def run(self):
        clock.tick(60)

        if self.splash:
            mixer.init()
            mixer.music.load(MUSIC_BASE_DIR + "pling.mp3")
            mixer.music.play()
            self.splash = False
            self.renderer.draw_background()
            SCREEN.blit(IMAGE_GROUP, (Variables.SCREEN_WIDTH / 2 - IMAGE_GROUP.get_width() / 2, Variables.SCREEN_HEIGHT / 2 - IMAGE_GROUP.get_height() / 2))
            pygame.display.flip()
            time.sleep(2)
            mixer.music.load(MUSIC_BASE_DIR + "click.ogg")

        self.draw_menu()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button['rect'].collidepoint(pygame.mouse.get_pos()):
                            self.on_click(button['name'])
                if event.type == pygame.QUIT:
                    self.running = False

    def on_click(self, name):
        mixer.music.play()

        if name == "btn.bauernschach":
            GuiGameMenu(self, SCREEN, BAUERNSCHACH_HEADER_IMAGE, BAUERNSCHACH_IMAGE, "Bauernschach").run()
            self.running = False

        if name == "profile":
            if Variables.PLAYER_ID != -1:
                GuiUserProfile(self).runUserProfile()
                self.running = False

        if name == "back":
            Variables.PLAYER_ID = None
            self.gui_login.runLoginScreen()
            self.running = False

        if name == "btn.dame":
            GuiGameMenu(self, SCREEN, DAME_HEADER_IMAGE, DAME_IMAGE, "Dame").run()
            self.running = False

        if "_difficulty_" in name:
            difficulty = int(name.split("_")[2])
            game_type = name.split("_")[0]

            if game_type == "bauernschach":
                self.bauernschach_difficulty = difficulty
                self.draw_highscores()
            elif game_type == "dame":
                self.dame_difficulty = difficulty
                self.draw_highscores()


    def draw_menu(self):

        self.renderer.draw_background()
        headerBtns = self.renderer.draw_heading("Spielesammlung", Variables.PLAYER_ID['name'], True, True)

        if headerBtns is not None:
            self.buttons = Util.append_array_to_array(self.buttons, headerBtns)

        buttonBauernschach = self.renderer.draw_game_card(BAUERNSCHACH_HEADER_IMAGE, BAUERNSCHACH_IMAGE, 80, 160)
        buttonDame = self.renderer.draw_game_card(DAME_HEADER_IMAGE, DAME_IMAGE, 80, 420)

        self.buttons.append({'rect': buttonBauernschach, 'name': 'btn.bauernschach'})
        self.buttons.append({'rect': buttonDame, 'name': 'btn.dame'})

        self.draw_highscores()

        pygame.display.update()

    def draw_highscores(self):
        for button in self.buttons:
            if "_difficulty_" in button['name']:
                self.buttons.remove(button)

        difficultyButtonsBauernschach = self.renderer.draw_highscore_list(
            "bauernschach",
            BAUERNSCHACH_HEADER_IMAGE,
            480,
            160
        )
        difficultyButtonsDame = self.renderer.draw_highscore_list(
            "dame",
            DAME_HEADER_IMAGE,
            760,
            160
        )

        scoresBauernschach = self.renderer.draw_highscores_on_list(
            480,
            160,
            self.getHighscores("Bauernschach", self.bauernschach_difficulty, 10)
        )

        scoresDame = self.renderer.draw_highscores_on_list(
            760,
            160,
            self.getHighscores("Dame", self.dame_difficulty, 10)
        )

        self.buttons = Util.append_array_to_array(self.buttons, difficultyButtonsBauernschach)
        self.buttons = Util.append_array_to_array(self.buttons, difficultyButtonsDame)

        pygame.display.update()


    def getHighscores(self, game_type, difficulty, player_count):
        bestPlayers = self.db.getTopPlayersForGameAndDifficulty(game_type, difficulty, player_count)
        return bestPlayers


GuiMainMenu().run()