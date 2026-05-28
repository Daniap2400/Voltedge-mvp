# Architecture documentation

Denne mappe indeholder teknisk dokumentation for VoltEdge MVP’ens arkitektur.

Dokumentationen kobler den implementerede løsning til rapportens arkitekturvalg, DDD-principper og DevSecOps-overvejelser.

---

## Dokumenter

| Fil | Indhold |
|---|---|
| `domain-model.md` | Beskriver DDD-begreber, bounded context, entities, value objects, domain events og domain services |
| `persistence.md` | Beskriver repository pattern, PostgreSQL og koblingen mellem domænemodel og databasemodel |
| `ci-cd.md` | Beskriver GitHub Actions workflow og CI/CD-tilgangen |
| `operations.md` | Beskriver logging, monitoring, fejlhåndtering, robusthed og rollback |

---

## Arkitektonisk fokus

MVP’en fokuserer på to centrale bounded contexts:

- Charging Context
- Analytics Context

Charging Context håndterer ladestandere, connectors, telemetri og charging sessions.

Analytics Context anvender data fra Charging Context til nøgletal, fejlrate, energiforbrug, forecast og anomalier.

---

## Kobling til rapport

Arkitekturdokumentationen understøtter rapportens røde tråd:

```text
Strategi
→ Domæner og kapabiliteter
→ Bounded contexts
→ Domain models
→ Persistence
→ Analytics
→ Test, deployment og operation
```

MVP’en viser dermed en afgrænset teknisk realisering af den arkitektur, der er beskrevet i rapporten.