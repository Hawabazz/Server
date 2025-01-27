import base64
import zlib
import marshal

def encode_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Convert to bytes
    content_bytes = content.encode('utf-8')
    
    # Compress and encode
    compressed = zlib.compress(content_bytes)
    marshalled = marshal.dumps(compressed)
    encoded = base64.b32encode(marshalled)
    
    # Reverse the string
    encoded = encoded[::-1]
    
    # Create the output
    output = f'''import base64, zlib, marshal, os
from flask import Flask

_ = lambda __ : __import__('marshal').loads(__import__('zlib').decompress(__import__('base64').b32decode(__[::-1])))

exec((_)(b'{encoded.decode()}'))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
'''
    
    # Write to new file
    with open('encoded_' + filename, 'w') as f:
        f.write(output)

# Encode app.py
encode_file('app.py')
