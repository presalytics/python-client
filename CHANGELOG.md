# Changes by Version

## TODO (v0.7)

- [ ] Add `presalytics.lib.tools.workflow.create_workspace`
- [ ] Change file handling support beyond ooxml files

## v0.6.4

- [x] Fix `presalytics.story.renderers.ClientSideRender` bug
- [x] Add `presalytics.story.outline.OutlineDecoder`

## v0.6.3

- [x] Add settings_path environ

## v0.6.2

- [x] Remove pkg_resources

## v0.6.1

- [x] Loosen requirements to `>=` to make installs more flexible

## v0.6.0

- [x] Change loader to allow for explicit loading via settings.py
- [x] Turn off logger, autodiscovery, and token caching by default
- [x] Create `presalytics.settings` module for default settings, incorprate into `__init__.py`
- [x] Create `presalytics.client.websocket` for event listener and forward events to localhost
- [x] Create `presalytics.story.renderers.ClientSideRenderer` to set up caching and return meta for client-side apps to render stories
- [x] Add CLI commands for websocket
- [x] Incorporate `requirements.txt` into `setup.py`
- [x] Standardize linting with mypy and flake8
- [x] Add ids to outline pages and widgets for tracking as page and widget order changes

## v0.5.24

- [x] Eliminate overwrite error in cli

## v0.5.23

- [x] Fix cli initial pull in empty workspace
- [x] Fix cli default to CACHE_TOKENS = True

## v0.5.22 (2020-10-13)

- [x] Add events handling to widgets with nested iframes

## v0.5.21 (2020-10-13)

- [x] Fix page css clases

## v0.5.20 (2020-10-13)

- [x] Fix json encoder in `presalytics.lib.widgets.datatable.DataTableWidget`
- [x] update Story Api Endpoints

## v0.5.19 (2020-09-20)

- [x] Point `ooxml.js` to static folder on main site in `presalytics.lib.plugins.external.ApprovedExternalScripts`
- [x] Add `presalytics.lib.widgets.url.UrlWidget`
- [x] Add `presalytics.lib.widgets.chart.ChartWidget`
- [x] Add `presalytics.lib.widgets.datatable.DataTableWidget`
- [x] Fix immutability bug in `presalytics.lib.plugins.reveal.RevealConfigPlugin.default_config`

## v0.5.18 (2020-09-01)

- [x] Update `ooxml_editors.TextReplace` to enable child object editing

## v0.5.17 (2020-08-30)

- [x] Fix font-awesome for CORS/CDN in `external.py`

## v0.5.16 (2020-08-28)

- [x] Add toolbar to reveal plugin
- [x] Change reveal.js approved links from cdn to presalytics.io

## v0.5.15 (2020-08-24)

- [x] Fix color insert libreoffice compatibility bug in `presalytics.lib.widgets.ooxml_editors.ChangeShapeColor`

## v0.5.14 (2020-08-24)

- [x] Increase match greediness in `presalytics.lib.widgets.ooxml_editors.TextReplace`

## v0.5.13 (2020-08-18)

- [x] add new story api endpoints

## v0.5.12 (2020-08-18)

- [x] Fix api_name and external_root_url bug
- [x] Incorporate async to workflows

## v0.5.11 (2020-08-13)

- [x] Fix single-page rendering bugs

## v0.5.10 (2020-08-13)

- [x] Enable single-page rendering

## v0.5.9 (2020-08-11)

- [x] Add methods to support async in the story api
- [x] Update tests to support async
- [x] Remove jwts from html generation

## v0.5.8 (2020-07-30)

- [x] Add cloning functionality for ooxml documents
- [x] Fix camelCase bug in `presalytics.lib.plugins.ooxml`

## v0.5.7 (2020-07-21)

- [x] Update `presalytics.story.revealer.Revealer` to hide controls for single page stories
- [x] Fix auth bug introduced to token caching with switch to 3rd party auth

## v0.5.6 (2020-07-17)

- [x] Add `external_root_url` to `AuthenticationMixIn`, implement in `D3Widget`

## v0.5.5 (2020-07-17)

- [x] Add D3Widget to `__init__.py`
- [x] Bug fix to `presalytics.lib.tools.workflows`

## v0.5.4 (2020-07-14)

- [x] Update D3pipWidget to include custom html, css from files

## v0.5.3 (2020-07-14)

- [x] Add D3Widget, Content Secuirty Policies

## v0.5.2 (2020-07-14)

- [x] Fix page order bug in `presalytics.lib.tools.ooxml_tools.create_pages_from_ooxml_document`

## v0.5.1 (2020-05-21)

- [x] Add json endpoint to presaltyics story

## v0.5.0 (2020-05-21)

- [x] Refactor authentication / authorization for 3rd Party Provider (Auth0)
- [x] Add `presalytics.client.oidc.OidcClent` to manage token acquisition
- [x] Improve fault tolerance of token handling and refresh
