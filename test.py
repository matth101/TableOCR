import cv2
import numpy as np
from matplotlib import pyplot as plt
from collections import deque, defaultdict

# Function for flood fill using BFS
def flood_fill_bfs(img, x, y, color_of_point, paint_color):
    top_left = (x, y)
    bottom_right = (-1, -1)
    order = []
    queue = deque([(x, y)])
    img[x, y] = paint_color
    while queue:
        current_x, current_y = queue.popleft()
        order.append((current_x, current_y))
        neighbors = [
            (current_x - 1, current_y),
            (current_x + 1, current_y),
            (current_x, current_y - 1),
            (current_x, current_y + 1),
        ]
        x_high, y_high = bottom_right
        if current_x >= x_high:
            x_high = current_x
        if current_y >= y_high:
            y_high = current_y
        bottom_right = (x_high, y_high)

        x_low, y_low = top_left
        if current_x <= x_low:
            x_low = current_x
        if current_y <= y_low:
            y_low = current_y
        top_left = (x_low, y_low)

        for neighbor_x, neighbor_y in neighbors:
            if (
                0 <= neighbor_x < len(img)
                and 0 <= neighbor_y < len(img[0])
                and img[neighbor_x, neighbor_y] == color_of_point
            ):
                img[neighbor_x, neighbor_y] = paint_color
                queue.append((neighbor_x, neighbor_y))
    return top_left, bottom_right, order


# Load image
img = cv2.imread("TestTable.png", cv2.IMREAD_GRAYSCALE)

# Identify most common color
from collections import defaultdict

frequencyMap = defaultdict(lambda: 0)
for row in img:
    for pixel in row:
        frequencyMap[pixel] += 1

most_common_color = max(frequencyMap, key=frequencyMap.get)

# Process image
num_cells = 0
cell_coordinates = []
order_of_cells = []

x, y = find_first_coord(img, most_common_color)

# Dictionaries to store rows and columns
row_table = defaultdict(list)
col_table = defaultdict(list)

while x < len(img):
    while y < len(img[0]) - 1:
        if img[x, y] == most_common_color:
            start, end, order = flood_fill_bfs(
                img, x, y, most_common_color, most_common_color - 1
            )
            cell_coordinates.append((start, end))
            order_of_cells.extend(order)
            num_cells += 1
            x, y = end

            # Update row and column tables
            row_index = start[1]
            col_index = start[0]
            row_table[row_index].append((start, end))
            col_table[col_index].append((start, end))
        y += 1
    y = 0
    x += 1

# Sort cell coordinates based on starting point
cell_coordinates_sorted = sorted(cell_coordinates, key=lambda x: x[0])

# Display processed image
plt.imshow(img, interpolation="nearest", cmap="gray")
plt.show()

# Print sorted order of cell coordinates
print("Sorted Order of Cell Coordinates:")
print(cell_coordinates_sorted)

# Print rows and columns
print("\nRow Table:")
for row_index, cells in row_table.items():
    print(f"Row {row_index}:")
    for cell in cells:
        print(f"  {cell}")

print("\nColumn Table:")
for col_index, cells in col_table.items():
    print(f"Column {col_index}:")
    for cell in cells:
        print(f"  {cell}")
