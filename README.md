# QA Idealista Bot

Just another comparator scrapper based on Selenium to avoid website restrictions and report with filter by email

### Prerrequisites

- 1. Create new virtual environment to ensure it's working : ```mkvirtualenv -p $(which python3) househunter```
- 2. Install dependencies : ```pip install qacode```
- 3. Copy and configure your settings : ```cp settings.example.json settings.json``` *(you will need and SMTP server or Gmail account ready to send emails)*
- 4. Execute bot : ```python idealista.py```

### Start

* 1. Modify GMAIL auth and search url at **settings.json** to ensure your bot is working
* 2. Modify **idealista.py** search url
* 3. Launch **bot** : ```python idealista.py```
