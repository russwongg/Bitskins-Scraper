import requests
import pyotp
import pprint
import json
import statistics

SECRET = 'Enter secret'
MY_OTP = pyotp.TOTP(SECRET)
print(MY_OTP.now())
CODE = str(MY_OTP.now())

API_KEY = 'Enter API KEY'
API_ENDPOINT = 'https://bitskins.com/api/v1/'
APP_ID = '&app_id=730'
DISCOUNT_RATE = 0.78

class Skins:
    def __init__(self, hash_name):
        '''
        hash_name = name of the item
        '''
        self.hash_name = hash_name

    def __str__(self):
        print('Skins class. Methods are price_history, on_sale, buy, relist.')

    def price_history(self):
        '''Get historical transacted prices for the item.'''
        # gets up to 5 pages of recent sales data on Bitskins
        URL = API_ENDPOINT + 'get_sales_info' + API_KEY + '&code=' + str(CODE) +\
         "&market_hash_name=" + self.hash_name +'&page=1' + APP_ID

        historical_price_list = []
        r = requests.post(url = URL)
        print('Status code: ', r.status_code)
        # print('Post request below.')
        output = r.json()
        raw_price_list = output['data']['sales']
        # print(raw_price_list)

        for price in raw_price_list:
            historical_price_list.append(float(price['price']))
        price_list = [float(i) for i in historical_price_list]
        # print(price_list)
        mean = statistics.mean(historical_price_list)
        low = min(historical_price_list)
        high = max(historical_price_list)

        print(self.hash_name + ' lowest price is: ', str(low))
        print(self.hash_name + ' high price is: ', str(high))
        print(self.hash_name + ' average price is: ', str(mean))
        print(' ')

        # convert historical_price_list to float
        historical_price_list = [float(i) for i in historical_price_list]

        return historical_price_list

    def on_sale(self, per_page = 60, sort_by = 'price', order = 'asc'):
        '''Retieves a list of prices of all outstanding items on sale on Bitskins.
        This method returns a list.
        '''
        self.per_page = '&per_page=' + str(per_page)
        self.sort_by = '&sort_by=' + sort_by
        self.order = '&order=' + order

        listed_prices = []
        # URL to run request on
        URL = API_ENDPOINT + 'get_inventory_on_sale' + API_KEY + '&page=1' + APP_ID + self.sort_by + self.order \
        + '&market_hash_name=' + self.hash_name + '&code=' + CODE

        # execute request on URL
        r = requests.post(url = URL)
        print('Status code: ', r.status_code)
        # print('Post request below.')
        output = r.json()
        available_item_prices = output['data']['items']

        i = 0
        for item in available_item_prices:
            i += 1
            item_name = item['market_hash_name'] + ' ' + str(i)
            item_price = item['price']
            suggested_price = item['suggested_price']
            print(item_name + ' price is: ' + str(item_price))
            listed_prices.append(float(item['price']))
        print(self.hash_name)
        print('Total listings is: ' + str(i))
        print('Suggested price is ' + str(suggested_price))
        print('   ')

        listed_prices = [float(i) for i in listed_prices]

        return listed_prices

    def pattern_finder(self, pattern_list, per_page = 60, sort_by = 'price', order = 'asc'):
        self.per_page = '&per_page=' + str(per_page)
        self.sort_by = '&sort_by=' + sort_by
        self.order = '&order=' + order

        # execute request on URL
        page_list = [1, 2, 3, 4, 5, 6, 7]

        for page in range(1, 11):
            URL = API_ENDPOINT + 'get_inventory_on_sale' + API_KEY + '&page=' + str(page) + APP_ID + self.sort_by + self.order \
            + '&market_hash_name=' + self.hash_name + '&code=' + CODE

            r = requests.post(url = URL)
            print('Status code: ', r.status_code)
            # print('Post request below.')
            output = r.json()
            available_item = output['data']['items']

            for item in available_item:
                try:
                    paintseed = item['pattern_info']['paintseed']
                except:
                    # print('Paintseed not in list')
                    continue
                if paintseed in pattern_list:
                    print('Pattern is ' + str(paintseed))
                    print('Price is ' + str(item['price']))


    def lowest_price(self, list_of_prices):
        '''List of prices input is Skins.on_sale()'''
        lowest_price = min(list_of_prices)
        return lowest_price

    def derive_sell_price(self, list_of_prices):
        '''Resell at second lowest price - 1 cent'''
        sell_price = min(list_of_prices) - 0.01
        return sell_price

    def buy(self, price, quantity = 1):
        self.price = str(price)
        self.quantity = str(quantity)

        URL = API_ENDPOINT + 'create_buy_order' + API_KEY + '&code=' + CODE + \
        '&name=' +self.hash_name + '&price=' + self.price + '&quantity=' + self.quantity \
        + APP_ID

        try:
            r = requests.get(url = URL)
        except:
            print('Failed to create buy order.')

    def sell(self, pending_inventory_list, sell_price):
        '''First extract inventory. Parse through inventory to see if hash name
        matches, then extract item_ids and relist.
        inventory_list = Skins.inventory()
        '''
        item_id = ''
        for item in pending_inventory_list:
            if item['market_hash_name'] == self.hash_name:
                print(item['item_id'])
                item_id = item['item_id']

        resell_URL = API_ENDPOINT + 'relist_item' + API_KEY + '&code=' \
        + CODE + '&item_ids=' + item_id + '&prices=' + str(sell_price) + \
        APP_ID

        print(resell_URL)
        r = requests.get(url = resell_URL)
        if r.json()['status'] == 'success':
            print('Relist order created for ' + self.hash_name + ' at $' + str(sell_price))
        else:
            print('Failed to create sell order.')


    def pending_inventory(self):
        URL = API_ENDPOINT + 'get_my_inventory' + API_KEY +'&code=' + CODE \
        + '&page=1' + APP_ID

        r = requests.get(url = URL)
        bitskins_inventory = r.json()['data']['pending_withdrawal_from_bitskins']
        for item in bitskins_inventory['items']:
            print(item)
        inventory_list = bitskins_inventory['items']
        print(inventory_list)
        return inventory_list


