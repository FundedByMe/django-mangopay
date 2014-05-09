from django.conf import settings

from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.tools.storages.memorystoragestrategy import (
    MemoryStorageStrategy)


def get_mangopay_api_client():
    api = MangoPayApi()
    api.OAuthTokenManager.RegisterCustomStorageStrategy(
        MemoryStorageStrategy())
    api.Config.ClientID = settings.MANGOPAY_CLIENT_ID
    api.Config.ClientPassword = settings.MANGOPAY_PASSPHRASE
    api.Config.DebugMode = settings.MANGOPAY_DEBUG_MODE
    api.Config.BaseUrl = settings.MANGOPAY_BASE_URL
    return api
