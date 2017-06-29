import requests
import time
import sys
import getopt
from datetime import datetime

def parsing_arguments(argv):

    try:
        opts, args = getopt.getopt(argv,"hvbt", ["help", "version", "balance", "transaction"])
    except getopt.GetoptError:
        print 'input errors'
        sys.exit(2)

    help_string = '\nthis is getting the balance of your wallets'

    balance = False
    transaction = False

    for opt, arg in opts:
        if opt == '-h':
            print help_string
            sys.exit()
        if opt == '-v':
            print 'chain.so version ' + version + ' \nCopyright Maerco.it'
            sys.exit()
        elif opt in ("-b", "--balance"):
            balance = True
        elif opt in ("-t", "--transaction"):
            transaction = True

    return balance, transaction

def coin_status(coinname):

    response = requests.get('https://chain.so/api/v2/get_info/' + coinname)

    if response.status_code == 200:
        # everything went swimmingly
        # parse the response as JSON
        content = response.json()

        print "Name:", content['data']['name']
        print "Total Blocks:", content['data']['blocks']

def wallet_balance(wallet_address, coinname):

    for i in range(0, 20):
        try:
            response = requests.get("https://chain.so/api/v2/get_address_balance/" + coinname + "/" + wallet_address)

            if response.status_code == 200:
                # everything went swimmingly
                # parse the response as JSON
                content = response.json()

                work_balance = float(content['data']['confirmed_balance'])
                work_unconfirmed_balance = float(content['data']['unconfirmed_balance'])

                print "Coin: " + coinname + " ==> Address: " + wallet_address + " ==> " + str(work_balance)

                return work_balance

            else:
                #print i, response.status_code
                time.sleep(i)
                raise ValueError('connection error')
        except:
            continue

def wallet_transactions(wallet_address, coinname):

    for i in range(0, 20):
        try:
            response = requests.get(
                "https://chain.so/api/v2/address/" + coinname + "/" + wallet_address)

            if response.status_code == 200:
                # everything went swimmingly
                # parse the response as JSON
                content = response.json()

            else:
                # print i, response.status_code
                sys.stdout.write('.')
                time.sleep(i)
                raise ValueError('connection error')
        except:
            continue

    print "\n"

    out_file = open(coinname + "_" + wallet_address + ".txt", "w")

    for transaction in content['data']['txs']:
        transactions_str = transaction['txid'] + " -- " + datetime.fromtimestamp(int(transaction['time'])).strftime('%Y-%m-%d %H:%M:%S') + " -- " + transaction['incoming']['value']
        print transactions_str
        out_file.write(transactions_str + "\n")

    out_file.close()



                # print response.status_code



def getprice(coinname, fiat):

    for i in range(0, 20):
        try:

            response = requests.get("https://chain.so/api/v2/get_price/" + coinname + "/" + fiat)

            if response.status_code == 200:
                # everything went swimmingly
                # parse the response as JSON
                content = response.json()

                price = float(content['data']['prices'][0]['price'])
                # work_unconfirmed_balance = float(content['data']['unconfirmed_balance'])

                return price

            else:
                #print i, response.status_code
                time.sleep(i)
                raise ValueError('connection error')
        except:
            continue


def run_function_on_list_of_addresses(function_name):

    global coin_list

    thismodule = sys.modules[__name__]

    lines = [line.rstrip('\n') for line in open('wallets.txt')]

    for row in lines:

        if (row[:1] == '#'):
            continue

        if (row[:1] == ''):
            continue

        values = row.split(';')

        method_to_call = getattr(thismodule, function_name)

        if function_name == 'wallet_balance':

            coin_amount[values[0]] += method_to_call(values[1], values[0])

        else:

            method_to_call(values[1], values[0])






balance, transaction = parsing_arguments(sys.argv[1:])

coin_list = []
coin_amount = {}
eur_price = {}
usd_price = {}
total_amount = 0


lines = [line.rstrip('\n') for line in open('wallets.txt')]

for row in lines:
    if (row[:1] == '#'):
        continue

    if (row[:1] == ''):
        continue

    values = row.split(';')

    if values[0] not in coin_list:
        coin_list.append(values[0])
        coin_amount[values[0]] = 0



# for coin in coin_list:
#     eur_price[coin]  = getprice(coin, 'EUR')

if balance == True:
    run_function_on_list_of_addresses('wallet_balance')
else:
    lines = [line.rstrip('\n') for line in open('wallet_balances.txt')]
    for row in lines:
        values = row.split(';')
        coin_amount[values[0]] = float(values[1])

for coin in coin_list:
    eur_price[coin]  = getprice(coin, 'EUR')
    usd_price[coin]  = getprice(coin, 'USD')
    print coin + " ==> " + str(coin_amount[coin]) + " ==> (EUR: " + str(coin_amount[coin] * eur_price[coin]) + " / UDS: " + str(coin_amount[coin] * usd_price[coin]) + ")"
    total_amount +=  coin_amount[coin] * eur_price[coin]

print "Total Amount = " + str(total_amount)

if balance == True:
    with open("wallet_balances.txt", "w") as f:
        for key, value in coin_amount.iteritems():
            f.write(str(key) + ";" + str(value) + "\n")

if transaction == True:
    run_function_on_list_of_addresses('wallet_transactions')