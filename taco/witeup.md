# Taco

## Challenge Description
It's salsa, so should be secure? But something's off...

## Initial Analysis
The challenge provides a Python script (taco.py) that implements the Salsa20 stream cipher. It also includes an encrypted message file (encrypted) that contains a ciphertext encrypted using the Salsa20 cipher with a secret key and a random nonce.

## Approach
1. Analyze the taco.py script to understand the cipher implementation.
2. Observe that implementation is not quite a full Salsa20 - it lacks final add of function.
3. Realize that the cipher is based entirely on a series of reversible operations: bitwise rotations and additions.
4. Craft a script that reverses the operations to recover the key, nonce, and counter from the first block of the keystream.
5. Use the recovered key, nonce, and counter to decrypt the entire ciphertext and obtain the flag.

## Exploiting the Vulnerability
The vulnerability in this challenge lies in the fact that the implementation of not-quite-Salsa20 is fully reversible. Having a known block of plaintext makes it possible to reverse the cipher operations, recover the key, nonce, and counter used for encryption.

The solve.py script does the following:
1. Reads the ciphertext from the encrypted file and converts it from hexadecimal to bytes.
2. Defines the known plaintext prefix of the message (64 bytes).
3. Computes the first block of the keystream by XORing the ciphertext with the known plaintext.
4. Defines reverse functions for the Salsa20 cipher operations, including `rev_rotl`, `rev_quarterround`, `rev_columnround`, `rev_rowround`, and `rev_doubleround`.
5. Defines a `rev_almost_salsa20_block` function that reverses the not-quite-Salsa20 block computation to recover the key, nonce, and counter.
6. Applies the `rev_almost_salsa20_block` function to the first block of the keystream to recover the key, nonce, and counter.

The key points of the exploit are:
- The vulnerable implementation of Salsa20 cipher is based on reversible operations, allowing us to reverse the cipher computations.
- By reversing the cipher operations on the first block of the keystream, we can recover the key, nonce, and counter used for encryption.
- Once we have the key, nonce, and counter, we can decrypt the entire ciphertext using the original Salsa20 decryption function (which is not necessary, the flag is in key).

## Obtaining the Flag
1. Run the solve.py script.
2. The script will read the ciphertext from the encrypted file and compute the first block of the keystream.
3. It will then reverse the not-quite-Salsa20 cipher operations to recover the key, nonce, and counter.
4. The recovered key contains the flag.

Flag: `1753c{reversible_without_an_add}`

### Conclusion
This challenge demonstrates that incorrect implementation of cryptography can lead to vulnerabilities. By reversing the cipher operations, we can recover the key, nonce, and counter used for encryption, effectively breaking the security of the cipher.

The exploit takes advantage of the reversible nature of the faulty implementation, such as bitwise rotations and additions. By applying the reverse operations on the first block of the keystream, we can recover the encryption parameters and decrypt the entire ciphertext.
