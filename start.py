import presalytics

c = presalytics.Client()

print(c.story.api_client.configuration.host)
