# Challenge 7.4 — Building a Tiny Shell

**Type:** Implementation + trace + security  
**Estimated time:** 50–60 minutes  
**Tools needed:** Python (on Linux/macOS for os.fork) or simulation

---

## Part A — Command Parser

1. Implement `parse_command(line)` that tokenises a shell command string, handling:
   - Simple commands: `"ls -la"` → `["ls", "-la"]`
   - Quoted strings: `"echo 'hello world'"` → `["echo", "hello world"]`
   - Output redirection: `"ls > out.txt"` → `{"cmd": ["ls"], "stdout": "out.txt"}`
   - Input redirection: `"sort < data.txt"` → `{"cmd": ["sort"], "stdin": "data.txt"}`
   - Pipes: `"ls | grep .py"` → `{"pipeline": [["ls"], ["grep", ".py"]]}`

2. Trace `parse_command("cat < input.txt | sort -n > output.txt")`. What is the parsed representation?

3. What shell built-ins **cannot** be implemented as child processes? Give two examples and explain why they must run in the shell process itself.

---

## Part B — fork/exec Trace

Trace every kernel call when the shell executes `ls -la`:

4. List the syscalls in order:
   - `fork()` — what does this return to the parent? To the child?
   - `execvp("ls", ["ls", "-la"])` — in which process?
   - `waitpid(pid, 0)` — in which process? What does it return?

5. Between `fork()` and `exec()`, what file descriptor operations would the shell perform for `ls > out.txt`? Show the `open()` and `dup2()` calls.

6. Why is the fork+exec pattern used rather than a single "create_process_from_program" call? What useful things can be done in the window between fork and exec?

---

## Part C — Pipe Implementation

7. Implement `run_pipeline(["ls", "-la"], ["grep", ".py"])` using `os.pipe()`, `os.fork()`, and `os.dup2()`. The output of `ls -la` should be the input of `grep .py`.

8. Trace the file descriptor state for the parent and both children:
   - Before `os.pipe()`: list all open fds
   - After `os.pipe()`: what are `r` and `w`?
   - In child 1 (ls): which dup2 call, which fds are closed?
   - In child 2 (grep): which dup2 call, which fds are closed?
   - Parent: which fds must it close and why?

9. What happens if the parent does **not** close the write end of the pipe? Why does `grep` never see EOF and hang forever?

---

## Part D — I/O Redirection

10. Implement a shell function `execute_with_redirection(cmd, stdin_file=None, stdout_file=None)` that runs `cmd` with optional file redirections using fork/exec/dup2.

11. The following command redirects both stdout and stderr: `cmd > out.txt 2>&1`. What does `2>&1` mean? What dup2 call implements it? In what **order** must the redirections be applied, and why does order matter?

---

## Part E — Security: Directory Traversal

12. A shell or web server receives a path from user input. Consider:
    ```python
    user_input = "../../etc/passwd"
    full_path = os.path.join("/var/www/html", user_input)
    ```
    What is `full_path`? Why is this a security vulnerability?

13. Write a `safe_path(base_dir, user_path)` function that raises an exception if the resolved path is outside `base_dir`. Use `os.path.realpath()`.

14. What other input validation is needed for a production shell or file server? Name three additional attack vectors.

---

## Rubric

| Part | Points |
|---|---|
| A command parser | 20 |
| B fork/exec trace | 22 |
| C pipe implementation | 28 |
| D I/O redirection | 16 |
| E security | 14 |

**Total: 100 points**

---

## Solutions

<details>
<summary>Part B.5 — redirection with dup2</summary>

```python
# In the child process, between fork() and exec():
fd = os.open("out.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
os.dup2(fd, 1)    # make stdout (fd=1) write to out.txt
os.close(fd)      # close original (it's been duplicated to fd 1)
os.execvp("ls", ["ls", "-la"])
```
</details>

<details>
<summary>Part C.7 — pipe between two processes</summary>

```python
import os, sys

def run_pipeline(cmd1, cmd2):
    r, w = os.pipe()

    pid1 = os.fork()
    if pid1 == 0:
        # Child 1: cmd1, stdout → pipe write end
        os.dup2(w, 1)
        os.close(r); os.close(w)
        os.execvp(cmd1[0], cmd1)
        sys.exit(1)

    pid2 = os.fork()
    if pid2 == 0:
        # Child 2: cmd2, stdin ← pipe read end
        os.dup2(r, 0)
        os.close(r); os.close(w)
        os.execvp(cmd2[0], cmd2)
        sys.exit(1)

    # Parent: close both ends (important!)
    os.close(r); os.close(w)
    os.waitpid(pid1, 0)
    os.waitpid(pid2, 0)
```
</details>

<details>
<summary>Part D.11 — 2>&1 ordering</summary>

`2>&1` means "redirect fd 2 (stderr) to wherever fd 1 (stdout) currently points."

Order matters: `> out.txt 2>&1` means:
1. `dup2(open("out.txt"), 1)` — redirect stdout to file
2. `dup2(1, 2)` — redirect stderr to current stdout (= the file)

If reversed (`2>&1 > out.txt`): step 1 redirects stderr to terminal (current stdout before any redirection), step 2 redirects stdout to file. Stderr still goes to terminal — wrong.
</details>

<details>
<summary>Part E.13 — safe_path</summary>

```python
import os

def safe_path(base_dir, user_path):
    base   = os.path.realpath(base_dir)
    target = os.path.realpath(os.path.join(base_dir, user_path))
    if not target.startswith(base + os.sep) and target != base:
        raise ValueError(f"Path escape attempt: {user_path!r}")
    return target
```
</details>
