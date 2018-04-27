# !/usr/bin/env python3
# -*- coding: utf-8 -*-
MAX_BLOCK_SIZE = 100
MAIN_CHAIN_INDEX = 0
COINBASE_MATURITY = 6
MONEY_PER_COIN = int(100e6)
TOTAL_COINS = 21000000
MAX_MONEY = MONEY_PER_COIN * TOTAL_COINS
MINE_TIME_BETWEEN_BLOCKS = 60
DIFFICULTY_PERIOD = 60 * 60 * 10
DIFFICULTY_PERIOD_IN_BLOCKS = DIFFICULTY_PERIOD // MINE_TIME_BETWEEN_BLOCKS
INITIAL_DIFFICULTY = 24
INITIAL_COIN_SUBSIDY = 50
HALF_SUBSIDY_AFTER_BLOCK_NUM = 210000
MAX_HALF_RATIO = 64
DEFAULT_WALLET_PATH = 'wallet.dat'
