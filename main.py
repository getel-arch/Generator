import sys
from src.generator.generator import CodeGenerator

def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <yaml_file> <output_file> <binary_name>")
        return 1

    yaml_path = sys.argv[1]
    output_path = sys.argv[2]
    binary_name = sys.argv[3]

    generator = CodeGenerator(yaml_path)
    generated_code = generator.generate()

    with open(output_path, 'w') as f:
        f.write(generated_code)

    # Determine required libraries for linking
    required_libraries = generator.get_required_libraries()
    libraries_option = f" -l{' -l'.join(required_libraries)}" if required_libraries else ""

    # Print GCC compilation command
    print("\nTo compile the generated code, use the following command:")
    print(f"gcc {output_path} -o {binary_name} -s -m64{libraries_option}")

if __name__ == '__main__':
    sys.exit(main())
