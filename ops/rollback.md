# Rollback-strategi

Denne MVP bruger en simpel rollback-strategi, der passer til projektets scope og Git-baserede workflow.

---

## Formål

Formålet med rollback er at kunne vende tilbage til en tidligere stabil version, hvis en ændring introducerer fejl.

For VoltEdge Mobility er rollback vigtigt, fordi platformen understøtter ladeinfrastruktur, hvor fejl i centrale flows kan påvirke drift, kunder og brugere.

---

## Rollback på MVP-niveau

På MVP-niveau håndteres rollback primært via Git og CI/CD.

Hvis en ændring viser sig at skabe fejl efter merge til `main`, kan teamet:

1. Identificere den commit, der introducerede fejlen.
2. Oprette en revert commit med `git revert`.
3. Køre tests lokalt.
4. Pushe revert commit til GitHub.
5. Lade GitHub Actions validere ændringen med automated tests og Docker build.

---

## Eksempel på rollback med Git

Find commits:

```bash
git log --oneline
```

Revert en commit:

```bash
git revert <commit-hash>
```

Push ændringen:

```bash
git push
```

---

## Kvalitetssikring efter rollback

Efter rollback bør teamet køre:

```bash
cd services/api
pytest
```

Og derefter:

```bash
docker compose up --build
```

Tjek derefter:

```text
http://localhost:8000/health
http://localhost:8000/docs
```

---

## Rollback i produktion

I en produktionsklar løsning bør rollback ske ved at redeploye et tidligere godkendt Docker image.

Et mere modent setup kunne være:

```text
Container Registry
        |
        v
Previous stable image
        |
        v
Redeploy to staging/production
        |
        v
Health check
        |
        v
Monitoring validation
```

---

## Afgrænsning

MVP’en har ikke automatisk production deployment.

Rollback er derfor dokumenteret som en Git- og CI/CD-baseret proces, hvilket passer til projektets scope.