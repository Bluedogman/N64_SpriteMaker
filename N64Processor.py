from io import BytesIO
from pathlib import Path
import struct

# import numpy
# My heart beats like a drum


class N64:
    def __init__(self):
        # N64 RAM
        self.NRAM = []  # The actual data stored in our fake RAM
        self.NRAM_counter = 0  # An int used for limiting the RAM to under or at 4KB, to simulate the N64's RAM limit

    # Will convert any data into bytes then read the size of the data
    # If the size of the data will cause NRAM_counter to exceed 4KB(4096 Bytes), return -1
    def register_RAM(self, data):

        my_buffer = BytesIO(data)
        data_size = my_buffer.getbuffer().nbytes

        if self.NRAM_counter + data_size > 4096:  # hard limit for memory
            self.NRAM.append(data)
            self.NRAM_counter += data_size
        else:  # Bad news bears
            print("Out of ram :(")
            return -1


# THIS FUNCTION IS GOOGLE GEMINI I TAKE NO CREDIT
def to_n64_rgba5551(r8, g8, b8, a8):
    # Quantize 8-bit channels (0-255) to 5-bit (0-31)
    r5 = r8 >> 3  # effectively r8 * 31 // 255
    g5 = g8 >> 3  # effectively g8 * 31 // 255
    b5 = b8 >> 3  # effectively b8 * 31 // 255
    # Quantize 8-bit alpha (0-255) to 1-bit (0 or 1)
    a1 = 1 if a8 > 127 else 0  # simple threshold

    # Pack into 16-bit integer: RRRRRGGGGG BBBBB A
    n64_color = (r5 << 11) | (g5 << 6) | (b5 << 1) | a1
    return n64_color


# until I get mor smarterererr, YOU will give MEEE the data typee
def convert_bytes(data, data_type):  # int, str, file, iter_int, iter_str
    if data_type == "file":
        return data.read_bytes()

    elif data_type == "iter_int":
        return bytes(data)

    elif data_type == "iter_str":
        output = b""
        for string in data:
            string.encode("utf-8")
            output += string
        return BytesIO(output).getvalue()

    elif data_type == "str":
        return BytesIO(data.encode("utf-8")).getvalue()

    elif data_type == "int":
        return data.to_bytes(2, "big")  # 2 bytes, big-endian


N64_1 = N64()


def main():
    data_byte = convert_bytes(3, "int")
    print(data_byte)
    N64_1.register_RAM(data_byte)


main()
