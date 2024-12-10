import os
import subprocess


def read_first_line(file_path):
    with open(file_path, 'r') as file:
        return file.readline()


def write(file_path, s):
    with open(file_path, 'w') as file:
        return file.write(s)


def main():
    """
    Runs the VM on each .circuit file in the 'sample_code' directory.

    The output is generated inside of the 'sample_code/tester_output' directory.

    This will skip if the IR file is missing or if code generation failed.
    """

    src_dir = 'sample_code'
    vm_binary = os.path.join('vm', 'build', 'circuit_script')

    for filename in sorted(os.listdir(src_dir)):
        file_path = os.path.join(src_dir, filename)
        filename_no_ext, ext = os.path.splitext(filename)

        if not os.path.isfile(file_path) or ext != '.circuit':
            continue

        test_output_dir = os.path.join(src_dir, 'tester_output', filename_no_ext)
        os.makedirs(test_output_dir, exist_ok=True)
        codegen_path = os.path.join(test_output_dir, '5_optimized.txt')
        vm_output_path = os.path.join(test_output_dir, '6_vm.txt')

        if os.path.exists(codegen_path):
            if read_first_line(codegen_path).startswith('Code generation error'):
                continue

            result = subprocess.run(
                [vm_binary, codegen_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            write(vm_output_path, result.stdout)


if __name__ == '__main__':
    main()
