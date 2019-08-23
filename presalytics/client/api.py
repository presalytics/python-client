import pkg_resources
import presalytics_doc_converter
import presalytics_ooxml_automation
from .auth import AuthenticationMixIn

def get_user_agent():
    try:
        VER = pkg_resources.require("presalytics")[0].version
    except:
        VER = 'build'
    return "presalytics-python-client/{0}".format(VER)


class DocConverterApiClientWithAuth(AuthenticationMixIn, presalytics_doc_converter.api_client.ApiClient):
    def __init__(self, config_file=None, **kwargs):
        AuthenticationMixIn.__init__(self, config_file=config_file)
        presalytics_doc_converter.api_client.ApiClient.__init__(self, **kwargs)
        self.user_agent = get_user_agent()

class OoxmlAutomationApiClientWithAuth(AuthenticationMixIn, presalytics_ooxml_automation.api_client.ApiClient):
    def __init__(self, config_file=None, **kwargs):
        AuthenticationMixIn.__init__(self, config_file=config_file)
        presalytics_ooxml_automation.api_client.ApiClient.__init__(self, **kwargs)
        self.user_agent = get_user_agent()

class OoxmlAutomationContainer(object):
    def __init__(self, config_file=None):
        ooxml_automation_api_client = OoxmlAutomationApiClientWithAuth(config_file=config_file)
        self.axes = presalytics_ooxml_automation.AxesApi(api_client=ooxml_automation_api_client)
        self.axis_data_types = presalytics_ooxml_automation.AxisDataTypesApi(api_client=ooxml_automation_api_client)
        self.background_fills = presalytics_ooxml_automation.BackgroundFillsApi(api_client=ooxml_automation_api_client)
        self.borders = presalytics_ooxml_automation.BordersApi(api_client=ooxml_automation_api_client)
        self.cells = presalytics_ooxml_automation.CellsApi(api_client=ooxml_automation_api_client)
        self.chart_data = presalytics_ooxml_automation.ChartDataApi(api_client=ooxml_automation_api_client)
        self.charts = presalytics_ooxml_automation.ChartsApi(api_client=ooxml_automation_api_client)
        self.color_maps = presalytics_ooxml_automation.ColorMapsApi(api_client=ooxml_automation_api_client)
        self.color_transformation_attributes = presalytics_ooxml_automation.ColorTransformationAttributesApi(api_client=ooxml_automation_api_client)
        self.color_transformations = presalytics_ooxml_automation.ColorTransformationsApi(api_client=ooxml_automation_api_client)
        self.color_types = presalytics_ooxml_automation.ColorTypesApi(api_client=ooxml_automation_api_client)
        self.colors = presalytics_ooxml_automation.ColorsApi(api_client=ooxml_automation_api_client)
        self.column_collections = presalytics_ooxml_automation.ColumnCollectionsApi(api_client=ooxml_automation_api_client)
        self.columns = presalytics_ooxml_automation.ColumnsApi(api_client=ooxml_automation_api_client)
        self.custom_colors = presalytics_ooxml_automation.CustomColorsApi(api_client=ooxml_automation_api_client)
        self.dash_types = presalytics_ooxml_automation.DashTypesApi(api_client=ooxml_automation_api_client)
        self.data_points = presalytics_ooxml_automation.DataPointsApi(api_client=ooxml_automation_api_client)
        self.document_types = presalytics_ooxml_automation.DocumentTypeApi(api_client=ooxml_automation_api_client)
        self.documents = presalytics_ooxml_automation.DocumentsApi(api_client=ooxml_automation_api_client)
        self.effect_attributes = presalytics_ooxml_automation.EffectAttributesApi(api_client=ooxml_automation_api_client)
        self.effect_maps = presalytics_ooxml_automation.EffectMapApi(api_client=ooxml_automation_api_client)
        self.effect_types = presalytics_ooxml_automation.EffectTypesApi(api_client=ooxml_automation_api_client)
        self.effects = presalytics_ooxml_automation.EffectsApi(api_client=ooxml_automation_api_client)
        self.fill_maps = presalytics_ooxml_automation.FillMapApi(api_client=ooxml_automation_api_client)
        self.fill_types = presalytics_ooxml_automation.FillTypesApi(api_client=ooxml_automation_api_client)
        self.fills = presalytics_ooxml_automation.FillsApi(api_client=ooxml_automation_api_client)
        self.fonts = presalytics_ooxml_automation.FontsApi(api_client=ooxml_automation_api_client)
        self.gradient_fills = presalytics_ooxml_automation.GradientFillsApi(api_client=ooxml_automation_api_client)
        self.gradient_stops = presalytics_ooxml_automation.GradientStopsApi(api_client=ooxml_automation_api_client)
        self.graphic_types = presalytics_ooxml_automation.GraphicTypesApi(api_client=ooxml_automation_api_client)
        self.graphics = presalytics_ooxml_automation.GraphicsApi(api_client=ooxml_automation_api_client)
        self.group_element_types = presalytics_ooxml_automation.GroupElementTypesApi(api_client=ooxml_automation_api_client)
        self.group_elements = presalytics_ooxml_automation.GroupElementsApi(api_client=ooxml_automation_api_client)
        self.groups = presalytics_ooxml_automation.GroupsApi(api_client=ooxml_automation_api_client)
        self.image_fills = presalytics_ooxml_automation.ImageFillsApi(api_client=ooxml_automation_api_client)
        self.intensities = presalytics_ooxml_automation.IntensityApi(api_client=ooxml_automation_api_client)
        self.line_end_sizes = presalytics_ooxml_automation.LineEndSizesApi(api_client=ooxml_automation_api_client)
        self.line_end_types = presalytics_ooxml_automation.LineEndTypesApi(api_client=ooxml_automation_api_client)
        self.line_maps = presalytics_ooxml_automation.LineMapApi(api_client=ooxml_automation_api_client)
        self.lines = presalytics_ooxml_automation.LinesApi(api_client=ooxml_automation_api_client)
        self.paragraphs = presalytics_ooxml_automation.ParagraphApi(api_client=ooxml_automation_api_client)
        self.pictures = presalytics_ooxml_automation.PicturesApi(api_client=ooxml_automation_api_client)
        self.plot_types = presalytics_ooxml_automation.PlotTypeApi(api_client=ooxml_automation_api_client)
        self.row_cols = presalytics_ooxml_automation.RowColApi(api_client=ooxml_automation_api_client)
        self.row_collections = presalytics_ooxml_automation.RowCollectionsApi(api_client=ooxml_automation_api_client)
        self.row_name_format_types = presalytics_ooxml_automation.RowNameFormatTypesApi(api_client=ooxml_automation_api_client)
        self.rows = presalytics_ooxml_automation.RowsApi(api_client=ooxml_automation_api_client)
        self.shape_trees = presalytics_ooxml_automation.ShapeTreesApi(api_client=ooxml_automation_api_client)
        self.slide_masters = presalytics_ooxml_automation.SlideMastersApi(api_client=ooxml_automation_api_client)
        self.slides = presalytics_ooxml_automation.SlidesApi(api_client=ooxml_automation_api_client)
        self.solid_fills = presalytics_ooxml_automation.SolidFillsApi(api_client=ooxml_automation_api_client)
        self.tables = presalytics_ooxml_automation.TablesApi(api_client=ooxml_automation_api_client)
        self.texts = presalytics_ooxml_automation.TextApi(api_client=ooxml_automation_api_client)
        self.text_containers = presalytics_ooxml_automation.TextContainerApi(api_client=ooxml_automation_api_client)
        self.themes = presalytics_ooxml_automation.ThemesApi(api_client=ooxml_automation_api_client)




class Client(object):
    def __init__(self, config_file=None, **kwargs):
        doc_converter_api_client = DocConverterApiClientWithAuth(config_file, **kwargs)
        self.doc_converter = presalytics_doc_converter.DefaultApi(api_client=doc_converter_api_client)
        self.ooxml_automation = OoxmlAutomationContainer(config_file=config_file)

