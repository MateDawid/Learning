# One Time Passwords

Source: https://testdriven.io/blog/web-authentication-methods/#one-time-passwords

## Intro
One time passwords (OTPs) are commonly used as confirmation for authentication. OTPs are randomly generated codes that can be used to verify if the user is who they claim to be. Its often used after user credentials are verified for apps that leverage two-factor authentication.

To use OTP, a trusted system must be present. This trusted system could be a verified email or mobile number.

Modern OTPs are stateless. They can be verified using multiple methods. While there are a few different types of OTPs, Time-based OTPs (TOTPs) is arguably the most common type. Once generated, they expire after a period of time.

Since you get an added layer of security, OTPs are recommended for apps that involve highly sensitive data, like online banking and other financial services.

## Flow
The traditional way of implementing OTPs:

* Client sends username and password
* After credential verification, the server generates a random code, stores it on the server-side, and sends the code to the trusted system
* The user gets the code on the trusted system and enters it back on the web app
* The server verifies the code against the one stored and grants access accordingly

How TOTPs work:

* Client sends username and password
* After credential verification, the server generates a random code using a randomly generated seed, stores the seed on the server-side, and sends the code to the trusted system
* The user gets the code on the trusted system and enters it back on the web app
* The server verifies the code against the stored seed, ensures that it has not expired, and grants access accordingly

How OTP agents like Google Authenticator, Microsoft Authenticator, and FreeOTP work:

* Upon registering for Two Factor Authentication (2FA), the server generates a random seed value and sends the seed to the user in the form of unique QR code
* The user scans the QR code using their 2FA application to validate the trusted device
* Whenever the OTP is required, the user checks for the code on their device and enters it on the web app
* The server verifies the code and grants access accordingly

## Pros
* Adds an extra layer of protection.
* No danger that a stolen password can be used for multiple sites or services that also implement OTPs.
## Cons
* You need to store the seed used for generating OTPs.
* OTP agents like Google Authenticator are difficult to set up again if you lose the recovery code.
* Problems arise when the trusted device is not available (dead battery, network error, etc.). Because of this, a backup device is typically required which adds an additional attack vector.