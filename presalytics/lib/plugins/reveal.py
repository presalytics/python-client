import presalytics.lib.plugins.base as ext
import presalytics.lib.plugins.jinja as jinja


class RevealConfigPlugin(ext.ScriptPlugin, jinja.JinjaPluginMakerMixin):
    """
    Allows users configure reveal.js initialization settings for when their 
    story is rendered via `presalytics.story.revealer.Revealer`

    For more information regarding reveal.js' initialization settings, please
    refer to https://github.com/hakimel/reveal.js/#configuration        
    """
    __plugin_name__ = 'reveal'

    __dependencies__ = [
        {
            'kind': 'script',
            'name': 'external_scripts',
            'config': {
                'approved_scripts_key': 'reveal.base'
            }
        },
        {
            'kind': 'style',
            'name': 'external_links',
            'config': {
                'approved_styles_key': 'reveal.base'
            }
        },
        {
            'kind': 'style',
            'name': 'external_links',
            'config': {
                'approved_styles_key': 'reveal.themes.white'
            }
        },
        {
            'kind': 'style',
            'name': 'external_links',
            'config': {
                'approved_styles_key': 'reveal.customizations'
            }
        },
        {
            'kind': 'script',
            'name': 'external_scripts',
            'config': {
                'approved_scripts_key': 'reveal.customizations'
            }
        },
        
        
    ]

    def to_script(self, config, **kwargs):
        reveal_config = self.default_config
        if config.get("reveal_params", None):
            reveal_config.update(config.pop("reveal_params"))
        config.update({'reveal_config': reveal_config})
        return self.render(config)

    template = """
    <script type="text/javascript"> 
        window.onload = function(e) {
            Reveal.initialize(
                {{ reveal_config|tojson(indent=4) }}
            );
        };
    </script>
    """
    """
    The `<script>` fragment that get populated with a initialization data 
    via the `presalytics.lib.plugins.jinja.JinjaPluginMakerMixin`
    """
    
    default_config = {
        'controls': True,  # Display presentation control arrows
        # Help the user learn the controls by providing hints, for example by
        # bouncing the down arrow when they first encounter a vertical slide
        'controlsTutorial': True,

        # Determines where controls appear, "edges" or "bottom-right" #
        'controlsLayout': 'bottom-right',

        # Visibility rule for backwards navigation arrows; "faded", "hidden"
        # or "visible"
        'controlsBackArrows': 'faded',

        # Display a presentation progress bar
        'progress': True,

        # Display the page number of the current slide
        'slideNumber': False,

        # Add the current slide number to the URL hash so that reloading the
        #page/copying the URL will return you to the same slide
        'hash': False,

        # Push each slide change to the browser history. Implies `hash: true`
        'history': False,

        # Enable keyboard shortcuts for navigation 
        'keyboard': True,

        # Enable the slide overview mode
        'overview': True,

        # Vertical centering of slides
        'center': True,

        # Enables touch navigation on devices with touch input
        'touch': True,

        # Loop the presentation
        'loop': True,

        # Change the presentation direction to be RTL
        'rtl': False,

        # See https://github.com/hakimel/reveal.js/#navigation-mode
        'navigationMode': 'default',

        # Randomizes the order of slides each time the presentation loads
        'shuffle': False,

        # Turns fragments on and off globally
        'fragments': True,

        # Flags whether to include the current fragment in the URL,
        # so that reloading brings you to the same fragment position #}
        'fragmentInURL': False,

        # Flags if the presentation is running in an embedded mode,
        # i.e. contained within a limited portion of the screen #}
        'embedded': False,

        # Flags if we should show a help overlay when the questionmark
        # key is pressed #}
        'help': True,

        # Flags if speaker notes should be visible to all viewers
        'showNotes': False,

        # Global override for autoplaying embedded media (video/audio/iframe)
        # - null: Media will only autoplay if data-autoplay is present
        # - true: All media will autoplay, regardless of individual setting
        # - false: No media will autoplay, regardless of individual setting
        'autoPlayMedia': 'null',

        # Global override for preloading lazy-loaded iframes
        # - null: Iframes with data-src AND data-preload will be loaded when within
        #   the viewDistance, iframes with only data-src will be loaded when visible
        # - true: All iframes with data-src will be loaded when within the viewDistance
        # - false: All iframes with data-src will be loaded only when visible #}
        'preloadIframes': 'null',

        # Number of milliseconds between automatically proceeding to the
        # next slide, disabled when set to 0, this value can be overwritten
        # by using a data-autoslide attribute on your slides #}
        'autoSlide': 0,

        # Stop auto-sliding after user input
        'autoSlideStoppable': True,

        # Use this method for navigation when auto-sliding
        'autoSlideMethod': 'Reveal.navigateNext',

        # Specify the average time in seconds that you think you will spend
        # presenting each slide. This is used to show a pacing timer in the
        # speaker view 
        'defaultTiming': 120,

        # Enable slide navigation via mouse wheel
        'mouseWheel': False,

        # Hide cursor if inactive
        'hideInactiveCursor': True,

        # Time before the cursor is hidden (in ms)
        'hideCursorTime': 5000,

        # Hides the address bar on mobile devices
        'hideAddressBar': True,

        # Opens links in an iframe preview overlay
        #  Add `data-preview-link` and `data-preview-link="false"` to customise each link
        # individually
        'previewLinks': False,

        # Transition style
        'transition': 'slide', # none/fade/slide/convex/concave/zoom

        # Transition speed
        'transitionSpeed': 'default', # default/fast/slow

        # Transition style for full page slide backgrounds
        'backgroundTransition': 'fade', # none/fade/slide/convex/concave/zoom

        # Number of slides away from the current that are visible
        'viewDistance': 3,

        # Parallax background image
        'parallaxBackgroundImage': '', # e.g. "'https://s3.amazonaws.com/hakim-static/reveal-js/reveal-parallax-1.jpg'"

        # Parallax background size
        'parallaxBackgroundSize': '', # CSS syntax, e.g. "2100px 900px"

        # Number of pixels to move the parallax background per slide
        # - Calculated automatically unless specified
        # - Set to 0 to disable movement along an axis 
        'parallaxBackgroundHorizontal': 'null',
        'parallaxBackgroundVertical': 'null',

        # The display mode that will be used to show slides
        'display': 'block',

        # Allow for responsive presenation formats
        'width': "100%",
        'height': "100%",
        'margin': 0,
        'minScale': 1,
        'maxScale': 1
    }
    """
    A dictionary containing default values for rendering presalytics stories
    """