import math


class block:
    block_position_x = 0
    block_position_y = 0
    block_size_x = 0
    block_size_y = 0
    block_color = ()
    is_alive = False
    block_id = (0, 0)

    def get_rect(self):
        return [self.block_position_x, self.block_position_y, self.block_size_x, self.block_size_y]

    # Block constructor
    def __init__(self, pos_x, pos_y, size_x, size_y, color, block_id):
        self.block_position_x = pos_x
        self.block_position_y = pos_y
        self.block_size_x = size_x
        self.block_size_y = size_y
        self.block_color = color
        self.block_id = block_id
