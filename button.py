"""Module containing interface features"""

import pygame.font


class Button:
    """Class representing stylish interactive button"""

    def __init__(self, game, msg):
        self.screen = game.screen

        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(
            0, 0, game.settings.screen_width // 6, game.settings.screen_height // 20
        )
        self.rect.centerx = game.settings.screen_width // 2
        self.rect.bottom = game.settings.screen_height - self.rect.height

        self.msg_image, self.msg_image_rect = None, None

        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Prepare text message as a pygame image"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Show button with the message on the screen in choosen position"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
