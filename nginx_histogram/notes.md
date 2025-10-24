### whoami
- Saurabh Hirani
- Principal SRE at One2N
- Chief Head Of Talent Upskilling at One2N
	- They call me C.H.O.T.U
- My joke pronouns are...
	- `awk` / `sed` 
		- `awk`ward / `sed` istic
-------
### What's `init` for you?
- Learn how to generate histograms on the cli
- Play with some interesting shell commands

---
### The setup
-  Before
	  ```
		network_load_balancer -> nginx -> application
	  ```
-  After
	 ```
		load_balancer -> nginx -> if_application_endpoint -> application
		                       -> if_metrics_endpoint -> Prometheus
	  ```
- Not a good idea.
	- Should keep application and metric traffic different

---
### The problem
- Logs littered with warnings
	```
	A client request body is buffered to a temporary file /var/cache/nginx/client_temp/0014975406
	```
- Occurs when
	- Content size of the POST request was greater than the in-memory buffer size set by Nginx. 
	- The file was being cached to `/tmp`.
- Logs started showing errors sporadically
	```
	413 Request Entity Too Large 
	```
- Occurs when
	- POST body size > permissible limit for `client_max_body_size`
	
-------

### The solution
- Set the `client_max_body_size` to a higher value e.g. 64MB
- But it failed when Prometheus remote write requests exceeded 64 MB
- How to find the maximum `client_max_body_size` for the last X hours?
	- Update logging format to print content length
	- Ship logs to S3
	- Perform offline analysis
	- Get a realistic number
- End of story

---

### After thought

- Can this be done on the cli?
- Recommendation
	- Don't be a hero
	- This is just for to learn something new
	
---

### CLI approach
- Drink from the tcpdump firehose
- Get HTTP headers
- Extract `Content-Length` header
- Crunch them numbers

---

### Demo
- Log in to traffic- generator
	- ```
		docker-compose exec traffic-generator sh
	  ```
- Log in to Nginx
	- ```
		 docker-compose exec nginx sh
	  ```
- Generate traffic from traffic-generator
	- ```
		/scripts/generate_traffic.sh 100 1024
	  ```
- Capture metrics on Nginx
	- ```
		/scripts/capture_content_lengths.sh /tmp/content-lengths.txt
	  ```
- Analyze metrics on nginx
	- ```
		/scripts/analyze_metrics.sh /tmp/content-lengths.txt
	  ```
---

### Interesting commands
- shuf
	- ```
		shuf -i 1-10
		shuf -i 1-100  -n 10
		shuf -e 1 2 3 4
		find . -type f | shuf
	  ```
- head with /dev/urandom
	- ```
		head -c "10" /dev/urandom  | base64
	  ```
- percentile calculation
	- ```
		target_percentile=50
		
		# Calculate which line number contains the 50th percentile
		# 1000 lines -> 50 * 1000 / 100 = 500
		target_line=$(echo "$target_percentile * $TOTAL_LINES / 100" | bc)
		
		# sed -n "500p" prints only line 500
		P50=$(sed -n "${target_line}p" /tmp/sorted_sizes.txt)
	  ```
- paste
	- ```
		seq 1 10 | paste -sd+ -
		cd commands/paste
		paste numbers.txt letters.txt
		paste -s numbers.txt letters.txt
		paste -sd+ numbers.txt letters.txt
		cat letters.txt | paste - -
		cat letters.txt | paste - - -
		cat letters.txt | paste - - - -
	  ```
- tcpdump
	- ```
		tcpdump -A -vvv -nli any '(port 80) and (length > 74)' -s 0 -w - 2>/dev/null
		-vvv - Maximum verbosity (shows detailed packet info)
		-n - Don't resolve hostnames (show IP addresses as numbers)
		-l - Line buffered output (flush output immediately)
		-i any - Capture on all network interfaces
		'(port 80) and (length > 74)' - Capture filter:
		 # port 80 - Only HTTP traffic (port 80)
		 # length > 74 - Only packets larger than 74 bytes (filters out small ACK packets)
		-s 0 - Capture full packet (no truncation)
		-w - - Write output to stdout (dash means stdout)	
	  ```

###  I asked myself
- ![[are-you-not-entertained.jpg]]
---

### The answer I got

- ![[michael.gif]]
---

### Show me the ~~money~~ distribution!
- termgraph is pretty cool
	- ```
		# Generate percentile distribution (10%, 20%, 30%, etc.)
		cat /tmp/content-lengths.txt | cut -f2 -d':' | tr -d ' ' | /scripts/percentile.sh $(seq 1 10 | while read p; do echo "$p * 10" | bc; done) | termgraph
	  ```
- Increase granularity 
	- ```
		cat /tmp/content-lengths.txt | cut -f2 -d':' | tr -d ' ' | /scripts/percentile.sh $(seq 1 20 | while read p; do echo "$p * 5" | bc; done) | termgraph
	  ```
----

### Conclusion
- Fast feedback loops help
- Know your primitives
- Think in pipelines i.e. generate -> capture -> analyze -> visualize
- `exit 0`

### Questions

- Saurabh Hirani
- Setup - https://github.com/saurabh-hirani/talks/tree/master/cpu_promql
- https://www.linkedin.com/in/shirani/
- https://one2n.io/blog
- https://www.linkedin.com/company/one2nc/
