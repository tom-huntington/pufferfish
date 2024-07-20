import toml
import sys
import os
import main



# Load the TOML file
toml_file = 'puzzles.toml'
with open(toml_file, 'r') as f:
    data = toml.load(f)

# Track if any test fails
all_tests_passed = True

# Iterate over puzzles
for puzzle in data['puzzles']:
    if puzzle.get('ignore', None): continue
    name = puzzle['name']
    code_file = f'solutions/{name}.puf'
    
    # Read the solution code
    if not os.path.exists(code_file):
        escaped = code_file.replace(' ', r'\ ')
        print(f"❌ Code file {escaped} not found.")
        all_tests_passed = False
        continue

    with open(code_file, 'r') as f:
        code = f.read()
    
    # Iterate over examples
    for example in puzzle['examples']:
        args = example['args']
        expected_result = example['result']
        
        try:
            result = main.evaluate_code_ignoring_default_args(code, args)
            if result == expected_result:
                print(f"✅ Test passed for puzzle: {name}, args: {args}")
            else:
                print(f"❌ Test failed for puzzle: {name}, args: {args}, expected: {expected_result}, got: {result}")
                all_tests_passed = False
        except Exception as e:
            print(f"❌ Test failed for puzzle: {name}, args: {args}, due to error: {e}")
            all_tests_passed = False
            raise e

# Exit with code 1 if any test failed
if not all_tests_passed:
    sys.exit(1)

