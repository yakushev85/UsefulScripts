# Scripts for daily usage in Ubuntu

## Show specs
- memory, cpu and disks
```
sudo lshw -short -C memory ; lscpu ; df
```

## Can't see camera
- PipeWire is a server for handling audio and video, so below command restart it 
```
systemctl --user restart pipewire
```



