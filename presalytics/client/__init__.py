"""
This module conatains objects for interacting with the Presalytics API.  It has three submodules:
`presalytics.client.presalytics_doc_converter`, 'presalytics.client.presalytics_ooxml_automation`, and 
`presalytics.client.presalytics_story` contain that auto-generate code using the 
[OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator) and specifications from 
http://api.presalytics.io .

Modules contained at this level are middlewares to simplify user interaction with the generated 
code base and the Presalytics API.  
 - `presalytics.client.auth` contains authentication and request handling handling middleware
 - `presalytics.client.api` conatains wrapper classes and convenience extensions so that users
only need to instantiate one object to get access to all public microservices in the Presalytics API
"""