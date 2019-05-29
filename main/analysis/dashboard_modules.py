import datetime
import calendar
from math import ceil
from dateutil.parser import parse
from django.utils.translation import ugettext_lazy as _
from django import forms

from jet.dashboard.modules import DashboardModule
from main.models import ObjectsItem, Votings, Collections, Chats, Users
from .widgets import DateRangeWidget


class DateForm(forms.Form):
    date_range = forms.CharField(widget=DateRangeWidget)


class BaseChart(DashboardModule):
    template = 'analysis.html'
    style = 'overflow-x: auto; overflow-y: auto;'
    ajax_load = True
    contrast = True
    deletable = False
    settings_form = DateForm
    date_range = None
    period = None
    _model = None
    date_format = None
    timedelta = None
    data = []

    class Media:
        js = ('jet.dashboard/vendor/chart.js/Chart.min.js',
              'jet.dashboard/dashboard_modules/google_analytics.js')

    def __init__(self, title=None, **kwargs):
        date_range = self._initial_date_range()
        kwargs.update({'date_range': date_range})
        super().__init__(title, **kwargs)

    def settings_dict(self):
        return {'date_range': self.date_range}

    def load_settings(self, settings):
        self.date_range = settings.get('date_range')

    def init_with_context(self, context):
        start, end = self._get_range()
        delta = (end - start).days + 1
        period, iterator = self._get_period(delta)

        self.data = self._get_chart_data(start, end, period, iterator)

    def _initial_date_range(self):
        today = datetime.datetime.today()

        start = (today - datetime.timedelta(days=7)).strftime('%B %d, %Y')
        end = today.strftime('%B %d, %Y')

        return start + ' - ' + end

    def _get_range(self):
        str_start, str_end = self.date_range.split(' - ')
        start = parse(str_start)
        end = parse(str_end) + datetime.timedelta(hours=23, minutes=59, seconds=59)

        return start, end

    def _get_period(self, delta):
        if delta == 1:
            self.date_format = "g a"
            self.timedelta = datetime.timedelta(hours=1)
            return "%b %d %Y %H", 24
        elif delta <= 31:
            self.date_format = "j/n"
            self.timedelta = datetime.timedelta(days=1)
            return "%b %d %Y", delta
        else:
            self.date_format = "M/Y"
            self.timedelta = datetime.timedelta(days=30)
            return "%b %Y", ceil(delta / 30)

    def _get_chart_data(self, start, end, period, iterator):
        date = start
        chart_obj = {}

        queryset = self._model.objects.filter(created_at__range=[start, end])

        for _ in range(iterator):
            chart_obj[date.strftime(period)] = [date, 0]
            date += self.timedelta

        for item in queryset:
            key = item.created_at.strftime(period)
            if key in chart_obj.keys():
                chart_obj[key][1] += 1

        chart_list = list(chart_obj.values())

        if iterator > 10:
            return self._dilution(chart_list, iterator)
        else:
            return chart_list

    def _dilution(self, chart_list, iterator):
        data = []
        last = 1
        value = 0

        if iterator < 20:
            delta = 2
        else:
            delta = 3

        data.append([chart_list[0]])

        while last < len(chart_list):
            data.append(chart_list[int(last):int(last + delta)])
            last += delta

        for index, _list in enumerate(data):
            item = [0, 0]
            for i in _list:
                item[0] = i[0]
                item[1] += i[1]

            item[1] += value
            value = item[1]

            data[index] = item

        return data


class ChatsChart(BaseChart):
    title = _('Chats char')
    _model = Chats


class UsersChart(BaseChart):
    title = _('Users char')
    _model = Users


class VotingsChart(BaseChart):
    title = _('Votings char')
    _model = Votings


class CollectionsChart(BaseChart):
    title = _('Collections char')
    _model = Collections
