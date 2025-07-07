# 🚍 When's The Bus?

A lightweight Flask-based web app to display **real-time Transperth bus departures** for your favourite stops, designed to run on:

- 🖥️ Mac (local Docker Desktop)
- 📦 Synology NAS (via Container Manager)
- 🍓 Raspberry Pi (optional)

---

## 🌟 Features

- Real-time bus arrival and departure times with countdown in minutes and seconds
- Auto-refresh every 10 seconds for live updates
- Collapsible **NORTHBOUND** and **SOUTHBOUND** stop groups
- Mobile-friendly responsive design
- Optional dark mode support
- Designed for easy home network use (no external hosting required)

---

## 🚀 Quick Start (Local)

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
```

4. Open in browser:
```
http://localhost:4000
```


### Build it:
docker build -t transperth:latest .

### Interactive:
docker run -it --rm -p 4000:5000 transperth:latest

### Background:
docker run -d -p 4000:5000 --name transperth transperth:latest

docker save -o transperth.tar transperth:latest

---

## 📦 Deploy to Synology NAS

1. Build and save the image:
```bash
docker save -o transperth.tar transperth:latest
```

### Load docker image on nas:
Copy transperth.tar to /docker volume.
ssh with Administrator priveleges
ssh -p 37676 perthelsons@synologynas.local
cd /volume1/docker
sudo -i
root@synologynas:/volume1/docker# docker load -i transperth.tar


2. Transfer the `.tar` file to your NAS (via File Station or `scp`).

3. SSH into the NAS and load the image:
```bash
sudo -i
cd /volume1/docker
docker load -i transperth.tar
```

4. In **Container Manager**:
   - Create new container from `transperth:latest`
   - Map ports: `4000` (local) → `5000` (container)

5. Access at:
```
http://your-nas-ip:4000
```

---

## ⚙️ Configuration

- Stop numbers and groups are defined in `config.yaml`.
- To avoid rebuilding for config changes:
  - Mount the config as a volume on the NAS.

---

## 📱 Mobile & Dark Mode

- Designed to work beautifully on phones and tablets.
- Adapts to system dark mode automatically.

---

## 💡 Future Enhancements

- API token management
- Train or ferry support
- Push notifications (optional)

---

## 📋 License

MIT License. Not affiliated with Transperth.

---

> "When's The Bus?"—because life’s too short to miss the ride. 🚌