#!/usr/bin/env python3
# File name          : xorencoder.py
# Author             : IllmaticJV
# Date created       : 18 Apr 2023

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

def main():
    # create an ArgumentParser object
    parser = argparse.ArgumentParser(description='XOR Encoder')

    # add command-line arguments for string, file, and key
    parser.add_argument('-s', '--string', help='Input string to encode')
    parser.add_argument('-f', '--file', help='Input file to encode')
    parser.add_argument('-k', '--key', help='Key value to XOR with')
    args = parser.parse_args()

    # check if neither string nor file is specified
    if not args.string and not args.file:
        print('Error: Please specify an input string or file')
        return

    # check if both string and file are specified
    if args.string and args.file:
        print('Error: Please specify only one input source')
        return

    # if file is specified, read the contents and extract the hex string
    if args.file:
        with open(args.file, 'r') as f:
            file_contents = f.read()   # read the file contents
            hex_str = ''.join(re.findall(r'0x([0-9a-fA-F]{2})', file_contents))   # extract the hex string using regex
    else:
        hex_str = args.string.replace('0x', '').replace(',', '').replace(' ', '')   # if string is specified, extract the hex string

    try:
        byte_arr = bytes.fromhex(hex_str)   # convert the hex string to bytes
    except ValueError:
        print('Error: Invalid hex string')
        return

    # if key is specified, convert it to an integer
    if args.key:
        try:
            key_value = int(args.key, 16)
        except ValueError:
            print('Error: Invalid key value')
            return
    else:
        key_value = int(input('Enter key value in format such as 0xfa: '), 16)   # if key is not specified, ask for user input

    # XOR each byte of the byte array with the key value
    encoded_bytes = [b ^ key_value for b in byte_arr]

    # Output XORed byte array as C-style byte array
    print('XOR payload:')
    byte_arr_str = ', '.join(['0x{:02x}'.format(b) for b in encoded_bytes])   # format the bytes as C-style byte array
    print('byte[] buf = new byte[{}] {{ {} }};'.format(len(encoded_bytes), byte_arr_str))

if __name__ == '__main__':
    main()
