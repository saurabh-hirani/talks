#### Demo setup of chef automated icinga2 host

- Add the following entry in **/etc/hosts**:

```
127.0.0.1   manual.monitoring-transition.com automated.monitoring-transition.com
```

- Start the vm

```
$ vagrant up
```

- Access the url - http://automated.monitoring-transition.com:8085/icinga2-classicui/

- For the first run, the machine will be provisioned and will take time to setup. For subsequent runs, use the following command to just bring up the machine without going through the provisioning cycle:

```
$ vagrant up --no-provision
```

- Setup [icinga2_api](https://github.com/saurabh-hirani/icinga2_api) on your host machine:

```
$ pip install icinga2_api
$ cat > ~/.icinga2/api.yml
vagrant:
  host: 127.0.0.1
  port: 5665
  user: root
  password: PASSWORD
  timeout: 5
  verbose: false
  verify: false
```

where PASSWORD is replaced by the password present in: 

```
/etc/icinga2/objects.d/api-users.conf
```

- Test the API

```
$ icinga2_api -p vagrant
```

should exit with status code 0
