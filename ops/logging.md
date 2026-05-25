# Logging-strategi

Denne MVP bruger simpel applikationslogning for at understøtte fejlfinding, drift og sporbarhed.

## Formål

Formålet med logging er at gøre vigtige API-kald og domænehændelser synlige under udvikling, test og drift.

Målet er ikke at implementere en fuld enterprise logging-platform, men at demonstrere hvordan servicen kan producere nyttige driftsdata.

## Hvad bliver logget?

API’et logger:

- HTTP-metode
- Request path
- HTTP-statuskode
- Request-varighed i millisekunder

Charging API’et logger også udvalgte domænehændelser:

- Registrering af telemetri
- Start af charging session
- Afslutning af charging session
- Fejl ved registrering af telemetri
- Fejl ved opslag på charger status
- Fejl ved afslutning af session

## Log levels

MVP’en bruger primært to log levels:

| Level | Brug |
|---|---|
| INFO | Normale driftsmæssige hændelser, fx registreret telemetri eller startet session |
| WARNING | Forventede fejlscenarier, fx ukendt charger ID eller ukendt session ID |

## Hvorfor er det relevant?

VoltEdge Mobility arbejder med ladeinfrastruktur, hvor oppetid, sporbarhed og hurtig fejlfinding er vigtigt.

Logs kan hjælpe driftsteamet med at svare på spørgsmål som:

- Hvilken ladestander sendte telemetri?
- Hvilken session fejlede?
- Hvilket endpoint returnerede en fejl?
- Hvor lang tid tog et API-kald?

## Perspektiv til produktion

I en rigtig produktionsløsning bør logs samles centralt i en platform som fx:

- Azure Monitor
- Azure Application Insights
- Grafana Loki
- ELK / OpenSearch

Et næste skridt ville også være at indføre struktureret JSON-logging, correlation IDs og alarmer baseret på fejlrate og svartider.