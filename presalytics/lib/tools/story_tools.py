import typing
import logging
import urllib.parse
import requests
import presalytics.lib.tools.ooxml_tools
import presalytics.lib.exceptions
if typing.TYPE_CHECKING:
    from presalytics.client.api import Client
    from io import BytesIO


logger = logging.getLogger(__name__)


def story_post_file_bytes(client: 'Client', 
                          binary_obj: 'BytesIO', 
                          filename: str,
                          mime_type: str = None):
    """
    Create a Presalytics API Story object from a file-like `io.BytesIO` object.  Helpful for server-side 
    interaction with the Presalytics Story API

    Parameters
    ----------
    client : presalytics.client.api.Client
        A client object for making api calls
    
    binary_obj : io.BytesIO
        A file-like object for storing file-data in memory.  Often found in multipart messages
        uploaded from browsers.
    
    filename : str
        The filename of the object to be uploaded

    mimetype : str, optional
        If known, please add the mimetype of the file.  Otherwise, this method will execute an 
        additional API call ascertain the file's mimetype

    Returns
    ----------
    A `presalytics.client.presalytics_story.models.story.Story` containing information about the Story object in the Presalytics API
    """
    if not mime_type:
        mime_type = presalytics.lib.tools.ooxml_tools.get_mime_type_from_filename(client, filename)
    _file = {'file': (filename, binary_obj, mime_type,)}
    headers = client.get_auth_header()
    headers.update(client.get_request_id_header())
    headers.update({
        'User-Agent': client.story.api_client.user_agent,
        'Accept': 'application/json'
    })
    endpoint = urllib.parse.urljoin(client.story.api_client.configuration.host, 'story/file')
    try:
        resp = requests.post(endpoint, headers=headers, files=_file)
    except Exception as ex:
        message = "An error occured in the presalytics API client"
        raise presalytics.lib.exceptions.ApiError(message=message, status_code=resp.status_code)
    data = resp.json()
    if resp.status_code > 299:
        logger.error(data['detail'])
        raise presalytics.lib.exceptions.ApiError(message=data["detail"], status_code=resp.status_code)
    else:
        try:
            story = client.story.api_client._ApiClient__deserialize(data, 'Story')
            return story
        except Exception as ex:
            logger.error("Story object could not be deserialized.")
            logger.exception(ex)
        return data
