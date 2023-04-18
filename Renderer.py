import pygame

import Variables

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK90 = (25, 25, 25)
COLOR_BLACK80 = (50, 50, 50)

class Renderer:
    def __init__(self, screen):
        self.screen = screen

        self.score_background_image = pygame.image.load(Variables.DIR_IMAGES + "score_background.png")
        self.button_quad_image = pygame.image.load(Variables.DIR_IMAGES + "button_quad.png")
        self.button_quad_selected_image = pygame.image.load(Variables.DIR_IMAGES + "button_quad_selected.png")
        self.background_image = pygame.image.load(Variables.DIR_IMAGES + "background.png")
        self.user_image = pygame.image.load(Variables.DIR_IMAGES + "profile_default.png")
        self.undo_image = pygame.image.load(Variables.DIR_IMAGES + "undo_button.png")
        self.button_wide_image = pygame.image.load(Variables.DIR_IMAGES + "button_wide.png")
        self.button_image = pygame.image.load(Variables.DIR_IMAGES + "button.png")
        self.score_card = pygame.image.load(Variables.DIR_IMAGES + "score_card.png")

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

    def draw_game_preview(self, title_image, image, x, y, difficulty, widthX=320, widthY=220):
        offset = 4
        buttons = []

        pygame.draw.rect(self.screen, (0, 0, 0), (x - offset, y - offset, widthX + offset * 2, widthY + offset * 2), border_radius=offset * 2)
        self.screen.blit(pygame.transform.scale(image, (widthX, widthY)), (x, y))

        self.screen.blit(pygame.transform.scale(title_image, (400, 48)), (x, y + widthY + 10))

        difficulties = 5

        label = self.get_font(30, True).render("SCHWIERIGKEIT & STATS", True, COLOR_WHITE)
        self.screen.blit(label, (x + widthX + 40 + (500 / 2) - (label.get_width() / 2), y))

        for i in range(difficulties):
            size = 87
            selected = i == difficulty - 1
            button = self.draw_quad_button(x + widthX + 40 + i * (size + 10), y + 42, size, size, str(i + 1), selected, 50)
            buttons.append({'rect': button, 'name': 'difficulty_' + str(i + 1)})

        button = self.screen.blit(pygame.transform.scale(self.button_image, (920, 123)), (x, Variables.SCREEN_HEIGHT - 150))
        label = self.get_font(45).render("SPIELEN", True, COLOR_WHITE)
        self.screen.blit(label, (x + (920 / 2) - (label.get_width() / 2), Variables.SCREEN_HEIGHT - 150 + (123 / 2) - (label.get_height() / 2)))

        buttons.append({'rect': button, 'name': 'play'})

        return buttons

    def draw_score_card(self, x, y, width, height, title, value):
        self.screen.blit(pygame.transform.scale(self.score_card, (width, height)), (x, y))

        # calculate font size based on width
        font_size = 20
        while self.get_font(font_size, True).render(title, True, COLOR_WHITE).get_width() > width - 22:
            font_size -= 1

        if " " in title:
            texts = title.split(" ")
            font_size = 12
        else:
            texts = [title]

        for i in range(len(texts)):
            title_text = self.get_font(font_size, True).render(texts[i], True, COLOR_WHITE)
            self.screen.blit(title_text, (x + (width / 2) - (title_text.get_width() / 2) + 2, y + (height - 18) - (title_text.get_height() / 2) - 10 * (len(texts) - 1) + 13 * i))

        value_text = self.get_font(45, True).render(value, True, COLOR_WHITE)
        self.screen.blit(value_text, (x + (width / 2) - (value_text.get_width() / 2) + 3, y + (height / 2) - (value_text.get_height() / 2) - 8))

        return pygame.Rect(x, y, width, height)

    def draw_quad_button(self, x, y, width, height, text, selected=False, font_size=30):
        if selected:
            self.screen.blit(pygame.transform.scale(self.button_quad_selected_image, (width, height)), (x, y))
        else:
            self.screen.blit(pygame.transform.scale(self.button_quad_image, (width, height)), (x, y))

        text = self.get_font(font_size).render(text, True, COLOR_WHITE)

        self.screen.blit(text, (x + (width / 2) - (text.get_width() / 2) + 3, y + (height / 2) - (text.get_height() / 2)))

        return pygame.Rect(x, y, width, height)

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

        return pygame.Rect(profile_image_pos_x, profile_image_pos_y, 30 + username_text.get_width(), 30)

    def draw_heading(self, header, username, back=False):
        buttons = []

        pygame.Surface.fill(self.screen, COLOR_BLACK90, rect=(0, 0, 1080, 60))
        pygame.Surface.fill(self.screen, COLOR_BLACK80, rect=(0, 60, 1080, 3))
        logout = self.draw_user(username, Variables.SCREEN_WIDTH - 20, 16)

        heading = self.get_font(26, True).render(header, True, COLOR_WHITE)

        add = 0
        backBtn = None
        if back:
            add = 40
            backBtn = self.screen.blit(pygame.transform.scale(self.undo_image, (20, 20)), (25, 21))

        self.screen.blit(heading, (20 + add, 16))

        buttons.append({'rect': logout, 'name': 'logout'})
        if back:
            buttons.append({'rect': backBtn, 'name': 'back'})

        return buttons

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



