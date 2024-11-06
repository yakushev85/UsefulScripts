# Scripts for daily usage in Ubuntu

## Show specs
- memory, cpu and disks
```
free -h ; lscpu ; df -h
```

## Can't see camera
- PipeWire is a server for handling audio and video, so below command restart it 
```
systemctl --user restart pipewire
```



