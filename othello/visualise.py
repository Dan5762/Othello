import matplotlib.pyplot as plt
from matplotlib import colors


def visualise_board(grid, possible_moves=[]):
    if possible_moves == []:
        cmap = colors.ListedColormap(['Green', 'White', 'Black'])
    else:
        cmap = colors.ListedColormap(['Green', 'White', 'Black', 'Yellow'])

    vis_grid = [[0]*len(grid) for _ in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == "w":
                vis_grid[i][j] = 1
            elif grid[i][j] == "b":
                vis_grid[i][j] = 2
            elif (i, j) in possible_moves:
                vis_grid[i][j] = 3

    plt.figure(figsize=(6,6))
    plt.pcolor(vis_grid, cmap=cmap, edgecolors='k', linewidths=3)
    plt.axis('off')
    plt.show()
