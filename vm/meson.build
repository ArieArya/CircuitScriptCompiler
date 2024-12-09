project('circuit-script-compiler', 'cpp',
  version: '0.1.0',
  license: 'MIT',
  default_options: ['cpp_std=c++17']
)

subdir('third_party/fmt')

executable('circuit_script', 'src/main.cc', include_directories: [fmt_include], link_with: [fmt_lib])
