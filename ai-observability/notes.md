### AI Observability Maturity

### $ whoami
  - Saurabh Hirani
  - Principal SRE at One2N
  - Infrastructure and reliability engineering
  - Joke pronouns - sed / awk
  - Sed-istic and Awk-ward

### What this talk is not about?
  - A hello-world exploration of tools
  - "I evaluated 20 tools in 2 hours so you don't have to"
  - "XYZ tool is the best"

### What's init for you?
  - A way to think about AI observability from first principles
  - How to evaluate what's good enough at your stage
  - Customer learnings compressed in demos
  - An open source repo you can tinker with

### Everybody wants to know...
  - What tool should I use for AI observability?
  - I don't want to waste time exploring what's already out there

### Everybody should ask...
  - Do I need instrumentation?
  - What am I instrumenting for?
  - Correctness - Is my AI application giving the right answers?
  - Performance - Is it doing so fast enough and cheap enough?
  - Is the tooling aligned with my current organizational priorities?

### Am I adopting what is trending?

### The default way to set alerts

- Google for dashboard for X
- Import said dashboard
- Google for alerts for X
- Copy paste said alerts
- Pray / Complain
- Same for instrumentation libraries / other tools

### Problems

- You are measuring what is easy
- You are not questioning what is right?
- Tools don't care about your failure modes
- Failure mode = blueprint - Alert = implementation
- Don't go oncall without knowing the failure modes you are responsible for

### Our approach
  - Start with failure modes
  - What can go wrong?
  - What signals can catch that scenario?
  - What tool emits that signal?
  - If the tool falls short - can I augment it manually?

### What we built
  - Worked with customers and saw addressable AI observability gaps
  - Solved with minimal intrusion
  - 2 customers - both using RAG applications
  - Compressed those learnings in a demo app with experiments

### Pre-requisite: What is RAG?
  - Retrieval Augmented Generation
  - Give the LLM relevant context so it answers from your data, not its training data
  - Two phases: Ingest and Ask

### RAG - Ingest phase
  - Take a document (PDF, text, etc.)
  - Split it into chunks
  - Embed each chunk (text → vector)
  - Store vectors in a vector database (pgvector)
  - This is a one-time setup per document

### RAG - Ask phase
  - User asks a question
  - Embed the question (text → vector)
  - Search vector DB for top-K similar chunks
  - Send chunks + question to LLM
  - LLM generates answer grounded in your data

### The demo application
  - FastAPI app with 2 endpoints: /ingest and /ask
  - /ingest: chunk a document → embed → store in pgvector
  - /ask: embed query → vector search → top-K chunks → LLM generates answer
  - Same app across all experiments, only instrumentation changes

### Demo-1 - OTEL
  - Vanilla OpenTelemetry - fully manual
  - You write every span yourself

### Demo-1 - OTEL - what you can answer ✅
  - Is my app up?
  - Why is my app slow?
  - Is the database connection failing?
  - Which RAG step is the bottleneck?

### Demo-1 - OTEL - what you can't answer ❌
  - How many tokens did this call use?
  - Which model was called?
  - What prompt was sent?
  - Is my embedding call failing?

### Demo-1 - OTEL - effort vs reward
  - Effort: High - you instrument everything by hand
  - Reward: You see what you explicitly coded for, nothing more
  - Error-prone for LLM-specific signals
  - Good for HTTP/DB layer, poor ROI for LLM layer

### Demo-2 - OpenLLMetry
  - Zero code changes - just initialize the SDK
  - Auto-instruments OpenAI SDK calls

### Demo-2 - OpenLLMetry - what you can answer ✅
  - How many tokens did this call use?
  - Which model was called?
  - What prompt/completion was sent?
  - Is the LLM provider slow?
  - Is the embedding API failing?
  - Am I blowing my token budget?

### Demo-2 - OpenLLMetry - what you can't answer ❌
  - Are the retrieved chunks relevant?
  - Which user is burning tokens?
  - Is the vector DB connection failing?
  - Did retrieval return zero results?

### Demo-2 - OpenLLMetry - effort vs reward
  - Effort: Near zero - SDK init + env vars
  - Reward: Full LLM visibility for free
  - Best ROI of any single step
  - But don't stop here - you're blind to retrieval quality
  - Don't throw away the tool. Augment it.

### Demo-3 - OpenLLMetry + manual instr
  - Same auto-instrumentation as Demo-2
  - Added ~30 lines: manual spans for embed, retrieve, vector_search, generate
  - Added custom metrics: similarity histogram, retrieve count, empty retrieval counter

### Demo-3 - OpenLLMetry + manual instr - what you can answer ✅
  - Is retrieval quality degrading?
  - Are retrievals returning empty?
  - Is the vector DB connection failing?
  - Which user is burning tokens?
  - Everything from Demo-2

### Demo-3 - OpenLLMetry + manual instr - what you can't answer ❌
  - Which provider is causing latency?
  - How many retries is the provider causing?
  - What's the per-model cost breakdown?
  - If you're single-provider, you might stop here.

### Demo-3 - OpenLLMetry + manual instr - effort vs reward
  - Effort: ~30 lines of code
  - Reward: Closes the biggest RAG blind spot (retrieval quality)
  - Most teams need this level
  - This is where failure mode analysis pays off - you instrument what matters

### Histogram issue
  - Our p50 retrieval similarity showed 2.5
  - For a metric bounded at 0-1
  - Dashboard looked fine. Numbers were plausible. Nobody noticed.
  - Root cause: OTel default histogram buckets [0, 5, 10, 25, ...]
  - All similarity values (0.3-0.6) land in first bucket → interpolation gives garbage
  - Fix: explicit bucket boundaries [0, 0.1, 0.2, ..., 1.0]
  - Lesson: tools give you defaults. Defaults assume your use case. Verify.

### Demo-3 - relevant document custom metric
  - Added `rag.retrieve.similarity` histogram
  - Added `rag.retrieve.count` and `rag.retrieve.empty` counters
  - These don't come from any library
  - Our failure mode analysis demanded them → we built them
  - This is what "augment the tool manually" looks like in practice
  - Don't throw away your tool because it doesn't give you everything for free

### Demo-4 - OpenLLMetry + manual instr + AI Gateway
  - Route LLM calls through Bifrost gateway
  - Gateway emits its own telemetry (OTLP)

### Demo-4 - AI Gateway - what you can answer ✅
  - Which provider is causing latency?
  - How many retries is the provider causing?
  - What's the per-model cost breakdown?
  - Is my API key/virtual key valid?
  - What's the gateway success rate?
  - Everything from Demo-3

### Demo-4 - AI Gateway - what you can't answer ❌
  - Is the model giving worse answers?
  - Is the LLM hallucinating?
  - Are my chunks too large/small?
  - These need an eval layer, not an observability layer
  - Know where observability ends and evaluation begins

### Demo-4 - AI Gateway - effort vs reward
  - Effort: Infrastructure change (add gateway), no app code changes
  - Reward: Provider-level visibility, cost attribution, retry detection
  - Worth it when: multi-provider, cost-sensitive, need provider SLA tracking
  - Not everyone needs this. Evaluate against your failure modes.

### Questions?

  Twitter - @sphirani
  LinkedIn - linkedin.com/in/shirani/
