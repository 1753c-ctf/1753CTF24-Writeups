# Resume

## Challenge Description
Hi, I'm Mike and this is my resume. Drop me an email if you want to get some flags, cause I got them all...

## Solution
1. Visit the provided URL: https://cv-13e304e345c1.1753ctf.com
2. Analyze the website's source code and notice the Gravatar URL in the avatar image: `https://www.gravatar.com/avatar/2471b1362bace767fdc0bb9c7e4df686?s=150`
3. Extract the MD5 hash from the Gravatar URL: `2471b1362bace767fdc0bb9c7e4df686`
4. Use a wordlist like `rockyou.txt` to generate possible email addresses at `@1753ctf.com` and compare their MD5 hashes with the extracted hash.
5. Find the matching email: `keeponrocking@1753ctf.com`
6. Send an email to `keeponrocking@1753ctf.com`
7. Receive a reply from Mike containing the flag.

Here's a short Python script to bruteforce the email:

```python
import hashlib

def get_md5(email):
    return hashlib.md5(email.encode()).hexdigest()

wordlist = "rockyou.txt"
target_hash = "2471b1362bace767fdc0bb9c7e4df686"

with open(wordlist, "r") as file:
    for line in file:
        word = line.strip()
        email = f"{word}@1753ctf.com"
        email_hash = get_md5(email)
        if email_hash == target_hash:
            print(f"Found matching email: {email}")
            break
```

The script reads words from the rockyou.txt wordlist, generates email addresses by appending @1753ctf.com, calculates the MD5 hash of each email, and compares it with the target hash. It stops when a matching email is found.

Mike replies with:

```
Hey, this is your buddy Mike

Got too many inquiries right now to reply to all, but please feel free to use this first sample flag I’m happy to share with you for free

1753c{i_have_dizzz_flagzz_baby}

I’ll be in touch soon
Mike!
```

> Flag: 1753c{i_have_dizzz_flagzz_baby}

## Conclusion

 By analyzing the website's source code and leveraging the Gravatar service, it was possible to deduce Mike's email address and obtain the flag by sending him an email. This challenge emphasizes the need for proper email obfuscation and the risks associated with using predictable email addresses.


