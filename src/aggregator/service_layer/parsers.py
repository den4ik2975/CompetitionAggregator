import aiohttp
import asyncio
import json
import re
from bs4 import BeautifulSoup


class ParserOlymp:
    # URL страницы олимпиады без id
    _main_url = 'https://olimpiada.ru/activity/'
    _file_path = 'olympiads.json'

    async def fetch_and_process(self, session, url, _id) -> (str, dict | None):
        async with session.get(url) as response:
            if response.status == 200:
                html = await asyncio.wait_for(response.text(), timeout=10)
                olymp_data = await self.get_info_from_html(html)
                return _id, olymp_data
            else:
                return _id, None

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

    @staticmethod
    async def get_timetable(soup) -> str | None:
        html = soup.find('tbody')
        if html:
            timetable_text = html.text.replace('\n', ' ').replace('\xa0', ' ')
            timetable = '\n'.join(item.strip() for item in timetable_text.split('   ') if item)
            return timetable
        else:
            event_info = soup.find('span', class_=lambda x: x.startswith('events-info')).getText()
            return event_info

    async def get_info_from_html(self, html) -> dict | None:
        soup = BeautifulSoup(html, 'html.parser')
        try:
            div_left = soup.find('div', class_='left')
            title = soup.find('h1').getText()
            classes = await self.get_classes(soup)
            description = await self.get_description(soup)
            timetable = await self.get_timetable(div_left)
            rating = soup.find('span', class_='rating').getText()
            grades = soup.find('span', class_='classes_types_a').getText()

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

        async with aiohttp.ClientSession() as session:
            for _id in range(6000):
                url_key = f'{self._main_url}{_id}'
                tasks.append(self.fetch_and_process(session, url_key, _id))

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
