from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard
from .dashboard_modules import ChatsChart, UsersChart, VotingsChart, \
    CollectionsChart


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        # Charts modules
        self.children.append(UsersChart(
            _('Users chart'),
            column=0
        ))
        self.children.append(ChatsChart(
            _('Chats chart'),
            column=1
        ))
        self.children.append(VotingsChart(
            _('Votings chart'),
            column=0
        ))
        self.children.append(CollectionsChart(
            _('Collections chart'),
            column=1
        ))

        # # append an app list module for "Administration"
        # self.children.append(modules.AppList(
        #     _('Administration'),
        #     models=('auth.*',),
        #     column=2,
        # ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('auth.*',),
            column=2,
            order=0
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            10,
            column=2,
            order=1
        ))
