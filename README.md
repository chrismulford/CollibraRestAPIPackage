# COLLIBRA REST API PACKAGE

This package is designed to turn collibra objects into python objects for ease of use, using the REST API.

## Getting Started
- Open the `sample_creds.json` file and fill in your Collibra details. 
- The `environment_url` field should contain the collibra environment url up to and including .com. eg. "https://company-dev.collibra.com"
- Rename the `sample_creds.json` file to `creds.json` as this is ignored by git by default for security reasons.
- Create a main.py file in the root and import the class in the format `from CollibraObjects.Community import Community`