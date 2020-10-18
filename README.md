# line_monitor
Scripts to ping a host, record the round-trip-time, and graph the resulting report.

## Overview
I coded this project to record the uptime of my home internet. I'm running a
[Netgear R7000](https://www.netgear.com/home/products/networking/wifi-routers/R7000.aspx) router, which is
supported by the [DD-WRT project](https://wiki.dd-wrt.com/wiki/index.php/Netgear_R7000).

This firmware is capable of answering ping requests, as well as being able to run a dynamic DNS client. This project resolves
the dynamic DNC hostname to a real IP address, pings that IP, and then records the RTT to a CSV file. I run this container
on a cheap DigitalOcean droplet, and get an uninterupted report of my home's internet connection. 

## Project Structure
This project is dockerized, and is intended to be run in one of two modes:
1. Dev mode, where the `./docker.sh run` command maps the project's `app` directory into the container to facilitate live coding.
1. Production mode, where the contents of the `app` directory is actually copied into the image such that the resulting artifact
is suitable to be deployed in production, wholly self contained.

## Running In Dev Mode
To use this project in dev mode, use `docker.sh` to drive docker:
1. Ensure LINE_MONITOR_REPO in `docker.sh` is pointing to this project directory
1. Ensure your target hostname is exported: `export TARGET_HOST=foo.example.com` (dynamic dns services work nicely here)
1. Build the docker image with: `$ docker.sh build`
1. Create and run the container with: `$ docker.sh run` (the container will self-delete when stopped)

You should now have a container named `line_monitor` running in daemon mode. The output log/report are placed in the
`app/logs` and `app/reports` directories, repsectively.


## Running In Production Mode
To use this project in production mode:
1. Uncomment the second `COPY` command in the `Dockerfile` so that the `app` directory contents will physically be copied into the image, not just mapped
1. Execute `$docker.sh build` to pick up and build the above change
1. Push the new image (of course changing to your repository name): `$ docker push sgskinner/line_monitor:latest`
1. Pull the image on your production machine: `$ docker pull sgskinner/line_monitor`
1. Create a persistnant place for logs/reports on the host to map into the container:

        $ mkdir logs
        $ mkdir reports
1. And finally, start a new container with something like:

        #!/bin/bash

        TARGET_HOST="foo.example.com"
        export TARGET_HOST
        
        function main() {
            docker run \
                -d \
                -v "$HOME/logs:/usr/src/app/logs" \
                -v "$HOME/reports:/usr/src/app/reports" \
                -e TARGET_HOST="$TARGET_HOST" \
                --rm \
                --name line_monitor \
                sgskinner/line_monitor:latest
        }
        
        main

## Graphing the Ping Report
The `app/scripts/plot_line_report.py` script is currently meant for offline use. Meaning, this script is meant to be used
locally with a given reports file. The generated graph will be sent to your browser for viewing.

To use, `scp` the `reports/line-monitor.csv` to your local machine, ensure the `plot_line_report.py`'s input is pointed
at this file, and then execute.

This might be an opportunity for a new feature: Perhaps a django instance that will display the same directly on the remote host? 