import pygame
import math
from block import *

screen_size = width, height = 1000, 1000  # Change this values to scale game screen
black = (0, 0, 0)
dead_color = (192, 192, 192)
alive_color = (255, 255, 0)
blocks = (10, 10)  # Number of blocks
list_of_blocks = []
blocks_to_change = []
alive_blocks = []


# REFACTOR
def change_blocks_state():  # Changing blocks statement
    for single_block in blocks_to_change:
        if single_block.is_alive:
            for block in alive_blocks:
                if block is single_block:
                    single_block.block_color = dead_color
                    single_block.is_alive = False
                    alive_blocks.remove(block)
        else:
            single_block.block_color = alive_color
            single_block.is_alive = True
            alive_blocks.append(single_block)


# ---------------------
def get_block_id(position):  # Getting blocks ID
    x_id = math.floor(position[0] * blocks[0] / screen_size[0])
    y_id = math.floor(position[1] * blocks[1] / screen_size[1])
    return x_id, y_id


def get_block_by_id(id):
    return list_of_blocks[id[1] * blocks[0] + id[0]]


def block_by_pos(mouse_pos: (int, int)) -> object:  # Getting blocks position
    return get_block_by_id(get_block_id(mouse_pos))


# TODO REFACTOR
def count_neighbors(single_block):  # Checking neighbors
    alive_neighbors = 0
    for x in range(single_block.block_id[0] - 1, single_block.block_id[0] + 2, 1):
        for y in range(single_block.block_id[1] - 1, single_block.block_id[1] + 2, 1):
            if x >= 0 and x < blocks[0] and y >= 0 and y < blocks[1]:
                checked_block = get_block_by_id((x, y))
                if checked_block.is_alive and checked_block is not single_block:
                    alive_neighbors += 1
    return alive_neighbors


def main():
    pygame.init()
    pygame.display.set_caption('Game Of Life')

    screen = pygame.display.set_mode(screen_size)
    is_running = True
    is_simulating = True
    block_size = [width / blocks[0], height / blocks[1]]
    for y in range(blocks[0]):
        for x in range(blocks[1]):  # Adding blocks to list/screen
            pos_x = block_size[0] * x
            pos_y = block_size[1] * y
            single_block = block(pos_x, pos_y, block_size[0], block_size[1], dead_color, get_block_id((pos_x, pos_y)))
            list_of_blocks.append(single_block)

    while is_running:
        # EVENT
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            # Mouse click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()

                if event.button == 1:  # LEFT MOUSE BUTTON
                    pressed_block = block_by_pos(mouse_position)
                    pressed_block.block_color = alive_color
                    pressed_block.is_alive = True
                    alive_blocks.append(pressed_block)

                if event.button == 3:  # RIGHT MOUSE BUTTON
                    pressed_block = block_by_pos(mouse_position)
                    pressed_block.block_color = dead_color
                    pressed_block.is_alive = False
                    alive_blocks.remove(pressed_block)
            if pressed[pygame.K_w]:
                is_simulating = not is_simulating

            if event.type == pygame.QUIT:
                is_running = False
        # ----------
        # Game rules
        for single_block in list_of_blocks:
            if is_simulating:

                alive_neighbors = count_neighbors(single_block)
                if alive_neighbors > 3 or alive_neighbors < 2 and single_block.is_alive:
                    blocks_to_change.append(single_block)
                if alive_neighbors == 3 and not single_block.is_alive:
                    blocks_to_change.append(single_block)

        pygame.time.wait(1)

        change_blocks_state()

        blocks_to_change.clear()

        for single_block in list_of_blocks:
            pygame.draw.rect(screen, single_block.block_color, single_block.get_rect())
            pygame.draw.rect(screen, black, single_block.get_rect(), 1)
            pygame.display.flip()


if __name__ == '__main__':
    main()
