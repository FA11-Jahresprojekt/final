import pygame
from pygame import mixer

import Util
import Variables
from Database import Database
from Renderer import Renderer

pygame.init()

clock = pygame.time.Clock()

# Sounds
MUSIC_BASE_DIR = "assets/sounds/"
mixer.music.load(MUSIC_BASE_DIR + "click.ogg")
mixer.music.set_volume(0.1)

# FONT
pygame.font.init()

class GuiGameMenu:
    def __init__(self, guiFrom, screen, headerImage, gameImage, gameName):
        self.db = Database.getInstance()
        self.renderer = Renderer(screen)
        self.screen = screen

        self.headerImage = headerImage
        self.gameImage = gameImage
        self.guiFrom = guiFrom

        self.running = True
        self.player_id = Variables.getPlayerId()

        self.buttons = []
        print(f'init buttons: {self.buttons}')

        self.difficulty = 3
        self.gameName = gameName

    def run(self):
        clock.tick(60)

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

        if "difficulty" in name:
            self.difficulty = int(name.split("_")[1])
            self.draw_menu()

        if name == "logout":
            Variables.PLAYER_ID = None
            self.guiFrom.gui_login.runLoginScreen()
            self.running = False

        if name == "back":
            self.guiFrom.run()
            self.running = False

    def draw_menu(self):
        self.buttons.clear()
        self.renderer.draw_background()

        headerBtns = self.renderer.draw_heading(self.gameName, Variables.getPlayerName(), True, True)
        self.buttons = Util.append_array_to_array(self.buttons, headerBtns)

        dButtons = self.renderer.draw_game_preview(self.headerImage, self.gameImage, 80, 160, self.difficulty, 400, 275)
        self.buttons = Util.append_array_to_array(self.buttons, dButtons)

        self.draw_scores()
        pygame.display.update()

    def getGameHistory(self):

        # get stats for game_type and difficulty
        if self.difficulty == -1:
            games_summary_player = self.db.getGameHistoryForChosenPlayerFiltered(self.player_id, self.gameName)
        else:
            games_summary_player = self.db.getGameHistoryForChosenPlayerFiltered(self.player_id, self.gameName, self.difficulty)

        return games_summary_player

    def draw_scores(self):
        x = 80
        y = 160
        widthX = 400
        size = 87

        games_summary_player = self.getGameHistory()

        # calculate stats based on game history
        total_games_played = len(games_summary_player)
        total_games_won = sum(1 for game in games_summary_player if game[2] == "won")
        total_games_lost = sum(1 for game in games_summary_player if game[2] == "lost")
        total_games_canceled = sum(1 for game in games_summary_player if game[2] == "cancelled")
        total_pawns_destroyed = sum(game[3] for game in games_summary_player)

        self.renderer.draw_score_card(x + widthX + 40, y + 150, size, size, "PLAYED GAMES", total_games_played)
        self.renderer.draw_score_card(x + widthX + 40 + (size + 10), y + 150, size, size, "WON GAMES", total_games_won)
        self.renderer.draw_score_card(x + widthX + 40 + (size + 10) * 2, y + 150, size, size, "LOST GAMES", total_games_lost)
        self.renderer.draw_score_card(x + widthX + 40 + (size + 10) * 3, y + 150, size, size, "CANCELLED GAMES", total_games_canceled)
        self.renderer.draw_score_card(x + widthX + 40 + (size + 10) * 4, y + 150, size, size, "DESTROYED PAWNS", total_pawns_destroyed)

    def getOwnScore(self, gameName, difficulty, playerID):
        ownScore = self.db.getGamesSummaryForGameAndDifficultyAndPlayerID(gameName, difficulty, playerID)
        return ownScore