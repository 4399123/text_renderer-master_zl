from dataclasses import dataclass

from PIL.ImageFont import FreeTypeFont


@dataclass
class FontText:
    font: FreeTypeFont
    text: str
    font_path: str
    horizontal: bool = True

    def _getbbox(self, text: str):
        """Return (left, top, right, bottom) bounding box for text."""
        return self.font.getbbox(text)

    @property
    def xy(self):
        left, top, right, bottom = self._getbbox(self.text)
        return -left, -top

    @property
    def offset(self):
        left, top, right, bottom = self._getbbox(self.text)
        return left, top

    @property
    def size(self) -> [int, int]:
        """
        Get text size without offset

        Returns:
            width, height
        """
        if self.horizontal:
            left, top, right, bottom = self._getbbox(self.text)
            return right - left, bottom - top
        else:
            bboxes = [self._getbbox(c) for c in self.text]
            width = max(b[2] - b[0] for b in bboxes)
            height = sum(b[3] - b[1] for b in bboxes)
            return height, width
