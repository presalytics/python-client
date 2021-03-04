import sys
import os


p_path = os.path.join(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(p_path)

import presalytics

CLIENT_SPECS = [
    {
        "update": True,
        "update_type": "patch",
        "endpoint": "{}/openapi.json".format(presalytics.settings.HOST_DOC_CONVERTER),
        "package_name": "doc_converter",
    },
    {
        "update": True,
        "update_type": "patch",
        "endpoint": "{0}/docs/v1-no-tags/openapi.json".format(presalytics.settings.HOST_OOXML_AUTOMATION),
        "package_name": "ooxml_automation"
    },
    {
        "update": True,
        "update_type": "patch",
        "endpoint": "{0}/no_tags_spec".format(presalytics.settings.HOST_STORY),
        "package_name": "story",
    },
    {
        "update": True,
        "update_type": "patch",
        "endpoint": "{0}/openapi/v0/openapi.json".format(presalytics.settings.HOST_EVENTS),
        "package_name": "events"

    }
]
