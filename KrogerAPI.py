import asyncio
import json
import KrogerCLI
import re
import datetime
import KrogerHelper
from Memoize import memoized
from pyppeteer import launch


class KrogerAPI:
    browser_options = {
        'headless': True,
        'args': ['--blink-settings=imagesEnabled=false']  # Disable images for hopefully faster load-time
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.129 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    def __init__(self, cli: KrogerCLI):
        self.cli = cli

    def complete_survey(self):
        return asyncio.run(self._complete_survey())

    @memoized
    def get_account_info(self):
        return asyncio.run(self._get_account_info())

    @memoized
    def get_points_balance(self):
        return asyncio.run(self._get_points_balance())

    def clip_coupons(self):
        return asyncio.run(self._clip_coupons())

    @memoized
    def get_purchases_summary(self):
        return asyncio.run(self._get_purchases_summary())

    async def _retrieve_feedback_url(self):
        # Model overlay pop up (might not exist)
        # Need to click on it, as it prevents me from clicking on `Order Details` link
        try:
            await self.page.waitForSelector('.ModalitySelectorDynamicTooltip--Overlay', {'timeout': 10000})
            await self.page.click('.ModalitySelectorDynamicTooltip--Overlay')
        except Exception:
            pass

        try:
            # `See Order Details` link
            await self.page.waitForSelector('.PurchaseCard-top-view-details-button', {'timeout': 10000})
            await self.page.click('.PurchaseCard-top-view-details-button a')
            # `View Receipt` link
            await self.page.waitForSelector('.PurchaseCard-top-view-details-button a', {'timeout': 10000})
            await self.page.click('.PurchaseCard-top-view-details-button a')
            content = await self.page.content()
        except Exception:
            link = 'https://www.' + self.cli.config['main']['domain'] + '/mypurchases'
            self.cli.console.print('[bold red]Couldn’t retrieve the latest purchase, please make sure it exists: '
                                   '[link=' + link + ']' + link + '[/link][/bold red]')
            raise Exception

        try:
            match = re.search('Entry ID: (.*?) ', content)
            entry_id = match[1]
            match = re.search('Date: (.*?) ', content)
            entry_date = match[1]
            match = re.search('Time: (.*?) ', content)
            entry_time = match[1]
            self.cli.console.print('Entry ID retrieved: ' + entry_id)
        except Exception:
            self.cli.console.print('[bold red]Couldn’t retrieve Entry ID from the receipt, please make sure it exists: '
                                   '[link=' + self.page.url + ']' + self.page.url + '[/link][/bold red]')
            raise Exception

        entry = entry_id.split('-')
        hour = entry_time[0:2]
        minute = entry_time[3:5]
        meridian = entry_time[5:7].upper()
        date = datetime.datetime.strptime(entry_date, '%m/%d/%y')
        full_date = date.strftime('%m/%d/%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')
        year = date.strftime('%Y')

        url = f'https://www.krogerstoresfeedback.com/Index.aspx?' \
              f'CN1={entry[0]}&CN2={entry[1]}&CN3={entry[2]}&CN4={entry[3]}&CN5={entry[4]}&CN6={entry[5]}&' \
              f'Index_VisitDateDatePicker={month}%2f{day}%2f{year}&' \
              f'InputHour={hour}&InputMeridian={meridian}&InputMinute={minute}'

        return url, full_date

    async def _complete_survey(self):
        # signed_in = await self.sign_in_routine(redirect_url='/mypurchases', contains=['My Purchases'])
        # if not signed_in:
        #     await self.destroy()
        #     return None
        # self.cli.console.print('Loading `My Purchases` page (to retrieve the Feedback’s Entry ID)')

        # try:
        #     url, survey_date = self._retrieve_feedback_url()
        # except Exception:
        #     await self.destroy()
        #     return None

        await self.init()
        url = 'https://www.krogerstoresfeedback.com/Index.aspx?CN1=703&CN2=264&CN3=98&CN4=4&CN5=500&CN6=598&Index_VisitDateDatePicker=05%2f22%2f2020&InputHour=04&InputMeridian=PM&InputMinute=40'
        survey_date = '05/22/2020'

        await self.page.goto(url)
        await self.page.waitForSelector('#Index_VisitDateDatePicker', {'timeout': 10000})
        # We need to manually set the date, otherwise the validation fails
        js = "() => {$('#Index_VisitDateDatePicker').datepicker('setDate', '" + survey_date + "');}"
        await self.page.evaluate(js)
        await self.page.click('#NextButton')

        for i in range(35):
            current_url = self.page.url
            try:
                await self.page.waitForSelector('#NextButton', {'timeout': 5000})
            except Exception:
                if 'Finish' in current_url:
                    await self.destroy()
                    return True
            await self.page.evaluate(KrogerHelper.get_survey_injection_js(self.cli.config))
            await self.page.click('#NextButton')

        await self.destroy()
        return False

    async def _get_account_info(self):
        signed_in = await self.sign_in_routine()
        if not signed_in:
            await self.destroy()
            return None

        self.cli.console.print('Loading profile info..')
        await self.page.goto('https://www.' + self.cli.config['main']['domain'] + '/accountmanagement/api/profile')
        try:
            content = await self.page.content()
            profile = self._get_json_from_page_content(content)
            user_id = profile['userId']
        except Exception:
            profile = None
        await self.destroy()

        return profile

    async def _get_points_balance(self):
        signed_in = await self.sign_in_routine()
        if not signed_in:
            await self.destroy()
            return None

        self.cli.console.print('Loading points balance..')
        await self.page.goto('https://www.' + self.cli.config['main']['domain'] + '/accountmanagement/api/points-summary')
        try:
            content = await self.page.content()
            balance = self._get_json_from_page_content(content)
            program_balance = balance[0]['programBalance']['balance']
        except Exception:
            balance = None
        await self.destroy()

        return balance

    async def _clip_coupons(self):
        signed_in = await self.sign_in_routine(redirect_url='/cl/coupons/', contains=['Coupons Clipped'])
        if not signed_in:
            await self.destroy()
            return None

        js = """
            window.scrollTo(0, document.body.scrollHeight);
            for (let i = 0; i < 150; i++) {
                let el = document.getElementsByClassName('kds-Button--favorable')[i];
                if (el !== undefined) {
                    el.scrollIntoView();
                    el.click();
                }
            }
        """

        self.cli.console.print('[italic]Applying the coupons, please wait..[/italic]')
        await self.page.keyboard.press('Escape')
        for i in range(6):
            await self.page.evaluate(js)
            await self.page.keyboard.press('End')
            await self.page.waitFor(1000)
        await self.page.waitFor(3000)
        await self.destroy()
        self.cli.console.print('[bold]Coupons successfully clipped to your account! :thumbs_up:[/bold]')

    async def _get_purchases_summary(self):
        signed_in = await self.sign_in_routine()
        if not signed_in:
            await self.destroy()
            return None

        self.cli.console.print('Loading your purchases..')
        await self.page.goto('https://www.' + self.cli.config['main']['domain'] + '/mypurchases/api/v1/receipt/summary/by-user-id')
        try:
            content = await self.page.content()
            data = self._get_json_from_page_content(content)
        except Exception:
            data = None
        await self.destroy()

        return data

    async def init(self):
        self.browser = await launch(self.browser_options)
        self.page = await self.browser.newPage()
        await self.page.setExtraHTTPHeaders(self.headers)
        await self.page.setViewport({'width': 700, 'height': 0})

    async def destroy(self):
        await self.browser.close()

    async def sign_in_routine(self, redirect_url='/account/update', contains=None):
        if contains is None and redirect_url == '/account/update':
            contains = ['Profile Information']

        await self.init()
        self.cli.console.print('[italic]Signing in.. (please wait, it might take awhile)[/italic]')
        signed_in = await self.sign_in(redirect_url, contains)

        if not signed_in and self.browser_options['headless']:
            self.cli.console.print('[red]Sign in failed. Trying one more time..[/red]')
            self.browser_options['headless'] = False
            await self.destroy()
            await self.init()
            signed_in = await self.sign_in(redirect_url, contains)

        if not signed_in:
            self.cli.console.print('[bold red]Sign in failed. Please make sure the username/password is correct.'
                                   '[/bold red]')

        return signed_in

    async def sign_in(self, redirect_url, contains):
        timeout = 20000
        if not self.browser_options['headless']:
            timeout = 60000
        await self.page.goto('https://www.' + self.cli.config['main']['domain'] + '/signin?redirectUrl=' + redirect_url)
        await self.page.type('#SignIn-emailInput', self.cli.username)
        await self.page.type('#SignIn-passwordInput', self.cli.password)
        await self.page.keyboard.press('Enter')
        try:
            await self.page.waitForNavigation(timeout=timeout)
        except Exception:
            return False

        if contains is not None:
            html = await self.page.content()
            for item in contains:
                if item not in html:
                    return False

        return True

    def _get_json_from_page_content(self, content):
        match = re.search('<pre.*?>(.*?)</pre>', content)
        return json.loads(match[1])
