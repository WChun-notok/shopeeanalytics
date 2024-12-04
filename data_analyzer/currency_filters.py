from django import template

register = template.Library()

@register.filter
def currency_vnd(value):
    """
    Custom filter: Định dạng giá trị thành tiền tệ VND.
    """
    if value is None:
        return "0 VND"
    return f"{value:,.0f} VND"  # :,.0f là định dạng số không có chữ số thập phân.
