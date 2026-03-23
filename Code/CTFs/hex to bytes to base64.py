import base64

hex_code = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
bytes_code = bytes.fromhex(hex_code)
base64_code = base64.b64encode(bytes_code)

print(base64_code)