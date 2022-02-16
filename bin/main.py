import sys, pygame, math
from block import *

screen_size = width, height = 800, 800  # Change this values to scale game screen
black = (0, 0, 0)
dead_color = (192, 192, 192)
alive_color = (255, 255, 0)
blocks = (10, 10)  # Number of blocks
list_of_blocks = []
blocks_to_change = []
alive_blocks = []
tick = 30


# REFACTOR
def change_blocks_state():  # Changing blocks statement
    for singleblock in blocks_to_change:
        if singleblock.is_alive:
            for i in range(0, len(blocks_to_change), 1):
                if alive_blocks[i] == singleblock:
                    del (alive_blocks[i])

                    singleblock.block_color = dead_color
                    singleblock.is_alive = False
                else:
                    singleblock.block_color = alive_color
                    singleblock.is_alive = True


# ---------------------
def get_block_id(position):  # Getting blocks ID
    x_id = math.floor(position[0] * blocks[0] / screen_size[0])
    y_id = math.floor(position[1] * blocks[1] / screen_size[1])
    return x_id, y_id


def get_block_by_id(id):  # Getting blocks identification
    return list_of_blocks[id[1] * blocks[0] + id[0]]


def block_by_pos(mouse_pos: (int, int)) -> object:  # Getting blocks position
    return get_block_by_id(get_block_id(mouse_pos))


# TODO REFACTOR
def count_neighbors(singleblock):  # Checking neighbors
    alive_neighbors = 0
    for x in range(singleblock.block_id[0] - 1, singleblock.block_id[0] + 1, 1):
        for y in range(singleblock.block_id[1] - 1, singleblock.block_id[1] + 1, 1):
            if 0 <= x <= blocks[0] - 1 and 0 <= y <= blocks[1]:
                if x != singleblock.block_id[0] and y != singleblock.block_id[1]:
                    if get_block_by_id((x, y)).is_alive:
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
                    is_simulating = not is_simulating

            if event.type == pygame.QUIT:
                is_running = False
            # ----------
            # Game rules
            for singleblock in alive_blocks:
                if is_simulating:
                    alive_neighbors = count_neighbors(singleblock)
                    if alive_neighbors > 3 or alive_neighbors < 2:
                        blocks_to_change.append(singleblock)

            pygame.time.wait(100)  # Screen delay

            change_blocks_state()

            blocks_to_change.clear()

            for singleblock in list_of_blocks:  #
                pygame.draw.rect(screen, singleblock.block_color, singleblock.get_rect())
                pygame.draw.rect(screen, black, singleblock.get_rect(), 1)
                pygame.display.flip()


if __name__ == '__main__':
    main()
