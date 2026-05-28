# Kobling mellem rapport og teknisk produkt

Dette repository understøtter rapportens tekniske MVP for VoltEdge Mobility A/S.

Formålet med denne fil er at gøre det tydeligt, hvordan repoet hænger sammen med rapportens analyse, arkitekturvalg og dataforståelse.

---

## Rapportens fokusområder

Rapporten fokuserer især på:

- Scale Operations
- Data-driven Services
- Domain Driven Design
- DevSecOps
- Monitoring og drift
- Business Intelligence
- Predictive maintenance

---

## Teknisk realisering i MVP’en

| Rapportområde | Realisering i repoet |
|---|---|
| Strategi | Fokus på Scale Operations og Data-driven Services |
| Business domains | Charging og Analytics er valgt som centrale MVP-områder |
| DDD | Domain models, use cases, repositories og domain service |
| Arkitektur | FastAPI, Docker, PostgreSQL og lagdelt struktur |
| Data | Chargers, connectors, telemetry readings og charging sessions |
| Analytics | AnalyticsService som domain service |
| Machine Learning | Predictive maintenance notebook |
| Business Intelligence | Power BI-rapport i `analytics/bi` |
| Test | Pytest-tests i `services/api/tests` |
| CI/CD | GitHub Actions workflow |
| Drift | Logging, monitoring, health checks og rollback-dokumentation |

---

## Afgrænsning

MVP’en implementerer ikke hele den fremtidige platform.

Den tekniske løsning er afgrænset til:

```text
Charging Context
+ Analytics Context
+ ML proof-of-concept
+ Power BI dashboard
+ Docker/API/CI setup
```

Billing, settlement, partnerintegrationer og fuld OCPP-kommunikation beskrives i rapporten som fremtidige arkitektur- og videreudviklingsområder.

---

## Hvorfor dette er relevant

Opgavens krav er ikke, at hele platformen skal bygges færdig.

Kravet er, at det tekniske produkt skal demonstrere en afgrænset, men central del af arkitekturen. Denne MVP viser derfor, hvordan VoltEdge kan gå fra strategiske udfordringer med fragmenteret data og drift til en mere struktureret teknisk løsning med API, datalagring, analytics og BI.