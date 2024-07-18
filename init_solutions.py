import os
import toml
import sys
import argparse

parser = argparse.ArgumentParser()

subparser = parser.add_subparsers(dest='command', help='Subcommands')
readme_parser = subparser.add_parser('readme', help='Generate the readme')
add_parser = subparser.add_parser('add', help='Add skeleton')
add_parser.add_argument('type', help="Add puzzle to toml file or add file to solutions dir")

args = parser.parse_args()

match args.command:
    case "readme":
        def get_solution(problem_name):
            solution_file = f"solutions/{problem_name}.puf"
            try:
                with open(solution_file, 'r') as f:
                    return f.read().strip()
            except FileNotFoundError:
                return "Solution not found"

        def generate_markdown_table(data):
            markdown_table = "| Problem | Solution |\n|---------|----------|\n"
    
            for puzzle in data['puzzles']:
                problem_name = puzzle['name']
                link = puzzle['links'][0] if puzzle['links'] else ''
                example, *_ = puzzle['examples']
                solution = get_solution(problem_name)
    
                markdown_table += f"| [{problem_name}]({link}) | `{solution}` |\n"
    
            return markdown_table

        # Load the TOML data from file
        toml_file = "puzzles.toml"  # replace with your TOML file name
        with open(toml_file, 'r') as f:
            data = toml.load(f)

        # Generate the Markdown table
        markdown_table = generate_markdown_table(data)

        with open("README_TEMPLATE.md") as f:
            template = f.read()

        with open("README.md", 'w') as f:
            f.write(template)
            f.write('\n')
            f.write(markdown_table)

        exit(0)

    case "add":
        xx = args.type
        match args.type:
            case "toml":
                with open('puzzles.toml', 'a') as file:
                    new_example = """
[[puzzles]]
name = ""
links = [""]
[[puzzles.examples]]
args = []
result = 
[[puzzles.examples]]
args = []
result = 
"""
                    file.write(new_example)
                
                print("written new example to puzzles.toml")
                exit(0)

            case "solutions":
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

