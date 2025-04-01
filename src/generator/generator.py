import yaml
import logging
import os
from .templates import get_required_headers, HEADER_TEMPLATE

class FunctionHandler:
    def __init__(self, config):
        self.config = config
        self.code_template = config['code_template']
        self.return_type = config['return_type']
        self.input_template = config.get('input_template', '{args}')
        self.variables = {}  # Add this line

    def generate_code(self, func, args, variables=None):
        # Create template context with all available variables directly
        context = {
            'func': func,
            **args,
            **(variables or {})  # Add variables directly to context
        }
        return self.code_template.format(**context)

class CodeGenerator:
    def __init__(self, yaml_path):
        with open(yaml_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.required_functions = set()
        self.flow = []
        self.process_config()
        
        # Load function handlers from snippet directories
        self.function_handlers = {}
        snippets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'snippets')
        for func_name in self.required_functions:
            config_path = os.path.join(snippets_dir, func_name, 'config.yaml')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                    self.function_handlers[func_name] = FunctionHandler(config)
        
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.variables = {}  # Add this as instance variable
        self.declared_variables = set()  # Add this line

    def process_config(self):
        if 'functions' in self.config:
            self.required_functions.update(self.config['functions'])
        
        if 'flow' in self.config:
            self.flow = self.config['flow']

        # Process dependencies
        snippets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'snippets')
        for func_name in list(self.required_functions):
            config_path = os.path.join(snippets_dir, func_name, 'config.yaml')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                    if 'dependencies' in config:
                        self.required_functions.update(config['dependencies'])

    def generate_declarations(self):
        declarations = []
        for func_name in self.required_functions:
            if (func_name in self.function_handlers) and (func_name not in self.declared_variables):
                declarations.append(self.function_handlers[func_name].config['declaration'])
                self.declared_variables.add(func_name)
        return '\n'.join(declarations)

    def generate_implementations(self):
        implementations = []
        snippets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'snippets')
        for func_name in self.required_functions:
            if func_name in self.function_handlers:
                # Load the implementation from the .c file
                snippet_file = os.path.join(snippets_dir, func_name, f'{func_name}.c')
                if os.path.exists(snippet_file):
                    with open(snippet_file, 'r') as f:
                        implementations.append(f.read().strip())
                else:
                    logging.warning(f"Implementation file not found for function: {func_name}")
        return '\n'.join(implementations)

    def generate_main(self):
        main_code = []
        self.declared_variables.clear()  # Reset declared variables
        
        # Generate variable declarations first
        for var_name, var_type in self.config.get('variables', {}).items():
            if var_name not in self.declared_variables:
                if var_type.endswith('[MAX_PATH]'):
                    base_type = var_type.replace('[MAX_PATH]', '')
                    main_code.append(f"{base_type} {var_name}[MAX_PATH];")
                else:
                    main_code.append(f"{var_type} {var_name} = NULL;")
                self.declared_variables.add(var_name)
                self.variables[var_name] = var_name

        # Command line setup section
        main_code.append("")  # Empty line for readability
        main_code.append("// Setup and convert command line")
        main_code.append("const char* cmd = \"cmd.exe /k echo This will not be logged in sysmon test\";")
        main_code.append("MultiByteToWideChar(CP_UTF8, 0, cmd, -1, cmdlineW, MAX_PATH);")
        
        # Process flow section
        for step in self.flow:
            if isinstance(step, dict):
                func = list(step.keys())[0]
                args = step[func]
                
                # Only pass declared variables to templates
                resolved_args = {}
                for key, value in args.items():
                    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
                        var_name = value[1:-1]
                        if var_name in self.declared_variables:
                            resolved_args[key] = var_name
                        else:
                            resolved_args[key] = f'"{value}"'
                    else:
                        resolved_args[key] = f'"{value}"' if isinstance(value, str) else value
                
                if func in self.function_handlers:
                    handler = self.function_handlers[func]
                    try:
                        filtered_vars = {k: v for k, v in self.variables.items() if k in self.declared_variables}
                        code = handler.generate_code(func, resolved_args, filtered_vars)
                        main_code.extend(code.split('\n'))
                    except Exception as e:
                        logging.error(f"Error generating code for function '{func}': {e}")
                        raise
        
        return '\n    '.join(main_code)

    def get_required_libraries(self):
        libraries = set()
        for func_name in self.required_functions:
            if func_name in self.function_handlers:
                config = self.function_handlers[func_name].config
                if config.get('linking_required', False) and 'libraries' in config:
                    libraries.update(config['libraries'])
        return sorted(libraries)

    def generate(self):
        headers = get_required_headers(self.function_handlers)
        includes = '\n'.join(f'#include <{h}>' for h in headers)
        return HEADER_TEMPLATE.format(
            includes=includes,
            declarations=self.generate_declarations(),
            implementations=self.generate_implementations(),
            main_code=self.generate_main()
        )
