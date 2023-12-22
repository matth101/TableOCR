# Find the dimensions of the table
num_rows = len(row_table)
num_cols = len(col_table)

# Create a mapping for row and column indices
row_mapping = {coord: idx for idx, coord in enumerate(sorted(row_table))}
col_mapping = {coord: idx for idx, coord in enumerate(sorted(col_table))}

# Create an empty table
table = np.zeros((num_rows, num_cols))

# Iterate through col_table and row_table to fill in the values
for col_coord, col_cells in col_table.items():
    col_index = col_mapping[col_coord]
    
    for row_coord, row_cells in row_table.items():
        row_index = row_mapping[row_coord]

        # Find the common cells between the current column and row
        common_cells = set(col_cells) & set(row_cells)

        # Assign the number of common cells to the corresponding position in the table
        table[row_index, col_index] = len(common_cells)

# Print the resulting table
print("Table array:")
print(table)