class Account:
    def __init__(self):
        self.account_bal = 'get_account_balance'
        self.money_events = 'get_money_events'

    def __str__(self):
        return 'Hello there'

    def account_balance(self):
        '''Retrieve my account balance'''

        URL = API_ENDPOINT + self.account_bal + API_KEY + '&code=' + CODE
        r = requests.post(url = URL)
        print('Status code: ' + str(r.status_code))
        # print('Post request below.')
        output = r.json()
        print('Account available balance is: ' + str(output['data']['available_balance']))
        print('   ')

        return output['data']['available_balance']

    def active_orders(self):
        '''Get all active buy orders for my account'''

        URL = API_ENDPOINT + 'get_active_buy_orders' + API_KEY + '&code=' + CODE \
        + '&page=1' + APP_ID

        r = requests.get(url = URL)
        print('Active orders are:')
        print(r.json()['data']['orders'])

    def inventory(self):
        URL = API_ENDPOINT + 'get_my_inventory' + API_KEY +'&code=' + CODE \
        + '&page=1' + APP_ID

        r = requests.get(url = URL)
        bitskins_inventory = r.json()['data']['bitskins_inventory']
        print('Items in inventory are:')
        for item in bitskins_inventory['items']:
            print(item)

    def pending_inventory(self):
        URL = API_ENDPOINT + 'get_my_inventory' + API_KEY +'&code=' + CODE \
        + '&page=1' + APP_ID

        r = requests.get(url = URL)
        bitskins_inventory = r.json()['data']['pending_withdrawal_from_bitskins']
        print('Items in pending inventory are:')
        for item in bitskins_inventory['items']:
            print(item)
        inventory_list = bitskins_inventory['items']
        return inventory_list

# helper functions
def second_lowest(lst):
    length = len(lst)
    lst.sort()
    low2 = lst[1]
    return low2

def price_opportunity(historical_prices, available_prices):
    ''' Historical prices come from Skins.price_history.
    Available prices come from Skins.on_sale().
    Both are lists.
    Criteria is that the lowest price is below the historical low and at least
    90% below the next price.
    '''
    low_historical_px = min(historical_prices)

    available_prices.sort()
    low_available_prices = available_prices[0]
    low2_available_prices = available_prices[1]

    print('Lowest historical price is: ' + str(low_historical_px))
    print('Lowest available price is: ' + str(low_available_prices))
    print('Low2 available price is ' + str(low2_available_prices))

    # if low_available_prices < low_historical_px:
    #     print('OPPORTUNITY. Lowest available price is less than lowest historical price')
    if low_available_prices <= (DISCOUNT_RATE * low2_available_prices):
        print('OPPORTUNITY. Low1 is at least 15% lower than low2')
        return True
    else:
        print('No opportunity!')
        print('  ')
        return False

