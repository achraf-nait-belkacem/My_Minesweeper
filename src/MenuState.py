import pygame
import sys
class MenuState:
    def __init__(self):
        self.font = pygame.font.Font(None, 50)

        self.bg_color = (51, 51, 51)
        self.button_color = (160, 160, 160)

        self.button_width = 250
        self.button_height = 60
        self.spacing = 20

    def draw(self, app):
        app.screen.fill(self.bg_color)

        
        center_x = app.screen.get_width() // 2 - self.button_width // 2
        start_y = 150

        
        self.play_button = pygame.Rect(center_x, start_y, self.button_width, self.button_height)
        self.settings_button = pygame.Rect(center_x, start_y + (self.button_height + self.spacing), self.button_width, self.button_height)
        self.scores_button = pygame.Rect(center_x, start_y + 2 * (self.button_height + self.spacing), self.button_width, self.button_height)
        self.quit_button = pygame.Rect(center_x, start_y + 3 * (self.button_height + self.spacing), self.button_width, self.button_height)

    
        pygame.draw.rect(app.screen, self.button_color, self.play_button)
        pygame.draw.rect(app.screen, self.button_color, self.settings_button)
        pygame.draw.rect(app.screen, self.button_color, self.scores_button)
        pygame.draw.rect(app.screen, self.button_color, self.quit_button)

        
        def draw_text(text, rect):
            surface = self.font.render(text, True, (0, 0, 0))
            rect_text = surface.get_rect(center=rect.center)
            app.screen.blit(surface, rect_text)

        draw_text("PLAY", self.play_button)
        draw_text("SETTINGS", self.settings_button)
        draw_text("BEST SCORES", self.scores_button)
        draw_text("QUIT", self.quit_button)

    def events(self, app, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.play_button.collidepoint(event.pos):
                print("Play")

            elif self.settings_button.collidepoint(event.pos):
                print("Settings")

            elif self.scores_button.collidepoint(event.pos):
                print("Scores")

            elif self.quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
    def update(self, app):
        pass