# Unbreakable

## Challenge Description
Me: Is one-time-pad unbreakable?

Chat GPT: Yes, Your Awesomeness, a one-time pad is theoretically unbreakable when used correctly. This is because each bit of plaintext is encrypted with a completely random bit of the key, and each key is used only once, making it impossible to derive the original message without the exact key.

Me: Okay, let's get that completely random bits!

## Initial Analysis
The challenge provides a C# code snippet that encrypts a flag using a one-time pad (OTP) encryption scheme. The encryption process is as follows:
1. Generate a random seed based on the current date (DateTime.Today).
2. Create a random number generator (Random) using the seed.
3. Generate a random byte buffer (randomBuffer) of the same length as the flag.
4. Convert the flag string to a byte array (flagBuffer).
5. XOR each byte of the random buffer with the corresponding byte of the flag buffer.
6. Convert the resulting byte array (resultBuffer) to a hexadecimal string (encrypted).

The encrypted flag is then printed to the console.

## Approach
To solve this challenge, we need to exploit the weakness in the random number generation. The code uses the current date as the seed for the random number generator, which means that the same seed will be used for all encryptions performed on the same day. By knowing the seed value, we can recreate the random byte buffer and XOR it with the encrypted flag to recover the original flag.

However, since we don't know the exact date when the flag was encrypted, we need to try different dates until we find a decrypted text that contains the flag format.

## Exploit Code
Here's the exploit code in C# to decrypt the flag:

```csharp
using System;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

class Program
{
   static void Main()
   {
       var encrypted = "22ECCDB90936D5C2454A65A5BB4C120FB1C8567381C6DB368EB57D4C6BE8B6D8C860E5C6FAC1F48BF2291A5C9EA3C354715857E7";
       var encryptedBuffer = Enumerable.Range(0, encrypted.Length)
                                       .Where(x => x % 2 == 0)
                                       .Select(x => Convert.ToByte(encrypted.Substring(x, 2), 16))
                                       .ToArray();

       var currentDate = DateTime.Today;
       var flagRegex = new Regex(@"1753c\{[^}]+\}");

       while (true)
       {
           var seed = new DateTimeOffset(currentDate).ToUnixTimeSeconds();
           var random = new Random((int)seed);
           var randomBuffer = new byte[encryptedBuffer.Length];
           random.NextBytes(randomBuffer);

           var flagBuffer = new byte[encryptedBuffer.Length];
           for (var i = 0; i < encryptedBuffer.Length; i++)
               flagBuffer[i] = (byte)(randomBuffer[i] ^ encryptedBuffer[i]);

           var decryptedText = Encoding.ASCII.GetString(flagBuffer);
           if (flagRegex.IsMatch(decryptedText))
           {
               Console.WriteLine($"Flag found on {currentDate:yyyy-MM-dd}:");
               Console.WriteLine(decryptedText);
               break;
           }

           currentDate = currentDate.AddDays(-1);
       }
   }
}
```

The exploit code does the following:
1. Convert the encrypted hexadecimal string to a byte array (encryptedBuffer).
2. Start with the current date and initialize a regular expression pattern to match the flag format.
3. Enter a loop that continues until the flag is found:
  - Generate a random seed based on the current date.
  - Create a random number generator using the seed.
  - Generate a random byte buffer (randomBuffer) of the same length as the encrypted flag.
  - XOR each byte of the random buffer with the corresponding byte of the encrypted flag buffer.
  - Convert the resulting byte array (flagBuffer) to a string (decryptedText).
  - Check if the decrypted text matches the flag format using the regular expression.
  - If the flag is found, print the date and the decrypted flag, and break the loop.
  - If the flag is not found, move to the previous date and continue the loop.

## Obtaining the Flag
1. Save the exploit code to a file with a .cs extension (e.g., exploit.cs).
2. Compile the exploit code using a C# compiler (e.g., csc exploit.cs).
3. Run the compiled executable (e.g., exploit.exe).
4. The exploit code will try different dates until it finds the decrypted flag.
5. The date and the flag will be printed to the console.

Flag: `1753c{you_will_never_guess_the_flag_coz_i_am_xorrro}`

### Conclusion
This challenge demonstrates the importance of using truly random and unique keys for one-time pad encryption. The vulnerability in the provided code lies in the use of a predictable seed value based on the current date. By exploiting this weakness and trying different dates, an attacker can recreate the random byte buffer used for encryption and recover the original flag.

The challenge highlights the need for secure random number generation and the proper implementation of cryptographic algorithms. It also serves as a reminder that the theoretical unbreakability of one-time pad encryption relies on the use of truly random and never-reused keys.
