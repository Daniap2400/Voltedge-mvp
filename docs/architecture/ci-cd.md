# CI/CD

Dette dokument beskriver projektets CI/CD-setup.

MVP’en bruger GitHub Actions som CI/CD-tilgang. Formålet er at sikre, at ændringer i koden automatisk testes og bygges, før de merges eller afleveres.

---

## Workflow-fil

CI/CD-workflowet ligger her:

```text
.github/workflows/ci.yml
```

---

## Pipeline-flow

Pipeline kører følgende trin:

1. Checkout af repository
2. Installation af Python 3.11
3. Installation af dependencies fra `requirements.txt`
4. Kørsel af pytest
5. Docker build af API-servicen

---

## Pipeline-overblik

```text
Developer push / pull request
        |
        v
GitHub Actions
        |
        v
Install dependencies
        |
        v
Run tests
        |
        v
Build Docker image
        |
        v
Ready for merge / delivery
```

---

## Hvad kvalitetssikres?

CI/CD-pipelinen kvalitetssikrer:

- at API’et kan installeres
- at dependencies kan hentes
- at tests stadig passerer
- at Docker image kan bygges
- at fejl opdages tidligt i udviklingsprocessen

---

## Relevans for DevSecOps

CI/CD understøtter DevSecOps-principper ved at gøre build og test automatiseret.

I MVP’en er fokus på:

- automatiseret test
- automatiseret Docker build
- ensartet validering af kodeændringer
- lavere risiko for manuelle fejl

I en produktionsklar løsning kunne pipeline udvides med:

- dependency scanning
- secret scanning
- static code analysis
- container image scanning
- deployment til staging
- manuel approval før production
- rollback til tidligere image version

---

## Miljøer

I MVP’en arbejdes der primært med:

| Miljø | Beskrivelse |
|---|---|
| Local development | Udvikling via lokal Python eller Docker Compose |
| Test/CI | GitHub Actions kører pytest og Docker build |
| Production | Ikke implementeret, men beskrevet som videreudvikling |

---

## Secrets og konfiguration

MVP’en bruger ikke rigtige secrets.

Konfiguration håndteres via:

```text
.env.example
docker-compose.yml
environment variables
```

I produktion bør secrets håndteres gennem en sikker secret manager, fx GitHub Secrets, Azure Key Vault eller tilsvarende.