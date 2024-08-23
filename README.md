# VKMusix [![PyPI version](https://d25lcipzij17d.cloudfront.net/badge.svg?id=py&r=r&ts=1683906897&type=6e&v=3.1.3&x2=0)](https://pypi.org/project/vkmusix)

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

client.close()
```
