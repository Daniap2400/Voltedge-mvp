```markdown
# Operations

Dette dokument beskriver de driftsmæssige hensyn i VoltEdge MVP’en.

## Formål

Operations-delen viser, hvordan løsningen kan drives, overvåges og fejlrettes på et realistisk MVP-niveau.

For VoltEdge Mobility er dette vigtigt, fordi ladeinfrastruktur kræver høj oppetid, god sporbarhed og hurtig fejlhåndtering.

## Sammenhæng mellem health, logs og CI/CD

MVP’en bruger tre simple mekanismer til at understøtte drift:

| Mekanisme | Rolle i drift |
|---|---|
| Health endpoint | Viser om API’et er tilgængeligt |
| Logs | Giver sporbarhed omkring requests, telemetri, sessions og fejl |
| CI/CD | Kører tests og build, så fejl opdages før merge eller deployment |

Tilsammen giver de et enkelt, men realistisk operations-setup.

## Fejlhåndtering

API’et håndterer centrale fejlscenarier:

| Scenarie | HTTP-status | Forklaring |
|---|---:|---|
| Ukendt charger ID | 404 | Ressourcen findes ikke |
| Ukendt session ID | 404 | Sessionen findes ikke |
| Negativ telemetry power | 422 | Inputdata er ugyldige |
| Tomt charger ID | 422 | Inputdata er ugyldige |
| Tomt connector ID | 422 | Inputdata er ugyldige |

Denne skelnen gør API’et mere robust og lettere at fejlfinde.

## Logging

API’et logger både generelle HTTP-requests og udvalgte domænehændelser.

Eksempler:

- Registrering af telemetri
- Start af charging session
- Afslutning af charging session
- Fejl ved ukendt charger
- Fejl ved ukendt session

I MVP’en bruges almindelig Python logging. I produktion bør dette udvides med struktureret JSON-logging og correlation IDs.

## Monitoring

MVP’en har ikke et fuldt monitoring-system, men den giver grundlaget for monitoring via:

- `/health`
- HTTP-statuskoder
- Request-varighed i logs
- Automated tests i CI/CD
- Docker build i pipeline

I produktion kunne dette kobles til Azure Monitor, Application Insights eller Prometheus/Grafana.

## Rollback

Rollback håndteres på MVP-niveau via Git.

Hvis en fejl når ind i `main`, kan teamet lave en revert commit med:

```bash
git revert <commit-hash>