The user wants a comprehensive introduction to their project. Let me explore the codebase to understand what this project is about, its architecture, tech stack, and implementation details.
Let me try to read the files directly using read_file tool.
Let me get more information about the project by reading the architecture docs and main application files.
Let me continue exploring the docs and the core components.
The docs are organized in subdirectories. Let me explore the architecture and other important docs.
Good, now let me read more important docs to understand the project better.
Now let me read more about the core components: graph state, agents, tools, etc.
Let me read the core graph state and orchestration files.
Now let me read the supervisor agent, LangGraph flow, and some more key docs to understand the full picture.
Now let me read a few more important files to understand the tools, compliance, monitoring, and voice pipeline.
Now let me check some of the generated visual outputs to see if there are any images I can show.
Let me also look at the GRAPH_SVG.svg to see if it can be displayed as an image, and read some more key docs.
Now I have a comprehensive understanding of the project. Let me now check the trace visualization images.
Now I have a very comprehensive understanding of the project. Let me synthesize all the information and provide a thorough introduction.

Let me also check a few more files about voice pipeline and compliance.
Let me check the compliance directory.
Now I have enough information to give a comprehensive introduction to the project. Let me organize and present this information clearly.

The project is called "ClinicVoxAI" - a Voice AI Clinic Assistant. Let me summarize:

1. **项目需求 (Project Requirements)**
2. **系统设计 (System Design)**
3. **技术栈 (Tech Stack)**
4. **核心流程 (Core Process)**
5. **最有价值的部分 (Most Valuable Part)**
6. **其他方面 (Other Aspects)**

Let me provide a thorough and well-organized response with text descriptions and diagrams.
现在我已经全面了解了你的项目。以下是对 **ClinicVoxAI** 的完整介绍：

---

## 1. 项目需求

**ClinicVoxAI** 是一个**面向小型美国诊所的 AI 语音助手**，目标是让患者通过电话就能完成常见业务，减少前台人工负担。

**核心业务场景（MVP）：**

| 场景 | 说明 |
|------|------|
| **新患者注册** | 收集姓名、联系方式、保险信息、就诊原因 |
| **老患者身份验证** | 电话号 + 生日 或 姓名 + 生日 |
| **预约日程** | 预约 / 改期 / 取消 |
| **报告解读** | 仅转述医生笔记，不提供诊断建议 |
| **人工转接** | 低置信度或出错时无缝转人工 |

**业务指标目标：**
- ≥80% 的简单咨询无需人工介入
- 患者满意度 ≥4.0/5
- 符合 HIPAA 基线审计要求

---

## 2. 系统架构设计

整体架构分为**语音管道层**、**多智能体编排层**、**工具层**和**可观测性层**：

```
┌─────────────────────────────────────────────────────────────────────┐
│                         呼叫者 (Caller)                              │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ 电话 (PSTN)
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      语音管道层 (Voice Pipeline)                       │
│  Twilio/Retell Media Stream  →  WebSocket 桥接  →  STT  →  TTS      │
└──────────────────────────────┬───────────────────────────────────────┘
                               │ 文本转录 (Transcript)
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                   LangGraph 编排层 (Orchestration)                     │
│                                                                      │
│  ┌────────────┐    ┌──────────────┐    ┌─────────────┐               │
│  │Router Agent│───▶│Supervisor    │───▶│Task Agent   │               │
│  │意图分类    │    │Agent          │    │业务执行     │               │
│  │patient_type│    │置信度/转接决策│    │工具调用     │               │
│  │intent      │    │clarify/proceed│    │slot-fill    │               │
│  └────────────┘    │handoff       │    └─────────────┘               │
│                    └──────┬───────┘                                   │
└──────────────────────────┼───────────────────────────────────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        工具层 (Tools)                                  │
│  ┌────────┐ ┌──────────┐ ┌────────┐ ┌────────────┐ ┌────────┐       │
│  │Patient │ │Calendar  │ │Report  │ │Notification│ │Handoff │       │
│  │DB Tool │ │Tool      │ │Tool    │ │Tool        │ │Tool    │       │
│  └────────┘ └──────────┘ └────────┘ └────────────┘ └────────┘       │
└──────────────────────────────┬───────────────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    可观测性层 (Observability)                          │
│  EventRecorder → trace.json → trace.html / swimlane.html / timeline  │
│                 collab_summary.csv  |  监控告警  |  合规审计日志      │
└─────────────────────────────────────────────────────────────────────┘
```

