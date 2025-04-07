import base64

#returns xor of input data with key
def xor(data, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

#returns xor of data with key encoded in base64
def xor_b64_encode(data, key):
    xor_data = xor(data, key)
    encode = base64.b64encode(xor_data.encode()).decode()
    return encode

#reverses encoding step
def xor_b64_decode(data, key):
    decode = base64.b64decode(data.encode()).decode()
    original_data = xor(decode, key)
    return original_data

def obfuscate_payload(payload, xor_key):
  obfuscate = {
      "status": "normal",
      "session" : "active",
      "logs": {}}

  i = 1
  for key in payload: 
      log = xor_b64_encode(payload[key], xor_key)
      obfuscate["logs"][f"log_{i}"] = log
      i += 1
  
  return obfuscate

def deobfuscate_payload(obs, xor_key):
  data = obs["logs"]

  payload = {}

  i = 1 
  for key in data:
      og = xor_b64_decode(data[key], xor_key)
      payload[f'data_{i}'] = og
      i+=1

  return payload
