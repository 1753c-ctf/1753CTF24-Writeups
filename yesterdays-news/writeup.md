# Yesterday's News

## Challenge Description
We've hijacked a note from a very strange individual. Seems to be some secret admin panel, but we can't really get in.

## Initial Analysis
The challenge provides an Android APK file. Upon decompiling the APK using an online decompiler like [JADX](https://jadx.io/), we can examine the source code of the app.

In the `MainActivity` class, we find a method called `generateTOTP()` that generates a Time-based One-Time Password (TOTP) using a secret key and a specific clock offset. The generated TOTP is displayed on the app's screen and updates every second.

However, the clock used to generate the TOTP is offset by -1 day, which means the TOTP is generated for the previous day.

## Approach
To solve this challenge, we need to:
1. Extract the secret key used for TOTP generation from the decompiled code.
2. Generate the correct TOTP using the secret key and the current time (without the -1 day offset).
3. Use the generated TOTP to access the secret admin panel and obtain the flag.

## Solution
Here's a Python script to generate the correct TOTP:

```python
import pyotp
import time

secret_key = "IMSEXYANDIKNOWIT"
totp = pyotp.TOTP(secret_key)

current_time = int(time.time())
totp_value = totp.at(current_time)

print("Current TOTP:", totp_value)
```

- Install the required dependencies:

```
pip install pyotp
```

- Save the script to a file (e.g., generate_totp.py).

- Run the script:

```
python generate_totp.py
```

- The script will output the current TOTP value.

- Use the generated TOTP to access the secret admin panel.

- Obtain the flag from the admin panel.

> Flag: 1753c{welcome_to_the_world_of_yesterday}

## Conclusion
The "Yesterday's News" challenge demonstrates the importance of properly implementing and securing Time-based One-Time Password (TOTP) systems. By analyzing the decompiled Android app, participants can identify the flaw in the TOTP generation process, where the clock is offset by -1 day.

Exploiting this flaw allows participants to generate the correct TOTP using the secret key and the current time, bypassing the intended security measure. This challenge highlights the need for careful implementation and testing of security mechanisms, especially when dealing with time-sensitive cryptographic algorithms like TOTP.

By leveraging the extracted secret key and generating the TOTP using the current time, participants can access the secret admin panel and retrieve the flag.