#### Demo setup of a manually maintained icinga host

- Add the following entry in **/etc/hosts**:

```
127.0.0.1   manual.monitoring-transition.com automated.monitoring-transition.com
```

- Start the container

```
# sudo ./start-container.sh
```

- Access the url - http://manual.monitoring-transition.com:8080/icinga/
