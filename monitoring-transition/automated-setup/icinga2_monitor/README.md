#### Demo setup of chef automated icinga2 host

- Start the vm

```
$ vagrant up
```

- Access the url - http://127.0.0.1:8085/icinga2-classicui/

- For the first run, the machine will be provisioned and will take time to setup. For subsequent runs, use the following command to just bring up the machine without going through the provisioning cycle:

```
$ vagrant up --no-provision
```
