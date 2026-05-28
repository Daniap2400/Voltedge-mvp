# Demo guide

Denne guide viser, hvordan VoltEdge MVP’en kan demonstreres i video eller til mundtlig eksamen.

Demoen viser den røde tråd fra API og data til analytics og Power BI.

---

## 1. Start løsningen

Kør fra projektets rodmappe:

```bash
docker compose up --build
```

Vent til både API og database er startet.

---

## 2. Åbn API docs

Åbn browseren:

```text
http://localhost:8000/docs
```

Her kan API’et testes direkte via Swagger UI.

---

## 3. Test health endpoint

Endpoint:

```text
GET /health
```

Forventet response:

```json
{
  "status": "healthy",
  "service": "voltedge-api"
}
```

Dette viser, at API’et kører.

---

## 4. Seed databasen

Kør i en ny terminal:

```bash
docker compose exec api python scripts/seed_database.py
```

Dette opretter demo-data for ladestandere, telemetry og charging sessions.

---

## 5. Registrer telemetry

Endpoint:

```text
POST /api/v1/telemetry
```

Eksempel:

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

Formål:

Dette viser, hvordan MVP’en modtager operationelle data fra en ladestander.

---

## 6. Start charging session

Endpoint:

```text
POST /api/v1/sessions/start
```

Eksempel:

```json
{
  "charger_id": "charger-1",
  "connector_id": "connector-1",
  "user_id": "user-1",
  "contract_id": "contract-1"
}
```

Formål:

Dette viser, hvordan Charging Context håndterer en ny ladesession.

---

## 7. Afslut charging session

Brug session ID fra forrige response.

Endpoint:

```text
POST /api/v1/sessions/{session_id}/end
```

Eksempel:

```json
{
  "energy_delivered_kwh": 22.5
}
```

Formål:

Dette viser, hvordan energiforbrug knyttes til en afsluttet ladesession.

---

## 8. Vis alle sessions

Endpoint:

```text
GET /api/v1/sessions
```

Formål:

Dette viser de registrerede charging sessions i MVP’en.

---

## 9. Vis analytics summary

Endpoint:

```text
GET /api/v1/analytics/summary
```

Formål:

Dette viser AnalyticsService som domain service.

Analytics summary viser blandt andet:

- antal chargers
- antal sessions
- total energy
- average session duration
- utilization rate
- charger fault rate
- expected demand
- anomalies

---

## 10. Vis charger analytics

Endpoint:

```text
GET /api/v1/analytics/chargers/charger-1
```

Formål:

Dette viser analytics for en specifik ladestander.

---

## 11. Vis Power BI-dashboard

Åbn Power BI-filen:

```text
analytics/bi/Voltedge Bi rapport.pbix
```

Forklar kort at dashboardet viser:

- KPI’er
- fejl fordelt på lokation
- fejl fordelt på model
- energiforbrug over tid
- maintenance predictions
- detaljeret charger-tabel

---

## 12. Afrunding i demo

Afslut demoen med at forklare:

MVP’en er et proof-of-concept, der demonstrerer en afgrænset del af VoltEdges fremtidige platform. Den viser sammenhængen mellem Charging Context, Analytics Context, Docker, API, persistence, machine learning, Power BI og CI/CD.

MVP’en er ikke en fuld produktionsløsning, men den viser et realistisk teknisk fundament for videreudvikling.