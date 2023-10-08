from widgets import *

_PINK_ON = '#FF89B2'
_PINK_OFF = '#99556F'

_BLUE_ON = '#00FFE0'
_BLUE_OFF = '#009983'

_YELLOW_ON = '#FFC655'
_YELLOW_OFF = '#997733'

_PURPLE_ON = '#BD86FF'
_PURPLE_OFF = '#6F5299'

_GREEN_ON = '#00FF93'
_GREEN_OFF = '#009953'

_BACKGROUND = '#212121'
_DARKER_ACCENT = '#131313'
_LIGHTER_ACCENT = '#383838'
_LIGHTEST_ACCENT = '#A5A5A5'
_TEXT = '#FFFFFF'

_FONT = ('TkFixedFont', 10)
_HEADING_FONT = ('TkFixedFont', 12, 'bold')
_TINY_FONT = ('TkFixedFont', 8, 'bold')

_BINARY_BUTTON_WIDTH = 15

_FONT_STYLES = WidgetFonts(heading=_HEADING_FONT label=_FONT, entry=_FONT, tiny=_TINY_FONT)
_BORDER_WIDTHS = BorderWidths(left=1, right=1, top=1, bottom=1)


_PINK_STYLE = WidgetStyle(
    enabled=WidgetStateColors(background=_DARKER_ACCENT, text=_TEXT, accent=_PINK_ON),
    disabled=WidgetStateColors(background=_DARKER_ACCENT, text=_LIGHTER_ACCENT, accent=_PINK_OFF),
    readonly=WidgetStateColors(background=_DARKER_ACCENT, text=_LIGHTER_ACCENT, accent=_PINK_OFF),
    borderwidths=_BORDER_WIDTHS,
    fonts=_FONT_STYLES,
    background=_BACKGROUND
)

_BLUE_STYLE = WidgetStyle(
    enabled=WidgetStateColors(background=_DARKER_ACCENT, text=_TEXT, accent=_BLUE_ON),
    disabled=WidgetStateColors(background=_DARKER_ACCENT, text=_LIGHTER_ACCENT, accent=_BLUE_OFF),
    readonly=WidgetStateColors(background=_DARKER_ACCENT, text=_LIGHTER_ACCENT, accent=_BLUE_OFF),
    borderwidths=_BORDER_WIDTHS,
    fonts=_FONT_STYLES,
    background=_BACKGROUND
)

_YELLOW_STYLE = WidgetStyle(
    enabled=WidgetStateColors(background=_DARKER_ACCENT, text=_TEXT, accent=_YELLOW_ON),
    disabled=WidgetStateColors(background=_DARKER_ACCENT, text=_LIGHTER_ACCENT, accent=_YELLOW_OFF),
    readonly=WidgetStateColors(background=_DARKER_ACCENT, text=_LIGHTER_ACCENT, accent=_YELLOW_OFF),
    borderwidths=_BORDER_WIDTHS,
    fonts=_FONT_STYLES,
    background=_BACKGROUND
)

_PURPLE_STYLE = WidgetStyle(
    enabled=WidgetStateColors(background=_DARKER_ACCENT, text=_TEXT, accent=_PURPLE_ON),
    disabled=WidgetStateColors(background=_DARKER_ACCENT, text=_LIGHTER_ACCENT, accent=_PURPLE_OFF),
    readonly=WidgetStateColors(background=_DARKER_ACCENT, text=_LIGHTER_ACCENT, accent=_PURPLE_OFF),
    borderwidths=_BORDER_WIDTHS,
    fonts=_FONT_STYLES,
    background=_BACKGROUND
)


_GREEN_STYLE = WidgetStyle(
    enabled=WidgetStateColors(background=_DARKER_ACCENT, text=_TEXT, accent=_GREEN_ON),
    disabled=WidgetStateColors(background=_DARKER_ACCENT, text=_LIGHTER_ACCENT, accent=_GREEN_OFF),
    readonly=WidgetStateColors(background=_DARKER_ACCENT, text=_LIGHTER_ACCENT, accent=_GREEN_OFF),
    borderwidths=_BORDER_WIDTHS,
    fonts=_FONT_STYLES,
    background=_BACKGROUND
)



_OCTET_COLORS = (('First', _PINK_STYLE), ('Second', _BLUE_STYLE), ('Third', _YELLOW_STYLE), ('Fourth', _PURPLE_STYLE))