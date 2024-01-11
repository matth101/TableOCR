def is_bbox_majority_within(bbox1, bbox2, threshold=0.5):
    x_min1, y_min1, x_max1, y_max1 = bbox1
    x_min2, y_min2, x_max2, y_max2 = bbox2

    intersection_x_min = max(x_min1, x_min2)
    intersection_y_min = max(y_min1, y_min2)
    intersection_x_max = min(x_max1, x_max2)
    intersection_y_max = min(y_max1, y_max2)

    intersection_area = max(0, intersection_x_max - intersection_x_min) * max(0, intersection_y_max - intersection_y_min)
    cell_area = (x_max1 - x_min1) * (y_max1 - y_min1)

    return (intersection_area / cell_area) > threshold
