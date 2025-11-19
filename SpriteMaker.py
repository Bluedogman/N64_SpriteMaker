# sprite maker for the N64
# Copilot can suck my hairy fat balls
import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
FPS = 30

white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
orange = (255, 165, 0)
red = (255, 0, 0)
cyan = (0, 255, 255)
purple = (255, 0, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
background_color = (175, 175, 175)
colors = [blue, green, red, cyan, purple, orange, yellow, white, black]

font = pygame.font.SysFont("Arial", 15)
line_height = font.get_linesize()


class IDrawable:
    def draw(self):
        pass


class Button(IDrawable):
    def __init__(self, text, x, y, width, height):
        self.button_rect = pygame.Rect(x, y, width, height)

        self.text_x = x + width // 4
        self.text_y = y + 5
        self.text = text
        buttons.append(self)

    def draw(self):
        pygame.draw.rect(screen, background_color, self.button_rect)
        draw_text(self.text, self.text_x, self.text_y)

    def click(self):  # Fires when the button is clicked
        """hello"""
        print("meow")


buttons: list[Button] = []

File_button = Button("File", 0, 0, 50, 50)


def draw_text(text_string, Start_TextX, Start_TextY):
    lines = text_string.split("\n")
    for i, line in enumerate(lines):
        main_text = font.render(line, True, black)
        text_rect = main_text.get_rect(topleft=(Start_TextX, Start_TextY + i * line_height))  # random number to give some shakyness
        screen.blit(main_text, text_rect)


def collides(rect_1: pygame.Rect, button_list: list[Button]):
    button_rects = [button.button_rect for button in button_list]
    if (clicked_button_idx := rect_1.collidelist(button_rects)) and clicked_button_idx >= 0:  # If it collides with anything
        return buttons[clicked_button_idx]


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if pygame.mouse.get_pressed:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_width = 5
            mouse_height = 5
            mouse_rect = pygame.Rect(
                mouse_x - (mouse_width // 2),
                mouse_y - (mouse_height // 2),
                mouse_width,
                mouse_height,
            )  # normalize x and y to center the hitbox
            if (clicked_btn := collides(mouse_rect, buttons)) and clicked_btn is not None:
                clicked_btn.click()

        screen.fill(background_color)
        objs: list[IDrawable] = [File_button]
        for obj in objs:
            obj.draw()

        pygame.display.flip()
        clock.tick(FPS)


main()
pygame.quit()
