import pygame
from pygame import mixer

import Util
import Variables
from Database import Database
from GuiGameMenu import GuiGameMenu
from Renderer import Renderer

pygame.init()

clock = pygame.time.Clock()

# Sounds
MUSIC_BASE_DIR = "assets/sounds/"
mixer.music.load(MUSIC_BASE_DIR + "click.ogg")
mixer.music.set_volume(0.1)

# SCREEN
SCREEN = pygame.display.set_mode((Variables.SCREEN_WIDTH, Variables.SCREEN_HEIGHT))
pygame.display.set_caption(Variables.LAUNCHER_TITLE)
pygame.display.set_icon(pygame.image.load(Variables.DIR_IMAGES + "favicon.png"))


class GuiUserProfile:
    def __init__(self, guiFrom):
        self.running = True
        self.db = Database.getInstance()
        self.renderer = Renderer(SCREEN)
        self.guiFrom = guiFrom

        self.buttons = []
        self.difficulty = 3
        self.game_type = '-1'

        self.username = Variables.getPlayerName()
        self.player_id = Variables.getPlayerId()

    def runUserProfile(self):

        clock.tick(60) # set FPS
        self.drawUserProfile()

        while self.running:
            for event in pygame.event.get():

                # on Quit
                if event.type == pygame.QUIT:
                    running = False

                # On Click
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    # inside button bounds
                    for button in self.buttons:
                        # print(self.buttons)
                        # print(button)
                        if button['rect'].collidepoint(pygame.mouse.get_pos()):
                            self.onClick(button['name'])


        pygame.quit()

    def onClick(self, buttonName):
        mixer.music.play()

        if "difficulty_" in buttonName:
            difficulty = int(buttonName.split("_")[1])

            if difficulty == self.difficulty:
                self.difficulty = -1
            else:
                self.difficulty = difficulty

            self.drawUserProfile()

        if buttonName == 'bauernschach_selected':
            game_type = 'Bauernschach'

            if game_type == self.game_type:
                self.game_type = '-1'
            else:
                self.game_type = game_type

            self.drawUserProfile()
            print('bauernschach selected')

        if buttonName == 'dame_selected':
            game_type = 'Dame'

            if game_type == self.game_type:
                self.game_type = '-1'
            else:
                self.game_type = game_type

            self.drawUserProfile()
            print('dame selected')

        if buttonName == "back":
            self.guiFrom.run()
            self.running = False


    def drawUserProfile(self):
        self.buttons.clear()

        # Background
        self.renderer.draw_background()
        # background_screen = pygame.Surface.fill(SCREEN, (125, 125, 125), rect=(80, 80, 920, 560))

        # Header
        backBtn = self.renderer.draw_heading("Mein Profil", self.username, True, False)
        self.buttons = Util.append_array_to_array(self.buttons, backBtn)

        # Profile
        user_image_rect = self.renderer.draw_user_profile_image_and_name(160, 120, self.username)
        player_stats_rect = self.drawPlayerStats(user_image_rect)
        difficulty_buttons = self.drawDifficultyButtons(player_stats_rect)
        self.buttons = Util.append_array_to_array(self.buttons, difficulty_buttons)

        self.drawGameSelection()
        self.drawPlayerGameHistory()

        # Game History

        pygame.display.update()

    def getGameHistory(self):
        # if difficulty and game not selected
        if self.difficulty == -1 and self.game_type == '-1':
            # show all stats
            games_summary_player = self.db.getGameHistoryForChosenPlayerFiltered(self.player_id)
        # else get stats for game_type and difficulty
        elif self.difficulty == -1:
            games_summary_player = self.db.getGameHistoryForChosenPlayerFiltered(self.player_id, self.game_type)
        elif self.game_type == '-1':
            games_summary_player = self.db.getGameHistoryForChosenPlayerFiltered(self.player_id, None, self.difficulty)
        else:
            games_summary_player = self.db.getGameHistoryForChosenPlayerFiltered(self.player_id, self.game_type, self.difficulty)

        return games_summary_player

    def drawPlayerStats(self, user_image_rect):

        games_summary_player = self.getGameHistory()
        player_stats_rect = self.renderer.draw_player_stats(user_image_rect.right + 20, user_image_rect.bottom - 80, 80,
                                                            80, games_summary_player)

        return player_stats_rect

    def drawDifficultyButtons(self, player_stats_rect):
        # stuff
        difficulty_buttons = self.renderer.draw_difficulty_buttons(player_stats_rect.x, player_stats_rect.top - 10 - 40, width=40, height=40,
                                              button_font_size=26, label_font_size=18, selected_difficulty=self.difficulty)

        pygame.display.update()
        return difficulty_buttons

    def drawGameSelection(self):

        bauernschach_selected = False
        if self.game_type == 'Bauernschach':
            bauernschach_selected = True
        button_bauernschach = self.renderer.draw_quad_button(650, 150, 80, 80, 'Bauernschach', bauernschach_selected, 12)
        self.buttons.append({'rect': button_bauernschach, 'name': 'bauernschach_selected'})

        dame_selected = False
        if self.game_type == 'Dame':
            dame_selected = True
        button_dame = self.renderer.draw_quad_button(button_bauernschach.right + 10, 150, 80, 80, 'Dame', dame_selected, 12)
        self.buttons.append({'rect': button_dame, 'name': 'dame_selected'})


    def drawPlayerGameHistory(self):
        # stuff (160, 340, 760, 260)
        games_summary_player = self.getGameHistory()
        self.renderer.drawGameHistory(160, 340, 760, 260, games_summary_player)
        pygame.display.update()