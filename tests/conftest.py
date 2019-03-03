import pytest


def pytest_configure():
    from django.conf import settings

    settings.configure()
    try:
        import django

        django.setup()
    except AttributeError:
        pass


@pytest.fixture
def base_model(mocker):
    return mocker.Mock(
        _meta=mocker.Mock(
            model="self_model",
            proxy_for_model=None,
            app_label="testapp",
            model_name="testmodel",
        )
    )


@pytest.fixture
def model(mocker, base_model):
    return mocker.Mock(
        _meta=mocker.Mock(model=base_model, proxy_for_model=None)
    )
