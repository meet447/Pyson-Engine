import pygame
import json

# Initialize Pygame
pygame.init()

class StartMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.title_text = self.font.render("Visual Novel Game", True, (0, 0, 0))
        self.start_text = self.font.render("Press SPACE to Start", True, (0, 0, 0))
        self.title_rect = self.title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.start_rect = self.start_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))

    def render(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.start_text, self.start_rect)
        

# Load JSON data
def load_json(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print("Error loading JSON:", e)
        return None

class VisualNovelGame:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("Visual Novel Engine")

        self.scene_index = 0
        self.dialogue_index = 0
        self.display_choices = False
        self.scenes = load_json("scenes.json")["scenes"]

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.handle_space_key()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click()

    def handle_space_key(self):
        current_scene = self.scenes[self.scene_index]
        if self.display_choices:
            selected_choice = current_scene["choices"][self.dialogue_index]
            self.scene_index = selected_choice["next_scene"]
            self.display_choices = False
            self.dialogue_index = 0
        else:
            if self.dialogue_index < len(current_scene["dialogues"]) - 1:
                self.dialogue_index += 1
            elif "choices" in current_scene:
                self.display_choices = True
            else:
                self.dialogue_index = 0
                self.scene_index += 1

    def handle_mouse_click(self):
        current_scene = self.scenes[self.scene_index]
        if self.display_choices:
            for i, choice in enumerate(current_scene["choices"]):
                button_rect = pygame.Rect(
                    self.dialogue_rect.left + 20,
                    self.dialogue_rect.top + i * 30,
                    self.dialogue_rect.width - 40,
                    30
                )
                if self.is_mouse_over_button(pygame.mouse.get_pos(), button_rect):
                    self.scene_index = choice["next_scene"]
                    self.display_choices = False
                    self.dialogue_index = 0
                    break

    def is_mouse_over_button(self, mouse_pos, button_rect):
        return button_rect.collidepoint(mouse_pos)

    def update(self):
        pass

    def render(self):
        current_scene = self.scenes[self.scene_index]
        mouse_pos = pygame.mouse.get_pos()
        self.screen.fill((255, 255, 255))

        # Display background
        background_image = pygame.image.load(current_scene["background"]).convert()
        background_image = pygame.transform.scale(background_image, (self.screen_width, self.screen_height))
        self.screen.blit(background_image, (0, 0))

        # Render dialogue box
        self.dialogue_rect = pygame.Rect(
            self.screen_width * 0.05,
            self.screen_height * 0.7,
            self.screen_width * 0.9,
            self.screen_height * 0.25
        )
        pygame.draw.rect(self.screen, (220, 220, 220), self.dialogue_rect)

        y = self.dialogue_rect.top + 20

        if not self.display_choices:
            self.render_text(
                current_scene["dialogues"][self.dialogue_index]["speaker"] +
                ": " + current_scene["dialogues"][self.dialogue_index]["text"],
                self.dialogue_rect.left + 10,
                y
            )
            y += 30
        else:
            for i, choice in enumerate(current_scene["choices"]):
                button_rect = pygame.Rect(
                    self.dialogue_rect.left + 20,
                    y + i * 30,
                    self.dialogue_rect.width - 40,
                    30
                )
                color = (150, 150, 150)
                if self.is_mouse_over_button(mouse_pos, button_rect):
                    color = (200, 200, 200)

                pygame.draw.rect(self.screen, color, button_rect)
                self.render_text(
                    str(i + 1) + ". " + choice["text"],
                    button_rect.left + 5,
                    button_rect.top + 5
                )

        # Display character sprites
        for character in current_scene["characters"]:
            character_sprite = pygame.image.load(character["sprite"]).convert_alpha()

            # Get the specified width and height from the JSON data
            sprite_width = character.get("width", 600)
            sprite_height = character.get("height", 500)

            # Scale the character sprite to the specified width and height
            character_sprite = pygame.transform.scale(character_sprite, (sprite_width, sprite_height))

            x = character["x"]  # Use the x-axis value

            if "side" in character and character["side"] == "right":
                x -= sprite_width  # Adjust the x-axis position for right-side characters
                character_sprite = pygame.transform.flip(character_sprite, True, False)

            y = self.dialogue_rect.top - sprite_height
            self.screen.blit(character_sprite, (x, y))

    def render_text(self, text, x, y):
        rendered_text = self.font.render(text, True, (0, 0, 0))
        self.screen.blit(rendered_text, (x, y))

    def run(self):
        self.running = True
        while self.running:
            self.handle_input()
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = VisualNovelGame()
    game.run()
