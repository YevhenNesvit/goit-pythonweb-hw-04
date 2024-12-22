import argparse
import logging
import asyncio
from aiopath import AsyncPath
from aioshutil import copyfile

logging.basicConfig(level=logging.ERROR)

async def read_folder(source_folder, output_folder):
    tasks = []
    async for item in AsyncPath(source_folder).rglob("*"):
        if item.is_file():
            tasks.append(copy_file(item, output_folder))
    await asyncio.gather(*tasks)

async def copy_file(source_path, output_folder):
    file_extension = source_path.suffix.strip('.') or output_folder
    output_path = AsyncPath(output_folder) / file_extension

    if not await output_path.exists():
        await output_path.mkdir(parents=True, exist_ok=True)

    try:
        destination = output_path / source_path.name
        await copyfile(source_path, destination)
        print(f"File {source_path.name} copied to {output_path}")
    except Exception as e:
        logging.error(f"Error copying file {source_path.name}: {e}")

async def main():
    parser = argparse.ArgumentParser(description="Sort files by extension")
    parser.add_argument("source_folder", help="Source folder path")
    parser.add_argument("output_folder", help="Output folder path")
    args = parser.parse_args()

    source_folder = AsyncPath(args.source_folder)
    output_folder = AsyncPath(args.output_folder)

    if not await output_folder.exists():
        await output_folder.mkdir(parents=True, exist_ok=True)

    await read_folder(source_folder, output_folder)

if __name__ == "__main__":
    asyncio.run(main())
