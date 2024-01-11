def is_cell_within_spanning(cell_bbox, spanning_bbox):
    xmin_cell, ymin_cell, xmax_cell, ymax_cell = cell_bbox
    xmin_span, ymin_span, xmax_span, ymax_span = spanning_bbox

    return (xmin_cell >= xmin_span and
            xmax_cell <= xmax_span and
            ymin_cell >= ymin_span and
            ymax_cell <= ymax_span)

# Example usage:
cell_bbox = (10, 20, 30, 40)
spanning_bbox = (5, 15, 35, 45)

result = is_cell_within_spanning(cell_bbox, spanning_bbox)
print(result)  # This will print True if the cell is within the spanning cell, otherwise False
