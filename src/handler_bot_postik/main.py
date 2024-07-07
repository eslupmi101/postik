import asyncio
import logging
import sys

from app.bot import start_bot


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start_bot())


if __name__ == '__main__':
    main()
