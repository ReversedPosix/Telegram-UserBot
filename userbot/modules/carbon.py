import os
from time import sleep
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, LANG, CHROME_DRIVER, GOOGLE_CHROME_BIN
from telethon import events
from selenium import webdriver
from urllib.parse import quote_plus
from userbot.events import register
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

@register(outgoing=True, pattern="^.carbonlang")
async def setlang(prog):
    if not prog.text[0].isalpha() and prog.text[0] not in ("/", "#", "@", "!"):
        global LANG
        LANG = prog.text.split()[1]
        await prog.edit(f"language set to {LANG}")

@register(outgoing=True, pattern="^.carbon")
async def carbon_api(e):
 if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
   """ A Wrapper for carbon.now.sh """
   await e.edit("Processing...")
   CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
   global LANG
   textx = await e.get_reply_message()
   pcode = e.text
   if pcode[8:]:
         pcode = str(pcode[8:])
   elif textx:
         pcode = str(textx.message) # Importing message to module
   code = quote_plus(pcode) # Converting to urlencoded 
   url = CARBON.format(code=code, lang=LANG)
   chrome_options = Options()
   chrome_options.add_argument("--headless")
   chrome_options.binary_location = GOOGLE_CHROME_BIN
   chrome_options.add_argument("--window-size=1920x1080")
   chrome_options.add_argument("--disable-dev-shm-usage")
   chrome_options.add_argument("--no-sandbox")
   chrome_options.add_argument('--disable-gpu')
   prefs = {'download.default_directory' : './'}
   chrome_options.add_experimental_option('prefs', prefs)
   await e.edit("Processing 30%")

   driver = webdriver.Chrome(executable_path=CHROME_DRIVER, options=chrome_options)
   driver.get(url)
   download_path = './'
   driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
   params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_path}}
   command_result = driver.execute("send_command", params)

   driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
   sleep(5)  # this might take a bit.
   await e.edit("Processing 50%")
   driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
   sleep(5) #Waiting for downloading
   
   await e.edit("Processing 90%")
   file = './carbon.png'
   await e.edit("Done!!")
   await e.client.send_file(
         e.chat_id,
         file,
         caption="Made using [Carbon](https://carbon.now.sh/about/), a project by [Dawn Labs](https://dawnlabs.io/)",
         force_document=True,
         reply_to=e.message.reply_to_msg_id,
         )
 
   os.remove('./carbon.png')
   # Removing carbon.png after uploading
   await e.delete() # Deleting msg 

CMD_HELP.update({
      "carbon":".carbon <text/reply>\nBeautify your code using carbon.now.sh\n\
      \n.carbonlang <text>\nSet language for you carbon module\n"
})
