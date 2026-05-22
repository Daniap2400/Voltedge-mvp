# VoltEdge MVP – Smart EV Charging Infrastructure

Dette repository indeholder den tekniske MVP til 6. semester eksamensopgaven i Økonomi og IT.

Casen tager udgangspunkt i VoltEdge Mobility A/S, som arbejder med smart EV charging infrastructure. MVP'en skal demonstrere en moderne, container-baseret løsning med API, data, analytics og DevSecOps-principper.

## Formål

Formålet med MVP'en er at demonstrere en afgrænset teknisk løsning, der understøtter VoltEdges strategiske behov for:

- skalerbar drift af ladeinfrastruktur
- standardiserede partner-API'er
- aktiv brug af data
- analytics som domain service
- BI/Power BI som separat analytics-løsning
- CI/CD og professionel teknisk dokumentation

## Teknisk scope

MVP'en vil gradvist blive bygget op omkring:

- API-service
- Docker-baseret udviklingsmiljø
- operationelle data om ladestandere og charging sessions
- analytics/domain service
- BI-datasæt til Power BI
- CI/CD pipeline til build og test

## Foreløbig arkitektur

```text
Partner / User
     |
     v
API Service
     |
     v
Operational Data
     |
     v
Analytics / Domain Service
     |
     v
BI / Power BI