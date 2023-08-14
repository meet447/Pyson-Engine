import pygame
import json

class StartMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)

        with open("main_menu.txt", "r") as file:
            menu_data = json.load(file)
            self.title_text = self.font.render(menu_data["title"], True, (0, 0, 0))

            self.option_texts = []
            for option in menu_data["options"]:
                self.option_texts.append(self.font.render(option, True, (0, 0, 0)))

        self.title_rect = self.title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.option_rects = []
        for i, option_text in enumerate(self.option_texts):
            option_rect = option_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + i * 50))
            self.option_rects.append(option_rect)

    def render(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.title_text, self.title_rect)
        for i, option_text in enumerate(self.option_texts):
            screen.blit(option_text, self.option_rects[i])