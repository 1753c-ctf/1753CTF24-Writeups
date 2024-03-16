# Kind of Magic

## Challenge Description
Why generate thumbnails locally, when there's a web service to do it remotely?

## Initial Analysis
The challenge provides a web service that allows users to resize images by sending a POST request to the `/resize` endpoint with an image file. The service is built using the Rust programming language and the Rocket web framework.

Upon analyzing the provided code, we notice that the service uses an outdated version of the ImageMagick library (7.1.0.49) to perform the image resizing. This version is known to be vulnerable to a known issue (CVE-2022-44268) that allows for arbitrary file read.

## Approach
1. Create a malicious PNG image with a specially crafted "profile" metadata field containing the path to the file we want to read.
2. Send the malicious image to the `/resize` endpoint of the web service.
3. The vulnerable ImageMagick library will process the image and include the contents of the specified file in the "Raw profile type" metadata of the resized image.
4. Extract the file contents from the "Raw profile type" metadata of the response image.

## Exploiting the Vulnerability
The solve.py script does the following:
1. Creates a 1x1 pixel PNG image using the Pillow library.
2. Adds a "profile" metadata field to the PNG image, specifying the path to the file we want to read (e.g., `/flag`).
3. Sends a POST request to the `/resize` endpoint of the web service with the malicious PNG image as the payload.
4. Receives the resized image in the response and extracts the "Raw profile type" metadata.
5. Decodes the extracted file contents from the metadata and prints them.

The key points of the exploit are:
- The ImageMagick library version 7.1.0.49 is vulnerable to CVE-2022-44268, which allows for arbitrary file read via crafted image metadata.
- The "profile" metadata field in the PNG image is used to specify the path to the file we want to read.
- The contents of the specified file are included in the "Raw profile type" metadata of the resized image returned by the server.

## Obtaining the Flag
1. Run the solve.py script.
2. The script will create a malicious PNG image with the "profile" metadata field set to `/flag`.
3. The script will send the malicious image to the `/resize` endpoint of the web service.
4. The server will process the image using the vulnerable ImageMagick library and include the contents of the `/flag` file in the "Raw profile type" metadata of the resized image.
5. The script will extract the file contents from the metadata and print the flag.

Flag: `1753c{there_is_magic_in_the_air_its_called_CVE_2022_44268}`

### Conclusion
This challenge demonstrates the importance of keeping third-party libraries up to date and being aware of known vulnerabilities. The use of an outdated and vulnerable version of the ImageMagick library allowed for an arbitrary file read exploit.

The exploit takes advantage of the CVE-2022-44268 vulnerability, which allows an attacker to specify a file path in the "profile" metadata field of a crafted PNG image. When the vulnerable ImageMagick library processes the image, it includes the contents of the specified file in the metadata of the resulting image.

By sending a malicious image with the "profile" metadata field set to the path of the flag file, we were able to retrieve the flag contents from the resized image returned by the server.

The challenge highlights the need for regular updates and security audits of third-party dependencies to prevent the introduction of known vulnerabilities into the codebase.
