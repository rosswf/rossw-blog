Title: Giving /home a new home on ZFS 
Date: 2021-04-10 10:00
Tags: zfs, linux, ubuntu, sysadmin
Summary: Moving /home to take advantage of ZFS the benefits of ZFS. Compression and snapshot backups.
Slug: home-to-zfs
Description: Moving /home to ZFS to take advantage of the benefits of compression and snapshot backups. 

Currently on my main desktop machine my `/home` directory resides on it's own 256gb SSD with an ext4 filesystem. I want to move this to a ZFS file system to take advantage of snapshots and compression.

I have a TrueNAS VM running in proxmox (more on this in future posts) that `/home` then gets backed up to using an `rsync` cronjob. However as I mentioned previously I would like to be able to take advantage of ZFS snapshots when doing backups so I have decided to move `/home` to ZFS. 
I run ubuntu 20.10 on my desktop PC so this is fairly straight forward. ZFS is supported out of the box in the kernel on ubuntu. 

The only aspect that makes this a little bit messy is that I want to use ZFS on the existing SSD that currently has `/home` on it. I'll need to do quite a bit of juggling files!

I am going to performing these steps on the live filesystem. I would recommend using a LiveCD for performing these tasks where possible, it'll make it a bit easier.

### Install ZFS tools
First of all, let's install the tools required for managing zfs using apt.

	:::text
	sudo apt install zfsutils-linux

