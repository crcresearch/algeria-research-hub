# Shell:
$ export AIRTABLE_API_KEY=API_KEY

# Node:
const base = require('airtable').base('appOsAavm2qNIJAOp');
EXAMPLE USING CUSTOM CONFIGURATION
var Airtable = require('airtable');
Airtable.configure({
    endpointUrl: 'https://api.airtable.com',
    apiKey: 'keyf60ogtVk1EdrOx'
});
var base = Airtable.base('appOsAavm2qNIJAOp');