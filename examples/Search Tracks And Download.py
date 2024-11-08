"""Расчёты:

1. 26,3 MB за 2 сек (5 треков):
   Скорость: 13,15 MB/сек
   Треки: 2,5 треков/сек

2. 46,4 MB за 3,39 сек (10 треков):
   Скорость: 13,68 MB/сек
   Треки: 2,95 треков/сек

3. 69 MB за 5,21 сек (15 треков):
   Скорость: 13,24 MB/сек
   Треки: 2,88 треков/сек

4. 93,2 MB за 6,7 сек (20 треков):
   Скорость: 13,91 MB/сек
   Треки: 2,99 треков/сек

5. 119 MB за 9,11 сек (25 треков):
   Скорость: 13,06 MB/сек
   Треки: 2,74 треков/сек

6. 313 MB за 20,2 сек (50 треков):
   Скорость: 15,5 MB/сек
   Треки: 2,48 треков/сек

7. 570 MB за 38,73 сек (100 треков):
   Скорость: 14,71 MB/сек
   Треки: 2,58 треков/сек

Итоги:
    Скорость загрузки варьируется от примерно 13,06 MB/сек до 15,5 MB/сек.
    Скорость обработки треков варьируется от 2,48 треков/сек до 2,99 треков/сек."""

import os
import asyncio

from vkmusix import Client
from vkmusix.types import Track
from vkmusix.enums import Language

query = "Маленький ярче"
limit = 10
directory = os.path.join(
    os.getcwd(),
    "tracks",
)

async def main() -> None:
    async with Client(
            language=Language.Russian,
    ) as client:
        tracks = await client.searchTracks(
            query=query,
            limit=limit,
        )

        if not tracks:
            return

        semaphore = asyncio.Semaphore(10)

        async def downloadWithSemaphore(track: Track) -> None:
            async with semaphore:
                return await track.download(
                    directory=directory,
                    metadata=True,
                )

        tasks = [downloadWithSemaphore(track) for track in tracks]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())