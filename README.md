# DevSecOps
End-to-End DevsSecOps project


DevSecOps

workflows
## CI 
    - code-quality.yml
    - secrets-scan
    - dependency-scan
    - docker-scan
Dependent jobs:
- build
- trivy
## CD
- deploy
