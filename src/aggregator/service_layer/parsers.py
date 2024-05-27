import aiohttp
import aiofile
import asyncio
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


class ParserOlymp:
    # URL страницы олимпиады без id
    _main_url = 'https://olimpiada.ru/activity/'
    _file_path = 'olympiads.json'
    _ids_path = 'ids.txt'
    _date_ru = {
        'янв': 1,
        'фев': 2,
        'мар': 3,
        'апр': 4,
        'май': 5,
        'мая': 5,
        'июн': 6,
        'июл': 7,
        'авг': 8,
        'сен': 9,
        'окт': 10,
        'ноя': 11,
        'дек': 12
    }

    async def fetch_with_retries(self, session, url, retries=0):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await asyncio.wait_for(response.text(), timeout=10)
                    return html
                else:
                    return None
        except (aiohttp.ClientError, asyncio.TimeoutError):
            if retries < 10:
                await asyncio.sleep(2 ** retries)
                return await self.fetch_with_retries(session, url, retries + 1)
            else:
                return None

    async def fetch_and_process(self, session, url, _id, semaphore, delay=0):
        async with semaphore:
            html = await self.fetch_with_retries(session, url)
            if html:
                olymp_data = await self.get_info_from_html(html)
                return _id, olymp_data
            else:
                await asyncio.sleep(delay)  # Задержка между запросами
                return _id, None

    async def check_valid_ids(self, delay=1):
        tasks = []
        semaphore = asyncio.Semaphore(50)

        async with aiohttp.ClientSession() as session:
            for _id in range(100000):
                url_key = f'{self._main_url}{_id}'
                tasks.append(self.fetch_and_process(session, url_key, _id, semaphore, delay))

            results = await asyncio.gather(*tasks, return_exceptions=True)

        ids = [
            str(_id) for _id, result in results
            if result is not None and not isinstance(result, Exception)
        ]
        return ids

    async def write_valid_ids(self):
        ids = await self.check_valid_ids()
        async with aiofile.async_open(self._ids_path, 'w') as f:
            await f.write('\n'.join(ids))

    async def get_valid_ids(self):
        async with aiofile.async_open(self._ids_path, 'r') as f:
            ids = await f.read()
            return ids.splitlines()

    @staticmethod
    async def get_classes(soup) -> list | None:
        html = soup.find('div', class_='subject_tags_full')
        if html:
            classes_text = html.text.replace('\n', '').replace('\xa0', ' ')
            classes = [item.strip() for item in re.findall(r'[А-Я]+[^А-Я]+', classes_text)]
            return classes

    @staticmethod
    async def get_description(soup) -> str | None:
        html = soup.find('div', class_='info block_with_margin_bottom')
        if html:
            html = html.find_all('p')
            description_text = ' '.join(map(lambda x: x.getText(), html))
            description = description_text.replace('...\nЕще\n', '.')
            return description

    async def get_timetable(self, soup) -> dict | str | None:
        html = soup.find('tbody')
        if html:
            stages = {}
            timetable_text = html.text.replace('\n', ' ').replace('\xa0', ' ')
            timetable = list(item.strip() for item in timetable_text.split('   ') if item)
            for info in timetable:
                data = re.findall(r'^([\w\s\d-]+)\s(\d{1,2})\s?([а-я]{3})?\.\.\.(\d{1,2})\s([а-я]{3})$', info)
                if not data:
                    data = re.findall(r'^([\w\s\d-]+)\s(\d{1,2})\s([а-я]{3})$', info)
                if data:
                    stage, *dt = data[0]
                    day1 = int(dt[0])
                    month_key = dt[1] if dt[1] else dt[-1]

                    if len(dt) == 4:
                        mouth1 = self._date_ru[month_key]
                        mouth2 = self._date_ru[dt[-1]]
                        day2 = int(dt[2])
                        year1 = 2024 if mouth1 <= mouth2 else 2023
                        year2 = 2024 if year1 <= datetime.now().year else 2023
                        start_date = datetime(day=day1, month=mouth1, year=year1)
                        end_date = datetime(day=day2, month=mouth2, year=year2)

                        date_list = [d.strftime("%Y-%m-%d") for d in (start_date, end_date)]

                    else:
                        mouth1 = self._date_ru[dt[-1]]
                        year1 = 2024 if mouth1 <= datetime.now().month else 2023

                        date_list = [datetime(day=day1, month=mouth1, year=year1).strftime("%Y-%m-%d")]

                    stages[stage] = date_list

            return stages

        else:
            event_info = soup.find('span', class_=lambda x: x.startswith('events-info')).getText()
            return event_info

    @staticmethod
    async def get_grades(soup) -> list | None:
        grades_text = soup.find('span', class_='classes_types_a').getText()
        start, end = re.search(r'\d+–\d+', grades_text).group().split('–')
        grades = [i for i in range(int(start), int(end) + 1)]
        return grades

    async def get_info_from_html(self, html) -> dict | None:
        soup = BeautifulSoup(html, 'html.parser')
        try:
            div_left = soup.find('div', class_='left')
            title = soup.find('h1').getText()
            classes = await self.get_classes(soup)
            description = await self.get_description(soup)
            timetable = await self.get_timetable(div_left)
            grades = await self.get_grades(soup)
            rating = soup.find('span', class_='rating').getText()

            olymp_data = {
                'title': title,
                'rating': rating,
                'classes': classes,
                'description': description,
                'grades': grades,
                'timetable': timetable
            }

            return olymp_data

        except AttributeError:
            return None

    async def run_process(self) -> None:
        await self.clear_json()

        tasks = []
        semaphore = asyncio.Semaphore(100000)

        async with aiohttp.ClientSession() as session:
            ids = await self.get_valid_ids()
            for _id in ids:
                url_key = f'{self._main_url}{_id}'
                tasks.append(self.fetch_and_process(session, url_key, _id, semaphore))

            results = await asyncio.gather(*tasks)

            for _id, olymp_data in results:
                if olymp_data:
                    await self.write_json(olymp_data, _id)

    async def write_json(self, olymp_data, _id) -> None:
        with open(self._file_path, 'r', encoding='utf-8') as f:
            olympiads = json.load(f)

        olympiads[_id] = olymp_data

        with open(self._file_path, 'w', encoding='utf-8') as f:
            json.dump(olympiads, f, ensure_ascii=False, indent=4)

    @staticmethod
    async def clear_json() -> None:
        with open('olympiads.json', 'w', encoding='utf-8') as f:
            json.dump({}, f)


async def main():
    parser = ParserOlymp()
    await parser.run_process()


if __name__ == '__main__':
    asyncio.run(main())
