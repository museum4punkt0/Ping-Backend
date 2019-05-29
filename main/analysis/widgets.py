from django.forms import TextInput


class DateRangeWidget(TextInput):
    template_name = 'date_widget.html'
