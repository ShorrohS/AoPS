# Module 7.4 — Building a Tiny Shell

---

## The Problem

> The shell is the user's interface to the operating system.
> Every time you type `ls -la | grep .py > output.txt`,
> something reads that line, parses it, and executes it.
>
> Building a tiny shell from scratch teaches you:
> - How `fork()` + `exec()` work together to create processes
> - How pipes are implemented at the OS level
> - How input/output redirection works
> - What the shell actually does when you type a command

---

## The Story

### The Shell as the First Application

The shell was the very first interactive program run by Unix — it was already present in the initial PDP-7 Unix system in 1969. Ken Thompson wrote the first Unix shell (the Thompson shell, `sh`) in a single weekend.

**Stephen Bourne** rewrote it in 1977 as the Bourne shell (`/bin/sh`) — the ancestor of every POSIX-compatible shell today. **Bill Joy** (founder of Sun Microsystems) wrote the C shell (`csh`) in 1978, adding job control and command history. **David Korn** wrote the Korn shell (`ksh`) in 1983, combining features of both. The **Bash** shell (Bourne Again SHell, Brian Fox, 1989) is the default on most Linux systems today.

All of these shells — despite their different features and syntaxes — implement the same fundamental mechanics: read a line, parse it, `fork()`, `exec()`, `wait()`.

---

## The Concept

### The Core Loop: REPL

A shell is a **Read-Eval-Print Loop**:

```python
import os, sys, subprocess

def shell():
    while True:
        # 1. Print prompt
        try:
            line = input(f"{os.getcwd()} $ ")
        except (EOFError, KeyboardInterrupt):
            print(); break

        line = line.strip()
        if not line: continue

        # 2. Parse
        parts = line.split()

        # 3. Built-in commands
        if parts[0] == 'exit':
            break
        if parts[0] == 'cd':
            try: os.chdir(parts[1] if len(parts) > 1 else os.environ.get('HOME', '/'))
            except FileNotFoundError as e: print(f"cd: {e}")
            continue

        # 4. Execute external command
        try:
            proc = subprocess.run(parts)
        except FileNotFoundError:
            print(f"{parts[0]}: command not found")

shell()
```

### fork() + exec() — The Unix Process Model

Under the hood, `subprocess.run(['ls', '-la'])` does exactly this:

```python
import os

pid = os.fork()
if pid == 0:
    # Child process
    os.execvp('ls', ['ls', '-la'])   # replace child with 'ls'
    # execvp never returns on success
    sys.exit(1)
else:
    # Parent process (the shell)
    os.waitpid(pid, 0)               # wait for child to finish
```

`fork()` creates an exact copy of the current process. `exec()` replaces the running program with a new one. The child never returns from `exec()` on success. The parent waits.

This two-step design gives the shell a window between `fork()` and `exec()` to manipulate file descriptors — which is how pipes and redirections are implemented.

### I/O Redirection

```bash
ls > output.txt       # stdout → file
cat < input.txt       # stdin ← file
ls 2> errors.txt      # stderr → file
```

Between `fork()` and `exec()`, the shell redirects file descriptors using `dup2()`:

```python
if redirect_stdout:
    fd = os.open(output_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    os.dup2(fd, 1)    # make stdout (fd 1) point to the file
    os.close(fd)      # close original (now duplicated)
```

`dup2(src, dst)`: makes `dst` a duplicate of `src`. After `dup2(fd, 1)`, writes to stdout go to the file. The `exec()`'d program never knows — it just uses fd 1 as normal.

### Pipes

```bash
ls | grep .py | wc -l
```

A pipe `|` connects stdout of one process to stdin of the next.

```python
def run_pipeline(commands):
    # commands = [['ls'], ['grep', '.py'], ['wc', '-l']]
    n = len(commands)
    pipes = [os.pipe() for _ in range(n - 1)]  # n-1 pipes for n commands

    pids = []
    for i, cmd in enumerate(commands):
        pid = os.fork()
        if pid == 0:  # child
            # Connect stdin to previous pipe's read end
            if i > 0:
                os.dup2(pipes[i-1][0], 0)  # stdin ← pipe read
            # Connect stdout to next pipe's write end
            if i < n - 1:
                os.dup2(pipes[i][1], 1)    # stdout → pipe write
            # Close all pipe fds (child doesn't need them)
            for r, w in pipes:
                os.close(r); os.close(w)
            os.execvp(cmd[0], cmd)
            sys.exit(1)
        pids.append(pid)

    # Parent: close all pipe fds
    for r, w in pipes:
        os.close(r); os.close(w)

    # Wait for all children
    for pid in pids:
        os.waitpid(pid, 0)
```

The kernel's `os.pipe()` creates a pair of file descriptors: `(read_end, write_end)`. Data written to `write_end` is buffered by the kernel and can be read from `read_end`. This is why `ls | grep` works: `ls`'s stdout writes to the pipe buffer; `grep`'s stdin reads from it.

### Job Control

Real shells support background jobs (`cmd &`), job suspension (`Ctrl+Z`), and foreground/background switching (`fg`, `bg`). This requires Unix signal handling:

- `SIGCHLD`: sent to parent when a child changes state
- `SIGINT` (Ctrl+C): interrupt the foreground job
- `SIGTSTP` (Ctrl+Z): suspend the foreground job
- `SIGCONT`: resume a suspended job

A minimal implementation:
```python
import signal

background_jobs = []

def run_background(cmd):
    pid = os.fork()
    if pid == 0:
        os.execvp(cmd[0], cmd); sys.exit(1)
    background_jobs.append(pid)
    print(f"[{len(background_jobs)}] {pid}")
```

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — Command Parser**
- Type shell commands; watch the tokenisation and parsing
- See quoted strings handled correctly: `echo "hello world"` → 2 tokens

**Tool 2 — fork/exec Visualiser**
- Type a command; watch the process tree
- See the parent shell fork a child, the child exec, and the parent wait
- See file descriptor table before and after dup2

**Tool 3 — Pipe Chain**
- Enter `cmd1 | cmd2 | cmd3`
- Watch the pipes created, fds redirected, and processes connected

---

## Going Deeper

**Signal handling in the shell**: when you press Ctrl+C, the kernel sends SIGINT to the **foreground process group**, not just the shell. The shell must set up process groups correctly so that signals reach the running pipeline, not the shell itself. This is why running `sleep 100` and pressing Ctrl+C kills sleep, not the shell.

**Environment variables**: each process inherits a copy of its parent's environment. `export VAR=value` in the shell adds a variable to the environment, which is then passed to every child process. This is why you can run `PYTHONPATH=/my/lib python script.py` — the shell sets PYTHONPATH in the child's environment before exec.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Implement a shell that supports redirection (`>`, `<`) and pipes (`|`), trace exactly what happens when you run `cat file.txt | sort | uniq > result.txt` at the kernel level (which fds, which dup2 calls, which exec calls), and extend the shell with a `history` built-in.
