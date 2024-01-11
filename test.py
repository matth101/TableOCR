def isolate_cells(image, row_boxes, col_boxes, label_ids, id2label, spanning_boxes=None):
    row_boxes = sorted(row_boxes, key=lambda x: (x[1], x[0]))  # Sort by ymin and then xmin
    col_boxes = sorted(col_boxes, key=lambda x: (x[0], x[1]))  # Sort by xmin and then ymin
    
    # If there are spanning boxes, sort them as well
    if spanning_boxes:
        spanning_boxes = sorted(spanning_boxes, key=lambda x: (x[0], x[1]))

    cell_data = []
    
    for row_index, row_box in enumerate(row_boxes):
        for col_index, col_box in enumerate(col_boxes):
            # Extract coordinates for the current cell
            xmin_row, ymin_row, xmax_row, ymax_row = map(int, row_box)
            xmin_col, ymin_col, xmax_col, ymax_col = map(int, col_box)
            
            # Check if the current cell intersects with any spanning box
            intersected = False
            if spanning_boxes:
                for span_box in spanning_boxes:
                    xmin_span, ymin_span, xmax_span, ymax_span = map(int, span_box)
                    if (xmin_col < xmax_span and xmax_col > xmin_span and
                        ymin_row < ymax_span and ymax_row > ymin_span):
                        intersected = True
                        break
            
            # If the current cell does not intersect with any spanning box, proceed
            if not intersected:
                # Crop the current cell from the image
                cell_image = image.crop((xmin_col, ymin_row, xmax_col, ymax_row))
                bbox = (xmin_col, ymin_row, xmax_col, ymax_row)
                # Add cell data to the list
                cell_data.append((cell_image, row_index, col_index, bbox))
    
    # If there are spanning boxes, add them to the cell data
    if spanning_boxes:
        for i, span_box in enumerate(spanning_boxes):
            xmin_span, ymin_span, xmax_span, ymax_span = map(int, span_box)
            span_image = image.crop((xmin_span, ymin_span, xmax_span, ymax_span))
            span_bbox = (xmin_span, ymin_span, xmax_span, ymax_span)
            # Add spanning cell data to the list
            cell_data.append((span_image, i, i, span_bbox))
    
    # Sort the cell data based on row and column indices
    cell_data.sort(key=lambda x: (x[1], x[2]))
    
    return cell_data

# Example usage:
row_label_id = model.config.label2id['table row']
col_label_id = model.config.label2id['table column']
span_label_id = model.config.label2id['table spanning cell']

row_boxes = results['boxes'][results['labels'] == row_label_id]
col_boxes = results['boxes'][results['labels'] == col_label_id]
spanning_boxes = results['boxes'][results['labels'] == span_label_id]

isolated_cells_data = isolate_cells(image, row_boxes, col_boxes, [row_label_id, col_label_id], model.config.id2label, spanning_boxes)

# Create a DataFrame from the isolated cell data
columns = ['Row', 'Column', 'Cell Contents']
df_cells = pd.DataFrame(columns=columns)

rows_list = []

# Save or display the isolated cell images and update the list
for i, (cell_image, row_index, col_index, bbox) in enumerate(isolated_cells_data):
    result = pytesseract.image_to_string(cell_image)
    cleaned_result = result.replace('\n', ' ').strip()

    rows_list.append({'Row': row_index, 'Column': col_index, 'Cell Contents': cleaned_result})

# Create a DataFrame from the list
df_cells = pd.DataFrame(rows_list)

# Sort the DataFrame based on Row and Column columns
df_cells = df_cells.sort_values(by=['Row', 'Column']).reset_index(drop=True)

# Display the sorted DataFrame
print("Original DataFrame:")
print(df_cells)

# Plot the visualization of the final cells after handling spanning cells
plot_cells(image, isolated_cells_data)
