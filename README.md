# Wallet Manager

This python script will collect the balance of multiple crypto-currencies.
It's based on call on chain.so APIs.

## configuration

you need to install python module request 

pip install requests

## Usage

wallet.txt need to be filled with all the wallet address you have each row need to contain:

<COIN_TYPE>;<address>

e.g.

DOGE;DRNDceWUjFbT1vS1UBmPTnu2Eq5rWhexrE
BTC;1KusD3dRJXuaBbHaHhoivdM8nUNKXcPdLt
LTC;LZ9KDeZw1ZBF1DTmrMtvmguRP8bA68r75V
DASH;XtsntGmmexnPkxo42HjFGBWJe7ioGtcb4C

Allowed currency are the one currently allowed by Chain.so (DOGE, BTC, LTC, DASH)

## Commands

*python walletmanager.py --balance*

this command will cycle all your address, will get the balance of them 
it will print on screen each balance and at the end, 
it will sum all the balance for the same coin and will give you the amount in EUR/USD:

additionally it will store in the file wallet_balances.txt 
all the amount of coin you have for each coin type.

*python walletmanager.py --transaction*

this command will cycle all your address, will get all the transaction for each of them
and will generate a file called <coin_type>_<address>.txt containing all the transaction

*python walletmanager.py*

this command will cycle coins present in your wallet_balances.txt and will give you the current amount of EUR/USD.
