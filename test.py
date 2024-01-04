import pandas as pd

def isolate_cells(image, row_boxes, col_boxes, label_ids, id2label):
    row_boxes = sorted(row_boxes, key=lambda x: (x[1], x[0]))  # Sort by ymin and then xmin
    col_boxes = sorted(col_boxes, key=lambda x: (x[0], x[1]))  # Sort by xmin and then ymin
    
    cell_data = []
    
    for row_index, row_box in enumerate(row_boxes):
        for col_index, col_box in enumerate(col_boxes):
            # Extract coordinates for the current cell
            xmin_row, ymin_row, xmax_row, ymax_row = map(int, row_box)
            xmin_col, ymin_col, xmax_col, ymax_col = map(int, col_box)
            
            # Crop the current cell from the image
            cell_image = image.crop((xmin_col, ymin_row, xmax_col, ymax_row))
            
            # Add cell data to the list
            cell_data.append((cell_image, row_index, col_index))
    
    # Sort the cell data based on row and column indices
    cell_data.sort(key=lambda x: (x[1], x[2]))
    
    return cell_data

# Example usage:
row_label_id = model.config.label2id['table row']
col_label_id = model.config.label2id['table column']

row_boxes = results['boxes'][results['labels'] == row_label_id]
col_boxes = results['boxes'][results['labels'] == col_label_id]

isolated_cells_data = isolate_cells(image, row_boxes, col_boxes, [row_label_id, col_label_id], model.config.id2label)

# Create a DataFrame from the isolated cell data
columns = ['Row', 'Column', 'Image_Path']
df_cells = pd.DataFrame(columns=columns)

rows_list = []

# Save or display the isolated cell images and update the list
for i, (cell_image, row_index, col_index) in enumerate(isolated_cells_data):
    image_path = f'isolated_cell_{i}.png'
    cell_image.save(image_path)
    rows_list.append({'Row': row_index, 'Column': col_index, 'Image_Path': image_path})

# Create a DataFrame from the list
df_cells = pd.DataFrame(rows_list)

# Sort the DataFrame based on Row and Column columns
df_cells = df_cells.sort_values(by=['Row', 'Column']).reset_index(drop=True)

# Display the sorted DataFrame
print(df_cells)
