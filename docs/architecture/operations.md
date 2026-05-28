# Operations

Dette dokument beskriver de driftsmæssige hensyn i VoltEdge MVP’en.

Operations-delen viser, hvordan løsningen kan drives, overvåges og fejlrettes på et realistisk MVP-niveau.

For VoltEdge Mobility er dette vigtigt, fordi ladeinfrastruktur kræver høj oppetid, god sporbarhed og hurtig fejlhåndtering.

---

## Formål

Formålet med operations-dokumentationen er at vise, hvordan MVP’en forholder sig til:

- logging
- monitoring
- health checks
- fejlhåndtering
- robusthed
- rollback
- CI/CD som kvalitetssikring

---

## Sammenhæng mellem health, logs og CI/CD

MVP’en bruger tre simple mekanismer til at understøtte drift:

| Mekanisme | Rolle i drift |
|---|---|
| Health endpoint | Viser om API’et er tilgængeligt |
| Logs | Giver sporbarhed omkring requests, telemetri, sessions og fejl |
| CI/CD | Kører tests og Docker build, så fejl opdages før merge eller aflevering |

Tilsammen giver de et enkelt, men realistisk operations-setup.

---

## Health endpoint

API’et har et health endpoint:

```text
GET /health
```

Eksempel på response:

```json
{
  "status": "healthy",
  "service": "voltedge-api"
}
```

Dette endpoint kan bruges til manuel kontrol eller kobles til et monitoring-værktøj.

---

## Fejlhåndtering

API’et håndterer centrale fejlscenarier:

| Scenarie | HTTP-status | Forklaring |
|---|---:|---|
| Ukendt charger ID | 404 | Ressourcen findes ikke |
| Ukendt session ID | 404 | Sessionen findes ikke |
| Negativ telemetry power | 422 | Inputdata er ugyldige |
| Tomt charger ID | 422 | Inputdata er ugyldige |
| Tomt connector ID | 422 | Inputdata er ugyldige |
| Ugyldig domænehandling | 400 | Forretningsregel kan ikke gennemføres |

Denne skelnen gør API’et mere robust og lettere at fejlfinde.

---

## Logging

API’et logger både generelle HTTP-requests og udvalgte domænehændelser.

Eksempler:

- registrering af telemetri
- start af charging session
- afslutning af charging session
- fejl ved ukendt charger
- fejl ved ukendt session
- HTTP-metode, path, statuskode og request-varighed

I MVP’en bruges almindelig Python logging.

I produktion bør dette udvides med:

- struktureret JSON-logging
- correlation IDs
- central logopsamling
- log retention policies
- audit logs for følsomme handlinger

---

## Monitoring

MVP’en har ikke et fuldt eksternt monitoring-system, men den giver grundlaget for monitoring via:

- `/health`
- HTTP-statuskoder
- request-varighed i logs
- automatiserede tests i CI/CD
- Docker build i pipeline

I produktion kunne dette kobles til:

- Azure Monitor
- Application Insights
- Prometheus/Grafana
- Grafana Loki
- ELK/OpenSearch

---

## Alarmering

MVP’en implementerer ikke aktiv alarmering.

I en produktionsløsning kunne der opsættes alerts på:

- høj fejlrate
- langsomme API-kald
- databasefejl
- høj responstid
- mange faulted chargers
- manglende heartbeat fra ladestandere
- failed CI/CD pipeline

---

## Rollback

Rollback håndteres på MVP-niveau via Git.

Hvis en fejl når ind i `main`, kan teamet lave en revert commit:

```bash
git revert <commit-hash>
git push
```

GitHub Actions vil derefter køre tests og Docker build igen.

I produktion bør rollback ske ved at redeploye et tidligere godkendt Docker image.

---

## Robusthed

MVP’en demonstrerer robusthed gennem:

- inputvalidering med Pydantic
- automatiserede tests
- repository pattern
- adskillelse mellem domain, application og infrastructure
- Docker-baseret runtime
- health endpoint
- logging
- CI/CD pipeline

---

## Videreudvikling

For at gøre løsningen mere produktionsklar bør følgende tilføjes:

- authentication og authorization
- rollebaseret adgang
- centraliseret logging
- metrics dashboard
- alerts
- database migrations
- secret management
- staging- og production-miljøer
- container registry
- automatiseret deployment