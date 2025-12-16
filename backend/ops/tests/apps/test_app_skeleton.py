# backend/ops/tests/apps/test_app_skeleton.py
import importlib



def test_ops_module_is_importable():
    # Arrange
    module_name = "ops.apps"



    # Act
    
    # startapp していないと、ここで ModuleNotFoundError になる
    apps_module = importlib.import_module(module_name)

    config = getattr(apps_module, "OpsConfig")



    # Assert
    assert config.name == "ops"
