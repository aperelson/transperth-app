docker build -t transperth:latest .

## Interactive:
docker run -it --rm -p 4000:5000 transperth:latest

## Background:
docker run -d -p 4000:5000 --name transperth transperth:latest

docker save -o transperth.tar transperth:latest



# Load docker image on nas:
Copy transperth.tar to /docker volume.
ssh with Administrator priveleges
ssh -p 37676 perthelsons@synologynas.local
cd /volume1/docker
sudo -i
root@synologynas:/volume1/docker# docker load -i transperth.tar
