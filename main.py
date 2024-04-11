import argparse

def main():
    parser = argparse.ArgumentParser(description='Example CLI program')
    
    # Add arguments
    parser.add_argument('file', type=str, help='Code file path')
    parser.add_argument('-w', '--watch', type=str, help='Server mode')
    parser.add_argument('-o', '--output', nargs=2, metavar=('OUTPUT_FILE', 'MODE'), help='Output file path and mode')
    
    # parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')

    # Parse arguments
    args = parser.parse_args()

    # Access parsed arguments
    input_file = args.input_file
    output_file = args.output
    verbose = args.verbose

    # Your program logic goes here
    print(f"Input file: {input_file}")
    if output_file:
        print(f"Output file: {output_file}")
    if verbose:
        print("Verbose mode is enabled")

if __name__ == '__main__':
    main()
