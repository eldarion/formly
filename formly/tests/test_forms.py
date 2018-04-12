from ..forms.widgets import MultiTextWidget
from .mixins import SimpleTests


class WidgetTests(SimpleTests):

    def test_multi_textwidget_decompress(self):
        widget = MultiTextWidget(widgets_length=2)

        # verify that None is decompressed to an empty list
        value = None
        decompressed = widget.decompress(value)
        self.assertEqual(decompressed, [])

        # verify that other values are passed through as-is
        value = [1, 2]
        decompressed = widget.decompress(value)
        self.assertEqual(decompressed, value)
