# OAuth and OpenID

> Source 1: https://testdriven.io/blog/web-authentication-methods/#oauth-and-openid
> 
> Source 2: https://developer.okta.com/blog/2019/10/21/illustrated-guide-to-oauth-and-oidc

## Intro

OpenID - used for authentication
OAuth - used for authorization

OAuth 2.0 is designed only for authorization, for granting access to data and features from one application to another. OpenID Connect (OIDC) is a thin layer that sits on top of OAuth 2.0 that adds login and profile information about the person who is logged in. Establishing a login session is often referred to as authentication, and information about the person logged in (i.e. the Resource Owner) is called identity. When an Authorization Server supports OIDC, it is sometimes called an identity provider, since it provides information about the Resource Owner back to the Client.

OpenID Connect enables scenarios where one login can be used across multiple applications, also known as single sign-on (SSO). For example, an application could support SSO with social networking services such as Facebook or Twitter so that users can choose to leverage a login they already have and are comfortable using.

OAuth/OAuth2 and OpenID are popular forms of authorization and authentication, respectively. They are used to implement social login, which is a form of single sign-on (SSO) using existing information from a social networking service such as Facebook, Twitter, or Google, to sign in to a third-party website instead of creating a new login account specifically for that website.

This type of authentication and authorization can be used when you need to have highly-secure authentication. Some of these providers have more than enough resources to invest in the authentication itself. Leveraging such battle-tested authentication systems can ultimately make your application more secure.

This method is often coupled with session-based auth.

## Flow

You visit a website that requires you to log in. You navigate to the login page and see a button called "Sign in with Google". You click the button and it takes you to the Google login page. Once authenticated, you're then redirected back to the website that logs you in automatically. This is an example of using OpenID for authentication. It lets you authenticate using an existing account (via an OpenID provider) without the need to create a new account.

The most famous OpenID providers are Google, Facebook, Twitter, and GitHub.

After logging in, you navigate to the download service within the website that lets you download large files directly to Google Drive. How does the website get access to your Google Drive? This is where OAuth comes into play. You can grant permissions to access resources on another website. In this case, write access to Google Drive.

## Pros

* Improved security.
* Easier and faster log in flows since there's no need to create and remember a username or password.
* In case of a security breach, no third-party damage will occur, as the authentication is passwordless.

## Cons

* Your application now depends on another app, outside of your control. If the OpenID system is down, users won't be able to log in.
* People often tend to ignore the permissions requested by OAuth applications.
* Users that don't have accounts on the OpenID providers that you have configured won't be able to access your application. The best approach is to implement both -- i.e., username and password and OpenID -- and let the user choose.

