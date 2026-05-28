# Monitoring-strategi

Denne MVP implementerer ikke et fuldt eksternt monitoring-system, men dokumenterer hvordan løsningen kan overvåges på et realistisk MVP-niveau.

---

## Formål

Formålet med monitoring er at opdage fejl, performance-problemer og ustabilitet tidligt.

For VoltEdge Mobility er dette vigtigt, fordi platformen understøtter ladeinfrastruktur, hvor oppetid og pålidelighed er centrale kvalitetskrav.

---

## Hvad kan overvåges i MVP’en?

MVP’en giver grundlag for at overvåge:

- om API’et svarer via `/health`
- om endpoints returnerer fejlstatuskoder
- hvor lang tid API-requests tager
- om telemetri bliver registreret korrekt
- om charging sessions kan startes og afsluttes
- om analytics endpoints svarer korrekt
- om CI/CD-pipelinen fejler ved test eller build

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

---

## MVP-monitoring

På MVP-niveau kan løsningen overvåges gennem:

| Element | Hvordan |
|---|---|
| API health | `/health` endpoint |
| API-fejl | HTTP-statuskoder |
| Performance | Request-varighed i logs |
| Kodekvalitet | Pytest i CI/CD |
| Container build | Docker build i GitHub Actions |
| Datagrundlag | Seed-script og analytics endpoints |

---

## Forslag til produktionsmonitorering

I en produktionsklar løsning bør monitoring udvides med:

- Azure Monitor
- Application Insights
- Prometheus/Grafana
- centraliseret logopsamling
- dashboards for API performance
- alerts ved fejlrate og høj responstid
- alerts ved manglende heartbeat fra ladestandere
- model monitoring for predictive maintenance

---

## Mulige alerts

Eksempler på relevante alerts:

| Alert | Betydning |
|---|---|
| API health fejler | API’et er utilgængeligt |
| Høj 5xx-fejlrate | Serverfejl i API’et |
| Høj responstid | Performance-problem |
| Mange faulted chargers | Driftsproblem i ladeinfrastruktur |
| CI/CD fejler | Ny ændring kan ikke valideres |
| Database utilgængelig | Persistence-laget fejler |

---

## Afgrænsning

Der er ikke implementeret et eksternt monitoringværktøj i MVP’en.

MVP’en viser i stedet det tekniske grundlag for monitoring gennem health endpoint, logging, tests og CI/CD.