# Box Noir

## Challenge Description
Did you know you can compile C for browsers? Possibilities are endless!

## Initial Analysis
The challenge provides a web page that includes a WebAssembly (WASM) module. The page allows users to input a flag guess, which is then passed to a function called `checkFlag` in the WASM module.

To solve this challenge, we need to decompile the WASM code and analyze it to understand how the flag is being mixed and compared.

## Decompiling the WASM Code
We can use online decompilers like [WebAssembly Studio](https://webassembly.studio/) or [WasmExplorer](https://mbebenita.github.io/WasmExplorer/) to decompile the WASM code.

After decompiling the code, we find the following important parts:
- The `checkFlag` function takes an input string, mixes its characters using the `mixString` function, and then compares the mixed input with the `mixedFlag` string.
- The `mixString` function swaps specific characters in the input string according to the defined `SWAP` macro.

## Exploit Script
To exploit this vulnerability and retrieve the original flag, we can reverse the character swapping process to unmix the `mixedFlag` string.

Here's a Python script that exploits the vulnerability:

```python
def swap(dst, a, b):
   dst[a], dst[b] = dst[b], dst[a]

def unmixString(dst):
   swap(dst, 11, 19)
   swap(dst, 10, 18)
   swap(dst, 8, 14)
   swap(dst, 7, 12)
   swap(dst, 6, 9)
   swap(dst, 3, 4)
   swap(dst, 2, 17)
   swap(dst, 1, 5)
   swap(dst, 0, 16)

mixedFlag = list("3{Lc374_0LU}UMKD155Z")
unmixString(mixedFlag)
flag = ''.join(mixedFlag)
print("Flag:", flag)
```

1. Save the script to a file (e.g., `exploit.py`).
2. Run the script:

```
python exploit.py
```

3. The script will output the original flag.

The exploit script does the following:
1. Defines the `swap` function to swap characters in a list.
2. Defines the `unmixString` function, which performs the character swapping operations in reverse order compared to the `mixString` function in the decompiled code.
3. Converts the `mixedFlag` string to a list of characters.
4. Calls the `unmixString` function to unmix the characters in the `mixedFlag` list.
5. Joins the characters in the `mixedFlag` list back into a string.
6. Prints the original flag.

Flag: `1753c{LUK45Z_M0D3LU}`

### Conclusion
The "Box Noir" challenge demonstrates the importance of properly obfuscating and securing sensitive information, even when using technologies like WebAssembly. By decompiling the WASM code, participants can analyze the logic behind the flag mixing process and reverse-engineer it to obtain the original flag.

This challenge highlights the need for robust obfuscation techniques and the avoidance of relying solely on client-side security measures. It also emphasizes the importance of thoroughly testing and validating the security of applications, especially when dealing with sensitive data like flags.

By understanding the character swapping algorithm and reversing the process, participants can unmix the `mixedFlag` string and retrieve the original flag.