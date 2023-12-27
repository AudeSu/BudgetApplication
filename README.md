# BudgetApplication

## Bedoeling van de applicatie:

Gebruikers van de budget applicatie kunnen zich registreren en dan inloggen. Nadat de gebruiker ingelogd is ziet hij eerst een overzicht van zijn totale inkomens en uitgaven en zijn totale uitgaven per category. Daarna krijg je een menu met alle keuzes dat de gebruiker kan maken. De gebruiker kan een inkomen/uitgave toevoegen, aanpassen of verwijderen. Als laatste kan de gebruiker ook zijn volledige data in een CSV bestand krijgen.

## Mappenstructuur:

- **app:** Deze package bevat alle python bestanden
    - **__init__.py:** zodat de app map een package zou zijn
    - **application.py:** hier staan alle methoden die opgeroepen worden in mijn menu.py
    - **database.py:** hier wordt de database aangemaakt en wordt er een testuser aangemaakt zodat er al een user met data aanwezig zou zijn
    - **main.py:** hier worden enkel de nodige methoden opgevraagd
    - **menu.py:** er staan drie methoden in om de drie verschillende menu's af te drukken
    - **user.py:** de klasse User wordt hier geimplementeerd met twee methoden om te registreren en in te loggen
- **data:** hier komt de database en het csv bestand terecht als deze aangemaakt worden
- **.env:** omdat ik de wachtwoorden wou versleutelen heb ik voor een .env bestand gezorgd met omgevingsvariabelen
- **.gitignore:** passende gitignore voor een python project
- **requirements.txt:** da packages die ik geinstalleerd heb

## Database:

De database heeft drie tabellen: users, incomes en expenses
- User(id, username, email, password)
- Income(id, user_id, amount, description)
- Expense(id, user_id, amount, category, description)

## Hoe de applicatie te runnen:

Nadat u de repository heeft gecloned installeer je de requirements en dan zou je de applicatie kunnen runnen.
> - git clone https://github.com/AudeSu/BudgetApplication.git
> - pip install -r requirements.txt
> - python main.py