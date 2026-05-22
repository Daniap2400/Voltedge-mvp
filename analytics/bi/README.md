@"
# Business Intelligence

Denne mappe dokumenterer BI-delen af VoltEdge MVP'en.

## Formål

BI-løsningen skal vise, hvordan data fra den operationelle løsning kan bruges til analyse og beslutningsstøtte.

## Mulige dashboards

Et Power BI-dashboard kan fx vise:

- Antal charging sessions
- Energiforbrug i kWh
- Gennemsnitlig session duration
- Charger uptime
- Fault events
- Peak load periods
- Revenue eller settlement-overblik

## Datakilder

Foreløbige datakilder:

- Charging sessions
- Charger telemetry
- Fault events
- Tariff eller pricing data

## Kobling til MVP

API'et håndterer den operationelle del af løsningen.

BI-delen fungerer som en separat analytics-løsning, hvor data kan visualiseres for fx operations managers, site owners eller fleet managers.
"@ | Set-Content analytics\bi\README.md