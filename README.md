## Webskrapa Myrornas Hemsida

### 1. Installera nödvändiga bibliotek
Installera `bs4`, `requests`, och `psycopg2-binary` med pip (se till att Python är installerat).

Kör följande kommando i terminalen:
```bash
pip3 install bs4 requests psycopg2-binary
```

### 2. Skrapa hemsidan Myrornas

För att skrapa data från Myrornas hemsida, kör Python-filen `main.py` (i src mappen):
```bash
python3 main.py
```
Om det inte funkar beror det högst sannolikt på att servern vi använder är tillfälligt stängd.

Se till att alla beroenden är installerade innan du kör filen.
För att se all data, följ kommande instruktioner.


## Installera PostgreSQL och Få Åtkomst till Databasen via Terminalen

### 1. Installera PostgreSQL om du inte har det (via terminalen)

#### Linux (Debian/Ubuntu-baserade system):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### macOS (via Homebrew):
```bash
brew update
brew install postgresql
```
Se till att Homebrew är installerat först.

#### Windows:
Det rekommenderas att Windows-användare använder Windows Subsystem for Linux (WSL) (laddas ner i windows store) eller en Linux-liknande miljö för att installera och köra PostgreSQL. Öppna WSL och följ därefter instruktionerna för linux system.

### 2. Få åtkomst till PostgreSQL-databasen via terminalen

För att komma in i databasen skriver du följande i terminalen:
```bash
psql -U admin -d products -h "83.250.197.163"
```

Ange sedan lösenordet "Projekt2025".

Om det inte funkar beror det högst sannolikt på att servern vi använder är tillfälligt stängd.

När du väl är inne i databasen kan du se all data genom att skriva följande:
```sql
SELECT * FROM products;
```