def bitskins_DB(weapon_type):
    '''Define weapon_type for the tyep of weapon you want to search. i.e. AK-47
    or M4A1-S'''
    # extract bitskins price db. get_market_data

    URL = API_ENDPOINT + 'get_price_data_for_items_on_sale' + API_KEY + '&code=' \
    + CODE + APP_ID

    weapon_list = []

    r = requests.post(url = URL)
    db_item_list = r.json()['data']['items']
    for item in db_item_list:
        if weapon_type in item['market_hash_name']:
            print(item['market_hash_name'])
            weapon_list.append(item['market_hash_name'])

    return weapon_list

def execute_buy(weapon_list, account):
    opportunity_list = []
    account_bal = float(account.account_balance())
    time = 0
    for weapon_name in weapon_list:
        skin = Skins(weapon_name)
        # testing to handle time out of OTP
        if time > 25:
            CODE = str(MY_TOP.now())
        low = skin.lowest_price(skin.on_sale())
        try:
            # if there is a price opportunity...
            if price_opportunity(skin.price_history(), skin.on_sale()) == True:
                # if price of opportunity is less than or equal to account bal
                if low <= account_bal and low > 0.5:
                    skin.buy(low)
                    print('Buy order created for ' + weapon_name + ' for $' + str(low))
                    account_bal -= low
                opportunity_list.append(weapon_name)
                print(opportunity_list)
        except:
            print('Error encountered. Try except continue.')
            continue
        time += 1

def execute_sell(pending_inventory_list):
    '''Pass account.pending_inventory() into pending_inventory_list'''
    for item in pending_inventory_list:
        pending_hash_name = item['market_hash_name']
        skin_to_relist = Skins(pending_hash_name)
        sell_price = skin_to_relist.derive_sell_price(skin_to_relist.on_sale())
        skin_to_relist.sell(pending_inventory_list, sell_price)

awp_wf = Skins('StatTrak™ AWP | Wildfire (Factory New)')
karam_tt = Skins('★ Karambit | Tiger Tooth (Factory New)')
awp_asi = Skins('StatTrak™ AWP | Asiimov (Field-Tested)') # bot USD 184
ak_fi = Skins('AK-47 | Fuel Injector (Factory New)') # bot USD 280
m9_tt = Skins('★ M9 Bayonet | Tiger Tooth (Factory New)')
usp_orion = Skins('StatTrak™ USP-S | Orion (Minimal Wear)')
ak_emp = Skins('AK-47 | Bloodsport (Minimal Wear)')
bnc = Skins('Five-SeveN | Berries And Cherries (Factory New)')
mm = Skins('USP-S | Monster Mashup (Factory New)')
ps = Skins('M4A1-S | Printstream (Factory New)')
jade = Skins('AUG | Carved Jade (Factory New)')
fade = Skins('MP7 | Fade (Factory New)')
dusk = Skins('Galil AR | Dusk Ruins (Factory New)')
heist = Skins('Desert Eagle | Night Heist (Factory New)')
stiletto_tt = Skins('★ Stiletto Knife | Tiger Tooth (Factory New)')

awp_wf.price_history()
awp_wf.on_sale()
karam_tt.price_history()
karam_tt.on_sale()
m9_tt.price_history()
m9_tt.on_sale()
stiletto_tt.price_history()
stiletto_tt.on_sale()
ak_emp.price_history()
ak_emp.on_sale()


items_list = ['AK-47', 'M4A4', 'Desert Eagle', 'AUG', 'AWP', 'FAMAS', 'Five-SeveN']
items_list2 = ['P250', 'P90', 'Galil AR', 'Glock-18','M4A1-S', 'MAC-10']
my_account = Account()
# execute_buy(bitskins_DB('M4A4'), my_account)
# for item in items_list2:
#     execute_buy(bitskins_DB(item), my_account)

# execute_buy(bitskins_DB('AWP'), my_account)
# my_account.pending_inventory()
# execute_sell(my_account.pending_inventory())
