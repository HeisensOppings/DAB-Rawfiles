import struct
import argparse
import os
import sys

def linear_map(value, min_in, max_in, min_out=0, max_out=255):
    mapped = int(((value - min_in) / (max_in - min_in)) * (max_out - min_out) + min_out)
    return max(min_out, min(max_out, mapped))

def convert_iq_to_u8(input_file, output_file, fmt):
    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)

    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            if fmt == 's8':
                chunk = f_in.read(2)
                if len(chunk) < 2:
                    break
                iq_i, iq_q = struct.unpack('bb', chunk)
                u8_i = linear_map(iq_i, -128, 127)
                u8_q = linear_map(iq_q, -128, 127)

            elif fmt == 's16le':
                chunk = f_in.read(4)
                if len(chunk) < 4:
                    break
                iq_q = int.from_bytes(chunk[0:2], byteorder='little', signed=True)
                iq_i = int.from_bytes(chunk[2:4], byteorder='little', signed=True)
                u8_i = linear_map(iq_i, -32768, 32767)
                u8_q = linear_map(iq_q, -32768, 32767)

            elif fmt == 's16be':
                chunk = f_in.read(4)
                if len(chunk) < 4:
                    break
                iq_i = int.from_bytes(chunk[0:2], byteorder='little', signed=True)
                iq_q = int.from_bytes(chunk[2:4], byteorder='little', signed=True)
                # =================

                u8_i = linear_map(iq_i, -32768, 32767)
                u8_q = linear_map(iq_q, -32768, 32767)

            else:
                print(f"Unsupported format: {fmt}")
                sys.exit(1)
            f_out.write(struct.pack('BB', u8_i, u8_q))

    print(f"Success: '{input_file}' ({fmt}) → '{output_file}' (u8 format)")

def main():
    parser = argparse.ArgumentParser(
        description="Convert IQ raw file from s8/s16le/s16be to u8 format."
    )
    parser.add_argument('-i', '--input', required=True, help="Input raw IQ file")
    parser.add_argument('-o', '--output', required=True, help="Output file in u8 format")
    parser.add_argument('-f', '--format', required=True, choices=['s8', 's16le', 's16be'],
                        help="Input file format (s8, s16le, s16be)")

    args = parser.parse_args()
    convert_iq_to_u8(args.input, args.output, args.format)

if __name__ == '__main__':
    main()