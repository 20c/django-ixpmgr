## Maintain requirements

We are using pipenv to manage dependencies.

After changes are made to the env and Pipfile has been relocked you should
also use ctl to sync requirements to setup.py

```sh
ctl venv sync_setup setup.py
```
