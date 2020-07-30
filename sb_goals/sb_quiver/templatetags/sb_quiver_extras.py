from django import template

register = template.Library()


def output_cm_as_feet_inches(cms:float) -> str:
    inches = cms * 0.393701
    feet_and_inches = str(inches / 12)
    return feet_and_inches[0] + "\'' " + feet_and_inches[2] + "\""

def output_ml_as_litres(ml:float) -> str:
    return ml / 1000

@register.filter(name='convert_length')
def convert_length(board) -> str:
    """Sends the length to the converstion function """
    return output_cm_as_feet_inches(board.length)

@register.filter(name='convert_width')
def convert_width(board) -> str:
    """Sends the width to the conversion function."""
    return output_cm_as_feet_inches(board.width)

@register.filter(name='convert_thickness')
def convert_thickness(board) -> str:
    """Sends the thickness to the conversion function."""
    return output_cm_as_feet_inches(board.thickness)

@register.filter(name='convert_volume')
def convert_thickness(board) -> str:
    """Sends the volume to the conversion function."""
    return str(output_ml_as_litres(board.volume)) + 'litres'

@register.filter(name='convert_wave_range_start')
def convert_wave_range_start(board) -> str:
    """Sends the wave_range_start to the conversion function."""
    return output_cm_as_feet_inches(board.wave_range_start)

@register.filter(name='convert_wave_range_end')
def convert_wave_range_end(board) -> str:
    """Sends the wave_range_start to the conversion function."""
    return str(output_cm_as_feet_inches(board.wave_range_end))
