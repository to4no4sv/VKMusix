import os
import asyncio

from vkmusix import Client
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

        tasks = [
            track.download(
                directory=directory,
                metadata=True,
            )
            for track in tracks
        ]

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())