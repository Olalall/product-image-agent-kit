# Security Policy

## Supported versions

The public starter is pre-1.0. Security fixes should target `main`.

## Reporting a vulnerability

Please open a private security advisory if the repository is hosted on GitHub, or contact the maintainer privately.

Do not post secrets, credentials, private product data, or exploit details in a public issue.

## Safety boundaries

Product Image Agent Kit is local-first by default:

- no API key is required for the demo;
- no paid API call is made by the default workflow;
- no external upload, overwrite, delete, or publish is performed by the default workflow;
- live external actions must require explicit human approval.
