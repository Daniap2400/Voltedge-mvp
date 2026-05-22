
# Domain Model

Dette dokument beskriver de centrale domænebegreber i VoltEdge MVP'en.

## Bounded Context

MVP'en tager udgangspunkt i et afgrænset bounded context:

**Charging Operations**

Dette context handler om ladestandere, ladesessioner, telemetri og simple load forecasts.

## Foreløbige domænebegreber

- Charger
- Charging Session
- Telemetry Event
- Load Forecast
- Fault Event

## DDD-fokus

Domain Driven Design bruges til at skabe kobling mellem:

- Forretningsbehov
- Domænemodel
- Kode
- Datamodel
- API-design

## Eksempel på domænelogik

Analytics-funktionalitet placeres som en domain service, fordi beregning af load forecast og peak-risk er forretningslogik, der ikke naturligt hører til én enkelt entity.

Eksempel:

- Input: Telemetry readings og charging sessions
- Output: Load forecast eller risk score
