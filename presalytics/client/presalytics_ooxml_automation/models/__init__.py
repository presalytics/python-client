# coding: utf-8

# flake8: noqa
"""
    OOXML Automation

    This API helps users convert Excel and Powerpoint documents into rich, live dashboards and stories.  # noqa: E501

    The version of the OpenAPI document: 0.1.0-no-tags
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

# import models into model package
from presalytics.client.presalytics_ooxml_automation.models.chart_axes import ChartAxes
from presalytics.client.presalytics_ooxml_automation.models.chart_axes_details import ChartAxesDetails
from presalytics.client.presalytics_ooxml_automation.models.chart_axis_data_types import ChartAxisDataTypes
from presalytics.client.presalytics_ooxml_automation.models.chart_chart_data import ChartChartData
from presalytics.client.presalytics_ooxml_automation.models.chart_chart_data_dto import ChartChartDataDTO
from presalytics.client.presalytics_ooxml_automation.models.chart_chart_data_details import ChartChartDataDetails
from presalytics.client.presalytics_ooxml_automation.models.chart_charts import ChartCharts
from presalytics.client.presalytics_ooxml_automation.models.chart_charts_details import ChartChartsDetails
from presalytics.client.presalytics_ooxml_automation.models.chart_column_collections import ChartColumnCollections
from presalytics.client.presalytics_ooxml_automation.models.chart_column_collections_details import ChartColumnCollectionsDetails
from presalytics.client.presalytics_ooxml_automation.models.chart_columns import ChartColumns
from presalytics.client.presalytics_ooxml_automation.models.chart_columns_details import ChartColumnsDetails
from presalytics.client.presalytics_ooxml_automation.models.chart_data_points import ChartDataPoints
from presalytics.client.presalytics_ooxml_automation.models.chart_data_points_details import ChartDataPointsDetails
from presalytics.client.presalytics_ooxml_automation.models.chart_plot_type import ChartPlotType
from presalytics.client.presalytics_ooxml_automation.models.chart_row_col import ChartRowCol
from presalytics.client.presalytics_ooxml_automation.models.chart_row_collections import ChartRowCollections
from presalytics.client.presalytics_ooxml_automation.models.chart_row_collections_details import ChartRowCollectionsDetails
from presalytics.client.presalytics_ooxml_automation.models.chart_row_name_format_types import ChartRowNameFormatTypes
from presalytics.client.presalytics_ooxml_automation.models.chart_rows import ChartRows
from presalytics.client.presalytics_ooxml_automation.models.chart_rows_details import ChartRowsDetails
from presalytics.client.presalytics_ooxml_automation.models.child_objects import ChildObjects
from presalytics.client.presalytics_ooxml_automation.models.document import Document
from presalytics.client.presalytics_ooxml_automation.models.document_details import DocumentDetails
from presalytics.client.presalytics_ooxml_automation.models.document_type import DocumentType
from presalytics.client.presalytics_ooxml_automation.models.ooxml_dto import OoxmlDTO
from presalytics.client.presalytics_ooxml_automation.models.problem_details import ProblemDetails
from presalytics.client.presalytics_ooxml_automation.models.shared_color_transformation_attributes import SharedColorTransformationAttributes
from presalytics.client.presalytics_ooxml_automation.models.shared_color_transformation_attributes_details import SharedColorTransformationAttributesDetails
from presalytics.client.presalytics_ooxml_automation.models.shared_color_transformations import SharedColorTransformations
from presalytics.client.presalytics_ooxml_automation.models.shared_color_transformations_details import SharedColorTransformationsDetails
from presalytics.client.presalytics_ooxml_automation.models.shared_color_types import SharedColorTypes
from presalytics.client.presalytics_ooxml_automation.models.shared_dash_types import SharedDashTypes
from presalytics.client.presalytics_ooxml_automation.models.shared_effect_attributes import SharedEffectAttributes
from presalytics.client.presalytics_ooxml_automation.models.shared_effect_attributes_details import SharedEffectAttributesDetails
from presalytics.client.presalytics_ooxml_automation.models.shared_effect_types import SharedEffectTypes
from presalytics.client.presalytics_ooxml_automation.models.shared_effects import SharedEffects
from presalytics.client.presalytics_ooxml_automation.models.shared_effects_details import SharedEffectsDetails
from presalytics.client.presalytics_ooxml_automation.models.shared_fill_map import SharedFillMap
from presalytics.client.presalytics_ooxml_automation.models.shared_fill_map_details import SharedFillMapDetails
from presalytics.client.presalytics_ooxml_automation.models.shared_fill_types import SharedFillTypes
from presalytics.client.presalytics_ooxml_automation.models.shared_gradient_fills import SharedGradientFills
from presalytics.client.presalytics_ooxml_automation.models.shared_gradient_fills_details import SharedGradientFillsDetails
from presalytics.client.presalytics_ooxml_automation.models.shared_gradient_stops import SharedGradientStops
from presalytics.client.presalytics_ooxml_automation.models.shared_gradient_stops_details import SharedGradientStopsDetails
from presalytics.client.presalytics_ooxml_automation.models.shared_image_fills import SharedImageFills
from presalytics.client.presalytics_ooxml_automation.models.shared_image_fills_details import SharedImageFillsDetails
from presalytics.client.presalytics_ooxml_automation.models.shared_line_end_sizes import SharedLineEndSizes
from presalytics.client.presalytics_ooxml_automation.models.shared_line_end_types import SharedLineEndTypes
from presalytics.client.presalytics_ooxml_automation.models.shared_lines import SharedLines
from presalytics.client.presalytics_ooxml_automation.models.shared_lines_details import SharedLinesDetails
from presalytics.client.presalytics_ooxml_automation.models.shared_paragraph import SharedParagraph
from presalytics.client.presalytics_ooxml_automation.models.shared_paragraph_details import SharedParagraphDetails
from presalytics.client.presalytics_ooxml_automation.models.shared_pictures import SharedPictures
from presalytics.client.presalytics_ooxml_automation.models.shared_pictures_details import SharedPicturesDetails
from presalytics.client.presalytics_ooxml_automation.models.shared_solid_fills import SharedSolidFills
from presalytics.client.presalytics_ooxml_automation.models.shared_solid_fills_details import SharedSolidFillsDetails
from presalytics.client.presalytics_ooxml_automation.models.shared_text import SharedText
from presalytics.client.presalytics_ooxml_automation.models.shared_text_container import SharedTextContainer
from presalytics.client.presalytics_ooxml_automation.models.shared_text_container_details import SharedTextContainerDetails
from presalytics.client.presalytics_ooxml_automation.models.shared_text_details import SharedTextDetails
from presalytics.client.presalytics_ooxml_automation.models.slide_color_maps import SlideColorMaps
from presalytics.client.presalytics_ooxml_automation.models.slide_color_maps_details import SlideColorMapsDetails
from presalytics.client.presalytics_ooxml_automation.models.slide_connector import SlideConnector
from presalytics.client.presalytics_ooxml_automation.models.slide_connector_details import SlideConnectorDetails
from presalytics.client.presalytics_ooxml_automation.models.slide_graphic_types import SlideGraphicTypes
from presalytics.client.presalytics_ooxml_automation.models.slide_graphics import SlideGraphics
from presalytics.client.presalytics_ooxml_automation.models.slide_graphics_details import SlideGraphicsDetails
from presalytics.client.presalytics_ooxml_automation.models.slide_group_element_types import SlideGroupElementTypes
from presalytics.client.presalytics_ooxml_automation.models.slide_group_element_types_details import SlideGroupElementTypesDetails
from presalytics.client.presalytics_ooxml_automation.models.slide_group_elements import SlideGroupElements
from presalytics.client.presalytics_ooxml_automation.models.slide_group_elements_details import SlideGroupElementsDetails
from presalytics.client.presalytics_ooxml_automation.models.slide_groups import SlideGroups
from presalytics.client.presalytics_ooxml_automation.models.slide_groups_details import SlideGroupsDetails
from presalytics.client.presalytics_ooxml_automation.models.slide_shape_trees import SlideShapeTrees
from presalytics.client.presalytics_ooxml_automation.models.slide_shape_trees_details import SlideShapeTreesDetails
from presalytics.client.presalytics_ooxml_automation.models.slide_shapes import SlideShapes
from presalytics.client.presalytics_ooxml_automation.models.slide_shapes_details import SlideShapesDetails
from presalytics.client.presalytics_ooxml_automation.models.slide_slide_masters import SlideSlideMasters
from presalytics.client.presalytics_ooxml_automation.models.slide_slide_masters_details import SlideSlideMastersDetails
from presalytics.client.presalytics_ooxml_automation.models.slide_slides import SlideSlides
from presalytics.client.presalytics_ooxml_automation.models.slide_slides_details import SlideSlidesDetails
from presalytics.client.presalytics_ooxml_automation.models.slide_smart_arts import SlideSmartArts
from presalytics.client.presalytics_ooxml_automation.models.slide_smart_arts_details import SlideSmartArtsDetails
from presalytics.client.presalytics_ooxml_automation.models.story_file_form_data import StoryFileFormData
from presalytics.client.presalytics_ooxml_automation.models.table_borders import TableBorders
from presalytics.client.presalytics_ooxml_automation.models.table_borders_details import TableBordersDetails
from presalytics.client.presalytics_ooxml_automation.models.table_cells import TableCells
from presalytics.client.presalytics_ooxml_automation.models.table_cells_details import TableCellsDetails
from presalytics.client.presalytics_ooxml_automation.models.table_columns import TableColumns
from presalytics.client.presalytics_ooxml_automation.models.table_columns_details import TableColumnsDetails
from presalytics.client.presalytics_ooxml_automation.models.table_rows import TableRows
from presalytics.client.presalytics_ooxml_automation.models.table_rows_details import TableRowsDetails
from presalytics.client.presalytics_ooxml_automation.models.table_table_data_dto import TableTableDataDTO
from presalytics.client.presalytics_ooxml_automation.models.table_tables import TableTables
from presalytics.client.presalytics_ooxml_automation.models.table_tables_details import TableTablesDetails
from presalytics.client.presalytics_ooxml_automation.models.theme_background_fills import ThemeBackgroundFills
from presalytics.client.presalytics_ooxml_automation.models.theme_background_fills_details import ThemeBackgroundFillsDetails
from presalytics.client.presalytics_ooxml_automation.models.theme_colors import ThemeColors
from presalytics.client.presalytics_ooxml_automation.models.theme_colors_details import ThemeColorsDetails
from presalytics.client.presalytics_ooxml_automation.models.theme_custom_colors import ThemeCustomColors
from presalytics.client.presalytics_ooxml_automation.models.theme_custom_colors_details import ThemeCustomColorsDetails
from presalytics.client.presalytics_ooxml_automation.models.theme_effect_map import ThemeEffectMap
from presalytics.client.presalytics_ooxml_automation.models.theme_effect_map_details import ThemeEffectMapDetails
from presalytics.client.presalytics_ooxml_automation.models.theme_fills import ThemeFills
from presalytics.client.presalytics_ooxml_automation.models.theme_fills_details import ThemeFillsDetails
from presalytics.client.presalytics_ooxml_automation.models.theme_fonts import ThemeFonts
from presalytics.client.presalytics_ooxml_automation.models.theme_fonts_details import ThemeFontsDetails
from presalytics.client.presalytics_ooxml_automation.models.theme_intensity import ThemeIntensity
from presalytics.client.presalytics_ooxml_automation.models.theme_line_map import ThemeLineMap
from presalytics.client.presalytics_ooxml_automation.models.theme_line_map_details import ThemeLineMapDetails
from presalytics.client.presalytics_ooxml_automation.models.theme_themes import ThemeThemes
from presalytics.client.presalytics_ooxml_automation.models.theme_themes_details import ThemeThemesDetails
