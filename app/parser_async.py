from datetime import datetime
from playwright.async_api import async_playwright
from time import sleep
from config import url, password, work_url, user, time_run, logger
import json


date_now = datetime.today()

async def login(page):
    await page.goto(url)
    await page.locator('#login').fill(user)
    await page.locator('#password').fill(password)
    await page.locator('#Auth').click()
    logger.info('authirization to page')
    sleep(5)
    await page.goto(work_url)
    # page.locator('xpath=//*[@id="someHidden"]/button').click()
    await page.locator('xpath=//*[@id="close_popup_instructions"]').click()
    logger.info('close ad modal dialog')

async def config(page, port: str):
    await page.locator('xpath=//*[@id="auction_date"]').fill(date_now.strftime('%d/%m/%y'))
    await page.locator('xpath=//*[@id="car_price"]').fill('0')
    await page.locator('xpath=//*[@id="Appointment"]').select_option(port)
    await page.locator('xpath=//*[@id="container"]').select_option('Sedan')

#get select data

async def click_select(page, xpath: str, select: str):
    await page.locator(xpath).select_option(select)
    await page.locator(xpath).click()
    sleep(1)

async def get_select_data(page, xpath: str)->list:
    options = await page.locator(xpath).all_inner_texts()
    return ''.join(options).split('\n')[1:]


async def parse_page(action: str, port: str)->list:
    logger.info('chrome prepare to open')
    data: list = []
    async with async_playwright() as p:
        
        browser = await p.chromium.launch()
        page = await browser.new_page(no_viewport=True)

        await login(page)
        await config(page, port)

        '''clicks'''
        await click_select(page,'//*[@id="auction"]', action)
        '''states'''
        states = await get_select_data(page, '//*[@id="state"]')
        # print(states)
        for state in states:
            logger.info(state)
            await click_select(page,'//*[@id="state"]', state)
            cities = await get_select_data(page, '//*[@id="citi"]')
            for city in cities:
                logger.info(city)
                await click_select(page,'//*[@id="citi"]', city)
                port = await get_select_data(page, '//*[@id="loading_port"]')
                if len(port) == 1:
                    port = ''.join(port)
                    await click_select(page,'//*[@id="loading_port"]', port)
                else:
                    port
                    logger.info('more datas for parameter')

                
                await page.locator('xpath=//*[@id="count"]').click()
                price = await page.locator('xpath=//*[@id="total_transportireba"]').input_value()
                data.append({'state': state,
                                'city': city,
                                'port': port,
                                'price': price})
            break
        
        await browser.close()
        return data #{"parsing data": data}
    