### 核心状态机（State Machine）

```
[START]
   │
   ▼
[ROUTER] ──── 分类意图 & 患者类型 ────▶ 更新 state.intent / patient_type
   │
   ▼
[SUPERVISOR]  ──── 评估置信度 & 错误数 ────▶ 决策
   │                                              │
   ├── clarify ──▶ 追问确认 ──▶ [ROUTER] (循环)  │
   ├── handoff ──▶ 转人工 ──▶ [END]              │
   └── proceed ──▶ [TASK] ──▶ [END]              │
                                    │             │
                                    └── tool error ──▶ [SUPERVISOR]
```

---

## 3. 技术栈

| 层次 | 技术选型 |
|------|---------|
| **Web 框架** | FastAPI 0.112 + Uvicorn |
| **多智能体编排** | LangGraph (StateGraph) |
| **LLM 调用** | OpenAI API (GPT-4o) / Mock LLM / 规则引擎 |
| **语音** | Twilio Media Streams + OpenAI Realtime API (STT/TTS) |
| **数据库** | SQLite (dev) / SQLAlchemy (可切换) |
| **语言** | Python 3.10+ |
| **测试** | pytest |
| **可观测性** | 自定义 EventRecorder + HTML/ Swimlane / Timeline 可视化 |
| **合规** | PHI 脱敏、审计日志（mock 阶段） |

---

## 4. 核心流程详解

### 完整预约流程示例（6 个轮次）：

```
Turn 1: 用户: "I want to schedule an appointment"
        Router    → intent=schedule, confidence=0.92
        Supervisor → proceed
        Task      → 追问: "Please tell me your first name, last name, date of birth."

Turn 2: 用户: "My first name is Jane"
        Task      → collected_fields.first_name="Jane"
                    追问: "Please tell me your last name, date of birth."

Turn 3: 用户: "My last name is Doe"
        Task      → collected_fields.last_name="Doe"
                    追问: "Please tell me your date of birth."

Turn 4: 用户: "My date of birth is 1990-01-01"
        Task      → 创建患者 record → patient_id=P001
                    调用 Calendar → 返回 slots
                    追问: "I have 2026-03-12T10:00 or 2026-03-12T14:00. Which works for you?"

Turn 5: 用户: "Wednesday morning works"
        Task      → selected_slot=2026-03-12T10:00
                    调用 Calendar.book()
                    调用 Notify.send_sms()
                    回复: "You're all set. I have confirmed your appointment and sent a text message."

Turn 6: 用户: "Actually, can you tell me my lab results?"
        Router    → intent=report (触发 context reset!)
        Supervisor → proceed
        Task      → 需要验证身份 → "Please provide your date of birth so I can verify your identity."
```

---

## 5. 最有价值的部分

### 多智能体协作与状态管理

这是项目**最核心的工程价值**，解决了一个看似简单但实际非常复杂的问题：**在多轮对话中，多个 Agent 如何安全地共享和修改状态？**

#### ① 状态所有权规则（Single-Writer Rule）

每个 Agent 只能写自己负责的字段，从根本上避免了状态污染：

```
Router Agent    → 只能写: intent, patient_type, intent_confidence
Supervisor Agent→ 只能写: handoff_reason, meta.decision
Task Agent      → 只能写: collected_fields, appointment_context, report_context,
                    patient_id, verification_status
```

#### ② 意图切换时的上下文重置

当用户中途改变意图（如从"预约"切换到"查看报告"），旧意图的上下文自动版本递增清零：

