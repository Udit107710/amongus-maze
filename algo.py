"""Maze-finding functions without the 'self' method attached"""

import numpy as np

def dfs(grid, vis, i, j, max_height, max_width):
    grid[i][j] = 1
    """
    North - 0
    East - 1
    South - 2
    West - 3
    """

    """Legend
    8 - Barrier
    9 - None
    """
    peg = 7
    barrier = 8
    no_barrier = 9

    """Stop at end"""
    if i == max_height-2 and j == max_width-2:
        return grid, peg, barrier, no_barrier

    possible_dir = [] #Array of possible directions

    """North"""
    if i != 1:
        if vis[i-2][j] == 0:
            possible_dir.append(0)
            vis[i-2][j] = 1

    """South"""
    if i != max_height-2:
        if vis[i+2][j] == 0:
            possible_dir.append(2)
            vis[i+2][j] = 1

    """West"""
    if j != 1:
        if vis[i][j-2] == 0:
            possible_dir.append(3)
            vis[i][j-2] = 1
    
    """East"""
    if j != max_width-2:
        if vis[i][j+2] == 0:
            possible_dir.append(1)   
            vis[i][j+2] = 1 

    direction = np.random.choice(possible_dir, 1)
    if direction == 0:
        grid[i-1][j] = no_barrier
        return dfs(grid, vis, i-2, j, max_height, max_width)
    if direction == 1:
        grid[i][j+1] = no_barrier
        return dfs(grid, vis, i, j+2, max_height, max_width)
    if direction == 2:
        grid[i+1][j] = no_barrier
        return dfs(grid, vis, i+2, j, max_height, max_width)
    if direction == 3:
        grid[i][j-1] = no_barrier
        return dfs(grid, vis, i, j-2, max_height, max_width)

while True:
    try: 
        grid = np.zeros([7, 19], dtype=np.int8)
        vis = np.zeros([7, 19])
        final_grid, peg, barrier, no_barrier = dfs(grid, vis, 1, 1, 7, 19)
        final_grid[0][1] = no_barrier
        final_grid[6][17] = no_barrier
        break
    except:
        print('ok')
        pass

print(final_grid)

def add_barriers(grid, num):
    """Add pegs"""
    for i in range(0, 7, 2):
        for j in range(0, 19, 2):
            grid[i][j] = peg

    while num:
        direction = np.random.choice(['LR', 'UD'], 1)
        if direction == 'LR':
            i = np.random.choice(np.arange(0, 7, 2))
            j = np.random.choice(np.arange(1, 19, 2))
        else:
            i = np.random.choice(np.arange(1, 7, 2))
            j = np.random.choice(np.arange(0, 19, 2))
        if grid[i][j] == 0:
            grid[i][j] = barrier
            num -= 1
    return grid
