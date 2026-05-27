# Persistering og databasedesign

MVP’en anvender et repository pattern til at adskille domænemodellen fra den konkrete databaseimplementering. Det betyder, at domænelaget ikke er afhængigt af, om data gemmes midlertidigt i hukommelsen eller permanent i en PostgreSQL-database.

## Valg af persistering

Løsningen understøtter to former for datalagring:

- Ved lokale tests anvendes in-memory repositories.
- Ved Docker-kørsel anvendes PostgreSQL, når `USE_DATABASE=true`.

Denne opdeling gør det muligt at holde testmiljøet simpelt og hurtigt, samtidig med at MVP’en demonstrerer et reelt persisteringslag i den tekniske løsning.

## Databasetabeller

| Tabel | Domænebegreb | Formål |
|---|---|---|
| `chargers` | `Charger` aggregate | Gemmer ladestanderens ID, lokation og aktuelle status |
| `connectors` | `Connector` entity | Gemmer status for de enkelte connectors på en ladestander |
| `charging_sessions` | `ChargingSession` entity | Gemmer startede og afsluttede ladesessioner |
| `telemetry_readings` | `TelemetryReading` value-object-lignende data | Gemmer målinger fra ladestandere, fx effekt, spænding, strøm og fejlkoder |

## Kobling til Domain Driven Design

Databasemodellen er udledt af de centrale begreber i domænemodellen. `Charger` fungerer som et aggregate, der indeholder én eller flere `Connector` entities. `ChargingSession` repræsenterer en konkret ladesession, mens `TelemetryReading` repræsenterer måledata fra ladestanderen.

API’et arbejder ikke direkte mod databasen, men gennem repository interfaces. Det betyder, at domæne- og applikationslaget holdes uafhængigt af infrastrukturen. Denne opdeling understøtter Domain Driven Design, fordi forretningslogikken kan udvikles og testes uden at være bundet til en bestemt database.

## Seed-data

Scriptet `services/api/scripts/seed_database.py` opretter realistisk demo-data for ladestandere, telemetry readings og ladesessioner. Disse data kan bruges til at teste API’et, demonstrere analytics endpoints og senere danne grundlag for BI/Power BI.

## Sammenhæng i løsningen

Den tekniske sammenhæng kan beskrives sådan:

```text
DDD-domænemodel
→ Repository interfaces
→ SQL repository implementation
→ PostgreSQL database
→ Analytics endpoints
→ BI/Power BI