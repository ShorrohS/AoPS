# Module 12.4 — AI Agents: Planning, Tool Use, and Memory

---

## The Problem

> A large language model can answer a question.
> But it cannot: browse the web to find current information,
> write code and run it to check if it works,
> send an email, query a database, or interact with an API.
>
> An **AI agent** extends the LLM with the ability to take actions:
> use tools, execute code, interact with external systems,
> and — most importantly — plan a sequence of actions to achieve a goal.
>
> This is the difference between an assistant that tells you how to do something
> and one that actually does it.

---

## The Story

### From Chatbots to Agents

The ELIZA chatbot (Weizenbaum, MIT, 1966) simulated a therapist through simple pattern matching. Users ascribed understanding to it despite its mechanical simplicity — the first demonstration of how humans project intelligence onto text.

**ReAct** (Reason + Act, Yao et al., 2022) was a key paper showing that LLMs could interleave reasoning (thinking through a problem) with action (using tools to gather information). The model writes its "thoughts" in text, then calls a tool, observes the result, thinks further. This simple pattern enabled solving problems that pure generation couldn't.

**AutoGPT** (2023) was an early attempt at autonomous agents — GPT-4 calling itself recursively, maintaining a task list, browsing the web, and writing files. It attracted enormous attention but also demonstrated the failure modes: lack of planning, context window limits, cascading errors.

**LangChain, LlamaIndex, Claude's tool use, OpenAI Function Calling** — all subsequent frameworks for building agents have converged on the same core pattern: give the LLM a set of tools, let it decide which to call and when.

---

## The Concept

### The ReAct Loop

```
User Goal
    ↓
[Thought]: Reason about what to do next
    ↓
[Action]: Call a tool (search, code execution, API call)
    ↓
[Observation]: Receive tool output
    ↓
(repeat Thought → Action → Observation until goal achieved)
    ↓
[Final Answer]
```

**Example trace:**

```
Goal: What is the current Python version and what was the main change in that release?

Thought: I need to find the current Python version. I'll search for it.
Action: web_search("current Python version 2026")
Observation: Python 3.13 was released in October 2024. Python 3.14 is in development.

Thought: I have the version. Now I need to find the main changes in Python 3.13.
Action: web_search("Python 3.13 major changes features")
Observation: Python 3.13 introduced experimental free-threaded mode (no GIL), improved error messages, and a new REPL.

Thought: I have all the information needed.
Final Answer: The current stable Python version is 3.13. Its major changes include experimental GIL-free threading, improved error messages, and a redesigned interactive interpreter.
```

### Tool Definition and Function Calling

Modern LLM APIs support **function calling** — you describe tools in a structured format, the model chooses which to call and with what arguments, you execute the tool and return the result:

```python
import openai, json

tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_python",
            "description": "Execute Python code and return the output",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python code to execute"}
                },
                "required": ["code"]
            }
        }
    }
]

def run_agent(goal, tools, tool_executors, max_steps=10):
    messages = [{"role": "user", "content": goal}]

    for step in range(max_steps):
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        msg = response.choices[0].message
        messages.append(msg)

        # If no tool call: model has finished reasoning
        if not msg.tool_calls:
            return msg.content

        # Execute each tool call
        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            result = tool_executors[name](**args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

    return "Max steps reached"
```

### Memory Types

An agent that forgets context is limited. Different tasks require different memory:

**In-context memory**: everything in the current prompt. Fast, exact, but limited to context window (4K–200K tokens depending on model).

**Episodic memory**: store past conversations and retrieve relevant ones via embedding similarity:
```python
def remember(agent, interaction):
    embedding = embed(interaction['summary'])
    memory_db.upsert(embedding, interaction)

def recall(agent, query, k=3):
    query_emb = embed(query)
    return memory_db.search(query_emb, k)
```

**Semantic memory**: distilled facts extracted from experience. "User prefers Python over JavaScript." "This codebase uses pytest for testing." Stored and retrieved as structured facts.

**Procedural memory**: how to do specific tasks. Often stored as few-shot examples retrieved from a library.

### Planning

For complex multi-step goals, ad-hoc tool use is insufficient. Planning approaches:

**Chain of Thought (CoT)**: instruct the model to reason step by step before acting. Dramatically improves performance on complex tasks without any additional architecture.

**Tree of Thought (ToT)**: generate multiple reasoning paths, evaluate each, select the most promising. Better for tasks where the correct approach is not obvious.

**Plan-and-Execute**: generate a complete plan upfront, then execute each step:
```python
def plan_then_execute(goal, llm, executor):
    # Step 1: generate a plan
    plan_prompt = f"Create a step-by-step plan to: {goal}\nSteps:"
    plan = llm(plan_prompt)

    # Step 2: execute each step
    results = []
    for step in parse_plan(plan):
        result = executor.run(step)
        results.append(result)

    # Step 3: synthesise results
    return llm(f"Based on these results: {results}\nAnswer: {goal}")
```

**Reflexion** (Shinn et al., 2023): after failure, the agent reflects on what went wrong and stores a verbal critique in memory. On retry, the critique guides better behaviour. Significantly improves agent performance on tasks requiring exploration.

### Multi-Agent Systems

Complex tasks can be decomposed among specialised agents:

```python
agents = {
    'researcher':  Agent(tools=['web_search', 'retrieve_docs']),
    'coder':       Agent(tools=['execute_python', 'read_file', 'write_file']),
    'critic':      Agent(tools=['code_review', 'fact_check']),
    'coordinator': Agent(tools=['delegate_to_agent'])
}

def multi_agent_pipeline(task):
    plan  = agents['coordinator'].plan(task)
    for subtask in plan:
        if subtask.type == 'research': result = agents['researcher'].run(subtask)
        elif subtask.type == 'code':   result = agents['coder'].run(subtask)
        # etc.
    return agents['critic'].review(results)
```

**AutoGen** (Microsoft) and **CrewAI** are frameworks for multi-agent orchestration with conversational coordination.

---

## Hands-On Exercise

**Open the simulation:** [`simulation.html`](./simulation.html)

**Tool 1 — ReAct Loop Tracer**
- A simulated agent with 3 tools: search, calculator, code runner
- Give it a multi-step task
- Watch: Thought → Action → Observation cycle, step by step

**Tool 2 — Memory Manager**
- Agent processes multiple conversations
- Watch episodic memory accumulate
- Issue a query — see which past interactions are retrieved as context

**Tool 3 — Planning Demo**
- Compare: no planning (pure reactive) vs. plan-then-execute vs. tree of thought
- Same task, observe how each approach finds (or fails to find) the solution

---

## Going Deeper

**Agent safety and sandboxing**: an agent that can execute code and call APIs can cause real damage — delete files, send emails, make purchases. Production agent systems need: sandboxed execution environments (Docker containers, WASM), minimal permissions (only what the task requires), human confirmation for high-stakes actions, and detailed audit logs. The problem of building agents that are powerful enough to be useful but constrained enough to be safe is an active area of both engineering and research.

**Context window management**: a long-running agent accumulates context. At some point the context window is full. Strategies: summarise older exchanges and replace them with the summary, use retrieval over conversation history, implement a sliding window. Each strategy loses some information — the right approach depends on what the task requires.

---

## Challenge

**Open:** [`challenge.md`](./challenge.md)

Build a minimal ReAct agent in Python with two tools (calculator and a dictionary lookup), trace an agent solving a 3-step research task showing the full Thought/Action/Observation trace, design the memory schema for an agent that helps users debug Python code (what would you store? how would you retrieve it?), and identify two scenarios where an agent with file-write access could cause unintended harm — and propose safety measures for each.
