Everything required for the "OBP Oauth1 Django"-Example

Version 0.2.0

The keywords "MUST," "MUST NOT," "REQUIRED," "SHALL," "SHALL NOT," "SHOULD," "SHOULD NOT," "RECOMMENDED," "MAY," and "OPTIONAL" in this document and all other documents within this repository are to be interpreted as described in RFC 2119.

## Example application (local)

1. Generate a virtual work environment, and install the required files

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    
2. Register with an OBP instance and register a new application. Save the OAUTH_KEY, and OAUTH_SECRET within your environment or patch main/settings.py
  
3. Generate a default database, default admin user and start the Django defaults server
  
4. Download and install "ngrok" or "local tunnel" (https://localtunnel.github.io/www/) within your development environment, for tests with "HTTPS."

5. Start Django and your tunnel, and select the provided link in your webbrowser. 
