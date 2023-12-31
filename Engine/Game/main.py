import pygame
from Data.data import load_json
from Menu.PauseMenu import PauseMenu
from Menu.StartMenu import StartMenu
import json, random

pygame.init()

class VisualNovelGame:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        
        
        self.slide_x = 100  # Initialize the slide X-coordinate
        self.screen_shake = 0  # Initialize screen shake displacement


        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("Pyson Game Engine")
        
        self.transition_alpha = 0
        self.transition_speed = 5  # Adjust this value to control the transition speed

        self.scene_index = 0
        self.dialogue_index = 0
        self.display_choices = False
        self.scenes = load_json("script.json")["scenes"]

        self.save_slots = 3  # Number of available save slots
        self.game_states = []

        # Load existing saved states or initialize new ones
        for i in range(self.save_slots):
            loaded_state = self.load_game_data(f"save_{i}")
            if loaded_state is not None:
                self.game_states.append(loaded_state)
            else:
                self.game_states.append({
                    "scene_index": 0,
                    "dialogue_index": 0,
                    "display_choices": False,
                    "pause_menu_active": False
                })

        self.current_state = self.game_states[0]

        self.start_menu = StartMenu(self.screen_width, self.screen_height)
        self.start_menu_active = True

        self.pause_menu = PauseMenu(self.screen_width, self.screen_height)
        self.pause_menu_active = False
        
    def update(self):
        if self.transition_alpha > 0:
            self.transition_alpha -= self.transition_speed
            if self.transition_alpha < 0:
                self.transition_alpha = 0
                
        if self.screen_shake > 0:
            self.screen_shake = max(0, self.screen_shake - 1)  # Gradually reduce the screen_shake magnitude

    def save_game_data(self, data, filename):
        with open(f"saves/{filename}.json", "w") as file:
            json.dump(data, file)

    def load_game_data(self, filename):
        try:
            with open(f"saves/{filename}.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return None

    def save_state(self, slot_index):
        state_copy = self.current_state.copy()
        self.game_states[slot_index] = state_copy
        self.save_game_data(state_copy, f"save_{slot_index}")

    def load_state(self, slot_index):
        if slot_index < len(self.game_states):
            self.current_state = self.game_states[slot_index].copy()

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
            return
        else:
            if self.current_state["dialogue_index"] < len(current_scene["dialogues"]) - 1:
                self.current_state["dialogue_index"] += 1
            elif "choices" in current_scene:
                self.current_state["display_choices"] = True
            else:
                if current_scene.get("transition_effect") == "shake":
                    self.shake_screen(magnitude=10, duration=100)  # Adjust magnitude and duration as needed
                else:
                    self.transition_alpha = 255
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
                    print("clickkk")
                    self.current_state["scene_index"] = choice["next_scene"]
                    self.current_state["display_choices"] = False
                    self.current_state["dialogue_index"] = 0
                    break  # Remove this break to iterate through all choices

    def is_mouse_over_button(self, mouse_pos, button_rect):
        return True
    
    def shake_screen(self, magnitude, duration):
        self.screen_shake = magnitude
        pygame.time.set_timer(pygame.USEREVENT + 1, duration)
        
        
    def render(self):
        current_scene = self.scenes[self.current_state["scene_index"]]
        mouse_pos = pygame.mouse.get_pos()
        self.screen.fill((255, 255, 255))
        

        # Apply transition effect based on JSON data
        transition_effect = current_scene.get("transition_effect")
        print(transition_effect)

        if transition_effect == "slide_left":
            if self.transition_alpha > 0:
                self.slide_x -= 10
                if self.slide_x <= -self.screen_width:
                    self.transition_alpha = 0
                    self.slide_x = 0

        # Display background based on transition
        background_image = pygame.image.load(current_scene["background"]).convert()
        if transition_effect == "slide_left":
            background_image = pygame.transform.scale(background_image, (self.screen_width, self.screen_height))
            self.screen.blit(background_image, (self.slide_x, 0))
        elif transition_effect == "shake":
            if self.screen_shake > 0:
                shake_offset = (random.randint(-self.screen_shake, self.screen_shake), random.randint(-self.screen_shake, self.screen_shake))
            else:
                shake_offset = (0, 0)
        else:
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
            pygame.display.flip()

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

    def run(self):
        self.running = True
        while self.running:
            self.handle_input()
            self.update()

            if self.start_menu_active:
                self.start_menu.render(self.screen)
            elif self.pause_menu_active:
                self.pause_menu.render(self.screen)
            else:
                self.render()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
