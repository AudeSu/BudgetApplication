# BudgetApplication

## Bedoeling van de applicatie:

Gebruikers van de budget applicatie kunnen zich registreren en dan inloggen. Nadat de gebruiker ingelogd is ziet hij/zij eerst een overzicht van zijn/haar totale inkomens en uitgaven en zijn/haar totale uitgaven per category. Daarna krijg je een menu met alle keuzes dat de gebruiker kan maken. De gebruiker kan een inkomen/uitgave toevoegen, aanpassen of verwijderen. Als laatste kan de gebruiker ook zijn/haar volledige budget data in een CSV bestand krijgen.

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
- User(id (PK), username, email, password)
- Income(id (PK), user_id (FK), amount, description)
- Expense(id (PK), user_id (FK), amount, category, description)

De volledige database wordt zelf aangemaakt dit staat in het database.py bestand uitgeschreven, je hoeft dus zelf enkel maar de main.py te runnen en alles zou moeten werken.

## Hoe de applicatie te runnen:

Eerst cloned u de repositroy, daarna installeer je de packages uit het requirements.txt bestand en als laatst maakt u een eigen .env bestand. Nu zou u in staat moeten zijn om de applicatie te runnen. Let er altijd op dat je in de juiste map staat wanneer je een commando uitvoert

```git clone https://github.com/AudeSu/BudgetApplication.git```

```pip install -r requirements.txt```

Maak een eigen .env bestand in de terminal (```nano .env``` of ```code .env```) met volgende inhoud:
        
    DATABASE_URL=sqlite:///../data/budget.db
    SECRET_KEY=mysecretkey

```python main.py```

> Er zou al een testuser aanwezig moeten zijn met username: "testuser" en password: "testpassword"