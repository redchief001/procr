#!/usr/bin/env python3

"""
procr.py - Get quick system or process information on the command line.

LICENSE:

Copyright © 2020 James Nicholson

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the “Software”), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import argparse
import sys
import psutil


def main():
    """
    The main function of procr.
    """

    # Parse the command line and get the parser
    args = parse_cmdline()

    # Set the flags for the rest of the program
    proc_list = args.list

    print_output_header()
    # Get the OS that the system is currently running on
    which_op_system = which_os()
    if which_op_system is None:
        print("ERROR! Operating system not detected!")
        sys.exit(1)

    # If the list flag is true, display a list of running processes
    if proc_list:
        processes_list = get_proc_list()
        for proc in processes_list:
            print("----------------------")
            for key, val in proc.items():
                print(key, "    ", val)
            print("----------------------")

    # Display the system information if no flags true
    if not proc_list:
        print("Operating system:         ", which_op_system)

        # Get and display the number of CPUs on the system
        print("System CPU count:         ", get_num_cpus())

        # Get the CPU usage percentage
        print("CPU usage percentage:     ", get_cpu_usage())

        # Get and display the system memory information
        print("System total memory:      ", get_total_system_memory())
        print("System available memory:  ", get_available_system_memory())

        # Get and display system storage information
        if which_op_system == "windows":
            sys_storage_info = get_system_storage_info("windows")
        else:
            sys_storage_info = get_system_storage_info("other")

        print("System storage information: ")
        print("    Total: ", sys_storage_info.total)
        print("    Free:  ", sys_storage_info.free)


def parse_cmdline():
    """
    Return the command line parser.
    """

    parser = argparse.ArgumentParser(
        prog='procr',
        description='Display system information')
    parser.add_argument('-l', '--list', action='store_true', )
    args = parser.parse_args()
    return args


def print_output_header():
    """
    Print some header information for the program output.
    """

    print("--- procr program output ---")
    print("----------------------------")
    print("*System information follows*")
    print("----------------------------")


def which_os():
    """
    Return the operating system the program runs in.
    """

    # Store the available OS constants in a dictionary
    avail_sys_types = {
        # TODO: make this fall-through in the case of POSIX
        # "posix": psutil.POSIX,
        "linux": psutil.LINUX,
        "windows": psutil.WINDOWS,
        "macos": psutil.MACOS,
        "freebsd": psutil.FREEBSD,
        "netbsd": psutil.NETBSD,
        "openbsd": psutil.OPENBSD,
        "bsd": psutil.BSD,
        "sunos": psutil.SUNOS,
        "aix": psutil.AIX
    }

    for key, val in avail_sys_types.items():
        if val is True:
            system_type = str(key)
            return system_type

        return None


def get_system_storage_info(os_type):
    """
    Return the total amount of usable system storage.
    """

    if os_type == "windows":
        sys_storage_info = psutil.disk_usage("C:\\")
    else:
        sys_storage_info = psutil.disk_usage("/")

    return sys_storage_info


def get_total_system_memory():
    """
    Return the total amount of system memory.
    """

    system_memory = psutil.virtual_memory()
    return system_memory.total


def get_available_system_memory():
    """
    Return the amount of available system memory.
    """

    system_memory = psutil.virtual_memory()
    return system_memory.available


def get_proc_list():
    """
    Return a list of currently running processes.
    """

    proc_list = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        proc_list.append(proc.info)
    return proc_list


def get_num_cpus():
    """
    Return the number of CPUs on the running system.
    """

    cpu_count = psutil.cpu_count()
    return cpu_count


def get_cpu_usage():
    """
    Return a snapshot of the systems CPU usage.
    """
    cpu_use_snapshot = psutil.cpu_percent(interval=None)
    return cpu_use_snapshot


if __name__ == "__main__":
    main()
