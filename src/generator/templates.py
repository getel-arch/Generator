import os

def load_snippets():
    snippets = {}
    snippets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'snippets')
    
    for snippet_dir in os.listdir(snippets_dir):
        snippet_path = os.path.join(snippets_dir, snippet_dir)
        if os.path.isdir(snippet_path):
            code_file = os.path.join(snippet_path, f'{snippet_dir}.c')
            if os.path.exists(code_file):
                with open(code_file, 'r') as f:
                    snippets[snippet_dir] = f.read().strip()
    
    return snippets

def get_required_headers(function_handlers):
    headers = set(['stdio.h'])  # stdio.h always required for logging
    for handler in function_handlers.values():
        if 'headers' in handler.config:
            headers.update(handler.config['headers'])
    return sorted(headers)

HEADER_TEMPLATE = '''
// Include required headers
{includes}

// Function declarations
{declarations}

// Function implementations
{implementations}

void log_error(const char* message) {{
    fprintf(stderr, "ERROR: %s\\n", message);
}}

void log_debug(const char* message) {{
    fprintf(stdout, "DEBUG: %s\\n", message);
}}

int main() {{
    log_debug("Starting program execution");
    {main_code}
    log_debug("Program execution completed");
    return 0;
}}
'''
