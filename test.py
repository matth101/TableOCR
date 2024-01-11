def plot_cells(pil_img, cell_data, spanning_cells=None):
    # Create a figure for visualization
    plt.figure(figsize=(16, 10))

    # Display the PIL image
    plt.imshow(pil_img)

    # Get the current axis
    ax = plt.gca()

    # Repeat the COLORS list multiple times for visualization
    colors = COLORS * 100

    # Iterate through cell data for visualization
    for i, (cell_image, row_index, col_index, bbox) in enumerate(cell_data):
        xmin_col, ymin_row, xmax_col, ymax_row = bbox

        # Add a rectangle to the image for the detected object's bounding box
        ax.add_patch(plt.Rectangle((xmin_col, ymin_row), xmax_col - xmin_col, ymax_row - ymin_row,
                                   fill=False, color=colors[i], linewidth=3))

        # Prepare the text for the cell number
        text = f'Cell {i + 1}'

        # Add the cell number text to the image
        ax.text(xmin_col, ymin_row, text, fontsize=12,
                bbox=dict(facecolor='white', alpha=0.8))

    # If there are spanning cells, visualize them
    if spanning_cells:
        for j, (span_image, span_index, _, span_bbox) in enumerate(spanning_cells):
            xmin_span, ymin_span, xmax_span, ymax_span = span_bbox

            # Add a rectangle to the image for the spanning cell's bounding box
            ax.add_patch(plt.Rectangle((xmin_span, ymin_span), xmax_span - xmin_span, ymax_span - ymin_span,
                                       fill=False, color=[0.8, 0.8, 0.8], linewidth=3, linestyle='--'))

            # Prepare the text for the spanning cell number
            text = f'Span {j + 1}'

            # Add the spanning cell number text to the image
            ax.text(xmin_span, ymin_span, text, fontsize=12,
                    bbox=dict(facecolor='white', alpha=0.8))

    # Turn off the axis
    plt.axis('off')

    # Display the visualization
    plt.show()

# Example usage:
row_label_id = model.config.label2id['table row']
col_label_id = model.config.label2id['table column']
span_label_id = model.config.label2id['table spanning cell']

row_boxes = results['boxes'][results['labels'] == row_label_id]
col_boxes = results['boxes'][results['labels'] == col_label_id]
spanning_boxes = results['boxes'][results['labels'] == span_label_id]

isolated_cells_data = isolate_cells(image, row_boxes, col_boxes, [row_label_id, col_label_id], model.config.id2label, spanning_boxes)

# Plot the visualization of the final cells after handling spanning cells
plot_cells(image, isolated_cells_data, spanning_cells=isolated_cells_data[len(cell_data):])
