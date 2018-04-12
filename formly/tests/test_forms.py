from ..forms.widgets import MultiTextWidget
from .mixins import SimpleTests


class WidgetTests(SimpleTests):

    def test_multi_textwidget_decompress(self):
        widget = MultiTextWidget(widgets_length=2)
        decompressed = widget.decompress("value")
