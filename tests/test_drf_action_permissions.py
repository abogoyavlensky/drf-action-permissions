import pytest

from drf_action_permissions.permissions import DjangoActionPermissions


def test_get_origin_model_returns_proxy_ok(mocker):
    permissions = DjangoActionPermissions()
    model = mocker.Mock(_meta=mocker.Mock(proxy_for_model="proxy_model"))
    result_model = permissions.get_origin_model(model)
    assert result_model == "proxy_model"


def test_get_origin_model_returns_self_model_ok(mocker):
    permissions = DjangoActionPermissions()
    model = mocker.Mock(
        _meta=mocker.Mock(model="self_model", proxy_for_model=None)
    )
    result_model = permissions.get_origin_model(model)
    assert result_model == "self_model"


def test_get_required_permissions_ok(mocker, model):
    permissions = DjangoActionPermissions()
    result = permissions.get_required_permissions("POST", model)
    assert result == ["testapp.add_testmodel"]


def test_get_perms_list_retruns_perms_map_from_permissions_class(mocker):
    permissions = DjangoActionPermissions()
    view = mocker.Mock(perms_map_action={}, action="list")
    result = permissions.get_perms_list(view)
    assert result == ["%(app_label)s.view_%(model_name)s_list"]


def test_get_perms_list_retruns_perms_map_from_view(mocker):
    permissions = DjangoActionPermissions()
    view = mocker.Mock(perms_map_action={"list": ["test"]}, action="list")
    result = permissions.get_perms_list(view)
    assert result == ["test"]


def test_get_required_action_permissions(mocker, model):
    permissions = DjangoActionPermissions()
    view = mocker.Mock(perms_map_action={}, action="list")
    result = permissions.get_required_action_permissions(view, model)
    assert result == ["testapp.view_testmodel_list"]


def test_user_has_action_perm_raise_perm_type_assert():
    permissions = DjangoActionPermissions()
    with pytest.raises(AssertionError) as e:
        permissions.user_has_action_perm(None, None, None)
    assert "Permission must be function or string" in str(e.value)


def test_user_has_action_perm_call_perm(mocker):
    permissions = DjangoActionPermissions()
    perm = mocker.Mock(return_value=True)
    assert permissions.user_has_action_perm(None, None, perm) is True


def test_user_has_action_perm_check_user_has_perm(mocker):
    permissions = DjangoActionPermissions()
    perm = mocker.Mock(return_value=True)
    user = mocker.Mock(has_perm=lambda x: x)
    assert permissions.user_has_action_perm(user, None, perm) is True


def test_has_action_permission(mocker, model):
    permissions = DjangoActionPermissions()
    permissions._queryset = mocker.Mock(model=model)
    request = mocker.Mock(user=mocker.Mock(has_perm=mocker.Mock(True)))
    view = mocker.Mock(perms_map_action={}, action="list")
    assert permissions.has_action_permission(request, view) is True


def test_has_permission(mocker, model):
    permissions = DjangoActionPermissions()
    permissions._queryset = mocker.Mock(model=model)
    request = mocker.Mock(user=mocker.Mock(has_perm=mocker.Mock(True)))
    view = mocker.Mock(perms_map_action={}, action="list")
    assert permissions.has_permission(request, view) is True


def test_has_object_permission(mocker, model):
    permissions = DjangoActionPermissions()
    permissions._queryset = mocker.Mock(model=model)
    request = mocker.Mock(user=mocker.Mock(has_perm=mocker.Mock(True)))
    view = mocker.Mock(
        action="list", perms_map_action={}, perms_map_action_obj={}
    )
    obj = mocker.Mock()
    assert permissions.has_object_permission(request, view, obj) is True
