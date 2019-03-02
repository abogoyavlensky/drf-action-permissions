"""
    drf_action_permissions/permissions.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tools for managing action permissions in Django REST framework.

    :copyright: (c) 2019 by Andrey Bogoyavlensky.
"""
from rest_framework.permissions import DjangoModelPermissions


class DjangoActionPermissions(DjangoModelPermissions):
    """Customize permission logic based on request, action and object.

    For every viewset with `queryset` you want to override some custom logic
    for particular action, you should define such attribute for `viewset`.
    Viewset permission at common action level:
    ```
        perms_map_action = {
            '<action>': [
                <str> | <function(user, view, obj=None)>,
                ...
            ],
            ...
        }
    ```

    Viewset permission at object action level:
    ```
        perms_map_action_obj = {
            '<action>': [
                <str> | <function(user, view, obj=None)>,
                ...
            ],
            ...
        }
    ```
    """

    perms_map = {
        "GET": [],
        "OPTIONS": [],
        "HEAD": [],
        "POST": [],
        "PUT": [],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }
    perms_map_action = {
        "retrieve": ["%(app_label)s.view_%(model_name)s"],
        "list": ["%(app_label)s.view_%(model_name)s_list"],
        "create": ["%(app_label)s.change_%(model_name)s"],
        "update": ["%(app_label)s.change_%(model_name)s"],
    }

    # pylint: disable=protected-access
    def get_origin_model(self, model_cls):
        """Return origin model even if proxy has been received."""
        return model_cls._meta.proxy_for_model or model_cls._meta.model

    def get_required_permissions(self, method, model_cls):
        """Add ability to define origin model even via proxy."""
        model_cls = self.get_origin_model(model_cls)
        return super().get_required_permissions(method, model_cls)

    def get_perms_list(self, view, obj=None):
        """Return permission list for action from backend and view."""
        perms_map_name = "perms_map_action_obj" if obj else "perms_map_action"
        view_perms_map = getattr(view, perms_map_name, {})
        view_perms_list = view_perms_map.get(view.action)
        if view_perms_list is not None:
            return view_perms_list
        backend_perms_map = getattr(self, perms_map_name, {})
        return backend_perms_map.get(view.action) or []

    # pylint: disable=protected-access
    def get_required_action_permissions(self, view, model_cls, obj=None):
        """Given a model and an action, return the list of permission codes."""
        model_cls = self.get_origin_model(model_cls)
        kwargs = {
            "app_label": model_cls._meta.app_label,
            "model_name": model_cls._meta.model_name,
        }
        return [
            perm % kwargs if isinstance(perm, str) else perm
            for perm in self.get_perms_list(view, obj)
        ]

    def user_has_action_perm(self, user, view, perm, obj=None):
        """Check if user has single permission for particular view action."""
        assert callable(perm) or isinstance(
            perm, str
        ), "Permission must be function or string"

        if callable(perm):
            return perm(user, view, obj)

        return user.has_perm(perm)

    def has_action_permission(self, request, view, obj=None):
        """Check action specific permissions ignoring custom method."""
        queryset = self._queryset(view)
        perms = self.get_required_action_permissions(view, queryset.model, obj)
        return all(
            self.user_has_action_perm(request.user, view, perm, obj)
            for perm in perms
        )

    def has_permission(self, request, view):
        """Apply action permission without object and with ignoring method."""
        result = super().has_permission(request, view)
        return result and self.has_action_permission(request, view)

    def has_object_permission(self, request, view, obj):
        """Apply action permission without object and with ignoring method."""
        return self.has_action_permission(request, view, obj)
