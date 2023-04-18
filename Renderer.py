import pygame

import Variables

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK90 = (25, 25, 25)
COLOR_BLACK80 = (50, 50, 50)

class Renderer:
    def __init__(self, screen):
        self.screen = screen

        self.score_background_image = pygame.image.load(Variables.DIR_IMAGES + "score_background.png")
        self.background_image = pygame.image.load(Variables.DIR_IMAGES + "background.png")
        self.user_image = pygame.image.load(Variables.DIR_IMAGES + "profile_default.png")

    def draw_background(self):
        self.screen.blit(self.background_image, (0, 0))

    def get_font(self, size, bold=False, italic=False):
        if bold and italic:
            return pygame.font.Font(Variables.DIR_FONTS + "MinecraftBoldItalic.otf", size)
        if bold:
            return pygame.font.Font(Variables.DIR_FONTS + "MinecraftBold.otf", size)
        if italic:
            return pygame.font.Font(Variables.DIR_FONTS + "MinecraftItalic.otf", size)
        else:
            return pygame.font.Font(Variables.DIR_FONTS + "MinecraftRegular.otf", size)

    def draw_game_card(self, title_image, image, x, y, widthX=320, widthY=220):
        offset = 4

        rect = pygame.draw.rect(self.screen, (0, 0, 0), (x - offset, y - offset, widthX + offset * 2, widthY + offset * 2), border_radius=offset * 2)
        self.screen.blit(pygame.transform.scale(image, (widthX, widthY)), (x, y))
        self.screen.blit(pygame.transform.scale(title_image, (widthX, 40)), (x, y - 25))

        return rect

    def draw_user(self, username, x, y):
        # Load and scale profile image
        profile_image = self.user_image.convert_alpha()
        profile_image_scaled = pygame.transform.smoothscale(profile_image, (30, 30))
        profile_image_pos_y = y
        username_text = self.get_font(20).render(username, True, COLOR_WHITE)
        username_pos_x = x - username_text.get_width()  # username_pos_x = profile_image_pos_x + 30 + 10
        username_pos_y = profile_image_pos_y + (
                (profile_image_scaled.get_height() / 2) - (username_text.get_height() / 2))
        profile_image_pos_x = username_pos_x - 20 - profile_image.get_width()

        # Create circular mask for profile image
        mask_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(mask_surface, (255, 255, 255, 255), (15, 15), 15)

        # Apply mask to profile image
        masked_profile_image = profile_image_scaled.copy()
        masked_profile_image.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Draw
        self.screen.blit(masked_profile_image, (profile_image_pos_x, profile_image_pos_y))
        self.screen.blit(username_text, (username_pos_x, username_pos_y))

    def draw_heading(self, header, username):
        pygame.Surface.fill(self.screen, COLOR_BLACK90, rect=(0, 0, 1080, 60))
        pygame.Surface.fill(self.screen, COLOR_BLACK80, rect=(0, 60, 1080, 3))
        self.draw_user(username, Variables.SCREEN_WIDTH - 20, 16)

        heading = self.get_font(26, True).render("Spielesammlung", True, COLOR_WHITE)
        self.screen.blit(heading, (20, 16))

    def draw_highscore_list(self, game, header_image, x, y):
        width = 240
        height = 480
        buttons = []

        highscore_posX = x
        highscore_posY = y

        self.screen.blit(self.score_background_image, (x, y))
        self.screen.blit(pygame.transform.scale(header_image, (width, 26)), (x, y - 30))

        text = self.get_font(24, True).render("SCHWIERIGKEIT", True, COLOR_WHITE)
        text_rect = text.get_rect(center=(x + width / 2, highscore_posY + 30))
        self.screen.blit(text, text_rect)

        button_width = (((width - 40) - 40) / 5)
        button_height = 30
        button_spacing = 10
        difficulty = 5
        for i in range(difficulty):
            button_x = highscore_posX + 20 + i * (button_width + button_spacing)
            button_y = highscore_posY + 50
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

            # draw button border
            button = pygame.draw.rect(self.screen, (230, 230, 230), button_rect, border_radius=15, width=3)

            # draw button background
            gradient = pygame.Surface((button_width, button_height)).convert_alpha()
            gradient.fill((0, 0, 0, 0))
            pygame.draw.rect(gradient, (255, 255, 255, 50), gradient.get_rect(), border_radius=15)
            pygame.draw.rect(gradient, (255, 255, 255, 30), gradient.get_rect().inflate(-5, -5), border_radius=15)
            self.screen.blit(gradient, button_rect)

            button_name = game + "_difficulty_" + str(i + 1)
            button_dict = {'rect': button_rect, 'name': button_name}
            buttons.append(button_dict)

            # draw button text
            text = self.get_font(22).render(str(i + 1), True, COLOR_WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

        return buttons

    def draw_highscores_on_list(self, x, y, highscore_list):
        removeable = []
        width = 240
        for i in highscore_list:
            place = i[0]
            name = i[1]
            score = i[4]

            text = self.get_font(24).render(str(place) + ". " + name, True, COLOR_WHITE)
            scoreText = self.get_font(24, True).render(str(score), True, COLOR_WHITE)

            rect = self.screen.blit(text, (x + 20, y + 100 + (place - 1) * 30))
            rect2 = self.screen.blit(scoreText, (x + width - 20 - scoreText.get_width(), y + 100 + (place - 1) * 30))
            removeable.append(rect)
            removeable.append(rect2)



