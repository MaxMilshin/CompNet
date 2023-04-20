def calculate_checksum(data, k=16):
    sum = 0
    for i in range(0, len(data), k):
        num = int.from_bytes(data[i:i+k], byteorder='big', signed=False)
        sum += num
        sum = (sum & 0xffff) + (sum >> 16)
    checksum = ~sum & 0xffff
    return checksum

def verify_checksum(data, checksum, k=16):
    sum = 0
    for i in range(0, len(data), k):
        num = int.from_bytes(data[i:i+k], byteorder='big', signed=False)
        sum += num
        sum = (sum & 0xffff) + (sum >> 16)
    sum += checksum
    sum = (sum & 0xffff) + (sum >> 16)
    return sum == 0xffff

data = bytes([0x12, 0x34, 0x56, 0x78])
checksum = calculate_checksum(data)
assert verify_checksum(data, checksum) == True

data = bytes([0x12, 0x34, 0x56, 0x78])
checksum = calculate_checksum(data) + 1  # adding 1 to the checksum to make it incorrect
assert verify_checksum(data, checksum) == False

data = bytes([0x12, 0x34, 0x56, 0x7F]) 
checksum = calculate_checksum(data)
broken_data = bytes([0x13, 0x34, 0x56, 0x7F]) # the first byte is incorrect
assert verify_checksum(broken_data, checksum) == False