import json
from typing import List, Union, Dict, Any

import aiofiles


async def send_application(data: List[dict], user_id: int, text: str) -> List[dict]:
    result = []
    result.append({'search': str(text)})
    n = 0
    for item in data:
        id_value = str(item['id'])
        brand = item['brand']
        name = item['name']
        reviewRating = item['reviewRating']
        feedbacks = item['feedbacks']

        is_adult = item['isAdult'] if 'isAdult' in item else None
        if is_adult is not None:
            is_adult = '18+' if is_adult else None
        sizes = item['sizes']
        if sizes and 'price' in sizes[0]:
            iznazhalno = sizes[0]['price']['basic'] / 100
            price = sizes[0]['price']['total'] / 100
        else:
            iznazhalno = 0
            price = 0

        photo = await choose_basket(id_value)
        if id_value is not None:
            n += 1
            result.append({
                           'nomer': n,
                           'id': id_value,
                           'brand': brand,
                           'name': name,
                           'iznachalno': iznazhalno,
                           'skidka': price,
                           'raiting': reviewRating,
                           'feedbacks': feedbacks,
                           'is_adult': is_adult,
                           'photo': photo})
    formatted_output = json.dumps(result, indent=2, ensure_ascii=False)

    async with aiofiles.open(f'wbs_{str(user_id)}.json', 'w', encoding='utf-8') as file:
        await file.write(formatted_output)

    return result[1]
    result.clear()


async def add_parapraph_send_application(data: List[dict], user_id: int, leaf: Union[str, int], existing_data: list[Dict[str, Any]]) -> List[dict]:
    leaf_ = int(leaf * 100)
    result = []
    n = int(leaf_)
    for item in data:
        id_value = str(item['id'])
        brand = item['brand']
        name = item['name']
        reviewRating = item['reviewRating']
        feedbacks = item['feedbacks']

        is_adult = item['isAdult'] if 'isAdult' in item else None
        if is_adult is not None:
            is_adult = '18+' if is_adult else None
        sizes = item['sizes']
        if sizes and 'price' in sizes[0]:
            iznazhalno = sizes[0]['price']['basic'] / 100
            price = sizes[0]['price']['total'] / 100
        else:
            iznazhalno = 0
            price = 0

        photo = await choose_basket(id_value)
        if id_value is not None:
            n += 1
            result.append({
                           'nomer': n,
                           'id': id_value,
                           'brand': brand,
                           'name': name,
                           'iznachalno': iznazhalno,
                           'skidka': price,
                           'raiting': reviewRating,
                           'feedbacks': feedbacks,
                           'is_adult': is_adult,
                           'photo': photo})
    existing_data.extend(result)

    async with aiofiles.open(f'wbs_{str(user_id)}.json', 'w', encoding='utf-8') as file:
        await file.write(json.dumps(existing_data, indent=2, ensure_ascii=False))

    result.clear()


async def choose_basket(id_value: str) -> str:
    if len(id_value) == 9:
        part = id_value[:6]
        vol = id_value[:4]
    elif len(id_value) == 8:
        part = id_value[:5]
        vol = id_value[:3]
    elif len(id_value) == 7:
        part = id_value[:4]
        vol = id_value[:2]
    vol = int(vol)
    if vol >= 0 and vol <= 143:
        basket = "01"
    elif vol >= 144 and vol <= 287:
        basket = "02"
    elif vol >= 288 and vol <= 431:
        basket = "03"
    elif vol >= 432 and vol <= 719:
        basket = "04"
    elif vol >= 720 and vol <= 1007:
        basket = "05"
    elif vol >= 1008 and vol <= 1061:
        basket = "06"
    elif vol >= 1062 and vol <= 1115:
        basket = "07"
    elif vol >= 1116 and vol <= 1169:
        basket = "08"
    elif vol >= 1170 and vol <= 1313:
        basket = "09"
    elif vol >= 1314 and vol <= 1601:
        basket = "10"
    elif vol >= 1602 and vol <= 1655:
        basket = "11"
    elif vol >= 1656 and vol <= 1919:
        basket = "12"
    elif vol >= 1920 and vol <= 2045:
        basket = "13"
    elif vol >= 2046 and vol <= 2186:
        basket = "14"
    elif vol >= 2187 and vol <= 2400:
        basket = "15"
    else:
        basket = "16"
    return f'https://basket-{str(basket)}.wbbasket.ru/vol{str(vol)}/part{str(part)}/{id_value}/images/big/1.webp'