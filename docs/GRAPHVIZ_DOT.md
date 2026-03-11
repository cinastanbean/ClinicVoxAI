# Graph Visualization (DOT)

```
digraph VoiceAIAgentGraph {
  rankdir=LR;
  node [shape=box];

  start [label="START"];
  router [label="Router Agent"];
  supervisor [label="Supervisor Agent"];
  task [label="Task Agent"];
  handoff [label="Handoff"];
  clarify [label="Clarify"];
  end [label="END"];

  start -> router;
  router -> supervisor;
  supervisor -> clarify [label="clarify"];
  supervisor -> handoff [label="handoff"];
  supervisor -> task [label="proceed"];
  clarify -> router;
  task -> end;
  handoff -> end;
}
```
