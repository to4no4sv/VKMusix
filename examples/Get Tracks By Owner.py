import aiofiles
import asyncio

from vkmusix import Client
from vkmusix.enums import Language

ownerId = None
full = True

async def main() -> None:
    async with Client(
        language=Language.Russian,
    ) as client:
        sections = await client.getSections(
            ownerId=ownerId,
        )

        if not sections:
            return

        subsections = (await sections[0].get()).subsections

        # Первый способ
        tracks = await subsections[0].getTracks()

        if not tracks:
            return

        # Часть кода ниже только если нужна полная информация о треках
        if full:
            ownerIds = [track.ownerId for track in tracks]
            trackIds = [track.trackId for track in tracks]

            batchSize = 343
            tasks = [
                client.get(
                    ownerIds=ownerIds[i:i + batchSize],
                    trackIds=trackIds[i:i + batchSize]
                )
                for i in range(0, len(tracks), batchSize)
            ]

            batches = await asyncio.gather(*tasks)

            tracks = [
                track
                for batch in batches if batch
                for track in batch
            ]
        # Часть кода выше только если нужна полная информация о треках

        async with aiofiles.open("Tracks V1.json", "w") as file:
            await file.write(str(tracks))

        # Второй способ
        async with aiofiles.open("Tracks V2.json", "w") as file:
            await file.write("[")

            first = True
            subsection = await subsections[0].get()

            while subsection:
                for track in subsection.tracks:
                    if not first:
                        await file.write(", ")

                    else:
                        first = False

                    await file.write(str(track))

                if not subsection.nextOffset:
                    break

                subsection = await subsections[0].get(subsection.nextOffset)

            await file.write("]")

if __name__ == "__main__":
    asyncio.run(main())