# Flag GPT

## Challenge Description
Chat GPT was too easy to fool, still giving our flag to unauthorized players.

Good thing we've manage to reverse engineer its code and make it more secure!

## Initial Analysis
The challenge provides a web application that simulates a chatbot similar to ChatGPT. The application is built using Node.js and Express.js.

Upon analyzing the provided code, we notice the following:
- The `/chat` endpoint accepts a `message` query parameter and responds with a JSON object containing a message.
- The code attempts to remove any occurrences of the word "flag" from the `message` parameter using a `replace` function and a `while` loop.
- The `replace` function uses a case-insensitive regular expression to replace occurrences of "flag" with an empty string.
- The `while` loop continues until the `indexOf` function, which is case-sensitive, no longer finds the substring "flag" in the message.
- If the `message` contains certain keywords like "hi", "hello", or "hey", the chatbot responds with a greeting.
- If the `message` contains question words like "what", "who", "were", "when", or "why", the chatbot responds with "I don't know!".
- If the `message` contains the word "flag", the chatbot responds with "The flag is " followed by the value of the `flag` environment variable or a fake flag for testing.

## Vulnerability
The vulnerability in this code lies in the discrepancy between the case-insensitive regular expression used in the `replace` function and the case-sensitive `indexOf` check in the `while` loop.

The `replace` function uses a case-insensitive regular expression to replace occurrences of "flag" with an empty string. However, the `while` loop continues until the case-sensitive `indexOf` function no longer finds the substring "flag" in the message.

This means that if the `message` contains the word "flag" with mixed case (e.g., "flAg" or "fLaG"), the `replace` function will only remove it in first run of the `while` loop and will still exit because the case-sensitive `indexOf` function won't find "flag" in the modified message.

## Exploit

The important part is that the `while` loop will fire at least once as it's a `do .. while` variant. For this we need to be smart and prepare the payload in a way that will still contain mixed case word "flag" after the `while` loop exits.

One of the ideas might be building message like "FLflagAG"

This when program will enter the `do .. while` loop it will remove the "flag" part, leaving user input as "FLAG". Then the `indexof` being case-sensitive will ignore that word as `"FLAG" != "flag"`.

Payload "FLAG" will then get to the final check and the flag will be returned.

## Conclusion

The "Flag GPT" challenge demonstrates the importance of consistently handling case-sensitivity in input validation and string manipulation. The vulnerability in the provided code lies in the discrepancy between the case-insensitive regular expression used in the replace function and the case-sensitive indexOf check in the while loop.

By crafting a payload that contains the word "flag" with mixed case, an attacker can bypass the case-insensitive replacement and still trigger the flag response. This allows the attacker to retrieve the flag despite the attempts to remove it from the user input.

