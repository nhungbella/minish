#!/usr/bin/env python3
import os
import sys
import subprocess


def get_input_command():
    """Use to get user input.

    Input:
        input of user
    Output:
        command_input
    """
    command_input = input("intek-sh$ ").split()
    # when no command_input return prompt
    while not command_input:
        command_input = input("intek-sh$ ")
    return command_input


def get_input_inPATH(command_input):
    """Run command in PATH.

    execute the first binary corresponding to the command name that it finds
    Input: a list of PATH
    Output: execute the first binary
    """
    if "./" in command_input[0]:
        try:
            subprocess.run([command_input[0]])
        except FileNotFoundError:
            print("No such file or directory: " + command_input[0])
        except PermissionError:
            print("intek-sh: " + command_input[0] + ": Permission denied")
    elif "PATH" in os.environ.keys():
        # list duong path toi bin
        list_paths = (os.environ['PATH']).split(":")
        found = False
        for sub_path in list_paths:
            command_path = os.path.join(sub_path, command_input[0])
            if os.path.exists(command_path):
                found = True
                if len(command_input) == 1:
                    subprocess.run([command_path])
                else:
                    subprocess.run([command_path] + command_input[1:])
                break
        if not found:
            print("intek-sh: " + command_input[0] + ": command not found")
    else:
        print("intek-sh: " + command_input[0] + ": command not found")


def get_input_cd(command_input):
    """Run cd command.

    Input:
        String user input
    Output:
        if no argument, return path HOME
        else: change to the directory indicated in the HOME variable
    """
    if len(command_input) == 1:
        if 'HOME' not in os.environ:
            print("intek-sh: cd: HOME not set")
        else:
            os.chdir(os.environ['HOME'])  # doi thu muc hien hanh ve home
    else:
        os.chdir(command_input[1])  # doi thu muc hien hanh ve new_path


def sort_key():
    """Sort key in dictionary environ.
    """
    list_key = []
    for key in os.environ:
        list_key.append(key)
    list_key.sort()
    return list_key


def create_printenv():
    """print all key and value in dict.
    """
    for key, value in os.environ.items():
        print(key, value, sep='=')


def get_input_printenv(command_input):
    """Run printenv command.

    Input:
        string user input
    Output:
        Print all environment variables.
        If an argument is provided, only the value of that
            variable will be printed.
        If the variable is not set, nothing should be printed out.
    """
    if len(command_input) == 1:
        create_printenv()
    else:
        for index in range(1, len(command_input)):
            argument = command_input[index]
            # just print key in dict
            if argument in os.environ.keys():
                print(os.environ[argument])
            else:
                pass


def create_export():
    """Use to print dictionary when run only export, not argument.
    """
    list_key = sort_key()
    for key in list_key:
        value = ("\"" + os.environ[key] + "\"")
        print("declare -x " + key + "=" + value)


def get_input_export(command_input):
    """Run export command.
    """
    if len(command_input) == 1:
        create_export()
    else:
        add_input_export(command_input)


def add_input_export(command_input):
    """Use to add new argument in list export.

    Input: command_input
    Output: new argument in list export
    """
    for index in range(1, len(command_input)):
        if "=" in command_input[index]:
            argument = command_input[index].split("=")
            os.environ[argument[0]] = argument[1]
        if "=" not in command_input[index]:
            os.environ[command_input[index]] = ""


def get_input_unset(command_input):
    """Run unset command.
    """
    for index in range(1, len(command_input)):
        argument = command_input[index]
        if argument in os.environ:
            del os.environ[argument]
        else:
            pass


def get_input_exit(command_input):
    """Run exit command.

    Exit the shell with the corresponding exit_code if an argument is provided
    """
    # join list argument => string
    argument = ' '.join(command_input[1:])
    if argument.isdigit() or not argument:
        print(command_input[0])
        sys.exit()
    else:
        print(command_input[0] + "\n" + "intek-sh: exit: " + argument)
        sys.exit()


def call_function(command_input):
    """Run function in built_ins.
    """
    if command_input[0] == "pwd":
        get_input_pwd(command_input)
    if command_input[0] == "cd":
        get_input_cd(command_input)
    if command_input[0] == "printenv":
        get_input_printenv(command_input)
    if command_input[0] == "export":
        get_input_export(command_input)
    if command_input[0] == "unset":
        get_input_unset(command_input)
    if command_input[0] == "exit":
        get_input_exit(command_input)


def main():
    while True:
        try:
            command_input = get_input_command()
            built_ins = ["cd", "printenv", "export", "unset", "exit"]
            if command_input[0] in built_ins:
                call_function(command_input)
            else:
                get_input_inPATH(command_input)
        # when read end of file, break
        except EOFError:
            break


if __name__ == "__main__":
    main()
