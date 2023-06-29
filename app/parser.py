from datetime import datetime
from playwright.sync_api import sync_playwright
from time import sleep
from config import url, password, work_url, user, time_run, logger
import json


date_now = datetime.today()

def login(page):
    page.goto(url)
    page.locator('#login').fill(user)
    page.locator('#password').fill(password)
    page.locator('#Auth').click()
    logger.info('authirization to page')
    sleep(5)
    page.goto(work_url)
    # page.locator('xpath=//*[@id="someHidden"]/button').click()
    page.locator('xpath=//*[@id="close_popup_instructions"]').click()
    logger.info('close ad modal dialog')

def config(page):
    page.locator('xpath=//*[@id="auction_date"]').fill(date_now.strftime('%d/%m/%y'))
    page.locator('xpath=//*[@id="car_price"]').fill('0')
    page.locator('xpath=//*[@id="Appointment"]').select_option('Klaipeda')
    page.locator('xpath=//*[@id="container"]').select_option('Sedan')

#get select data

def click_select(page, xpath: str, select: str):
    page.locator(xpath).select_option(select)
    page.locator(xpath).click()
    sleep(1)

def get_select_data(page, xpath: str)->list:
    options = page.locator(xpath).all_inner_texts()
    return ''.join(options).split('\n')[1:]


def parse_page(action: str)->list:
    logger.info('chrome prepare to open')
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=True, timeout=10000, args=['--start-maximized'])
        logger.info('chrome opened')
        page = browser.new_page(no_viewport=True)
        
        ''' default config'''
        login(page)
        config(page)
        '''clicks'''
        
        data: list = []
        click_select(page,'//*[@id="auction"]', action)
        
        '''states'''
        states = get_select_data(page, '//*[@id="state"]')
        # print(states)
        for state in states:
            logger.info(state)
            click_select(page,'//*[@id="state"]', state)
            cities = get_select_data(page, '//*[@id="citi"]')
            for city in cities:
                logger.info(city)
                click_select(page,'//*[@id="citi"]', city)
                port = get_select_data(page, '//*[@id="loading_port"]')
                if len(port) == 1:
                    port = ''.join(port)
                    click_select(page,'//*[@id="loading_port"]', port)
                else:
                    port
                    logger.info('more datas for parameter')

                
                page.locator('xpath=//*[@id="count"]').click()
                price = page.locator('xpath=//*[@id="total_transportireba"]').input_value()
                data.append({'state': state,
                                'city': city,
                                'port': port,
                                'price': price})
            break

    # page.pause()
        # with open(f'{action}.json', 'w') as json_file:
        #     json.dump(data, json_file, ensure_ascii=False, indent=4)
        page.close()
    return data
    

