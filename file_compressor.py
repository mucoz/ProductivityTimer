import heapq
import pickle


class HuffmanNode:
    """ Represents a node in Huffman tree"""
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCompression:
    def __init__(self):
        self.huffman_codes = {}
        self.reverse_codes = {}
        self.root = None

    def _build_frequency_map(self, data):
        frequency_map = {}
        for char in data:
            frequency_map[char] = frequency_map.get(char, 0) + 1
        return frequency_map

    def _build_huffman_tree(self, frequency_map):
        heap = [HuffmanNode(char, freq) for char, freq in frequency_map.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)

            merged = HuffmanNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(heap, merged)
        self.root = heap[0]

    def _generate_huffman_codes(self, node, code):
        if node is None:
            return
        if node.char is not None:
            self.huffman_codes[node.char] = code
            self.reverse_codes[code] = node.char

        self._generate_huffman_codes(node.left, code + "0")
        self._generate_huffman_codes(node.right, code + "1")

    def compress(self, data):
        frequency_map = self._build_frequency_map(data)
        self._build_huffman_tree(frequency_map)
        self._generate_huffman_codes(self.root, "")

        compressed_data = "".join(self.huffman_codes[char] for char in data)
        return compressed_data

    def decompress(self, binary_data):
        current_code = ""
        decoded_data = []
        for bit in binary_data:
            current_code += bit
            if current_code in self.reverse_codes:
                decoded_data.append(self.reverse_codes[current_code])
                current_code = ""
        return "".join(decoded_data)

    def save_to_file(self, compressed_data, output_file):
        byte_array = self._binary_string_to_bytes(compressed_data)
        with open(output_file, "wb") as file:
            pickle.dump((self.huffman_codes, byte_array, len(compressed_data)), file)

    def load_from_file(self, input_file):
        with open(input_file, "rb") as file:
            huffman_codes, byte_array, bit_length = pickle.load(file)
            self.huffman_codes = huffman_codes
            self.reverse_codes = {v: k for k, v in self.huffman_codes.items()}
            binary_data = self._bytes_to_binary_string(byte_array, bit_length)
            return self.decompress(binary_data)

    def _binary_string_to_bytes(self, binary_string):
        if len(binary_string) % 8 != 0:
            padding_length = 8 - (len(binary_string) % 8)
            binary_string += "0" * padding_length
        byte_array = bytearray()
        for i in range(0, len(binary_string), 8):
            byte = binary_string[i:i+8]
            byte_array.append(int(byte, 2))
        return byte_array

    def _bytes_to_binary_string(self, byte_array, bit_length):
        binary_string = "".join(f"{byte:08b}" for byte in byte_array)
        return binary_string[:bit_length]

    def _compress_data(self, data, output_file_path):
        compressed_data = self.compress(data)
        self.save_to_file(compressed_data, output_file_path)

    def _read_compressed_file(self, input_file_path):
        decompressed_data = self.load_from_file(input_file_path)
        return decompressed_data

    @staticmethod
    def compress_data(data, output_file_path):
        compressor = HuffmanCompression()
        compressor._compress_data(data, output_file_path)

    @staticmethod
    def read_compressed_file(input_file_path):
        compressor = HuffmanCompression()
        data = compressor._read_compressed_file(input_file_path)
        return data



