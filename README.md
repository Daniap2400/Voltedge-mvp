# VoltEdge MVP – Smart EV Charging Infrastructure

Dette repository indeholder vores tekniske MVP til eksamensopgaven på 6. semester i Økonomi og IT.

Projektet tager udgangspunkt i casevirksomheden VoltEdge Mobility A/S, som arbejder med digitale løsninger til styring og overvågning af ladeinfrastruktur. I MVP’en har vi valgt at fokusere på en mindre, men central del af platformen: håndtering af ladestandere, ladesessioner, telemetri og analytics.

Målet har ikke været at bygge hele VoltEdges fremtidige platform færdig. I stedet viser MVP’en, hvordan nogle af de vigtigste dele kan hænge sammen teknisk gennem API, database, Docker, analytics, machine learning, Power BI og CI/CD.

---

## Hvad løsningen fokuserer på

I rapporten arbejder vi især med VoltEdges udfordringer omkring skalering, fragmenteret data og behovet for mere datadrevet drift.

Derfor fokuserer MVP’en på to områder:

- Charging Context
- Analytics Context

Charging Context dækker den del af løsningen, hvor ladestandere, connectors, telemetri og ladesessioner håndteres.

Analytics Context dækker den del, hvor data bruges videre til nøgletal, fejlrate, energiforbrug, simple forecasts og anomalier.

Det vigtigste i løsningen er, at data ikke kun bliver modtaget og gemt, men også bliver brugt videre til analyse og visualisering.

---

## Hvad MVP’en indeholder

MVP’en indeholder:

- FastAPI-baseret API
- Docker Compose setup med API og PostgreSQL
- Domain models for chargers, connectors, telemetry og charging sessions
- Repository pattern og persistence layer
- AnalyticsService som domain service
- Machine learning notebook til predictive maintenance
- Power BI dashboard som separat BI-løsning
- GitHub Actions til CI/CD
- Dokumentation for logging, monitoring, fejlhåndtering og rollback

---

## Afgrænsning

MVP’en er et proof-of-concept og ikke en produktionsklar løsning.

Vi har valgt at implementere en afgrænset del af arkitekturen, så løsningen stadig er realistisk inden for projektets scope.

Det betyder, at følgende ikke er fuldt implementeret:

- rigtig OCPP-kommunikation
- billing og settlement
- partnerintegrationer
- authentication og authorization
- realtime integration mellem API og Power BI
- ekstern monitoring
- produktionsklar ML-model

De dele er i stedet beskrevet i rapporten som videreudvikling og som en del af den større arkitektur.

---

## Overordnet arkitektur

```text
EV Charger / Demo Client
        |
        v
FastAPI API
        |
        v
Application Use Cases
        |
        v
Domain Layer
- Charger
- Connector
- TelemetryReading
- ChargingSession
- AnalyticsService
        |
        v
Repository Pattern
        |
        v
PostgreSQL / In-memory repositories
        |
        v
Analytics endpoints
        |
        v
ML notebook + Power BI dashboard
```

---

## Teknologier

| Område | Teknologi |
|---|---|
| API | FastAPI |
| Sprog | Python |
| Database | PostgreSQL |
| Container | Docker og Docker Compose |
| Test | Pytest |
| CI/CD | GitHub Actions |
| Analytics | Domain service i Python |
| Machine Learning | Jupyter Notebook, scikit-learn, pandas |
| Business Intelligence | Power BI |
| Dokumentation | Markdown |

---

## Projektstruktur

