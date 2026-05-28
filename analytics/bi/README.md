# Business Intelligence

Denne mappe indeholder Power BI-rapporten for VoltEdge MVP’en.

Rapporten fungerer som en uafhængig analytics-løsning oven på MVP’ens operationelle og analytiske datagrundlag. Formålet er at vise, hvordan data fra ladestandere, ladesessioner og machine learning kan omsættes til beslutningsstøtte for operations-teamet.

---

## Power BI-fil

Power BI-rapporten ligger her:

```text
analytics/bi/Voltedge Bi rapport.pbix
```

---

## Formål

BI-løsningen understøtter VoltEdges strategiske mål om data-driven services.

Dashboardet giver overblik over:

- driftstilstand
- energiforbrug
- fejl
- oppetid
- vedligeholdelsesrisiko
- forskelle mellem lokationer og ladestandermodeller

Dette gør det muligt at gå fra reaktiv drift til mere proaktiv og datadrevet vedligeholdelse.

---

## Dashboardet viser

Power BI-dashboardet indeholder:

- Total chargers
- Total sessions
- Total energy
- Average uptime
- Total faults
- Faults by location
- Faults by charger model
- Maintenance predictions
- Energiforbrug over tid
- Detaljeret charger-tabel

---

## Datakilder

BI-rapporten anvender flade CSV-filer fra MVP’ens data- og ML-del.

Datagrundlaget består af:

- syntetiske charger-data
- syntetiske operationsdata
- output fra predictive maintenance notebook
- maintenance risk level
- predicted maintenance required
- maintenance risk probability

Data er ikke produktionsdata og indeholder ikke reelle personoplysninger.

---

## Analysetyper

BI-rapporten understøtter tre analysetyper:

| Analysetype | Eksempel i rapporten |
|---|---|
| Deskriptiv analyse | Total sessions, total energy, average uptime |
| Diagnostisk analyse | Faults by location og faults by model |
| Predictive analyse | Maintenance predictions baseret på ML-output |

---

## Afgrænsning

I MVP’en er Power BI-rapporten baseret på manuelle CSV-filer.

Det er valgt, fordi projektet er et proof-of-concept, hvor formålet er at demonstrere sammenhængen mellem data, machine learning og visualisering uden at bygge en fuld enterprise data platform.

---

## Perspektiv til produktion

I en produktionsklar løsning ville Power BI ikke være baseret på manuelle CSV-filer.

Data ville typisk blive behandlet gennem et ETL/ELT-flow, fx:

```text
Operational database
+ Telemetry streams
+ ML output
+ External data sources
        |
        v
ETL/ELT layer
        |
        v
Microsoft Fabric / Lakehouse
        |
        v
Power BI semantic model
        |
        v
Power BI dashboard
```

Dette ville give:

- bedre automatisering
- bedre datakvalitet
- mere robust historik
- bedre governance
- mulighed for rollebaseret adgang
- bedre model monitoring