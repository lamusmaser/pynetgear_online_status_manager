# PyNetGear Online Status Manager
Utilizes the pynetgear_enhanced pypi package to manage the online status of a local router or wireless access point.

# Running Container
```
docker run --rm --pull always -e ROUTER_USERNAME=admin -e ROUTER_PASSWORD=password -e ROUTER_IP=192.168.1.1 lamusmaser/video-filename-title-matcher:latest
```

This has three environment variables that you can utilize, otherwise it will attempt to use the defaults:

| Variable | Default | Description |
| :------- | :------ | :---------- |
| `ROUTER_USERNAME` | `admin` | Netgear Username. | 
| `ROUTER_PASSWORD` | `password` | Netgear account password. | 
| `ROUTER_IP` | `192.168.1.1` | Netgear router or WAP IP. Could be FQDN, but it is untested. | 