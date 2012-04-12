# Digest Demo

This is sample code for implementing HTTP Digest Authentication on the Google App Engine using the python 2.7 runtime.

## Notes

The code uses memcache to store the digest nonce. This means on the one hand that unused nonces are automatically removed, but on the other hand that they might be removed too early. This would result in an authentication failure when none should happen.

Re-using nonces with different client nonces is not implemented, but not really required (for the cost of an additional HTTP roundtrip).

## License

DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
                    Version 2, December 2004 

 Copyright (C) 2012 Andreas Monitzer <andy@monitzer.com>

 Everyone is permitted to copy and distribute verbatim or modified 
 copies of this license document, and changing it is allowed as long 
 as the name is changed. 

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 

  0. You just DO WHAT THE FUCK YOU WANT TO. 
