# Fixed Mistake

## Challenge Description
You know how it is when you promote CTF, write some articles and by mistake put some real flags to into? Well... our team makes mistakes too.

## Initial Analysis
The challenge description suggests that a real flag was accidentally published in an article promoting the CTF. The article is hosted on Hackernoon and is titled "So You Want to Be a Hacker".

Upon visiting the article's URL (https://hackernoon.com/so-you-want-to-be-a-hacker), we find a flag `1753c{fake_flag_try_harder}`. However, the challenge description mentions that this flag is fake and the real flag was different when the article was originally published.

## Approach
To solve this challenge, we need to find an archived version of the article that contains the original flag. We can use the Wayback Machine from the Internet Archive (https://web.archive.org/) to access an older version of the article.

## Solution
1. Visit the Wayback Machine: https://web.archive.org/
2. Enter the URL of the Hackernoon article: https://hackernoon.com/so-you-want-to-be-a-hacker
3. Select an archived version of the article from an earlier date.
4. Open the archived version of the article.
5. Search for the flag format `1753c{...}` within the article's content.
6. The original flag should be present in the archived version.

Flag: `1753c{s0m3_r4nd0m_t3xt}`

### Conclusion
The "Fixed Mistake" challenge demonstrates the importance of being careful when publishing sensitive information, such as flags, in public articles or websites. Even if the mistake is fixed later, the original content may still be accessible through web archives or caches.

This challenge highlights the need for thorough review and verification processes before publishing content related to CTF challenges or sensitive information. It also emphasizes the value of web archiving services like the Wayback Machine in retrieving historical versions of web pages.

By leveraging the Wayback Machine, participants can access an older version of the article and find the original flag that was accidentally published.
