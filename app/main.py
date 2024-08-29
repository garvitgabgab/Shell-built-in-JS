import sys
import os
import subprocess

def main():
    while True:
        # Print the shell prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            # Read and parse the command
            command = input().strip()
            command_array = command.split()

            if command_array == ["exit", "0"]:
                break
            elif command_array[0] == 'echo':
                print(" ".join(command_array[1:]))
            elif command_array[0] == 'pwd':
                print(f'{os.getcwd()}')
            elif command_array[0] == 'cd':
                if len(command_array) > 1:
                    if command_array[1] == '~':
                        os.chdir(os.path.expanduser("~"))
                    else:
                        try:
                            os.chdir(command_array[1])
                        except FileNotFoundError:
                            print(f"cd: {command_array[1]}: No such file or directory")
            elif command_array[0] == 'ls':
                files = os.listdir(os.getcwd())  # List files in the current directory
                for file in files:
                    print(file)
            elif command_array[0] == 'type':
                if len(command_array) > 1:
                    eval_command = command_array[1]

                    # Check if the command is a shell builtin
                    if eval_command in ['echo', 'exit', 'type', 'pwd', 'cd', 'ls']:
                        print(f'{eval_command} is a shell builtin')
                    else:
                        # Search for the command in the PATH
                        path_dirs = os.environ.get("PATH", "").split(":")

                        command_found = False
                        for directory in path_dirs:
                            full_path = os.path.join(directory, eval_command)
                            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                                print(f'{eval_command} is {full_path}')
                                command_found = True
                                break

                        if not command_found:
                            print(f'{eval_command}: not found')
                else:
                    print('type: not found')
            else:
                # Handle external program execution
                program_name = command_array[0]
                program_args = command_array[1:]

                # Search for the program in PATH
                path_dirs = os.environ.get("PATH", "").split(":")
                program_path = None
                for directory in path_dirs:
                    full_path = os.path.join(directory, program_name)
                    if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                        program_path = full_path
                        break

                if program_path:
                    # Execute the program with arguments
                    try:
                        result = subprocess.run([program_path] + program_args, check=True, text=True, capture_output=True)
                        print(result.stdout, end='')  # Ensure no extra newline
                    except subprocess.CalledProcessError as e:
                        print(f"Error executing {program_name}: {e}")
                else:
                    print(f'{program_name}: not found')

        except EOFError:
            break

if __name__ == "__main__":
    main()