### Copy /home to a temporary location
The next thing to do is copy the entire contents of the `/home` directory that currently resides on the SSD to a temporary location. I have plenty of space on my main drive so I'm just going to create a folder there and copy everything to it but if you don't then feel free to use an external drive.

	:::text
	sudo mkdir /temp-hone
	sudo cp -av /home/* /temp-home/

Using the `-a` flag with `cp` preserves all file attributes and copies recursively so there shouldn't be any strange file permission issues.

### Edit fstab and un-mount the drive
Now that the `/home` directory has been safely copied to another location `fstab` can be edited to stop the partition being mounted at boot. For now we can simply comment out the relevant line incase something goes wrong and we need to revert this step.
	
	:::text
	sudo vim /etc/fstab

	# /home was on /dev/sda1 during installation
	# UUID=myuuid /home           ext4    defaults

Next we can un-mount the drive. We use the `-lf` flags for force and lazy un-mounting. Without this it won't work as there are programs running that are actively trying to access this file system. As I mentioned in the introduction, doing this in a live filesystem is less than ideal, which is why we had to take this step.

	:::text
	sudo umount -lf /dev/sda1

### Copy /temp-home back to /home
Due to doing this live and having plenty of drive space we are going to copy the `/temp-home/` to `/home` so that when we reboot everything is where ubuntu suspects it to be, this now resides on the main OS drive.
A reboot is required because the `home` drive was unmounted lazily and we need to be able to delete the partition(s) so that ZFS can do it's thing! 

	:::text
	sudo cp -a /temp-home/* /home/
	reboot

The system should come back up as if nothing has changed.

### Use fdisk to delete partition
Before we can create the ZFS pool we need to delete all partitions from the second SSD, which is `/dev/sda`. For this we can use `fdisk`.

	:::text
	$ sudo fdisk /dev/sda

	Welcome to fdisk (util-linux 2.36).
	Changes will remain in memory only, until you decide to write them.
	Be careful before using the write command.


	Command (m for help): d
	Selected partition 1
	Partition 1 has been deleted.

	Command (m for help): w

	The partition table has been altered.
	Calling ioctl() to re-read partition table.
	Synching disks.

Using `d` to delete the partition as there was only one and then `w` to write the changes to the partition table.

### Create a ZFS pool
The preparation is done so now we can finally create the ZFS pool. I'm going with `mypool` for lack of a better name but feel free to choose whatever you like. I also only have the one drive so don't need to worry about any sort of RAIDZ or mirroring. If you have multiple drives you'd like in your pool you'll want to check out the manpages for `zpool create`.

	:::text
	sudo zpool create mypool /dev/sda

Then just a quick `zpool status` to check it was created.

	:::text
	$ sudo zpool status
	pool: mypool
	state: ONLINE
	scan: none requested
	config:

		NAME        STATE     READ WRITE CKSUM
		mypool      ONLINE       0     0     0
		sda       	ONLINE       0     0     0

	errors: No known data errors

### Create the ZFS filesystem
Next create the `home` filesystem in the pool.

	:::text
	sudo zfs create mypool/home

And check it was created.

	:::text
	sudo zfs list
	NAME          USED  AVAIL     REFER  MOUNTPOINT
	mypool        984K   225G      192K  /mypool
	mypool/home   192K   225G      192K  /mypool/home

### Enable Compression
Another benefit of ZFS is being able to use compression, there is a slight performance hit for doing this but since it's just my home directory I don't see this causing me any issues. So let's enable that now.

	:::text
	sudo zfs set compression=lz4 mypool

I'm going to go with lz4 since this gives a great compression ratio for minimal performance impact. ServeTheHome have a great [article](https://www.servethehome.com/the-case-for-using-zfs-compression/) about it. 

### Copy /temp-home to it's new home
Great! Now that we have the filesystem and it is mounted at `/mypool/home` we can copy all the contents of the `/temp-home/` directory to it once again using the `cp -a` command.

	:::text
	sudo cp -av /temp-home/* /mypool/home

Then check the pool usage and compression ratio.

	:::text
	$ sudo zfs list -o name,used,avail,refer,mountpoint,compressratio
	NAME          USED  AVAIL     REFER  MOUNTPOINT  	RATIO
	mypool       54.9G   170G      192K  /mypool     	1.22x
	mypool/home  54.9G   170G     54.9G  /mypool/home   1.22x

And yep, we can now see that 54.9G is used up and the compression ratio is 1.22x. Compression has definitely paid off!

### Delete everything in /home and mount the ZFS filesystem
Now to clean up and get the ZFS filesystem mounted at `/home`.

Delete the `/home` directory.

	:::text
	sudo rm -rf /home

Then change the mountpoint of `mypool/home` to `/home`. And while we are it we can stop `mypool` from mounting by setting it's mountpoint to `none`

	:::text
	sudo zfs set mountpoint=/home mypool/home
	sudo zfs set mountpoint=none mypool

Check that the files are there in `/home`.

	:::text
	$ ll /home
	total 22
	drwxr-xr-x  4 root root    4 Apr  6 12:40 ./
	drwxr-xr-x 24 root root 4096 Apr  6 12:46 ../
	drwx------  2 root root    2 Mar  4 17:42 lost+found/
	drwxr-xr-x 46 ross ross   72 Apr  6 13:57 ross/

Awesome! Everything is there and now on a ZFS filesystem.

### Reboot
Finally a quick reboot to make sure it mounts correctly on boot, there's no reason it shouldn't but better to be safe than sorry.

	:::text
	sudo reboot

And everything is there as expected. Success!

	:::text
	$ ll /home
	total 22
	drwxr-xr-x  4 root root    4 Apr  6 12:40 ./
	drwxr-xr-x 24 root root 4096 Apr  6 12:46 ../
	drwx------  2 root root    2 Mar  4 17:42 lost+found/
	drwxr-xr-x 46 ross ross   72 Apr  6 13:57 ross/

### Summary
This process would have been a bit less painful if I'd use a LiveCD environment as I wouldn't have to have copies of copies of my home directory but overall it seems to have gone well.

I'm going to keep `/temp-home` around for a week or so just incase something goes wrong but once I'm happy everything is okay that will be deleted.

The next steps are to learn more about ZFS snapshots and replication so that I can start using these for my backups. I'm pretty new to ZFS and this is the first time I've created pools and file systems in this manor, my only previous experience was in TrueNAS which gives a nice web UI interface for performing all these tasks.

I've heard great things about [sanoid](https://github.com/jimsalterjrs/sanoid) so I'm probably going to go with that for my snapshot and backup solution. I'll of course write a blog post about it but for now I'm just going to keep my `rsync` cronjob around for backups.

If you have any questions or suggestions for using ZFS please get in touch. Contact details be found [here]({filename}/pages/about.md).