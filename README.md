# Spectre-Alliance-Manager
 python based war strategy manager. Get the wars that your alliance is currently involved in, display them in a tabular view with filter and different orders (EOF, ATT/DEF).
 They will be displayed simmilar to Locutus war sheet but easier to manage.

## Features

1) Tabular view with all informations (Like Locutus war sheet).
2) Graph view that makes managing war much easier and comprehensive.
3) Statistics dashboard

Coming soon:
1) Accounts and account management
2) Member projects overview
3) Spy co-ordination hub

## Getting started (New, starting from 01.04.2026)
Esentially, the new build process involves building the docker image with the python requirements and mapping your work directory into the container. That way it has instant access to code changes and the container does not have to be rebuild to apply code changes (DEV version has hot reload enabled).

### Prerequisites
0) git ?
1) Docker Engine
2) Docker compose


### git clone
Replace <repository> with the link you get from the green Code button.
```
git clone <repository>
```

### Image building
Run the docker build command in the projects root directory. (must be executed as root, idk is a Docker requirement)
```
sudo docker build --no-cache -t sam-web-image ./
```

### Password and APIKEYs
Change passwords in docker-compose.yaml for database and pgadmin access. (Can be ommited in DEV verion, but please don't deploy with the default passwords.)

### Image deployment
Start the container stack which includes the Spectre Alliance Manager web server, postgres as database together with pgadmin. 
```
sudo docker-compose up
```

### Production setup
To access SAM from outside of a local network, the following services need to be set up.
1) DDNS service (DuckDNS or ex.) To automatically point SAM Domain to your routers IP.
2) Router port forwarding 443 to a locally running reverse proxy.
3) Reverse proxy (Nginx proxy manager for ex.) routing 443 with SAM Domain to container or server running SAM web on port 4221.

## Getting started (OUTDATED since 01.04.2026)

### git clone
Replace <repository> with the link you get from the green Code button.
```
git clone <repository>
```

### Venv
Change directory into pnw-strategy-manager. Create a virtual environment and load it.
```
python -m venv .venv
source .venv/bin/activate
```
### Dependencies
Install dependencies.
```
pip install -r requirements.txt
```

### Start
Use this command to start the strategy manager, after leaving the virtual environment or restarting the console the source command has to be re-run.
```
python3 app.py
```
