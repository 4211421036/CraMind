LANGUAGE_CONFIG = {
    'python': {
        'extension': 'py',
        'run_command': ['python', '{file}'],
        'build_command': None
    },
    'javascript': {
        'extension': 'js',
        'run_command': ['node', '{file}'],
        'build_command': None
    },
    'java': {
        'extension': 'java',
        'run_command': ['javac', '{file}', '&&', 'java', '{filename}'],
        'build_command': None
    },
    'cpp': {
        'extension': 'cpp',
        'run_command': ['g++', '{file}', '-o', '{filename}.out', '&&', './{filename}.out'],
        'build_command': ['g++', '{file}', '-o', '{filename}.out']
    },
    'csharp': {
        'extension': 'cs',
        'run_command': ['dotnet', 'run', '--project', '{file}'],
        'build_command': ['dotnet', 'build', '{file}']
    },
    'go': {
        'extension': 'go',
        'run_command': ['go', 'run', '{file}'],
        'build_command': ['go', 'build', '-o', '{filename}.out', '{file}']
    },
    'ruby': {
        'extension': 'rb',
        'run_command': ['ruby', '{file}'],
        'build_command': None
    },
    'php': {
        'extension': 'php',
        'run_command': ['php', '{file}'],
        'build_command': None
    },
    'swift': {
        'extension': 'swift',
        'run_command': ['swift', '{file}'],
        'build_command': ['swiftc', '-o', '{filename}.out', '{file}']
    },
    'kotlin': {
        'extension': 'kt',
        'run_command': ['kotlinc', '{file}', '-include-runtime', '-d', '{filename}.jar', '&&', 'java', '-jar', '{filename}.jar'],
        'build_command': ['kotlinc', '{file}', '-include-runtime', '-d', '{filename}.jar']
    },
    'rust': {
        'extension': 'rs',
        'run_command': ['rustc', '{file}', '&&', './{filename}'],
        'build_command': ['rustc', '{file}', '-o', '{filename}.out']
    },
    'typescript': {
        'extension': 'ts',
        'run_command': ['ts-node', '{file}'],
        'build_command': ['tsc', '{file}']
    }
}

def get_language_config(language):
    return LANGUAGE_CONFIG.get(language.lower(), LANGUAGE_CONFIG['python'])
