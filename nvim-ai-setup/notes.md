### whoami
- Saurabh Hirani

- Principal SRE at One2N

- Chief Head Of Talent Upskilling at One2N
	- They call me C.H.O.T.U

- My joke pronouns are...
	- `awk` / `sed`
		- `awk`ward / `sed` istic

- Proof
  - What would you call an upcoming area near aiport?
    - Neovim-annagar

---

### What's `init` for you?

- Peek under the hood of how agents and editors communicate

- neovim > your_editor ❌

- You do you ✅
---

### Why should you care if you're happy with your editor?

- Steal like an artist - good ideas cross editor boundaries

- See what you like -> adopt what makes you faster -> discard the rest

- Today's niche feature -> tomorrow's mainstream default

  - Did you imagine agentic UX would be better on CLI than editor chat windows?
---

### vi -> vim -> neovim

- vi (1976) - Bill Joy, visual mode for ex editor

- vim (1991) - Bram Moolenaar, "Vi IMproved"
  - VimScript for configuration and plugins

- neovim (2014) - fork of vim by Thiago de Arruda
  - Lua as first-class config/plugin language
---

### Where was I ?

- Pre-AI era
  - (Happy?) neovim user

- AI era begins..
  - FOMO of - "My neovim doesn't have a chat window"
  - See - agent chat window
    - :!open images/vscode-chat-window.png
  - Moves to vscode

- Today
  - (Happy!) neovim user

---

### The moment of truth

- See - jumping from editor to terminal
  - :!open images/vscode-to-terminal-jump.png
- If the agent has come to the terminal, so should my editor!

---

### Agents covered

- Claude code

- Opencode

- That's it ❌
  - Everything else! ✅

### Claude code

- [claudecode.nvim](https://github.com/coder/claudecode.nvim)

- See - nvim to Claude code flow
  - :!open images/claudecode-nvim-interaction.png

- Flow
  1. Neovim: Starts a WebSocket server on a random localhost port
  2. Neovim: Writes a lock file to ~/.claude/ide/[port].lock with port + auth token
  3. Claude: Reads the lock file to discover the connection details
  4. Claude: Connects to Neovim's WebSocket using the auth token
  5. Neovim: Pushes selection/context changes to Claude over WebSocket
  6. Claude: Calls tools (openFile, openDiff, getDiagnostics) back through WebSocket

- Validate
  - $HOME/.claude/ide/

- Keys
  - ,ac - start the websocket
  - ,as - send to claude
  - ,aa - accept diff
  - ,ad - deny diff

### Opencode

- [opencode.nvim](https://github.com/nickjvandyke/opencode.nvim)

- See - nvim to Opencode flow
  - :!open images/opencode-nvim-interaction.png

- Flow
  1. Opencode: Starts an HTTP + SSE server on a localhost port
  2. Neovim: Discovers opencode by scanning running processes for the port
  3. Neovim: Sends commands to opencode via REST API (curl)
  4. Opencode: Streams events back to Neovim via SSE (session updates, diffs, permissions)
  5. Neovim: Runs an in-process LSP that calls opencode run for hover/code actions

- Keys
  - ,oc - start Opencode
  - Join Opencode to next tab
  - ,os - send events to Opencode

### Design choices

- claudecode.nvim
  - WebSocket
    - Phone call
    - Neovim starts a WebSocket server, Claude connects to it
    - Both send messages to each other on the same connection
    - One two-way channel for all communication

- opencode.nvim
  - SSE
    - Radio broadcast
    - Neovim listens to Opencode via SSE (one-way stream)
    - Neovim sends events to Opencode via HTTP/curl (separate requests)
    - Two one-way channels instead of one two-way connection

### Pi / Kiro / XYZ

- ACP - Agent Client Protocol - to the rescue
- Standardizes communication between code editors/IDEs and coding agents
- See - Rejected ACP
  - :!open images/rejected-acp.png
- See - Accepted ACP
  - :!open images/agentic-nvim-interaction.png
- ACP to agents is what Language Server Protocol is for editors.
- Native text window

- Keys
  - ,kt - Toggle agentic chat
  - ,ks - Send context
  - ,s  - switch ACP providers mid way (kiro to opencode)
  - ,m  - change models

### ACP limitations

- Not all agents implement the full spec
- Kiro implements ACP but many slash commands are missing
- "Write once, works with any agent" isn't fully there yet

### Best of both the worlds

- Editor to any agent communication (like agentic.nvim)
- Full control over any agent (like claudecode.nvim)

### prompt-picker to the rescue

- [prompt-picker](https://github.com/saurabh-hirani/prompt-picker.nvim)

- See - Attention and tmux is all you need
  - :!open images/prompt-picker-interaction.png

- Flow

  1. User: Selects text or places cursor in Neovim
  2. Neovim: Opens prompt picker with predefined + custom prompts
  3. prompt-picker: Renders template with context (file, selection, diagnostics)
  4. prompt-picker: Sends rendered prompt to AI agent in tmux pane via tmux send-keys

- Advantages
  - No protocol, no server - just text over tmux
  - Decoupled: I neither know or care which agent is in the tmux pane
    - Works with any CLI agent
    - Swap agents without changing a single line of config
  - Customize prompts

- Keys
  - ,pa - adhoc prompt
  - ,pp - your prompts to render
  - ,pR - reload config

### Race your agents!

### How to ask why

- [code-explainer](https://github.com/saurabh-hirani/code-explainer.nvim)
- See - diffs powered by your agent
  - :!open images/code-explainer-interaction.png

- Keys
  - ,qd - open diff window
  - ,qt - open current file

### Conclusion

- Know how you talk to your agents
- Hold your agents accountable for what and why
- YOLO -> YOLO SOLR

### Questions?

- Saurabh Hirani
- Setup - https://github.com/saurabh-hirani/talks/tree/master/cpu_promql
- https://www.linkedin.com/in/shirani/
- https://one2n.io/blog
- https://www.linkedin.com/company/one2nc/

### References

- WebSocket
  - Think of it like a phone call — both parties can talk whenever they want.
  - A persistent two-way connection between client and server.
  - Either side can send messages at any time.

- SSE (Server-Sent Events)
  - Think of it like a radio broadcast — you listen, but to talk back you make a separate call (HTTP request).
  - A one-way stream from server to client over HTTP.
  - The server pushes updates, but the client can't send messages back on the same connection.

- LSP (Language Server Protocol)
  - Standardized how editors talk to language tools.
  - Before LSP, every editor had its own way of getting autocomplete, go-to-definition, diagnostics, etc.
  - LSP made it so one language server works with any editor.
  - Editor implements an LSP client, and the language tool implements an LSP server.
  - They talk to each other over a standard protocol (JSON-RPC).
