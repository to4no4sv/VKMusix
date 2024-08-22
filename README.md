# VKMusix [![PyPI version](https://badge.fury.io/py/vkmusix.sv)](https://pypi.org/project/vkmusix)

## Установка и обновление
```bash
pip install --upgrade vkmusix
```

## Быстрый старт
```python
from vkmusix import Client

client = Client()

result = client.searchArtists("prombl")
print(result)
