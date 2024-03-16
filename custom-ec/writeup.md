# Custom EC

## Challenge Description
Small bad. Big Good.

`nc 143.47.53.106 34871`

## Initial Analysis
The challenge provides a netcat command to connect to a server that performs some cryptography on a user provided elliptic curve. Upon connecting, the server prompts the user to provide the parameters for the elliptic curve, including the prime modulus `p`, the curve coefficients `a` and `b`, the generator point `g`, and the order `n` of the generator. Only some rudimentary checks on parameters are performed.

The server then generates a private key `challenge_priv` and calculates the corresponding public key `challenge_pub` by multiplying the generator `g` with the private key. The user is challenged to guess the private key `x` given the public key.

If the user successfully guesses the private key, the server encrypts the flag using the generator `g` and the flag value and sends the encrypted flag as a point on the curve.

## Approach
1. Generate a weak elliptic curve that allows for efficient discrete logarithm computation (for example if the order of generator is smooth, it's possible to easily  compute discrete logarithm using the Pohlig-Hellman algorithm).
2. Connect to the server and provide the parameters of the weak curve.
3. Receive the challenge public key and calculate the corresponding private key using the discrete logarithm.
4. Send the calculated private key to the server to obtain the encrypted flag.
5. Decrypt the flag by calculating the discrete logarithm of the encrypted flag point.

## Exploiting the Vulnerability
The vulnerability in this challenge lies in the fact that the server allows the user to provide custom elliptic curve parameters. By generating a weak curve, we can efficiently compute discrete logarithms, break the challenge, and decrypt the flag.

The solve.py script does the following:
1. Defines a `gen_q` function that generates a prime `q` such that `q - 1` has a smooth order with only small prime factors.
2. Defines a `make_smooth_order_ec` function that generates a weak elliptic curve mod `q` generated by `gen_q`, with order `q - 1` using the complex multiplication method.
3. Connects to the server and provides the parameters of the weak curve.
4. Receives the challenge public key and calculates the corresponding private key using the discrete logarithm.
5. Sends the calculated private key to the server to obtain the encrypted flag.
6. Decrypts the flag by calculating the discrete logarithm of the encrypted flag point.

The key points of the exploit are:
- The `gen_q` function generates a prime `q` such that `q - 1` has a smooth order, allowing for efficient discrete logarithm computation using the Pohlig-Hellman algorithm.
- The `make_smooth_order_ec` function generates a weak elliptic curve with a smooth order using the `gen_q` function.
- The discrete logarithm computations are performed using the `discrete_log` method provided by the `EllipticCurve` class in SageMath. This method uses the Pohlig-Hellman algorithm.

## Obtaining the Flag
1. Run the solve.py script.
2. The script will connect to the server, generate a weak curve, and provide the curve parameters to the server.
3. The script will receive the challenge public key, calculate the private key, and send it to the server.
4. The server will respond with the encrypted flag point.
5. The script will decrypt the flag by calculating the discrete logarithm of the encrypted flag point.
6. The decrypted flag will be printed.

Flag: `1753c{sometimes_size_wont_help}`

### Conclusion
This challenge demonstrates the importance of using secure elliptic curve parameters in cryptographic implementations. By allowing the user to provide custom curve parameters, the challenge opens the door for generating weak curves that can be exploited to break the cryptographic security.

The exploit takes advantage of the smooth order of the weak curve, which enables efficient discrete logarithm computations using the Pohlig-Hellman algorithm. By calculating the discrete logarithm of the challenge public key, we can obtain the private key and decrypt the flag.

The challenge highlights that parameter selection is security critical, and that usage of arbitrary, user selected parameters leads to vulnerabilities.