```python
def reset_context_on_intent_change(state: SessionState, new_intent: str) -> None:
    if new_intent != state.intent:
        state.appointment_context = AppointmentContext(
            version=state.appointment_context.version + 1
        )  # 旧 slot_candidates 自动丢弃
        state.report_context = ReportContext(
            version=state.report_context.version + 1
        )
```

版本号 `version` 记录在 trace 中，使得意图切换**完全可追踪**。

#### ③ LangGraph 条件边路由

用有向图表达协作逻辑，每个节点的输出决定下一步走哪条边：

```python
def route_decision(state) -> str:
    if decision == "handoff":    return "__end__"
    if decision == "clarify":    return "router"   # 循环回 Router
    return "task"                          # 继续执行业务
```

#### ④ 完整的 Trace 可视化

每个对话轮次的 `state_diff`（字段级变更）都被完整记录，生成三种可视化：

| 可视化 | 用途 |
|--------|------|
| **trace.html** (表格) | 查看每轮的完整状态快照 |
| **trace_swimlane.html** (泳道图) | 最佳教学视图：每个 Agent 一行，每个轮次一列 |
| **trace_timeline.html** (时序图) | 查看每个节点的执行耗时（毫秒级） |

泳道图示例：
```
        Turn 1         Turn 2         Turn 3         Turn 4         Turn 5
router   [intent=sched] [intent=sched] [intent=sched] [intent=sched] [intent=sched]
supervisor[proceed     ] [proceed     ] [proceed     ] [proceed     ] [proceed     ]
task     [追问姓名...   ] [追问姓氏...  ] [追问生日...  ] [返回slots   ] [预约成功+短信]
```

---

## 6. 其他重要方面

### ① 工具层韧性设计

```
Tool Call
    │
    ▼
ResilientCall ──▶ try/catch ──▶ 1次自动重试
    │
    ├── 失败 → send_alert() → append_error() → Supervisor 决定
    │                                          ├── retry
    │                                          ├── clarify
    │                                          └── handoff
    └── 超时 → 记录 + 告警
```

### ② 故障注入（Fault Injection）

通过 `FAULTS.fail_db / fail_calendar / fail_notify` 开关，可以在测试中模拟任意工具失败，验证整个错误处理链路是否正确：

```bash
python scripts/demo_fault_injection.py
```

### ③ 合规与安全（HIPAA 对齐，Mock 阶段）

- **PHI 脱敏**：`app/compliance/redaction.py` 对日志中的敏感字段打码
- **审计日志**：`app/compliance/audit.py` 记录每次 PHI 访问
- **最小化数据**：不存储音频，只保留必要的患者字段
- **报告 Agent 安全约束**：严格限制为"仅转述医生原文"，禁止给出医疗建议

### ④ 多存储后端切换

通过 `app/config.py` 的 `storage_backend = "sqlite"` 开关，可以无感切换存储实现：

| 模式 | PatientDB | Calendar | Reports |
|------|-----------|----------|---------|
| `sqlite` | SQLitePatientDB | SQLiteCalendar | SQLiteReportStore |
| `sqlalchemy` | SQLAlchemyPatientDB | SQLAlchemyCalendar | SQLAlchemyReportStore |
| `memory` | PatientDBTool | CalendarTool | ReportTool |

### ⑤ 语音管道（Voice Pipeline）

支持多种接入方式：
- **Mock 模式**：纯文本 transcript 输入，适合快速调试
- **Twilio Media Streams**：电话 WebSocket 音频流
- **Retell Streaming**：另一个电话平台桥接
- **OpenAI Realtime API**：端到端语音对话（WebSocket 直连）

### ⑥ 当前阶段与待完成

根据 `TODO.md`，项目仍处于 **学习导向的演示阶段**，下一步产品化需要攻克：

1. **真实集成**：Twilio/Retell + 真实 EHR/日历系统
2. **合规加固**：正式 BAA 签署、PHI 保留策略、审计日志硬化
3. **可靠性**：Prometheus/Grafana 指标、PagerDuty 告警、后台重试任务系统
4. **对话质量**：模糊匹配验证、动态提示词、意图记忆优化
5. **工程整洁**：Schema 版本化、PYTHONPATH 处理