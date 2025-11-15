import asyncio
from pathlib import Path
from config import Config
from downloader import ChapterDownloader
import argparse
import sys
import json
import os

def prompt_user_config() -> Config:
    print("=== MangaLib Downloader Config ===\n")

    manga_url = input("Введите ссылку на мангу: ").strip()
    # Извлекаем slug из ссылки, например "https://mangalib.me/114307--kaoru-hana-wa-rinto-saku"
    manga_slug = manga_url.split("/")[-1].split("?")[0]

    start = int(input("Введите начальную главу: ").strip() or "1")
    end = int(input("Введите конечную главу: ").strip() or str(start))

    title_override = input("Название манги (Enter — оставить по умолчанию): ").strip() or None

    try:
        max_chapters = int(input("Максимум одновременно загружаемых глав (по умолчанию 1): ") or "1")
        max_images = int(input("Максимум одновременно загружаемых изображений (по умолчанию 5): ") or "5")
        delay = float(input("Задержка между запросами (по умолчанию 0.8): ") or "0.8")
    except ValueError:
        max_chapters, max_images, delay = 1, 5, 0.8

    pack_cbz_input = input("Собирать CBZ архивы? (y/n, по умолчанию y): ").strip().lower()
    pack_cbz = pack_cbz_input != "n"

    generate_metadata_input = input("Создавать ComicInfo/series.json? (y/n, по умолчанию y): ").strip().lower()
    generate_metadata = generate_metadata_input != "n"

    cfg = Config(
        manga_slug=manga_slug,
        chapter_range=(start, end),
        series_title_override=title_override,
        max_concurrent_chapters=max_chapters,
        max_concurrent_images=max_images,
        request_delay=delay,
        output_dir=Path("downloads"),
        cleanup_temp=True,
        # pack_cbz=pack_cbz,
        # generate_metadata=generate_metadata
    )

    return cfg

def generate_base_config():
    base_config = {
        "manga_slug": "paste here your link",
        "chapter_begin": 1,
        "chapter_end": 10,
        "series_title_override": "enter your overrided title",
        "max_concurrent_chapters": 1,
        "max_concurrent_images": 5,
        "request_delay": 0.8
    }

    with open("config.json", "w", encoding="utf-8") as file:
        json.dump(base_config, file, indent=4, ensure_ascii=False)

    print("Базовая конфигурация успешно создана")

def read_config_file(file_path: str) -> Config:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    cfg = Config(
        manga_slug = data["manga_slug"].split("/")[-1].split("?")[0],
        chapter_range = (data["chapter_begin"], data["chapter_end"]),
        series_title_override = data["series_title_override"],
        max_concurrent_chapters = data["max_concurrent_chapters"],
        max_concurrent_images = data["max_concurrent_images"],
        request_delay = data["request_delay"],
        output_dir = Path("downloads"),
        cleanup_temp = True
    )

    return cfg

async def main():
    parser = argparse.ArgumentParser("Загрузчик глав с MangaLib") # Необходим для принятия входящих аргументов

    parser.add_argument("--make_base_config", action="store_true", help="Создать пример конфигурационного файла")
    parser.add_argument("--config_file", type=str, help="Использовать конфигурационный файл для скачивания главы")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        cfg = prompt_user_config()
        downloader = ChapterDownloader(cfg)
        await downloader.download_chapters(cfg.chapter_range)

    if args.make_base_config:
        generate_base_config()

    if args.config_file:
        cfg = read_config_file(args.config_file)
        downloader = ChapterDownloader(cfg)
        await downloader.download_chapters(cfg.chapter_range)

if __name__ == "__main__":
    asyncio.run(main())
