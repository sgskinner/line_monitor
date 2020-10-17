# line_monitor
Scripts to ping a host, record the round-trip-time, and graph the resulting report.

## Project Structure
This project is dockerized, and is intended to be run in one of two modes:
1. Dev mode, where the `docker run` command maps this `app` directory into the container to facilitate live coding
1. Production mode, where the contents of the `app` dir is actually copied into the image such that the resulting artifact
is suitable to be deployed in production, wholly self contained

To use this project in dev mode, use `docker.sh` to drive docker:
1. Ensure LINE_MONITOR_REPO in `docker.sh` is pointing to this project directory
1. Ensure your target hostname is exported: `export TARGET_HOST=foo.example.com` (dynamic dns services work nicely here)
1. Build the docker image with: `$ docker.sh build`
1. Create and run the container with: `$ docker.sh run` (the container will self-delete when stopped)

You should now have a container named `line_monitor` running in daemon mode. The output log/report are placed in the
`app/logs` and `app/reports` directories, repsectively.

To use this project in production mode:
1. Uncomment the second `COPY` command in the `Dockerfile` so that the `app` directory contents will physically be copied into the image, not just mapped
1. Execute `$docker.sh build` to pick up and build the above change
1. Push the new image (of course changing to your repository name): `$ docker push sgskinner/line_monitor:sgskinner`
1. Pull the image on your production machine: 