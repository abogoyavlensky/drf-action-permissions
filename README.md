drf-action-permissions
===

| Release | CI | Coverage |
|---------|----|----------|
|[![pypi](https://img.shields.io/pypi/v/drf-action-permissions.svg)](https://pypi.python.org/pypi/drf-action-permissions)|[![build](https://img.shields.io/travis/com/abogoyavlensky/drf-action-permissions.svg)](https://travis-ci.com/abogoyavlensky/drf-action-permissions)|[![codecov](https://img.shields.io/codecov/c/github/abogoyavlensky/drf-action-permissions.svg)](https://codecov.io/gh/abogoyavlensky/drf-action-permissions)|

Flexible ability to add action permissions on view level
for Django REST framework. Permissions can be as complex or simple as you want.
It can be a plain string or a function.

## Requirements

- Python (3.6+)
- Django (1.11.x, 2.0+)
- Django REST Framework (3.7+)

## Installation

```bash
$ pip install drf-common-exceptions
```

You cound define common permissions class for whole project:

```
REST_FRAMEWORK = {
    ...
    "DEFAULT_PERMISSION_CLASSES": (
        "drf_action_permissions.DjangoActionPermissions",
    )
    ...
}
```

Or use it just for particular viewset in combination with others:

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from drf_action_permissions import DjangoActionPermissions

class MyView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, DjangoActionPermissions)
    perms_map_action = {
        'retrieve': ['users.view_user'],
    }
```

## Usage examples

Permission as string template or plain string:
```python
class PostViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, DjangoActionPermissions)
    perms_map_action = {
        'likes': ['%(app_label)s.view_%(model_name)s_list',
                  '%(app_label)s.view_like_list'],
    }
```

Permission as function with current object access:
```python
def can_view_application(user, _view, obj):
    """Can view only archived applications."""
    if obj.is_archived:
        return user.has_perm('applications.view_archived_application')
    return user.has_perm('applications.view_application')


class ApplicationView(ModelViewSet):
    permission_classes = (IsAuthenticated, DjangoActionPermissions)
    perms_map_action_obj = {
        'retrieve': [can_view_application],
    }
```


## Development

Install poetry and requirements:

```bash
$ curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
$ python3 -m venv path/to/venv
$ source path/to/venv/bin/activate
$ poetry install
```

Run main commands:

```bash
$ make test
$ make watch
$ make clean
$ make lint
```

Publish to pypi by default patch version:
```bash
$ make publish
```

or any level you want:
```bash
$ make publish minor
```
