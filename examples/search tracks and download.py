async def searchTracksAndDownload(query: str = "Heronwater", limit: int = 5, directory: str = os.path.join(os.getcwd(), "tracks")) -> None:
    import os
    import asyncio
    from vkmusix import Client, Error

    async with Client(errorsLanguage="ru") as client:
        tracks = await client.searchTracks(query=query, limit=limit)

        if isinstance(tracks, Error):
            print(tracks)
            return

        semaphore = asyncio.Semaphore(8)

        async def downloadWithSemaphore(track: "Track") -> None:
            async with semaphore:
                return await track.download(directory=directory)

        trackTasks = [downloadWithSemaphore(track) for track in (tracks if isinstance(tracks, list) else [tracks])]
        await asyncio.gather(*trackTasks)

if __name__ == "__main__":
    import asyncio
    asyncio.run(searchTracksAndDownload())
