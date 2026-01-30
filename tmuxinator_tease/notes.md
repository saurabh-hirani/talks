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
- An interesting debugging story around zshrc and kiro-cli

-------
### Pre-requisites
- kiro-cli
	- cli interface to interact with Kiro AI coding agent, developed by Amazon
	- Demo
- tmux
	- Terminal multiplexer
	- Demo
- tmuxinator
	- tmux session manager
	- Demo

-------
### Before the problems started

- tmuxinator worked
	- `tmuxinator start sample`
-------
### Something happened

	`./something.sh`
	
-------
### Tmuxinator impacted

- Odd behaviour in opening windows
	- `tmuxinator start sample`
	
- Implement workaround and moved on
	- `tmuxinator start sample`
	- `./sample-commands.sh`
	- tmuxinator `sends commands as key` to tmux
	- Ritual changed from 
		- `tmuxinator start sample` to `tmuxinator start sample && ./sample-commands.sh`
	
-------
### In parallel

- Had installed kiro-cli
- `Enabled autocomplete` in kiro-cli
- Didn't see any difference in ghostty
	- `echo $TERM_PROGRAM`
- Checked vscode - autocompletion worked
	- `echo $TERM_PROGRAM`
- Seemed like an over-eager programmer throwing hints at my face. Wanted to disable it. 

-------
### Stumbled upon a hint

- Googled disabling and found
	- `kiro-cli integrations uninstall dotfiles`
- Disabling auto-complete fixed the tmuxinator issue
	- `tmuxinator start sample`
- `something.sh` code
	- `kiro-cli integrations install dotfiles`
	- Done by kiro-cli during installation

-------
### What's going on?
- `kiro-cli integrations uninstall dotfiles`
- Why are dotfiles being changed?
- Check zshrc
	- `head ~/.zshrc`
	- `tail ~/.zshrc`

-------
### What does the pre-block generate?

- `~/.local/bin/kiro-cli init zsh pre --rcfile zshrc > /tmp/kiro_pre_block.sh`
- Something is happening which is messing with the way tmuxinator is sending keys to zsh
- Poked around with AI ("What can mess around with characters passed to a shell in this script?") and found
	- `Q_EXECUTION_STRING="${Q_EXECUTION_STRING}" Q_START_TEXT="$(printf "%b" "${INITIAL_TEXT}")" Q_SHELL="${Q_SHELL}" Q_IS_LOGIN_SHELL="${Q_IS_LOGIN_SHELL}" exec -a "${Q_TERM_NAME}" "${Q_TERM_PATH}"`
- exec!

----

### What impact does exec have on the current shell?

```
echo $$
zsh
echo $$
```

```
pstree -p $(echo $$)
```

vs

```
echo $$
exec zsh
echo $$
```

```
pstree -p $(echo $$)
```

---
### kiro-cli is doing something more

```
kiro-cli integrations install dotfiles
# new tab
echo $$
pstree -p $(echo $$)
```

vs

```
kiro-cli integrations uninstall dotfiles
# new tab
echo $$
pstree -p $(echo $$)
```
- Revisit
	- `Q_EXECUTION_STRING="${Q_EXECUTION_STRING}" Q_START_TEXT="$(printf "%b" "${INITIAL_TEXT}")" Q_SHELL="${Q_SHELL}" Q_IS_LOGIN_SHELL="${Q_IS_LOGIN_SHELL}" exec -a "${Q_TERM_NAME}" "${Q_TERM_PATH}"`
	- `Q_TERM_NAME="$(basename "${Q_SHELL}")`
	- `Q_TERM_NAME="zsh"`
	- `Q_TERM_PATH="kiro-cli-term"`
	- `exec -a "zsh (kiro-cli-term)" kiro-cli-term`
- Why `-a`?
	- `exec -a down top`

---
### kiro-cli sits between your emulator and shell

- Normal terminal:
	`Terminal Emulator (e.g. ghostty) ->  Shell (zsh/bash)`
	
- ~~Mentos~~  kiro terminal
	`Terminal Emulator -> kiro-cli-term (PTY wrapper) -> Shell (zsh/bash)`
	
- Why?
	- Creates a pseudo-terminal (PTY) - a virtual terminal device
	- Intercepts all input/output between terminal and shell
	 - Allows kiro-cli to capture commands, output, context and do fancy UIs
	 - Passes data through transparently (ideally)

---
### But why is tmuxinator teasing me with the printed but not executed command?

```
 # Get initial text.
    INITIAL_TEXT=""
    # shellcheck disable=SC2031
    if [[ -z "${BASH:-}" || "${BASH_VERSINFO[0]}" -gt "3" ]]; then
      while read -rt 0; do
        if [[ -n "${BASH:-}" ]]; then
          read -r
        fi
        INITIAL_TEXT="${INITIAL_TEXT}${REPLY}\n"
      done
    fi
```
- kiro-cli tries to ensure - If text was already piped or typed before the wrapper takes over 
	- Capture it
	- Replay it inside the wrapped terminal
	- Without this, keystrokes and piped input would be lost.

---
### The road to hell is paved with good intentions
- Tmuxinator sends commands via stdin to the pane
- PRE block consumes those commands into a variable
- The wrapper doesn't properly receive or execute the consumed commands

---
### One liner
- Why?
	- When kiro-cli-term receives the consumed stdin from the PRE block (via Q_START_TEXT), it's supposed to replay it to the shell as if you typed it. 
	- But maybe it's not properly preserving the newline characters that trigger command execution. 
	- Cannot debug further because
		- ```
		 file /Users/Saurabh.Hirani/.local/bin/kiro-cli-term
		    /Users/Saurabh.Hirani/.local/bin/kiro-cli-term: Mach-O universal binary with 2 architectures: [x86_64:Mach-O 64-bit executable x86_64] [arm64]
		    /Users/Saurabh.Hirani/.local/bin/kiro-cli-term (for architecture x86_64):	Mach-O 64-bit executable x86_64
		    /Users/Saurabh.Hirani/.local/bin/kiro-cli-term (for architecture arm64):	Mach-O 64-bit executable arm64
		  ```

---
### Other impact

```
kiro-cli integrations uninstall dotfiles
for i in $(seq 1 10); do time $SHELL -i -c exit; done
kiro-cli integrations install dotfiles
for i in $(seq 1 10); do time $SHELL -i -c exit; done
```

---
### Takeaways
- Value != cost
	- Know the value being provided and the cost you are incurring for it.
- Ask yourself
	- Do I actually want my shell process replaced at startup?
	- Am I comfortable trusting kiro-cli-term to sit between me and my shell?
	
---
### Post credits scene
- Speed check made me go from
	-  `cp ~/.zshrc.oh-my-zsh ~/.zshrc && for i in $(seq 1 10); do time $SHELL -i -c exit; done`
	- to
	- `cp ~/.zshrc.zimfw ~/.zshrc && for i in $(seq 1 10); do time $SHELL -i -c exit; done `
---
### echo $?

- Saurabh Hirani
- Setup - https://github.com/saurabh-hirani/talks/blob/master/tmuxinator_tease
	- Slides in `notes.md`
- https://www.linkedin.com/in/shirani/
- https://one2n.io/blog
- https://www.linkedin.com/company/one2nc/