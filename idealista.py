# -*- coding: utf-8 -*- 


import time
import datetime
import email.message as EmailMessage
import smtplib 

from qacode.core.bots.bot_base import BotBase
from qacode.core.webs.pages.page_base import PageBase
from qautils.files import settings


SETTINGS = settings(
    file_path="./",
    file_name="settings.json"
)

EMAIL_TEMPLATE = """
<html>
<head>
  <!-- Latest compiled and minified CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
  <!-- Optional theme -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
  <!-- JQuery -->
  <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
  <!-- Latest compiled and minified JavaScript -->
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
</head>
<body>
<h1>IDEALISTA Bot search</h1>
<table class="table table-striped table-bordered">
  <thead>
    <tr>
      <th>PRICE</th>
      <th>CONTACT</th>
      <th>DETAILS</th>
      <th>TITLE</th>
    </tr>
  </thead>
  <tbody>
    {}
  </tbody>
</table>
</body>
</html>
"""
EMAIL_TEMPLATE_ROW = """
    <tr>
      <td>{}</td>
      <td><a href="tel:+0034{}">{}</a></td>
      <td>{}</td>
      <td><a href="{}" target="_blank">{}</a></td>
    </tr>
"""

IDEALISTA = SETTINGS["apps"][0]
BY = IDEALISTA["data"]["by"]
USER = IDEALISTA["data"]["user"]
PASS = IDEALISTA["data"]["pass"]
EMAIL_SRC = IDEALISTA["data"]["email_src"]
EMAILS_DST = IDEALISTA["data"]["emails_dst"]

def main():
    bot = None
    try:
        curr_date = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        results = []
        # START
        bot = BotBase(**SETTINGS)
        for page_config in IDEALISTA["pages"]:
            page = PageBase(bot, **page_config)
            # flats found : .i
            # tems-container .item 
            flats = page.flat_containers.elements
            bot.log.info("Found flats : {}".format(len(flats)))
            for flat_container in flats:
                # title
                _title = flat_container.find_element(BY, ".item-info-container>a")
                bot.navigation.execute_js("arguments[0].scrollIntoView();", _title)
                title_href = _title.get_attribute("href")
                title = _title.text
                # price
                price = flat_container.find_element(BY, ".item-info-container .item-price.h2-simulated").text
                # details
                details = ''
                detail_elements = flat_container.find_elements(BY, ".item-info-container .item-detail")
                for detail in detail_elements:
                    details += detail.text
                # contact
                try:
                    contact = flat_container.find_element(BY, ".item-toolbar-contact a span").text
                except:
                    contact = "FAIL at obtain CONTACT for this flat"
                # Parse
                result = {
                    "price": price,
                    "details": details,
                    "contact_href": contact.replace(" ", ""),
                    "contact": contact,
                    "title_href": title_href,
                    "title": title
                }
                results.append(result)
            # END
            if len(flats) <= 0:
                page.error_ddos.reload()
                if page.error_ddos.element is None:
                    bot.log.warning("Not going to send an email for 0 flats founds")
                raise InterruptedError(1, "IDEALISTA think you are performing DDos attack")
            email_rows_str = ''
            bot.log.info("EMAIL: building...")
            for result in results:
                email_row = EMAIL_TEMPLATE_ROW.format(
                    result['price'],
                    result['contact_href'],
                    result['contact'],
                    result['details'],
                    result['title_href'],
                    result['title']
                )
                email_rows_str += (email_row)
            bot.log.info("EMAIL: adding HTML content...")
            for email_dst in EMAILS_DST:
                bot.log.debug("Building email to='{}'".format(email_dst))
                email_html = EMAIL_TEMPLATE.format(email_rows_str)
                email = EmailMessage.Message()
                email ['Subject'] = "IDEALISTA | Flat search - {}".format(curr_date)
                email['From'] = EMAIL_SRC
                email['To'] = email_dst
                email.add_header('Content-Type','text/html')
                email.set_payload(email_html)
                bot.log.info("EMAIL: added HTML content...")
                bot.log.info("GMAIL: connecting...")
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.login(USER, PASS)
                bot.log.info("GMAIL: connected!")
                bot.log.info("GMAIL: send an email")
                server.sendmail(email['From'], email['To'], email.as_string().encode())
                bot.log.info("GMAIL: email sent!")
                server.close()
            # END, next iteration
            bot.log.info("Hardcoded waiting to avoid idealista think it's DDos Error")
            bot.log.info("Waiting 15 seconds before continue")
            time.sleep(15)
    except Exception as err:
        bot.log.error("ERROR: {}".format(err))
    finally:
        bot.log.info("BOT: closing...")
        bot.close()
        bot.log.info("BOT: closed!")

# STARTs
main()
