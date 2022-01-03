# Tranquillity :rainbow:

![Workflow](https://github.com/Freonius/tranquillity/actions/workflows/gh-action-python.yml/badge.svg)
[![codecov](https://codecov.io/gh/Freonius/tranquillity/branch/master/graph/badge.svg?token=F6HK01BK76)](https://codecov.io/gh/Freonius/tranquillity)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Freonius/tranquillity.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Freonius/tranquillity/context:python)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/Freonius/tranquillity.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Freonius/tranquillity/alerts/)
![Dependencies alerts](https://img.shields.io/snyk/vulnerabilities/github/freonius/tranquillity)
![Docker image Size](https://img.shields.io/docker/image-size/federiker/tranquillity/latest)
![Lines of code](https://tokei.rs/b1/github/Freonius/tranquillity)
![License](https://img.shields.io/github/license/Freonius/tranquillity)

Tranquillity is a set of utilities that I got tired of copying and pasting everywhere,
and that helps me doing the things that need to be done, without worrying too much
about connections, logging, requests, or endpoints.

It is a work in progress, so, if you use it, keep that in mind. (As soon as I am done working on it, I'll remove this line)

:bangbang: **Seriously**, don't use it now, it doesn't even work (except for a couple of modules).

If you want to help me out, or make any changes, write me at freonius@gmail.com.

I think it's nice, but I am biased, but if nobody else uses it, I will.

Anyway, enough about this -- I haven't talked about me, so I could not say "enough about me" --, here's the documentation
so far.

## Python :snake:

The Python section is divided into modules. Some modules build on top of others, but some are self sustained.

Here are the modules.

### Api :x:

TODO

### Connections :x:

TODO

### Data :x:

TODO

### Email :x:

TODO

### Enums :x:

TODO

### Exceptions :soon:

The exception part is pretty easy to understand. Some are really simple exceptions, others are Http Exceptions, that have a reason and a status code. So, if you didn't find a resource, you could raise a ResourceNotFound, and you would automatically get a 404 status code.

### Files :x:

TODO

### GIS :x:

TODO

### Html :x:

TODO

### Logger :soon:

TODO

### Path :soon:

TODO

### Query :x:

TODO

### Queue :x:

TODO

### Regexes :x:

TODO

### Schedulable :soon:

TODO

### Settings :ok:

Different classes to get application settings. All the data will be flat and accessible through 'key.subkey'.

Imagine you have this Yaml file

```yaml
# settings.yml
app:
  name: Cool-Name
  port: 8000
```

If the name is `settings.yml` or `tranquillity.yml`, and it's in the main project folder, you don't even have to specify
the file name.

```python
from tranquillity.settings import Yaml, Env

settings = Yaml()

print(settings['app.name']) # Prints 'Cool-Name'

env = Env()
env['path'] # Prints the PATH environment
```

The supported settings providers are:

- Yaml \*
- Json \*
- Ini \*
- Properties
- Spring Config Server
- Sqlite \*\*
- Environment Variables
- Any dictionary

\* Defaults to tranquillity or settings + extension
\*\* Defaults to in memory db

It is also possible to implement other providers by extending the `ISettings` class.

```python
from tranquillity.settings import ISettings

class NewSetting(ISettings):
    def __init__(self):
        super().__init__()
        self._config(
            {'key': 'value'},                   # The data to use
            defaults={'missing': 'no problem'}, # Default values if missing
            raise_on_missing=True,              # If False it will return None if the key is missing
            read_only=True)                     # Don't update

    def _update(self, key: str, val: str) -> None:
        pass    # Your update operation
```

### Shell :ok:

TODO

### Utils :ok:

TODO

## Docker :whale2:

### Tranquillity :soon:

TODO

### Pandas :soon:

TODO

### Flutter :x:

TODO

### Tizen :soon:

TODO

## Flutter :phone:

TODO

## React :page_with_curl:

TODO
