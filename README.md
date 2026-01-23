# SP_FinalProject
Group M, Final Project for Scientific Programming (MHEDAS_25-26)




Docker Commands
1. Download the Docker Image and run
```bash
docker run -d --name ckd-app -p 8080:8000 inigoarriazu/ckd-prediction-app:latest
```

2. Go to: http://localhost:9000

# To pause and rebuild (used port / errors) 
docker stop ckd-app
docker rm ckd-app
docker run -d --name ckd-app -p 9000:8000 inigoarriazu/ckd-prediction-app:latest