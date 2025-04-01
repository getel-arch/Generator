# Generator

## Overview

The **Generator** project is a code generation tool designed to dynamically create C programs based on YAML configuration files. It supports modular snippets, dependencies, and customizable workflows to generate executable code for various use cases.

## Features

- Modular code snippets with reusable configurations.
- Dependency resolution between snippets.
- Automatic generation of function declarations, implementations, and main logic.
- Support for linking required libraries.
- Easy-to-use YAML-based configuration for defining workflows.

## Directory Structure

```
Generator/
├── main.py                     # Entry point for the generator
├── src/
│   ├── generator/
│   │   ├── generator.py        # Core logic for code generation
│   │   ├── templates.py        # Templates for generated code
│   ├── snippets/               # Modular code snippets
│       ├── <snippet_name>/     # Individual snippet directories
│           ├── <snippet_name>.c   # Implementation of the snippet
│           ├── config.yaml        # Configuration for the snippet
├── example.yaml                # Example YAML configuration for code generation
├── LICENSE                     # License information
└── README.md                   # Project documentation
```

## Prerequisites

- Python 3.6 or later
- GCC (for compiling the generated C code)
- Windows environment (for Windows-specific APIs)

## Usage

1. **Prepare a YAML Configuration File**  
   Define the functions and flow in a YAML file. For example:

   ```yaml
   functions:
     - replace_arguments_with_spaces
     - create_suspended_process
     - modify_process_command_line
     - resume_thread
   
   variables:
     hProcess: HANDLE
     hThread: HANDLE
     spoofedCmdline: "char[MAX_PATH]"
     cmdlineW: "wchar_t[MAX_PATH]"
   
   flow:
     - replace_arguments_with_spaces:
         original: "cmd.exe /k echo This will not be logged in sysmon test"
         modified: "{spoofedCmdline}"
     - create_suspended_process:
         commandLine: "{spoofedCmdline}"
     - modify_process_command_line:
         hProcess: "{hProcess}"
         newCommandLine: "{cmdlineW}"
     - resume_thread:
         threadHandle: "{hThread}"
   ```

2. **Run the Generator**  
   Use the following command to generate the C code:

   ```bash
   python main.py <yaml_file> <output_file> <binary_name>
   ```

   Example:

   ```bash
   python main.py example.yaml output.c output_binary
   ```

3. **Compile the Generated Code**  
   After running the generator, compile the generated C code using GCC:

   ```bash
   gcc output.c -o output_binary -s -m64 -lntdll
   ```

4. **Run the Compiled Binary**  
   Execute the compiled binary:

   ```bash
   ./output_binary
   ```

## Example

The provided `example.yaml` demonstrates how to use the `hide_lolbin` function. The generated code will create a process with a spoofed command line to hide its arguments.

## Adding New Snippets

1. Create a new directory under `src/snippets/` with the snippet name.
2. Add the implementation file (`<snippet_name>.c`) and configuration file (`config.yaml`).
3. Define the snippet's parameters, dependencies, and templates in `config.yaml`.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.
