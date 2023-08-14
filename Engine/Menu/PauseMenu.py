import pygame
import json

class PauseMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.resume_text = self.font.render("Resume", True, (0, 0, 0))
        self.quit_text = self.font.render("Quit to Main Menu", True, (0, 0, 0))
        self.resume_rect = self.resume_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.quit_rect = self.quit_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))

    def render(self, screen):
        screen.fill((200, 200, 200))
        pygame.draw.rect(screen, (255, 255, 255), (self.screen_width // 4, self.screen_height // 4,
                         self.screen_width // 2, self.screen_height // 2))
        screen.blit(self.resume_text, self.resume_rect)
        screen.blit(self.quit_text, self.quit_rect)