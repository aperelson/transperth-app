# 🚍 When's The Bus?

A lightweight Flask-based web app to display **real-time Transperth bus departures** for your favourite stops, designed to run on:

- Mac (local Docker Desktop)
- Synology NAS (via Container Manager)
- fly.io (optional)

---

## Features

- Real-time bus arrival and departure times with countdown in minutes and seconds
- Auto-refresh every 10 seconds for live updates
- Customisable stop groups
- Mobile-friendly responsive design
- Optional dark mode support
- Designed for easy home network use (no external hosting required)

---

## Quick Start (Local)

1. Clone this repo:
```bash
git clone https://github.com/YOUR_USERNAME/transperth-app.git
cd transperth-app
```

2. Build the Docker image:
```bash
docker build -t transperth:latest .
```

3. Run the app:
```bash
docker run -it --rm -p 4000:5000 transperth:latest
OR
docker run -d -p 4000:5000 --name transperth transperth:latest
```

4. Open in browser:
```
http://localhost:4000
```

## Deploy to Synology NAS

1. Build and save the image:
```bash
docker save -o transperth.tar transperth:latest
```

### Load docker image on nas:

Copy transperth.tar to /docker volume.
ssh with an account that has Administrator privileges
ssh -p 37676 <user-name>@synologynas.local
cd /volume1/docker
sudo -i
root@synologynas:/volume1/docker# docker load -i transperth.tar

In **Container Manager** on the nas:
   - Create new container from `transperth:latest`
   - Map ports: `4000` (local) → `5000` (container)

Access at:
```
http://your-nas-ip:4000
```

---

## Configuration

- Stop numbers and groups are defined and baked in `config.yaml`.
- To avoid rebuilding for config changes:
  - Will need to mount the config as a volume on the NAS or Somewhere.

---

## Mobile & Dark Mode

- Designed to work on phones and tablets.
- Adapts to system dark mode automatically.

---


# Hosted version:

---

## Fly.io Integration

Run fly.io integration
```
brew install flyctl

flyctl auth login

flyctl launch
```

To update later:
```
There's a github action in place that auto deploys on update to the main branch.

OR 

flyctl deploy
```


---

# License

MIT License. Not affiliated with Transperth.

---
 
> "When's The Bus?"—because life’s too short to miss the ride. 🚌