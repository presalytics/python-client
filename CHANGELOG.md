
## v0.5.12 (2020-08-18)

* Fix api_name and external_root_url bug
* Incorporate async to workflows
* add new story api endpoints

## v0.5.11 (2020-08-13)

* Fix single-page rendering bugs

## v0.5.10 (2020-08-13)

* Enable single-page rendering

## v0.5.9 (2020-08-11)

* Add methods to support async in the story api
* Update tests to support async
* Remove jwts from html generation

## v0.5.8 (2020-07-30)

* Add cloning functionality for ooxml documents
* Fix camelCase bug in `presalytics.lib.plugins.ooxml`

## v0.5.7 (2020-07-21)

* Update `presalytics.story.revealer.Revealer` to hide controls for single page stories
* Fix auth bug introduced to token caching with switch to 3rd party auth

## v0.5.6 (2020-07-17)

* Add `external_root_url` to `AuthenticationMixIn`, implement in `D3Widget`

## v0.5.5 (2020-07-17)

* Add D3Widget to `__init__.py`
* Bug fix to `presalytics.lib.tools.workflows`

## v0.5.4 (2020-07-14)

* Update D3pipWidget to include custom html, css from files

## v0.5.3 (2020-07-14)

* Add D3Widget, Content Secuirty Policies 

## v0.5.2 (2020-07-14)

* Fix page order bug in `presalytics.lib.tools.ooxml_tools.create_pages_from_ooxml_document`

## v0.5.1 (2020-05-21)

* Add json endpoint to presaltyics story 

## v0.5.0 (2020-05-21)

* Refactor authentication / authorization for 3rd Party Provider (Auth0)
* Add `presalytics.client.oidc.OidcClent` to manage token acquisition
* Improve fault tolerance of token handling and refresh