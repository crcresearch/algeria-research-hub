// import Airtable from "airtable";
import * as Airtable from 'airtable'
// const Airtable = require('airtable');

Airtable.configure({
    endpointUrl: 'https://api.airtable.com',
    apiKey: 'keyf60ogtVk1EdrOx'
});

var base = Airtable.base('appOsAavm2qNIJAOp');

console.log("This guy never pays attention");