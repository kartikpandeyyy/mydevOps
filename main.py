import heapq
import os
import struct
from node import HuffmanNode


class HuffmanCoding:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    # ---------- BUILD HUFFMAN TREE ----------

    def make_frequency_dict(self, text):
        freq = {}
        for ch in text:
            freq[ch] = freq.get(ch, 0) + 1
        return freq

    def make_heap(self, frequency):
        for ch, freq in frequency.items():
            heapq.heappush(self.heap, HuffmanNode(ch, freq))

    def merge_nodes(self):
        while len(self.heap) > 1:
            n1 = heapq.heappop(self.heap)
            n2 = heapq.heappop(self.heap)

            merged = HuffmanNode(None, n1.freq + n2.freq)
            merged.left = n1
            merged.right = n2
            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, node, code):
        if node is None:
            return

        if node.char is not None:
            self.codes[node.char] = code
            self.reverse_mapping[code] = node.char
            return

        self.make_codes_helper(node.left, code + "0")
        self.make_codes_helper(node.right, code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        self.make_codes_helper(root, "")

    

    def get_encoded_text(self, text):
        return "".join(self.codes[ch] for ch in text)

    def pad_encoded_text(self, encoded):
        padding = 8 - len(encoded) % 8
        encoded += "0" * padding
        padded_info = format(padding, "08b")
        return padded_info + encoded

    def get_byte_array(self, padded_encoded):
        b = bytearray()
        for i in range(0, len(padded_encoded), 8):
            b.append(int(padded_encoded[i:i+8], 2))
        return b

    

    def remove_padding(self, bit_string):
        padding = int(bit_string[:8], 2)
        bit_string = bit_string[8:]
        return bit_string[:-padding]

    def decode_text(self, bit_string):
        current = ""
        decoded = ""

        for bit in bit_string:
            current += bit
            if current in self.reverse_mapping:
                decoded += self.reverse_mapping[current]
                current = ""

        return decoded

    

    def compress_file(self, path):
        filename, _ = os.path.splitext(path)
        output_path = filename + ".bin"

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        frequency = self.make_frequency_dict(text)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        encoded = self.get_encoded_text(text)
        padded = self.pad_encoded_text(encoded)
        byte_array = self.get_byte_array(padded)

        with open(output_path, "wb") as out:
            # write number of unique symbols
            out.write(struct.pack("H", len(frequency)))

            # write frequency table (binary, compact)
            for ch, freq in frequency.items():
                out.write(struct.pack("<cI", ch.encode(), freq))

            # write compressed data
            out.write(byte_array)

        print("Compressed")
        return output_path

    

    def decompress_file(self, path):
        filename, _ = os.path.splitext(path)
        output_path = filename + "_decompressed.txt"

        with open(path, "rb") as f:
            # read frequency table
            freq_len = struct.unpack("H", f.read(2))[0]
            frequency = {}

            for _ in range(freq_len):
                ch, freq = struct.unpack("<cI", f.read(5))
                frequency[ch.decode()] = freq

            # rebuild tree
            self.heap = []
            self.codes = {}
            self.reverse_mapping = {}
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()

            # read encoded data
            bit_string = ""
            byte = f.read(1)
            while byte:
                bit_string += format(ord(byte), "08b")
                byte = f.read(1)

        encoded = self.remove_padding(bit_string)
        decompressed = self.decode_text(encoded)

        with open(output_path, "w", encoding="utf-8") as out:
            out.write(decompressed)

        print("Decompressed")
        return output_path
