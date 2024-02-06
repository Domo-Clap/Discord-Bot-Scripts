import asyncio
import os
import discord
import requests
import json
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from keep_alive import keep_alive

intents = discord.Intents().all()
client = discord.Client(intents=intents)

TOKEN = os.environ['Token']

old_chapter_list_length = 1109


def checkForNewChapters():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("disable-infobars")
  chrome_options.add_argument("--disable-extensions")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--start-maximized")

  driver = webdriver.Chrome(options=chrome_options)

  driver.get("https://tcb-scans.com/mangas/5/one-piece")

  main_column = driver.find_element(By.CSS_SELECTOR, "div.col-span-2")

  chapter_links = main_column.find_elements(By.TAG_NAME, 'a')

  chapter_links_text = [link.text for link in chapter_links]

  current_chapter_list_length = len(chapter_links_text)

  global old_chapter_list_length

  if (current_chapter_list_length > old_chapter_list_length):
    print('New Chapter of One Piece is HERE!!!!!')

    old_chapter_list_length = current_chapter_list_length

    link_new_chapter = chapter_links[0].get_attribute("href")

    driver.quit()

    return link_new_chapter

  else:
    print("No new Chapters of One Piece yet")

    driver.quit()

    return False


async def background_task():
  channel_id = 0 # Replace with your channel ID
  channel = client.get_channel(channel_id)

  while True:

    clicked_link = checkForNewChapters()

    if clicked_link:

      await channel.send(
          f"New Chapter of One Piece is HERE!!!!!\nHere is the link: {clicked_link}"
      )
    else:
      await channel.send("No new Chapters of One Piece yet")

    await asyncio.sleep(120)


#first event :logging in
@client.event
async def on_ready():
  print("successful login as {0.user}".format(client))
  client.loop.create_task(background_task())


keep_alive()

#getting the secret token
client.run(TOKEN)