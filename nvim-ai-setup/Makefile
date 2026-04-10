.PHONY: images

images:
	@for f in images/mermaid-files/*.md; do \
		name=$$(basename "$$f" .md); \
		awk '/^```mermaid/{found=1;next} /^```/{found=0} found' "$$f" > "/tmp/$$name.mmd"; \
		mmdc -i "/tmp/$$name.mmd" -o "images/$$name.png"; \
		rm "/tmp/$$name.mmd"; \
		echo "Generated images/$$name.png"; \
	done
