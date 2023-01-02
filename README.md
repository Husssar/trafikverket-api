# trafikverket-api
This is just collecting values from road stations, with open API from
Trafikverket. Just signup and add a key to be able to use this, and when
collected the values are being pushed to a thingsboard integration. The
integration in Thingsboard is storing the values.

Just put the key you are given from Trafikverket in keys.py and also add the
integration key added for thingsboard. In thingsboard the integration having an
added header field to create some more securty.

The python file is the one that is being used. 

The .js file that is also in this lib, is to be able to test or/if needed for
other applications. Tried using the .js in Thingsboard directly, but
Thingsboard having some issues when using this as a integration directly.
