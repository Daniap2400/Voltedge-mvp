# VoltEdge MVP – Smart EV Charging Infrastructure

Dette repository indeholder den tekniske MVP til 6. semester eksamensopgaven i Økonomi og IT.

Projektet tager udgangspunkt i casevirksomheden VoltEdge Mobility A/S, som arbejder med smart EV charging infrastructure. MVP’en demonstrerer en afgrænset, men central del af den fremtidige platform med fokus på Charging Context og Analytics Context.

MVP’en er ikke en fuld produktionsklar løsning, men et teknisk proof-of-concept, der viser hvordan API, data, Docker, analytics, machine learning, Business Intelligence og CI/CD kan kobles sammen i en realistisk løsning.

---

## Formål

Formålet med MVP’en er at understøtte VoltEdges strategiske fokusområder:

- Scale Operations
- Data-driven Services
- Secure & Reliable Platform
- Monitoring og drift
- Predictive maintenance
- Business Intelligence

Løsningen viser, hvordan operationelle data fra ladestandere og ladesessioner kan struktureres, gemmes og anvendes til analytics og visualisering.

---

## Hvad demonstrerer MVP’en?

MVP’en demonstrerer:

- FastAPI-baseret API
- Docker Compose setup med API og PostgreSQL
- Domain models for chargers, connectors, telemetry og charging sessions
- Repository pattern og persistence layer
- AnalyticsService som domain service
- Machine learning notebook til predictive maintenance
- Power BI dashboard som uafhængig BI-løsning
- GitHub Actions til CI/CD
- Dokumentation for logging, monitoring, fejlhåndtering og rollback

---

## Afgrænsning

MVP’en implementerer ikke hele den fremtidige event-driven microservice-arkitektur.

I stedet realiserer løsningen en afgrænset del af arkitekturen:

- Charging Context: håndtering af ladestandere, connectors, telemetri og charging sessions
- Analytics Context: beregning af nøgletal, fejlrate, energiforbrug, forecast og anomalier
- BI/ML: predictive maintenance og Power BI-rapport baseret på syntetiske data

Billing, settlement, OCPP-kommunikation og partnerintegrationer indgår som arkitektur- og rapportmæssige perspektiver, men er ikke fuldt implementeret i MVP’en.

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

Disse data kan bruges til API-demo og analytics endpoints.

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

Analytics er implementeret som en domain service i:

```text
services/api/app/domain/analytics_service.py
```

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

Dette understøtter rapportens fokus på data-driven services og viser, hvordan operationelle data kan omsættes til forretningsmæssig indsigt.

---

## Machine Learning

Machine learning-delen ligger i:

```text
analytics/ml/predictive_maintenance.ipynb
```

Notebooken demonstrerer predictive maintenance baseret på syntetiske operationsdata.

Formålet er at vise, hvordan historiske data om ladestandere, fejl, oppetid og energiforbrug kan bruges til at forudsige vedligeholdelsesrisiko.

---

## Business Intelligence

Power BI-rapporten ligger i:

```text
analytics/bi/Voltedge Bi rapport.pbix
```

Rapporten visualiserer blandt andet:

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

BI-rapporten er baseret på flade CSV-filer som proof-of-concept. I en produktionsklar løsning ville data typisk blive ført gennem et ETL/ELT-lag, fx Microsoft Fabric og Lakehouse.

---

## CI/CD

Projektet bruger GitHub Actions.

Workflowet ligger i:

```text
.github/workflows/ci.yml
```

Pipeline kører:

1. Checkout af repository
2. Installation af Python
3. Installation af dependencies
4. Pytest
5. Docker build

Formålet er at sikre, at ændringer testes automatisk før merge eller aflevering.

---

## Drift og operations

Driftsdokumentation ligger i:

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

I produktion ville dette kunne udvides med Azure Monitor, Application Insights, Prometheus/Grafana, struktureret JSON logging, alerts og correlation IDs.

---

## Demo

Demo-guide ligger i:

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

MVP’en har følgende afgrænsninger:

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

Repoet understøtter rapportens røde tråd:

```text
Strategi
→ Domæner og kapabiliteter
→ DDD og bounded contexts
→ Arkitektur og teknologivalg
→ Data og analytics
→ Test, deployment og operation
→ Evaluering og refleksion
```

Den tekniske løsning viser konkret, hvordan rapportens arkitekturvalg kan realiseres i en mindre MVP.