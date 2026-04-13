from django.urls import path

from application_blocker.api.application_block import (
    add_block_application,
    disable_block,
    enforce_block,
    list_blocked_application,
    list_installed_applications,
    remove_block_application,
)

urlpatterns = [
    path("list/", list_blocked_application),
    path("add/", add_block_application),
    path("remove/", remove_block_application),
    path("enforce/", enforce_block),
    path("disable/", disable_block),
    path("installed/", list_installed_applications),
]
