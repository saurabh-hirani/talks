### whoami
- 
	- Saurabh Hirani
	- Principal SRE at One2N
	- Reading, writing, systems engineering 🛠️

---
### Agenda
- 
	- CPU monitoring basics
	- That PromQL
	- Breaking it down 🔨
	- Building it up 🧱
------- 

### The AI angle
- 
	- No CPU == No AI

### Vibe alerting
- 
	- Google for "awesome prometheus alerts $resource"
	-  $resource = cpu | memory | ...
	- Copy paste the alert query
	- Critical operation
		- Pray 🙏
------

### The setup
- minikube
- [polinux/stress](https://hub.docker.com/r/polinux/stress)
- k9s

### Is load average of 10 high?
- 
	- Depends
------
### What is load average?
- 
	- A metric that measures system load.
	- How busy your system is at a given time.
	- Represents the average number of processes that are either:
		- Currently running on the CPU.
		- Waiting for the CPU to become available.
		- Waiting for I/O operations to complete.
------
### Reading load average
- 
	- Typically 3 numbers - 1.50, 1.25, 1.10
	- These represent the average load over:
		- Last 1 minute
		- Last 5 minutes
		- Last 15 minutes
------
### Interpreting load average

- 
	- Load == Number of cores: 
		- System is fully utilized but not overloaded.
	- Load < Number of cores: 
		- System has spare capacity.
	- Load > Number of cores: 
		- System is overloaded, processes are waiting.
	- 4 core system
		  - Load of 2.0 
			  - 50% utilization
		  - Load of 4.0 
			  - 100% utilization
		  - Load of 6.0 
			  - 150% utilization (overloaded)
------
### Utilization is in %
------

### Your alertmanager entry

```yaml
- alert: ContainerHighCpuUtilization 
  expr: (sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) by (pod, container) / sum(container_spec_cpu_quota{container!=""}/container_spec_cpu_period{container!=""}) by (pod, container) * 100) > 80 
  for: 2m 
  labels: 
	  severity: warning 
  annotations: 
	  summary: Container High CPU utilization (instance {{ $labels.instance }}) 
	  description: "Container CPU utilization is above 80%\n VALUE = {{ $value }}\n LABELS = {{ $labels }}"
```
- Looks like PromQL
	- Smells like ~~teen spirit~~ PromQ-Hell.
### K8s metric 

- `container_cpu_usage_seconds_total`
- Why is this in seconds?
------

### container_cpu_usage_seconds_total
- 
	- **counter** that tracks the total amount of CPU time a container has consumed since it **started**
		- 12:00:00 - init
		- 12:01:00 - running at 50% CPU
			- container_cpu_usage_seconds_total = 30
		- 12:02:00 - running at 50% CPU
			- container_cpu_usage_seconds_total = 30 + 30 = 60
		- 12:03:00 - running at 100% CPU
			- container_cpu_usage_seconds_total = 30 + 30 + 60 = 120
	- counter properties
	    - Never goes down. (until container restarts)
	    - Accumulates over time. (car's odometer)
	    - Raw value is not useful for current CPU usage.
	- counter rate
		- 12:00:00: 100 CPU seconds
		- 12:01:00: 105 CPU seconds
		- Rate = (105 - 100) / 60 = 0.083 CPU core
	- counter can span days
		- Tuesday at 10:00 AM: `container_cpu_usage_seconds_total` = 3600 (1 hour of CPU time over 25 hours)
		- Tuesday at 10:01 AM: `container_cpu_usage_seconds_total` = 3630 (30 more seconds in 1 minute)
		- Rate over the last 1 minute = (3630 - 3600) / 60 = 0.5 CPU cores (50% CPU usage in the last 1 minute)
---

### Show me the demo

```
./query.sh 'container_cpu_usage_seconds_total' -d '5 minutes ago' | less

./query.sh 'container_cpu_usage_seconds_total{pod=~"cpu-memory-demo.*"}' -d '5 minutes ago' | less

./query.sh 'rate(container_cpu_usage_seconds_total{pod=~"cpu-memory-demo.*"}[5m])' -d '5 minutes ago' | less

./query.sh 'sum(rate(container_cpu_usage_seconds_total{pod=~"cpu-memory-demo.*"}[5m]))' -d '5 minutes ago' | less

./query.sh '(sum(rate(container_cpu_usage_seconds_total{pod=~"cpu-memory-demo.*"}[5m])) by (container_name) / sum(container_spec_cpu_quota{pod=~"cpu-memory-demo.*"}/container_spec_cpu_period{pod=~"cpu-memory-demo.*"}) by (container_name) * 100)' -d '5 minutes ago' | less
```

### Break it down

- Numerator = `(sum(rate(container_cpu_usage_seconds_total{pod=~"cpu-memory-demo.*"}[5m])) by (container_name)` == A
- Denominator = `sum(container_spec_cpu_quota{pod=~"cpu-memory-demo.*"}/container_spec_cpu_period{pod=~"cpu-memory-demo.*"}) by (container_name) * 100)' -d '5 minutes ago`  == B
- Denominator 
	- Numerator =  `container_spec_cpu_period{pod=~"cpu-memory-demo.*"}` = B1
	- Denominator =  `container_spec_cpu_period{pod=~"cpu-memory-demo.*"}` = B2
- Abstraction = `A / (B1 / B2) * 100`

### container_spec_cpu_period
```
./query.sh 'container_spec_cpu_period' -d '5 minutes ago' | less
```
- What is that number?
	- 100000 microseconds = 100 ms
- What does it mean?
	-  Quota enforcement window:
		- Every 100ms, the kernel scheduler checks if container exceeded its CPU **quota**.
		- If exceeded - **throttle**  the container.
		- If not exceeded - **allow** container to continue.
	- NOT 
		- Scheduler frequency:
			- Kernel scheduler runs much more frequently (every few milliseconds).
			- 100ms period is just the **quota** accounting window.
			- Scheduler and **quota** enforcement are separate mechanisms.
		- Time slices:
		    - Container doesn't get "100ms to run, then stop".
		    -  Container can run continuously as long as it stays within **quota**.
		    - **Throttling** only happens when **quota** is exceeded withi'n the 100ms window.
---
### container_spec_cpu_quota
```
./query.sh 'container_spec_cpu_quota' -d '5 minutes ago' | less
./query.sh 'container_spec_cpu_quota{pod=~"cpu-memory-demo.*"}' -d '5 minutes ago' | less
```
- Do the math
	- cpu_quota / cpu_period
	- `30000 / 100000 = 0.3`
	- This what we know as:
		- CPU limit
		  ```yaml
		     resources:
	         requests:
		         memory: "64Mi"
		         cpu: "100m"
	         limits:
		         memory: "128Mi"
		         cpu: "300m" # <---------
		  ```
    - This implies
		m = thousandth of a core - `300/1000 = 0.3`
	- Your container gets:
	    - 30ms of CPU time every 100ms.
	    - 70ms of waiting/idle time every 100ms (if tries to use more)
	    - This enforces the 300m CPU limit.

### Updated query
- 
	-  `A / (B1 / B2) * 100` 
	-  `A / (0.3) * 100` 

### Can CPU usage exceed 100%?
```
./query.sh '(sum(rate(container_cpu_usage_seconds_total{pod=~"cpu-memory-demo.*"}[5m])) by (container_name) / sum(container_spec_cpu_quota{pod=~"cpu-memory-demo.*"}/container_spec_cpu_period{pod=~"cpu-memory-demo.*"}) by (container_name) * 100) > 101' -d '30 minutes ago'
```
- Sample output
	- ``` "values": [ [ 1760120423, "101.68000388888889" ] ]```

### Limits can be exceeded momentarily
- 
	- Linux CFS (completely fair scheduler) scheduler granularity - doesn't enforce limits at microsecond precision.
	- Burst allowance - containers can briefly exceed limits before being throttled.
	- Measurement timing - rate() captures these brief spikes over 5-minute windows.

### How does throttling work?

- Container tries to use more than 300m.
- Briefly succeeds (causing >100% reading)
    - CFS makes scheduling decisions every few milliseconds.
    - Container can burst above limit between scheduling decisions.
    - Throttling happens when CFS checks and finds quota exceeded.
    - Brief burst is normal before throttling kicks in.
	- Throttling kicks in (container gets blocked).
	- Usage drops back down.

### Revisit the alert
 ```
 ./query.sh '(sum(rate(container_cpu_usage_seconds_total{pod=~"cpu-memory-demo.*"}[5m])) by (container_name) / sum(container_spec_cpu_quota{pod=~"cpu-memory-demo.*"}/container_spec_cpu_period{pod=~"cpu-memory-demo.*"}) by (container_name) * 100) > 80' -d '10 minutes ago'
 ```
 - Tells you
	 - How much is my usage as compared to the limits?
	 - If it is greater than 80% - raise an alert.
### Do you really want this alert?

- Would you rather
	- alert every time you hit or are about to hit 100% limits? 
	- OR 
		- Would you alert if you hit the limit beyond an acceptable window?
- Would you rather 
	- Have a smoke detector that goes off every time you cook?
	- OR
		- have one that alerts if there is sustained smoke?
-  Would you rather
	- Use the Linux cli and demo with raw numbers
	- OR
		- use the Linux cli and demo with raw numbers

### Another alert

```
./query.sh 'sum(rate(container_cpu_cfs_throttled_seconds_total{pod=~"cpu-memory-demo.*"}[5m])) / sum(rate(container_cpu_cfs_periods_total{pod=~"cpu-memory-demo.*"}[5m])) * 100' -d '10 minutes ago'
```

- 
	- Tell me how much of the time I am being throttled?
	- Your 9s are not important if
		- Your users are not happy.

### container_cpu_cfs_periods_total

```
./query.sh 'container_cpu_cfs_periods_total{pod=~"cpu-memory-demo.*"}' -d '10 minutes ago'
./query.sh 'sum(rate(container_cpu_cfs_periods_total{pod=~"cpu-memory-demo.*"}[5m]))' -d '10 minutes ago'
./query.sh 'rate(container_cpu_cfs_periods_total{pod=~"cpu-memory-demo.*"}[5m])' -d '10 minutes ago'

```
- Each period 
	- 100ms (0.1 seconds) ➡️
		- 10 periods per second ➡️
			- 20 periods for 2 containers

### container_cpu_cfs_throttled_seconds_total
```
./query.sh 'sum(rate(container_cpu_cfs_throttled_seconds_total{pod=~"cpu-memory-demo.*"}[5m]))' -d '10 minutes ago'
./query.sh 'rate(container_cpu_cfs_throttled_seconds_total{pod=~"cpu-memory-demo.*"}[5m])' -d '10 minutes ago'
```
- 
	- Counter representing how many seconds was the container throttled till now?

### Bring it all together

```
./query.sh 'sum(rate(container_cpu_cfs_throttled_seconds_total{pod=~"cpu-memory-demo.*"}[5m])) / sum(rate(container_cpu_cfs_periods_total{pod=~"cpu-memory-demo.*"}[5m])) * 100' -d '10 minutes ago'
```
- English
	-  Every second, your containers get 20 chances to run (10 per container)
	- ~3 of those chances result in "sorry, you're over your limit, wait"
	- 15.4% rejection rate for CPU time requests (3/20)
- Decide your degradation
	-   **0% throttling** = Container runs whenever it needs CPU
	-  **10% throttling** = Container is blocked 10% of the time (noticeable slowdown)
	- **50% throttling** = Container is blocked half the time (significant performance issues)
	- **90% throttling** = Container barely gets to run (severe performance problems)
### This vs that query
``
```
- alert: ContainerHighCpuUtilization 
  expr: (sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) by (pod, container) / sum(container_spec_cpu_quota{container!=""}/container_spec_cpu_period{container!=""}) by (pod, container) * 100) > 80 
  for: 2m 
  labels: 
	  severity: warning 
  annotations: 
	  summary: Container High CPU utilization (instance {{ $labels.instance }}) 
	  description: "Container CPU utilization is above 80%\n VALUE = {{ $value }}\n LABELS = {{ $labels }}"
```

vs

```yaml
- alert: ContainerHighCpuThrottling 
  expr: (sum(rate(container_cpu_cfs_throttled_seconds_total{container!=""}[5m])) by (pod, container) / sum(rate(container_cpu_cfs_periods_total{container!=""}[5m])) by (pod, container) * 100) > 10 
  for: 2m 
  labels: 
	  severity: warning 
  annotations: 
	  summary: Container High CPU throttling (instance {{ $labels.instance }}) 
	  description: "Container CPU throttling is above 10%\n VALUE = {{ $value }}%\n LABELS = {{ $labels }}"
```

- 
	- Utilization vs Saturation (USE metrics)
	
### Remember

- 
	- It's only magic till you learn the trick.
		- Don't start with alerts.
		- Start with failure modes.
		- Work your way to the alert.
	
### self.throttled - Questions?

- Saurabh Hirani
- Setup - https://github.com/saurabh-hirani/talks/tree/master/cpu_promql
- https://www.linkedin.com/in/shirani/
- https://one2n.io/blog
- https://www.linkedin.com/company/one2nc/
