from pprint import pprint

LITERAL_TYPE_ID = 4


class Bitstream:
    def __init__(self, binary_string):
        self._binary_string = binary_string
        self._position = 0

    def read(self, n) -> str:
        part = self._binary_string[self._position:self._position+n]
        self._position += n
        return part

    def skip_leftovers(self):
        if self._position % 4 != 0:
            self._position += 4 - self._position % 4

    @property
    def is_empty(self):
        return self._position >= len(self._binary_string)

    @property
    def position(self):
        return self._position

    @classmethod
    def from_hex(cls, hex_string):
        binary_string = format(int(hex_string, 16), "b")
        if len(binary_string) % 4 != 0:
            binary_string = '0' * (4 - len(binary_string) % 4) + binary_string
        return cls(binary_string)


def get_input():
    with open("day 16.txt") as input_file:
        return input_file.read().splitlines()[0]

def iter_bitstream(hex_string):
    binary_string = format(int(hex_string, 16), "b")
    yield from binary_string

def iter_packets(bitstream: Bitstream, packets_to_read=None):
    if packets_to_read is None:
        while not bitstream.is_empty:
            yield read_packet(bitstream)
    else:
        for _ in range(packets_to_read):
            yield read_packet(bitstream)

def read_packet(bitstream: Bitstream):
    initial_bitstream_position = bitstream.position
    version = int(bitstream.read(3), 2)
    if version == 0:
        return None
    packet_type = int(bitstream.read(3), 2)

    if packet_type == LITERAL_TYPE_ID:
        last_group_read = False
        number = ''
        while not last_group_read:
            bits = bitstream.read(5)
            last_group_read = bits[0] == "0"
            number += bits[1:]
        number = int(number, 2)
        # if skip_leftovers:
        #     bitstream.skip_leftovers()
        
        return {
            "version": version,
            "packet_type": packet_type,
            "number": number,
            "length": bitstream.position - initial_bitstream_position
        }
    
    else:
    
        length_type = bitstream.read(1)
        if length_type == "0":
            sub_packets_len = int(bitstream.read(15), 2)
            return {
                "version": version,
                "packet_type": packet_type,
                "sub_packets_len": sub_packets_len,
                "sub_packets": list(iter_packets(
                    Bitstream(bitstream.read(sub_packets_len))
                )),
                "length": bitstream.position - initial_bitstream_position
            }
        else:
            sub_packets_count = int(bitstream.read(11), 2)
            return {
                "version": version,
                "packet_type": packet_type,
                "sub_packets_count": sub_packets_count,
                "sub_packets": list(iter_packets(bitstream, sub_packets_count)),
                "length": bitstream.position - initial_bitstream_position
            }            

for packet in iter_packets(Bitstream.from_hex("620080001611562C8802118E34")):
    pprint(packet)