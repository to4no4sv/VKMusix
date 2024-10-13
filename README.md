# VKMusix [![PyPI version](https://d25lcipzij17d.cloudfront.net/badge.svg?id=py&r=r&ts=1683906897&type=6e&v=4.1.1&x2=0)](https://pypi.org/project/vkmusix)

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

## Основные возможности

**• Работа в синхронном и асинхронном режимах**

**• Интуитивно понятные названия методов, параметров, классов и атрибутов, а также подробная вложенная документация**

**• Работа от имени нескольких аккаунтов одновременно благодаря поддержке прокси**

**• Возможность подключения авторешения капч через сервис [RuCaptcha](https://rucaptcha.com)**

**• Получение доступа к трекам в приватных плейлистах и музыке пользователей или групп при авторизации в аккаунт**

**• Лёгкий и простой поиск исполнителей, альбомов, треков, плейлистов, или всего сразу, в пару строк кода**

**• Доступ к текстам треков и функция для их загрузки в MP3, а также ссылкам на обложки в формате JPG для альбомов и плейлистов**

**• Управление своей музыкальной коллекцией и музыкой сообществ: добавление или удаление треков, альбомов и плейлистов легко и быстро**

**• Загрузка своих аудиофайлов на платформу за считанные секунды**

**• Клонирование альбомов и плейлистов других пользователей, создавая собственные плейлисты одной строчкой кода**

**• Функция `APIReq` для отправки запроса к любому методу ВКонтакте API**
