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

### Example: Connection pool exhaustion

  - Failure mode: DB pool saturated -> new requests hang -> timeout cascade
  - Signal: active connections at pool max + rising request queue
  - Tool: app metrics (pgbouncer) - only if you expose it
  - Alert: `db_pool_active / db_pool_max > 0.9`
  - App -> Failure mode -> Alert

### Recommended approach

  - Start with failure modes
  - Who cares about these failures? e.g. application developer
  - What can go wrong? e.g. DB pool saturation
  - What signals can catch that scenario? e.g. `db_pool_active`
  - What tool emits that signal? e.g. exporter querying pgbouncer metrics
  - Start with that tool till you hit its limitations

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

### Who cares?

  - Platform/SRE: Is the service up? Is it slow?
  - FinOps: How much are we spending? Per user? Per model?
  - ML/AI Engineer: Is the RAG pipeline working correctly?
  - Product Manager: How long do users wait for answers?
  - Security/Compliance: What data is being sent to LLMs?

### Layers of AI observability

  - Application: is the service up, slow, erroring
  - User: who is calling, how often, at what cost
  - Retrieval: are the right documents being returned
  - Provider: is the LLM provider healthy, fast, reliable
  - Model: which model, how many tokens, what cost
  - Our questions in each demo will revolve around these layers

### Why layers matter

  - Failure modes live at specific layers
  - If you can only see the Application layer, everything looks like "app is slow"
  - Isolating layers tells you which subsystem is impacted
  - More layers visible = faster isolation = lower MTTI = lower MTTD
  - Each demo adds visibility into more layers

### The demo application

  - FastAPI app with 2 endpoints: /ingest and /ask
  - /ingest: chunk a document → embed → store in pgvector
  - /ask: embed query → vector search → top-K chunks → LLM generates answer
  - Same app across all experiments, only instrumentation changes

### Demo-1 - OTEL

  - Vanilla OpenTelemetry - fully manual
  - You write every span yourself

### Demo-1 - OTEL - effort vs reward

  - Effort: High - you instrument everything by hand
  - Reward: You see what you explicitly coded for, nothing more
  - Error-prone for LLM-specific signals
  - Good for HTTP/DB layer, poor ROI for LLM layer

### Demo-2 - OpenLLMetry

  - Zero code changes - just initialize the SDK
  - Auto-instruments OpenAI SDK calls

### Demo-2 - OpenLLMetry - effort vs reward

  - Effort: Near zero - SDK init + env vars
  - Reward: Full LLM visibility for free
  - Best ROI of any single step
  - But don't stop here - you're blind to retrieval quality
  - Don't throw away the tool. Augment it.

### Demo-3 - OpenLLMetry + manual instr

  - Same auto-instrumentation as Demo-2
  - Manual spans for embed, retrieve, vector_search, generate
  - Added custom metrics: similarity histogram, retrieve count, empty retrieval counter

### Demo-3 - OpenLLMetry + manual instr - effort vs reward

  - Effort: ~30 lines of code
  - Reward: Closes the biggest RAG blind spot (retrieval quality)
  - Most teams need this level
  - Failure mode analysis pays off - you instrument what matters

### Demo-3 - relevant document custom metric

  - Added `rag.retrieve.similarity` histogram
  - Added `rag.retrieve.count` and `rag.retrieve.empty` counters
  - Our failure mode analysis demanded them → we built them
  - Don't throw away your tool because it doesn't give you everything for free

### Demo-4 - OpenLLMetry + manual instr + AI Gateway

  - Route LLM calls through Bifrost gateway
  - Gateway emits its own telemetry (OTLP)

### Demo-4 - AI Gateway - effort vs reward

  - Effort: Infrastructure change (add gateway), no app code changes
  - Reward: Provider-level visibility, cost attribution, retry detection
  - Tradeoff: one more component that can fail (gateway itself becomes a dependency)
  - Worth it when: multi-provider, cost-sensitive, need provider SLA tracking
  - Not everyone needs this. Evaluate against your failure modes.

### What we didn't cover

  - Catching hallucination, quality regressions, bad chunking - harder parts
  - Metrics give you objective numbers. Learn domain specific subjective means e.g. evals

### The road ahead

  - OpenLLMetry is not a panacea - Python only, has its own gaps
  - Upcoming experiments - OpenLIT and more
  - No single tool will cover everything. And that's fine.
  - Know what's good enough today and stay flexible to change tomorrow.

### Closing thought

  "Large software systems are unpredictable and nondeterministic, with emergent behaviors. The mere existence of users injects chaos into the system. Components can be automated, but complexity can only be managed."

  — Charity Majors

### Questions?

  Twitter - @sphirani
  LinkedIn - linkedin.com/in/shirani/

### Histogram issue

  - Our p50 retrieval similarity showed 2.5
  - For a metric bounded at 0-1
  - Dashboard looked fine. Numbers were plausible. Nobody noticed.
  - Root cause: OTel default histogram buckets [0, 5, 10, 25, ...]
  - All similarity values (0.3-0.6) land in first bucket → interpolation gives garbage
  - Fix: explicit bucket boundaries [0, 0.1, 0.2, ..., 1.0]
  - Lesson: tools give you defaults. Defaults assume your use case. Verify.

### Other notes

  - What it means: OpenTelemetry has GenAI semantic conventions (https://opentelemetry.io/docs/specs/semconv/gen-ai/) that define standard attribute names like gen_ai.system, gen_ai.request.model, gen_ai.usage.input_tokens. But they're marked "Experimental" — the attribute names, metric names, and what's required vs optional can still change between releases. Libraries like OpenLLMetry implement these conventions today, but a future OTel release might rename or restructure them.
  - "We showed you tools and layers and failure modes. But here's the thing - you will never instrument your way to zero surprises. The best you can do is manage the complexity, not eliminate it. Charity Majors puts it well:"
