# PBJ

**Category:** Misc **Difficulty:** 7/10 **Author:** NoobMaster

# Description
The bot does all the trading, while I sit back and relax.

# Distribution

* Chall.sol

# Solution

The code below is a basic ETH to FlagCoin where you provide some Ether and it gives the number of flagCoins you can buy with that much ether (rounded down). The extra ether is still added to the reserve. The problem here is not in the code itself, but the fact that there is a dummy "bot" doing heavy transactions at specific intervals, and also there is a memory pool where transactions stay for 10 seconds. Since you can view the mempool and the transactions happening, you can create a sandwich attack: wait for the bot to buy, as soon as you see the buy transaction in the mempool, send a buy transaction with higher gasPrice, allowing your transaction to happen first. Then, send a sell transaction afterwards. When you buy some, then the bot buys a heavy amount, the price goes up, allowing you to sell yours to gain profit. Doing this multiple times allows you to earn more money (about 4 ether per attack).

Solve at: challenge/solve.py
