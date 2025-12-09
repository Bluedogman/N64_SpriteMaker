# sprite maker for the N64
import pygame, pathlib
from PIL import Image
import numpy as np

pygame.init()
screen_height = 480
screen_width = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
FPS = 30

canvas_height = int(screen_height // 1.2) + 50
canvas_width = int(screen_width // 1.2)

cell_size = 60
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


buttons: list["Button"] = []


# Kinda a super-class for the the current user
class User:
    def __init__(self) -> None:
        self.tool = 1  # 1=pen, 2=eraser, 3=bucket
        self.active_color = black  # default

        # 8 bit can hold one 256-color palette, 4bit can hold 16 different palettes each with 16 colors
        self.texture_format = "8bit"  # 8 bit, 4 bit

    def change_tool(self, next_tool: str | int):  # Surely over-complicated
        if isinstance(next_tool, str):
            match next_tool.strip().lower():
                case "pen":
                    self.tool = 1
                case "eraser":
                    self.tool = 2
                case "bucket":
                    self.tool = 3
        else:
            self.tool = next_tool


class IDrawable:
    def draw(self):
        pass


class Button(IDrawable):
    def __init__(self, text, x, y, width, height, color, text_color):
        self.button_rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text_x = x + (width // 4) - 7
        self.text_y = y
        self.text = text
        self.text_color = text_color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.button_rect)
        draw_text(self.text, self.text_x, self.text_y, self.text_color)

    def click(self):  # Fires when the button is clicked
        print("")


class ExportButton(Button):
    def __init__(self, text, x, y, width, height, color, text_color=black):
        super().__init__(text, x, y, width, height, color, text_color)

    def click(self):
        if user.texture_format == "8bit":  # (height, width, 3)
            raw_colors = [cell.color for cell in grid_cells]
            pixels = np.array(raw_colors, dtype=np.uint8)
            if pixels.size == canvas_height // cell_size * canvas_width // cell_size * 3:
                pixels = pixels.reshape((canvas_height // cell_size, canvas_width // cell_size, 3))
            else:
                print("Image format is Invalid.")

            image = Image.fromarray(pixels)
            image.save("Output_image.png")

        else:  # user.texture_format == "5bit"
            raw_colors = [cell.color for cell in grid_cells]
            pixels = np.array(raw_colors, dtype=np.uint8)

            image = Image.fromarray(pixels >> 3)  # bitshift by 3 to convert to 5 bit color data
            image.save("Output_image.png")


class PenButton(Button):
    def __init__(self, text, x, y, width, height, color, text_color=black):
        super().__init__(text, x, y, width, height, color, text_color)

    def draw(self):
        pygame.draw.rect(screen, user.active_color, self.button_rect)
        if user.active_color == black:
            draw_text(self.text, self.text_x, self.text_y, white)
        else:
            draw_text(self.text, self.text_x, self.text_y, self.text_color)

    def click(self):
        user.change_tool(1)
        print("Changed to Pen")


class BucketButton(Button):
    def __init__(self, text, x, y, width, height, color, text_color=black):
        super().__init__(text, x, y, width, height, color, text_color)

    def draw(self):
        pygame.draw.rect(screen, user.active_color, self.button_rect)
        if user.active_color == black:
            draw_text(self.text, self.text_x, self.text_y, white)
        else:
            draw_text(self.text, self.text_x, self.text_y, self.text_color)

    def click(self):
        user.change_tool("bucket")
        print("Changed to bucket")


class EraserButton(Button):
    def __init__(self, text, x, y, width, height, color, text_color=black):
        super().__init__(text, x, y, width, height, color, text_color)

    def draw(self):
        pygame.draw.rect(screen, background_color, self.button_rect)
        pygame.draw.rect(screen, black, self.button_rect, 2)
        draw_text(self.text, self.text_x, self.text_y + 5, self.text_color)

    def click(self):
        user.change_tool("eraser")
        print("Changed to eraser")


class PaletteButton(Button):
    def __init__(self, x, y, width, height, color, text=""):
        super().__init__(text, x, y, width, height, color, text_color=color)

    def click(self):
        old_color = user.active_color
        user.active_color = self.color
        self.verify_color(old_color)

    def verify_color(self, old_color):
        if old_color != user.active_color:
            print(f"active color is now {user.active_color}!")
        else:
            print(f"Sowwyy... I twied tuh change the color to {self.color} but it didn't workkkk!!!")


palettes = []


def make_palette():
    for idx, color in enumerate(colors):
        y_level = idx * 40
        palettes.append(PaletteButton(660, y_level, 60, 40, color))

    # for i in range(0, 480, 80):
    #     if i > 0:
    #         color_idx = i // 80
    #     else:
    #         color_idx = 0
    #     palettes.append(PaletteButton(660, i, 60, 40, colors[color_idx]))
    # for color in palettes:
    #     palettes_path.write_text(color)


class GridCell(IDrawable):
    def __init__(self, color, x, y, width, height):
        super().__init__()
        self.color = color
        self.border_color = black
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect((x, y, cell_size, cell_size))

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 1)  # That sweet sweet outline :3 :3 :3 X3

    def click(self, tool):
        if tool == 1:  # pen
            self.color = user.active_color
        elif tool == 2:  # eraser
            self.color = background_color
        elif tool == 3:  # bucket
            for cell in grid_cells:
                cell.color = user.active_color

    def __str__(self) -> str:
        return str(self.rect)


grid_cells: list[GridCell] = []


# Create Objects #######
def make_grid():
    # canvas_rect = pygame.Rect(screen_width // 4, screen_height // 4, canvas_width, canvas_height)
    for row in range(canvas_height // cell_size):
        for col in range(canvas_width // cell_size):
            x = col * cell_size + (screen_width - canvas_width) // 2 % canvas_width
            y = row * cell_size + (screen_height - canvas_height) // 2 % canvas_height
            active_rect = GridCell(background_color, x, y, cell_size, cell_size)
            grid_cells.append(active_rect)
    for item in grid_cells:
        print(item)
    return grid_cells


def make_buttons():
    buttons.append(ExportButton("Export", 0, 0, 60, 30, black, white))
    buttons.append(
        PenButton("*Pen*", 0, 35, 60, 30, black, white),
    )
    buttons.append(BucketButton("Bucket", 0, 70, 60, 30, black, white))
    buttons.append(EraserButton("Eraser!", 0, 105, 60, 30, black, white))


########################


def draw_text(text_string, Start_TextX, Start_TextY, text_color: tuple):
    lines = text_string.split("\n")
    for i, line in enumerate(lines):
        main_text = font.render(line, True, text_color)
        text_rect = main_text.get_rect(topleft=(Start_TextX, Start_TextY + i * line_height))
        screen.blit(main_text, text_rect)


def collides_btn(rect_1: pygame.Rect, button_list: list[Button]):
    """rect_1 is the mouse ALWAYALWAS ALWAYS ALWAYSALWAYSALWAYSALWAYSALWAYSALWAYSALWAYSALWAYSALWAYSALWAYSALWAYS"""
    button_rects = [button.button_rect for button in button_list]
    if (clicked_button_idx := rect_1.collidelist(button_rects)) >= 0:  # If it collides with anything
        return buttons[clicked_button_idx]


def click_palette(rect_1: pygame.Rect, palette_list: list[PaletteButton]):
    """rect_1 is the mouse ALWAYALWAS ALWAYS ALWAYSALWAYSALWAYSALWAYSALWAYSALWAYSALWAYSALWAYSALWAYSALWAYSALWAYS"""
    button_rects = [palette.button_rect for palette in palette_list]
    if (clicked_button_idx := rect_1.collidelist(button_rects)) >= 0:  # If it collides with anything
        return palettes[clicked_button_idx]


def clicked_grid(mouse_rect: pygame.Rect, grid_lst: list[GridCell]):
    grid_rects = [button.rect for button in grid_lst]
    if (grd_idx := mouse_rect.collidelist(grid_rects)) >= 0:
        return grid_cells[grd_idx]


user = User()


def main():
    running = True
    make_grid()
    make_buttons()
    make_palette()
    drawable_objects: list[IDrawable] = []
    drawable_objects.extend(grid_cells)
    drawable_objects.extend(buttons)
    drawable_objects.extend(palettes)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_width = 5
                mouse_height = 5
                mouse_rect = pygame.Rect(
                    mouse_x - (mouse_width // 2),
                    mouse_y - (mouse_height // 2),
                    mouse_width,
                    mouse_height,
                )  # normalize x and y to center the hitbox
                print(mouse_rect)
                if (clicked_btn := collides_btn(mouse_rect, buttons)) and clicked_btn is not None:  # If collides with anything in buttons
                    clicked_btn.click()
                elif (clicked_grid_cell := clicked_grid(mouse_rect, grid_cells)) and clicked_grid_cell is not None:  # Else if it collides with the drawing grid
                    print(f"GRID{clicked_grid_cell}")
                    clicked_grid_cell.click(user.tool)
                elif (clicked_palette := click_palette(mouse_rect, palettes)) and clicked_palette is not None:
                    clicked_palette.click()

        screen.fill(background_color)

        for obj in drawable_objects:
            obj.draw()

        pygame.display.flip()
        clock.tick(FPS)


main()
pygame.quit()
