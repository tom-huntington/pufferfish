import os
import toml

# Read the TOML file
with open('puzzles.toml', 'r') as file:
    data = toml.load(file)

# Directory where .puf files should be created
solutions_dir = 'solutions/'

# Ensure the solutions directory exists
# os.makedirs(solutions_dir, exist_ok=True)

# Iterate over puzzles in the TOML data
for puzzle in data['puzzles']:
    puzzle_name = puzzle['name']
    file_name = f"{puzzle_name}.puf"
    file_path = os.path.join(solutions_dir, file_name)
    
    # Check if the file exists, if not, create it
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            pass  # Create an empty file

print("Missing files have been created.")

