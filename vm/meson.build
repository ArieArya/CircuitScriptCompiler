project('circuit-script-compiler', 'cpp',
  version: '0.1.0',
  license: 'MIT',
  default_options: ['cpp_std=c++20']
)

# This is required for std::format library.
add_project_arguments('-fexperimental-library', language: 'cpp')

# TODO: Rename the executable.
executable('circuit_script_compiler', 'src/main.cc')
