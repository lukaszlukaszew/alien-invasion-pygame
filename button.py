"""Module containing interface features"""

import pygame.font


class Button:
    """Class representing stylish interactive button"""

    def __init__(self, screen, msg):
        """Initialize basic characteristics of the button"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # button looks
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # buttons rect
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.height - self.rect.height

        # message
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Prepare message at the center of the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Show button with the message on the screen"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
