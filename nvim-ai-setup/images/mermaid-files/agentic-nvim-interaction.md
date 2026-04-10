```mermaid
graph TD
    N[Neovim] -->|1. Spawn as child process| A[AI Agent]
    A <-->|2. JSON-RPC over stdin/stdout| N
```