```text
.
├── analytics/
│   ├── bi/
│   │   ├── README.md
│   │   └── Voltedge Bi rapport.pbix
│   ├── ml/
│   │   ├── generate_sample_data.py
│   │   ├── predictive_maintenance.ipynb
│   │   └── requirements.txt
│   └── notebooks/
│       └── README.md
├── docs/
│   ├── architecture/
│   │   ├── README.md
│   │   ├── ci-cd.md
│   │   ├── domain-model.md
│   │   ├── operations.md
│   │   └── persistence.md
│   ├── report-link/
│   │   └── README.md
│   └── demo-guide.md
├── ops/
│   ├── logging.md
│   ├── monitoring.md
│   └── rollback.md
├── services/
│   └── api/
│       ├── app/
│       ├── scripts/
│       ├── tests/
│       ├── Dockerfile
│       ├── pytest.ini
│       └── requirements.txt
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Sådan køres projektet

Kør dette fra projektets rodmappe:

```bash
docker compose up --build
```

Når containerne kører, kan API’et åbnes her:

```text
http://localhost:8000/docs
```

Health check kan åbnes her:

```text
http://localhost:8000/health
```

---

## Seed database

Når Docker Compose kører, kan databasen seedes med demo-data:

```bash
docker compose exec api python scripts/seed_database.py
```

Seed-scriptet opretter demo-data for:

- chargers
- connectors
- telemetry readings
- charging sessions

De data kan bruges til API-demo og analytics endpoints.

---

## Kør tests

Kør tests lokalt fra API-mappen:

```bash
cd services/api
pytest
```

Forventet resultat:

```text
20 passed
```

---

## Centrale API endpoints

| Endpoint | Metode | Formål |
|---|---:|---|
| `/health` | GET | Health check |
| `/api/v1/telemetry` | POST | Registrerer telemetry for en charger |
| `/api/v1/sessions/start` | POST | Starter en charging session |
| `/api/v1/sessions/{session_id}/end` | POST | Afslutter en charging session |
| `/api/v1/sessions` | GET | Viser charging sessions |
| `/api/v1/chargers/{charger_id}/status` | GET | Viser status for en charger |
| `/api/v1/analytics/summary` | GET | Viser samlet analytics summary |
| `/api/v1/analytics/chargers/{charger_id}` | GET | Viser analytics for en specifik charger |

---

## Eksempel: registrer telemetry

Endpoint:

```text
POST /api/v1/telemetry
```

Body:

```json
{
  "charger_id": "charger-1",
  "connector_id": "connector-1",
  "power_kw": 11.0,
  "voltage": 230.0,
  "current_amp": 16.0,
  "error_code": null
}
```

---

## Eksempel: start charging session

Endpoint:

```text
POST /api/v1/sessions/start
```

Body:

```json
{
  "charger_id": "charger-1",
  "connector_id": "connector-1",
  "user_id": "user-1",
  "contract_id": "contract-1"
}
```

---

## Eksempel: afslut charging session

Endpoint:

```text
POST /api/v1/sessions/{session_id}/end
```

Body:

```json
{
  "energy_delivered_kwh": 22.5
}
```

---

## Analytics som domain service

Analytics-delen ligger i:

```text
services/api/app/domain/analytics_service.py
```

Her har vi samlet analysefunktionalitet i en domain service i stedet for at placere beregningerne direkte i API-laget.

AnalyticsService beregner blandt andet:

- antal ladestandere
- antal ladesessioner
- afsluttede sessioner
- samlet energiforbrug
- gennemsnitlig sessionstid
- udnyttelsesgrad
- fejlrate
- forventet efterspørgsel
- energianomalier

Det viser, hvordan operationelle data kan bruges videre til indsigt og ikke kun til almindelig lagring.

---

## Machine Learning

Machine learning-delen ligger her:

```text
analytics/ml/predictive_maintenance.ipynb
```

Notebooken arbejder med predictive maintenance baseret på syntetiske operationsdata.

Formålet er at vise, hvordan data om fejl, oppetid, sessioner og energiforbrug kan bruges til at vurdere, hvilke ladestandere der har forhøjet risiko for vedligeholdelse.

ML-delen skal ikke forstås som en færdig produktionsmodel, men som et eksempel på, hvordan VoltEdge kunne arbejde videre med predictive analytics.

---

## Business Intelligence

Power BI-rapporten ligger her:

```text
analytics/bi/Voltedge Bi rapport.pbix
```

Rapporten viser blandt andet:

- total chargers
- total sessions
- total energy
- average uptime
- total faults
- faults by location
- faults by charger model
- maintenance predictions
- energiforbrug over tid
- detaljeret charger-tabel

I MVP’en er Power BI-rapporten baseret på flade CSV-filer. Det er valgt for at holde løsningen enkel og demonstrere sammenhængen mellem data, ML og BI uden at bygge en fuld data platform.

I en mere færdig løsning ville data typisk gå gennem et ETL/ELT-lag, fx Microsoft Fabric og Lakehouse, før det blev brugt i Power BI.

---

## CI/CD

Projektet bruger GitHub Actions.

Workflowet ligger her:

```text
.github/workflows/ci.yml
```

Pipeline kører:

1. Checkout af repository
2. Installation af Python
3. Installation af dependencies
4. Pytest
5. Docker build

Det gør, at ændringer automatisk bliver valideret, før de merges eller afleveres.

---

## Drift og operations

Driftsdokumentation ligger her:

```text
ops/
docs/architecture/operations.md
```

MVP’en forholder sig til:

- logging
- monitoring
- health checks
- fejlhåndtering
- rollback
- CI/CD som kvalitetssikring

Der er ikke implementeret et fuldt eksternt monitoring-setup, men løsningen har grundlaget for det gennem health endpoint, logs, tests og CI/CD.

---

## Demo

Demo-guide ligger her:

```text
docs/demo-guide.md
```

Den kan bruges til video demo og mundtlig præsentation.

Demoen viser:

1. Start af Docker Compose
2. API docs
3. Health endpoint
4. Telemetry request
5. Start charging session
6. End charging session
7. Analytics endpoint
8. Power BI dashboard

---

## Kendte begrænsninger

MVP’en har følgende begrænsninger:

- Data er syntetiske og ikke fra en rigtig VoltEdge-platform
- Power BI er baseret på flade CSV-filer
- API og BI er ikke realtime-integreret
- OCPP er ikke implementeret som rigtig protokol
- Billing og settlement er ikke implementeret
- Authentication og authorization er ikke implementeret
- Monitoring er dokumenteret, men ikke fuldt implementeret med eksternt værktøj
- ML-modellen er proof-of-concept og ikke produktionsklar

---

## Kobling til rapporten

Repoet følger samme røde tråd som rapporten:

```text
Strategi
→ Domæner og kapabiliteter
→ DDD og bounded contexts
→ Arkitektur og teknologivalg
→ Data og analytics
→ Test, deployment og operation
→ Evaluering og refleksion
```

Den tekniske løsning viser, hvordan nogle af rapportens arkitekturvalg kan realiseres i en mindre MVP.