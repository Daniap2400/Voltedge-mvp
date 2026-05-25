# Monitoring-strategi

Denne MVP implementerer ikke et fuldt monitoring-system, men dokumenterer hvordan løsningen kan overvåges på et realistisk MVP-niveau.

## Formål

Formålet med monitoring er at opdage fejl, performance-problemer og ustabilitet tidligt.

For VoltEdge Mobility er dette vigtigt, fordi platformen understøtter ladeinfrastruktur, hvor oppetid og pålidelighed er centrale kvalitetskrav.

## Hvad kan overvåges i MVP’en?

MVP’en giver grundlag for at overvåge:

- Om API’et svarer via `/health`
- Om endpoints returnerer fejlstatuskoder
- Hvor lang tid API-requests tager
- Om telemetri bliver registreret korrekt
- Om charging sessions kan startes og afsluttes
- Om CI/CD-pipelinen fejler ved test eller build

## Health endpoint

API’et har et health endpoint:

```text
GET /health