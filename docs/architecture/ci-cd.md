@"
# CI/CD Pipeline

Dette dokument beskriver projektets CI/CD-setup.

Pipeline-flow:

1. Developer pusher kode til GitHub
2. GitHub Actions starter automatisk
3. Dependencies installeres
4. Tests køres
5. Docker image bygges
6. Deployment kan senere tilføjes til staging/production

Formålet er at understøtte DevSecOps-principper gennem automatiseret build, test og deployment.

## Relevans for eksamensopgaven

CI/CD-delen viser, hvordan MVP'en kan kvalitetssikres og leveres på en professionel måde.

Pipeline skal på sigt understøtte:

- Build
- Test
- Security checks
- Docker image build
- Deployment
- Håndtering af miljøer og secrets
"@ | Set-Content docs\architecture\ci-cd.md