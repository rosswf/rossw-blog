Title: Homelab Tour
Date: 2021-05-22 14:30
Tags: homelab, proxmox, microserver 
Summary: A brief tour of my humble, space-limited homelab. What I'm running and what I use it for.
slug: homelab-tour 
Description: A brief tour of my humble, space-limited homelab. What I'm running and what I use it for.

Today, I'm going to be telling you about my small homelab which I started putting together only in November last year. I don't have much space and wanted something quiet and power-efficient. The HPE MicroServer Gen8 seemed very popular online and could be picked up relatively cheaply on the second hand market, but the hardware seems to be showing its age. After a bit of research and an incredible review by [ServeTheHome](https://www.servethehome.com/hpe-proliant-microserver-gen10-plus-review-this-is-super/), I settled on starting out with the HPE MicroServer Gen10 Plus.

### Hardware
**HPE MicroServer Gen10 Plus**

- CPU: Intel Xeon E-2224
- RAM: 32gb DDR4-2226 ECC (Upgraded from the standard 16gb)
- OS Storage: WD Blue 500gb NVME (PCIe card required)
- Bulk Storage: 4x 4TB WD Red Plus SATA

The specs are nothing to write home about but it is perfect for my needs (for now) and the form factor is great; it easily fits on a bookshelf. I also purchased the iLO enablement kit which is required to utilise iLO on this particular model.

**Raspberry Pis**

I have a cluster of 4 Raspberry Pi 4B's that used to act as my home lab before I bought something a bit more robust in the MicroServer. My intention for these is to set them up in a kubernetes cluster as workers. I'll probably need to run the master in a virtual machine as they just won't have enough memory for that, but they should be perfectly fine as workers.

**Network Gear**

Right now, I have a fairly cheap ethernet switch and a wireless access point. I am looking to upgrade to a managed switch in the future so if anybody has any recommendations, please let me know!

**UPS - Cyberpower 1500VA/900W**

I chose this one because it wasn't too expensive compared to the other options out there. It gives me plenty of headroom for what I need and also has x2no regular UK plug outlets alongside the x4 EIC C13 which is great for connecting my modem, network switch, and other items that just have a plug.

It comes with software that allows it to send a shutdown signal to a device if the power is out for a certain amount of time. My server runs 24/7 and being able to have it cleanly shut down if there is a power outage while I'm away or sleeping provides me with peace of mind, which is great.

The other benefit of a UPS is it always ensures that any connected devices have clean power.


### Software

I'm running [Proxmox VE](https://www.proxmox.com/en/) as the OS on the MicroServer. I’ve never used this kind of hypervisor before, but I have found proxmox really easy to get up and running with. There are a whole host of advanced features that I haven't had a chance to dive into yet.

There are a number of Virtual Machines and LXC Containers that form my homelab:

![Proxmox Dashboard]({static}/images/homelab-tour/homelab-tour-proxmox-dashboard.webp)

**Virtual Machines**

- truenas - This runs [TrueNAS Core](https://www.truenas.com/) with the 4x 4TB hard drives passed through to it and serves as my home NAS.
- pfsense - This runs [pfSense Community Edition](https://www.pfsense.org/). I've talked about this in some previous posts where I've discussed setting up [OpenVPN]({filename}/pfSense/openvpn-pfsense.md) and [network booting Ubuntu 21.04]({filename}/pfSense/pxeboot-ubuntu-pfsense.md).
- atom - This isn't running anything specialised, it's just a standard [Ubuntu](https://ubuntu.com/) Server 20.04 VM. I use it mainly for testing, at the moment it's mainly used as a bit of a docker playground.

**Containers**

I try to keep everything in its own single container so that if there are ever any issues, I can just kill the container and create a new one from backup. It makes configuration way more straight forward.

- pihole - A container that just runs [pihole](https://pi-hole.net/) for DNS level ad-blocking across my entire network and is also used as DNS for all of my local infrastructure. As an example, I can access truenas by navigating to https://truenas.rossw.co.uk.
- minecraft-e2e - A container running a small minecraft server for some friends.
- jupyter - A container running [JupyterLab](https://jupyter.org/) for easy access to notebooks from any of my devices.
- code - A container running [VS Code Server](https://github.com/cdr/code-server) which allows access to VS Code from a browser. I don't really use this as much as I used to, but it is handy for not having to configure and install plugins on a device that I'm going to be using infrequently. It is also nice for getting access to a bash shell on devices that don't support that.
- influxdb - A container running an instance of [InfluxDB](https://www.influxdata.com/). I'm currently using this to store temperature data for a project I'm working on where I have a raspberry pi hooked up to a temperature sensor and then a Flask app to display the data. I'm planning to rewrite this project entirely using FastAPI instead of Flask with a JS framework front-end (most likely Vue). Watch this space for updates!
- mongodb - A container running an instance of [MongoDB](https://www.mongodb.com/). I'm not really using this at the moment, I had set it up for use with a project but that is on the back burner right now. It'll get some use eventually.
- jenkins - A container running jenkins, at the moment it is responsible for building and deploying this blog whenever there are any updates! I intend to write about this later in my blog series on deploying this Blog. You can check out [part 1]({filename}/Terraform/blog-part1.md) now which covers provisioning using terraform.
- irc - A container running [WeeChat](https://weechat.org/) for the few times that I do use IRC. I use [Glowing Bear](https://www.glowing-bear.org/) as a front end so I can access it from any device. I would definitely recommend this setup for anybody that regularly uses IRC.
- bitwarden - I have only recently set this up with the intention of using it to self host [bitwarden](https://bitwarden.com/) and still needs some work, but once it is up and running, I'll be writing a blog post about it. I have written about setting up [OpenVPN on pfSense]({filename}/pfSense/openvpn-pfsense.md) so that once it is all set up, I can access it from anywhere.

### Summary

Well that's everything I'm running! As you can see from the dashboard, I still have a bit of headroom available and have plans in the future to look into setting up [Traefik](https://bitwarden.com/), getting a proper Kubernetes setup going, and some sort of smart home automation. 

If any of you have a homelab or can recommend anything that's worth self hosting, please get in touch! Contact details be found [here]({filename}/pages/about.md).
