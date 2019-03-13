import datetime

from azure.mgmt.monitor import MonitorManagementClient
from ScoutSuite.providers.utils import run_concurrently


class MonitorFacade:
    def __init__(self, credentials, subscription_id):
        self._client = MonitorManagementClient(credentials, subscription_id)

    async def get_activity_logs(self):

        list_filter = " and ".join([
            "eventTimestamp le {}".format(datetime.datetime.now()),  # before today
            "eventTimestamp ge {}".format(datetime.datetime.now() - datetime.timedelta(days=90)),  # after 90 days ago
            # The below filter makes the query *significantly* faster
            # Additional resources can be fetched according to need
            "resourceProvider eq {}".format('Microsoft.Storage/storageAccounts')
        ])

        return await run_concurrently(
            lambda: self._client.activity_logs.list(
                filter=list_filter,
            )

        )
