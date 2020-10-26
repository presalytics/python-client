## v0.5.22 (2020-10-13)

* Add events handling to widgets with nested iframes

## v0.5.21 (2020-10-13)

* Fix page css clases

## v0.5.20 (2020-10-13)

* Fix json encoder in `presalytics.lib.widgets.datatable.DataTableWidget`
* update Story Api Endpoints

## v0.5.19 (2020-09-20)

* Point `ooxml.js` to static folder on main site in `presalytics.lib.plugins.external.ApprovedExternalScripts`
* Add `presalytics.lib.widgets.url.UrlWidget`
* Add `presalytics.lib.widgets.chart.ChartWidget`
* Add `presalytics.lib.widgets.datatable.DataTableWidget`
* Fix immutability bug in `presalytics.lib.plugins.reveal.RevealConfigPlugin.default_config`

## v0.5.18 (2020-09-01)

* Update `ooxml_editors.TextReplace` to enable child object editing

## v0.5.17 (2020-08-30)

* Fix font-awesome for CORS/CDN in `external.py`

## v0.5.16 (2020-08-28)

* Add toolbar to reveal plugin
* Change reveal.js approved links from cdn to presalytics.io

## v0.5.15 (2020-08-24)

* Fix color insert libreoffice compatibility bug in `presalytics.lib.widgets.ooxml_editors.ChangeShapeColor` 

## v0.5.14 (2020-08-24)

* Increase match greediness in `presalytics.lib.widgets.ooxml_editors.TextReplace`

## v0.5.13 (2020-08-18)

* add new story api endpoints

## v0.5.12 (2020-08-18)

* Fix api_name and external_root_url bug
* Incorporate async to workflows


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