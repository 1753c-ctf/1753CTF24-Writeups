# Questions

To solve this challenge, you must ask the bot for all bits of the flag string.

You can do this manually, but it will be quite time-consuming.

The best way will be to write a small telegram scraper, for example built in Python using the [Telethon](https://github.com/LonamiWebs/Telethon) library.

First you need to create a Telegram account and register with [api access](https://my.telegram.org/apps), the process is well documented in [Telethon docs](https://docs.telethon.dev/en/stable/basic/signing-in.html).

After receiving all the flag bits you have to concatenate them and convert to string, for example using [CyberChef](https://gchq.github.io/CyberChef/).

Scrapper tool example is attached to this writeup.

What is important in such cases is to respect the telegram [request limits](https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this).
