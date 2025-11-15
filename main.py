import asyncio
from pathlib import Path

from config import Config
from downloader import ChapterDownloader


async def main():
    # ========== КОНФИГУРАЦИЯ ==========
    cfg = Config(
        manga_slug="1357--vagabond", # https://mangalib.me/ru/manga/ВОТ ЗДЕСЬ БУДУТ ЦИФРЫ И НАЗВАНИЕ, СКОПИРОВАТЬ ДО ВОПРОСИТЕЛЬНОГО ЗНАКА ВКЛЮЧИТЕЛЬНО (если есть)
        chapter_range=(326, 328),  # (начальная глава, конечная глава)
        series_title_override="Vagabond",
        
        # Параметры производительности
        max_concurrent_chapters=2,  # рекомендуется: 1-5
        max_concurrent_images=3,    # рекомендуется: 2-10
        request_delay=5,          # рекомендуется: 0.5-5
        
        # Дополнительные параметры
        output_dir=Path("downloads"),
        cleanup_temp=True,
        fallback_volume_range=(1, 15),

        # если False — НЕ распределять по томам (все главы в одной папке архива)
        group_by_volume=False,
    )
    # ========== КОНФИГУРАЦИЯ ==========

    downloader = ChapterDownloader(cfg)
    await downloader.download_chapters(cfg.chapter_range)


if __name__ == "__main__":
    asyncio.run(main())
