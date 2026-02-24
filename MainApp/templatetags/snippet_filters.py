from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='nl2br')
def nl2br(value):
    """
    Заменяет символы переноса строки \n на HTML-теги <br>
    Отключает автоэкранирование для безопасного вывода
    """
    if value:
        # Заменяем \n на <br> и помечаем как безопасный HTML
        return mark_safe(value.replace('\n', '<br>'))
    return value


@register.filter(name='format_code')
def format_code(value):
    """
    Форматирует код для вывода в HTML:
    - Экранирует HTML-символы (безопасность)
    - Заменяет \n на <br>
    - Заменяет пробелы на &nbsp; для сохранения форматирования
    """
    if value:
        from django.utils.html import escape
        # Сначала экранируем HTML-символы (защита от XSS)
        escaped = escape(value)
        # Заменяем переносы строк и пробелы
        formatted = escaped.replace('\n', '<br>').replace(' ', '&nbsp;')
        return mark_safe(formatted)
    return value