# bitskins_scraper
Web scraper to pull various data from Bitskins.com

**About this project**

This project aims to leverage on the API created by Bitskins.com to extract historical price data, current inventory, and relevant account information from the website's database. 

Bitskins.com is an online marketplace where millions of players from popular online games like Counter-Strike: Global Offensive ("CSGO") and Dota 2 can go to sell their virtual items for real money. Traditionally, players have been limited to selling their items on the Steam marketplace, where proceeds from sales are credited directly into the player's account. As such, players who want to "cash out" their virtual items often turn to third-party marketplaces to sell their items in return for real world cash. 

A key feature of the Steam marketplace is that Steam takes a 15% "tax" on all items being sold. For instance, if a player sells an item for $100 on the steam marketplace, he would only receive $85 in account credits. As a result of this tax, buyers of virtual items on third-party marketplaces will typically demand that sellers list their items at least 15% less than the current market price on the official Steam market. 

The benefit of this is two-fold. First, sellers get to cash out their items, and second, buyers get to purchase their items at a cheaper price. Because both parties benefit from this transaction, third-party marketplaces experience large transaction volumes with a great number of buyers and sellers trading each day. 

**Objective of this project**

Ultimately, the objective of this project is to create a program that allows the user to run an arbitrage strategy for liquid virtual CSGO items. Currently, the unrefined model screens a list of item categories, and uses a set of criteria to execute buy and sell orders.

If users are not interested in such practice, they can simply use the program to run price checks, which returns a list of items on sale and their prices, account balances, etc. 

**Notes**

This program is a practice project for object-oriented programming in Python as well as practice for web scraping using APIs.
