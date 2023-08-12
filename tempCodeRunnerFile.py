import pygame
import json
import os

# Initialize Pygame
pygame.init()

# Load JSON data
def load_json(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print("Error loading JSON:", e)
        return None

# Create directory for save files
if not os.path.exists("saves"):
    os.makedirs("saves")

class VisualNovelGame:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("Visual Novel Engine")

        self.scenes_data = load_json("scenes.json")
        self.scenes = self.scenes_data["scenes"]

        # Initialize game state
        self.current_state = {
            "scene_index": 0,
            "dialogue_index": 0,
            "display_choices": False,
            "pause_menu_active": False
        }

        self.transition_alpha = 0
        self.transition_speed = 5  # Adjust this value to control the transition speed

        self.start_menu_active = True
        self.pause_menu_active = False

    def update(self):
        if self.transition_alpha > 0:
            self.transition_alpha -= self.transition_speed
            if self.transition_alpha < 0:
                self.transition_alpha = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.start_menu_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.start_menu_active = False
            else:
                if not self.pause_menu_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.handle_space_key()
                        elif event.key == pygame.K_ESCAPE:
                            self.pause_menu_active = True  # Activate the pause menu
                        elif event.key == pygame.K_s:  # Save state on 'S' key
                            self.save_state(0)  # Save to the first slot
                        elif event.key == pygame.K_l:  # Load state on 'L' key
                            self.load_state(0)  # Load from the first slot
                        elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                            slot_index = int(event.key) - pygame.K_1
                            self.save_state(slot_index)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.handle_mouse_click()
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.pause_menu_active = False  # Close the pause menu

    def handle_space_key(self):
        current_scene = self.scenes[self.current_state["scene_index"]]
        if self.current_state["display_choices"]:
            selected_choice = current_scene["choices"][self.current_state["dialogue_index"]]
            self.current_state["scene_index"] = selected_choice["next_scene"]
            self.current_state["display_choices"] = False
            self.current_state["dialogue_index"] = 0
        else:
            if self.current_state["dialogue_index"] < len(current_scene["dialogues"]) - 1:
                self.current_state["dialogue_index"] += 1
            elif "choices" in current_scene:
                self.current_state["display_choices"] = True
            else:
                self.transition_alpha = 255  # Start the fade-out transition
                self.current_state["dialogue_index"] = 0
                self.current_state["scene_index"] += 1

    def handle_mouse_click(self):
        current_scene = self.scenes[self.current_state["scene_index"]]
        if self.current_state["display_choices"]:
            for i, choice in enumerate(current_scene["choices"]):
                button_rect = pygame.Rect(
                    self.dialogue_rect.left + 20,
                    self.dialogue_rect.top + i * 40,
                    self.dialogue_rect.width - 40,
                    30
                )
                if self.is_mouse_over_button(pygame.mouse.get_pos(), button_rect):
                    self.current_state["scene_index"] = choice["next_scene"]
                    self.current_state["display_choices"] = False
                    self.current_state["dialogue_index"] = 0
                    break

    def is_mouse_over_button(self, mouse_pos, button_rect):
        return button_rect.collidepoint(mouse_pos)

    def render(self):
        current_scene = self.scenes[self.current_state["scene_index"]]
        mouse_pos = pygame.mouse.get_pos()
        self.screen.fill((255, 255, 255))

        # Display background
        background_image = pygame.image.load(current_scene["background"]).convert()
        background_image = pygame.transform.scale(background_image, (self.screen_width, self.screen_height))
        self.screen.blit(background_image, (0, 0))

        # Render dialogue box
        text_box_style = current_scene.get("text_box_style", {})  # Get the style data, or use default if not provided
        self.dialogue_rect = pygame.Rect(
            self.screen_width * 0.05,
            self.screen_height * 0.7,
            self.screen_width * 0.9,
            self.screen_height * 0.25
        )
        background_color = text_box_style.get("background_color", (220, 220, 220))
        border_color = text_box_style.get("border_color", (100, 100, 100))
        border_width = text_box_style.get("border_width", 2)
        transparency = text_box_style.get("transparency", 1.0)

        # Convert background_color to tuple if it's a list
        if isinstance(background_color, list):
            background_color = tuple(background_color)

        # Apply transparency
        surface = pygame.Surface((self.dialogue_rect.width, self.dialogue_rect.height), pygame.SRCALPHA)
        background_color_with_alpha = background_color + (int(255 * transparency),)
        pygame.draw.rect(surface, background_color_with_alpha, surface.get_rect())
        pygame.draw.rect(surface, border_color, surface.get_rect(), border_width)
        self.screen.blit(surface, self.dialogue_rect.topleft)

        y = self.dialogue_rect.top + 20

        if self.transition_alpha > 0:
            transition_overlay = pygame.Surface((self.screen_width, self.screen_height))
            transition_overlay.set_alpha(self.transition_alpha)
            transition_overlay.fill((0, 0, 0))  # Fill with black color
            self.screen.blit(transition_overlay, (0, 0))

        if not self.current_state["display_choices"]:
            self.render_text(
                current_scene["dialogues"][self.current_state["dialogue_index"]]["speaker"] +
                ": " + current_scene["dialogues"][self.current_state["dialogue_index"]]["text"],
                self.dialogue_rect.left + 10,
                y
            )
            y += 30
        else:
            for i, choice in enumerate(current_scene["choices"]):
                button_rect = pygame.Rect(
                    self.dialogue_rect.left + 20,
                    y + i * 40,  # Increased the spacing between buttons
                    self.dialogue_rect.width - 40,
                    30
                )
                color = (200, 200, 200) if self.is_mouse_over_button(mouse_pos, button_rect) else (150, 150, 150)

                pygame.draw.rect(self.screen, color, button_rect)
                self.render_text(
                    str(i + 1) + ". " + choice["text"],
                    button_rect.left + 5,
                    button_rect.centery - 10  # Center the text vertically in the button
                )
                y += 40  # Increment the y position for the next button

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

    def save_state(self, slot_index):
        state_copy = self.current_state.copy()
        self.scenes_data["scenes"] = self.scenes  # Update scenes data
        self.current_state["scene_index"] = max(0, min(self.current_state["scene_index"], len(self.scenes) - 1))
        self.current_state["dialogue_index"] = max(0, min(self.current_state["dialogue_index"], len(self.scenes[self.current_state["scene_index"]]["dialogues"]) - 1))
        self.scenes_data["current_state"] = state_copy
        self.save_game_data(self.scenes_data, f"saves/save_{slot_index}.json")

    def load_state(self, slot_index):
        try:
            with open(f"saves/save_{slot_index}.json", "r") as file:
                saved_data = json.load(file)
                self.scenes_data = saved_data
                self.scenes = saved_data["scenes"]
                self.current_state = saved_data["current_state"]
        except FileNotFoundError:
            pass

    def run(self):
        self.running = True
        while self.running:
            self.handle_input()
            self.update()

            if self.start_menu_active:
                self.start_menu_render()
            elif self.pause_menu_active:
                self.pause_menu_render()
            else:
                self.game_render()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def start_menu_render(self):
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
            
    def pause_menu_render(self):
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

    def game_render(self):
        self.render()

if __name__ == "__main__":
    game = VisualNovelGame()
    game.run()
