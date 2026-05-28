# Persistering og databasedesign

Dette dokument beskriver MVP’ens persisteringslag og koblingen mellem domænemodellen og databasen.

MVP’en anvender repository pattern til at adskille domænemodellen fra den konkrete databaseimplementering. Det betyder, at domænelaget ikke er afhængigt af, om data gemmes midlertidigt i hukommelsen eller permanent i en PostgreSQL-database.

---

## Valg af persistering

Løsningen understøtter to former for datalagring:

| Miljø | Persistering | Formål |
|---|---|---|
| Tests | In-memory repositories | Hurtige og simple tests uden database |
| Docker/local demo | PostgreSQL | Realistisk persisteringslag til MVP-demo |

Ved Docker-kørsel anvendes PostgreSQL, når:

```env
USE_DATABASE=true
```

Database connection sættes med:

```env
DATABASE_URL=postgresql+psycopg://voltedge:voltedge@db:5432/voltedge
```

---

## Databasetabeller

| Tabel | Domænebegreb | Formål |
|---|---|---|
| `chargers` | `Charger` aggregate | Gemmer ladestanderens ID, lokation og aktuelle status |
| `connectors` | `Connector` entity | Gemmer status for de enkelte connectors på en ladestander |
| `charging_sessions` | `ChargingSession` entity | Gemmer startede og afsluttede ladesessioner |
| `telemetry_readings` | `TelemetryReading` value-object-lignende data | Gemmer målinger fra ladestandere, fx effekt, spænding, strøm og fejlkoder |

---

## Kobling til Domain Driven Design

Databasemodellen er udledt af de centrale begreber i domænemodellen.

I MVP’en er de vigtigste begreber:

- `Charger`
- `Connector`
- `TelemetryReading`
- `ChargingSession`
- `AnalyticsService`

`Charger` fungerer som et aggregate, der indeholder én eller flere `Connector` entities.

`ChargingSession` repræsenterer en konkret ladesession.

`TelemetryReading` repræsenterer måledata fra en ladestander på et bestemt tidspunkt.

`AnalyticsService` anvender data fra repositories til at beregne nøgletal og indsigter.

---

## Repository pattern

API’et arbejder ikke direkte mod databasen.

I stedet går dataflowet gennem repositories:

```text
API endpoint
        |
        v
Application use case
        |
        v
Repository interface
        |
        v
Repository implementation
        |
        v
Database / memory
```

Denne opdeling understøtter Domain Driven Design, fordi forretningslogikken kan udvikles og testes uden at være bundet til en bestemt database.

---

## Seed-data

Scriptet til seed-data ligger her:

```text
services/api/scripts/seed_database.py
```

Scriptet opretter realistisk demo-data for:

- ladestandere
- connectors
- telemetry readings
- ladesessioner

Kør scriptet med:

```bash
docker compose exec api python scripts/seed_database.py
```

---

## Sammenhæng i løsningen

Den tekniske sammenhæng kan beskrives sådan:

```text
DDD-domænemodel
→ Repository interfaces
→ SQL repository implementation
→ PostgreSQL database
→ Analytics endpoints
→ BI/Power BI
```

---

## Afgrænsning

MVP’en bruger ikke database migrations.

I en produktionsklar løsning bør der tilføjes migrationsværktøj, fx Alembic, så ændringer i databasemodellen kan versioneres og rulles sikkert ud.