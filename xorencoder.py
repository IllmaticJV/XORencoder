#!/usr/bin/env python3
# File name          : xorencoder.py
# Author             : IllmaticJV
# Date created       : 19 Apr 2023

import argparse 
import re 

def banner():
  print("__   __ _____ ______   _____                          _                ")
  print("\ \ / /|  _  || ___ \ |  ___|                        | |               ")
  print(" \ V / | | | || |_/ / | |__   _ __    ___   ___    __| |  ___  _ __    ")
  print(" /   \ | | | ||    /  |  __| | '_ \  / __| / _ \  / _` | / _ \| '__|   ")
  print("/ /^\ \\ \_/ /| |\ \  | |___ | | | || (__ | (_) || (_| ||  __/| |      ")
  print("\/   \/ \___/ \_| \_| \____/ |_| |_| \___| \___/  \__,_| \___||_|      ")
  print("                                                                       ")
  print("                                                                       ")
  print("___  ___ _____ ______    _             _____    _  _                   ")
  print("|  \/  |/  ___||  ___|  | |           /  __ \ _| || |_                 ")
  print("| .  . |\ `--. | |_     | |_   ___    | /  \/|_  __  _|                ")
  print("| |\/| | `--. \|  _|    | __| / _ \   | |     _| || |_                 ")
  print("| |  | |/\__/ /| |      | |_ | (_) |  | \__/\|_  __  _|                ")
  print("\_|  |_/\____/ \_|       \__| \___/    \____/  |_||_|                  ")
  print("                                                                       ")
  print("                                                                       ")
  print("                                            Created by IllmaticJV      ")
  print("                                                                       ")

def get_arguments():
    # create an ArgumentParser object
    parser = argparse.ArgumentParser(description='XOR Encoder')
    # add command-line arguments for string, file, and key
    parser.add_argument('-f', '--file', help='Input file to encode')
    parser.add_argument('-k', '--key', help='Key value to XOR with')
    return parser.parse_args()

def c_read_hex_string_from_file(file_path):
    with open(file_path, 'r') as f:
        file_contents = f.read()   # read the file contents
        hex_str = ''.join(re.findall(r'0x([0-9a-fA-F]{2})', file_contents))   # extract the hex string using regex
    return hex_str

def convert_hex_string_to_bytes(hex_str):
    try:
        byte_arr = bytes.fromhex(hex_str)   # convert the hex string to bytes
    except ValueError:
        print('Error: Invalid hex string')
        return None
    return byte_arr

def get_key_value(args):
    if args.key:
        try:
            key_value = int(args.key, 16)
        except ValueError:
            print('Error: Invalid key value')
            return None
    else:
        while True:
            key_input = input('Enter key value in format such as 0xfa: ')
            try:
                key_value = int(key_input, 16)
                break
            except ValueError:
                print('Error: Invalid key value')
    return key_value

def xor_encode(byte_arr, key_value):
    encoded_bytes = [b ^ key_value for b in byte_arr]
    return bytes(encoded_bytes)

def output_c_style_byte_array(encoded_bytes):
    print('XOR payload:')
    byte_arr_str = ', '.join(['0x{:02x}'.format(b) for b in encoded_bytes])   # format the bytes as C-style byte array
    output = 'byte[] buf = new byte[{}] {{ {} }};'.format(len(encoded_bytes), byte_arr_str)
    print(output)
    write_to_file(output)

def write_to_file(output: str):
    """Writes content to a file based on user input."""
    response = input("Do you want to write the content to a file? (y/n) ")
    if response.lower() == 'y':
        file_path = input("Enter the file path to write to (default is current folder): ") or "output.xor"
        with open(file_path, 'w') as f:
            f.write(output)
        print(f"Content written to file: {file_path}")
    else:
        print("Content not written to file.")

def main():
    args = get_arguments()
    # check if neither string nor file is specified
    if not args.file: 
        print('Error: Please specify an input file')
        return  
    key_value = get_key_value(args)
    if not key_value:
        return    
    hex_str = c_read_hex_string_from_file(args.file)
    if not hex_str:
        return
    byte_arr = convert_hex_string_to_bytes(hex_str)
    if not byte_arr:
        return
    encoded_bytes = xor_encode(byte_arr, key_value)
    output_c_style_byte_array(encoded_bytes)

if __name__ == '__main__':
    banner()
    main()
