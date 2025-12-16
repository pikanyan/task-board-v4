# backend/ops/tests/apps/test_app_registration.py
from django.conf import settings



def test_ops_in_installed_apps():
    # Arrange
    app_label = "ops"



    # Act
    installed_apps = settings.INSTALLED_APPS



    # Assert
    assert app_label in installed_apps
