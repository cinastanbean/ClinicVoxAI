以下是为您的 **ClinicVoxAI** 项目（语音智能诊所客服系统）绘制的**多Agent交互核心时序图**，重点描述典型的多轮对话中 **Agent之间信息交互与协作过程**。

我使用 **PlantUML** 语法提供（可直接复制到 plantuml.com/plantuml 或任意支持PlantUML的工具渲染成图片）。这个图聚焦于**多Agent协作**的本质，而不是单纯的单次意图处理。

### 多Agent协作典型场景：老患者来电 → 验证 → 查询报告 → 需要改约 → 最终确认（涉及多个Agent协作）

```plantuml
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam ParticipantPadding 20
skinparam BoxPadding 10

actor 患者 as Patient
participant "Twilio / Retell\n(语音网关)" as Twilio
participant "入口 / Router Agent\n(意图识别 + 路由)" as Router
participant "Auth Agent\n(身份验证)" as Auth
participant "Report Agent\n(报告查询 & 解释)" as Report
participant "Booking Agent\n(预约管理)" as Booking
participant "LLM Core\n(共享大模型调用)" as LLM
participant "State / Memory\n(共享上下文)" as State
participant "HIPAA DB + Calendar" as Backend

== 通话开始 ==
Patient -> Twilio: 拨打电话 + 第一句语音
activate Twilio
Twilio -> Twilio: STT → 文本
Twilio -> Router: 用户输入文本 + 会话ID
activate Router

== 意图识别与首次路由 ==
Router -> LLM: "分析意图：老患者？想查报告？改约？"
LLM --> Router: 意图 = "老患者 + 查询报告"
Router -> State: 保存当前意图 & 会话历史
Router -> Auth: 调用 Auth Agent (需要验证身份)
deactivate Router

== 身份验证阶段 ==
Auth -> Patient: TTS "请告诉我您的手机号或姓名+出生日期"
Patient --> Auth: 语音回复
Auth -> Twilio: STT → 文本
Auth -> Backend: 查询患者记录 (模糊匹配)
Backend --> Auth: 匹配成功 → 返回 patient_id
Auth -> State: 更新 patient_id 到共享状态
Auth -> Router: 返回 "验证通过" + patient_id
deactivate Auth

== Router 重新接管 + 路由到 Report ==
Router -> State: 读取 patient_id + 上次意图
Router -> Report: 路由到 Report Agent
activate Report

Report -> Patient: TTS "您想查询哪份报告？例如上个月的血检"
Patient --> Report: "我想知道最近的血检结果"
Report -> Backend: 查询报告 (patient_id + 关键词)
Backend --> Report: 返回报告原始文本 / JSON
Report -> LLM: "用通俗语言总结报告关键点 + 医生建议（禁止诊断）"
LLM --> Report: 自然语言总结文本
Report -> Patient: TTS 播报总结 + "需要我读详细数值吗？"
Patient --> Report: "是的，请读一下胆固醇值"
Report -> Patient: TTS 读具体数值 + 解释

== 意图变化：患者想顺便改约 ==
Patient -> Report: "对了，我周三的预约能不能改到周四？"
Report -> State: 检测到新意图 → "改约"
Report -> Router: 主动返回控制权 + 新意图 = "改约"
deactivate Report

== Router 路由到 Booking Agent ==
Router -> Booking: 调用 Booking Agent + 传递 patient_id & 当前预约信息
activate Booking

Booking -> Backend: 查询当前预约 (patient_id)
Backend --> Booking: 当前预约：周三 10:00 Dr.Smith
Booking -> Backend: 查询 Dr.Smith 周四可用槽
Backend --> Booking: 周四 14:00 & 15:30 可用
Booking -> Patient: TTS "您当前预约周三10点，能改到周四下午2点或3点半吗？"
Patient --> Booking: "2点吧"
Booking -> Backend: 更新预约 → 新事件ID
Backend --> Booking: 更新成功
Booking -> State: 更新预约状态
Booking -> Patient: TTS "已改约成功，周四下午2点 Dr.Smith，已发短信确认"
Booking -> Router: 任务完成，返回控制权
deactivate Booking

== 结束或继续 ==
Router -> Patient: TTS "还有其他可以帮您的吗？"
alt 患者说“没有了”
  Router -> Twilio: 结束通话
else 继续其他意图
  Router -> LLM: 继续意图识别 → 循环
end

deactivate Twilio

note right of State
  共享状态（LangGraph state / memory）：
  - patient_id
  - 会话历史
  - 当前意图
  - 已验证标志
  - 预约详情
end note

@enduml
```

### 这个时序图的核心信息交互过程说明

1. **Router Agent 是中央协调者**（类似 Supervisor / Orchestrator）  
   - 负责首次意图识别  
   - 根据当前状态 + 用户最新输入决定调用哪个子Agent  
   - 子Agent完成后把控制权还给Router（或直接结束）

2. **子Agent 之间不直接调用彼此**（松耦合）  
   - 通过 **共享 State / Memory** 传递关键信息（patient_id、意图历史、预约详情等）  
   - 这符合 LangGraph 的典型设计：state 是全局可读写的“黑板”

3. **信息流向总结**  
   - 用户 → Twilio(STT) → Router → 子Agent  
   - 子Agent → LLM（解释/总结） → Backend（查/改数据） → 子Agent → 用户(TTS)  
   - 子Agent 完成 → 返回 Router（或状态变更触发新路由）  
   - Router → 下一个子Agent 或 结束

4. **典型协作模式**  
   - **顺序协作**：验证 → 报告 → 改约  
   - **动态跳转**：Report Agent 检测到改约意图 → 主动让出控制权给 Router  
   - **状态驱动**：所有决定基于共享 state，而不是硬编码顺序

如果您使用的是 LangGraph，这个图几乎可以直接对应到 graph 的 node（每个Agent是一个node）和 edge（router 的条件分支）。

需要调整为更偏向 **CrewAI**（角色+任务委派）或 **AutoGen**（group chat 风格）的交互方式吗？或者想聚焦某个具体子流程（如只看报告解释时的多Agent调用），我可以再画一张更细的。



# 完整多Agent协作流程图


```plantuml
@startuml
skinparam monochrome true
skinparam shadowing false
skinparam ActivityBorderThickness 2
skinparam ActivityFontSize 14
skinparam ArrowThickness 2

title ClinicVoxAI: 完整多Agent协作流程图 (Activity Diagram)

start
:患者拨打电话;
-> Twilio/Retell 捕获语音;

partition "Router Agent (入口协调)" {
  :STT 转文本;
  :调用 LLM 识别意图;
  if (新患者?) then (是)
    :路由到 Register Agent;
  else (否)
    :路由到 Auth Agent;
  endif
}

partition "Auth Agent (身份验证)" {
  :询问验证信息 (手机号/姓名+生日);
  :后端查询匹配;
  if (验证成功?) then (是)
    :更新共享 State (patient_id);
    :返回 Router;
  else (否)
    :重试或转人工;
    kill
  endif
}

partition "Register Agent (新患者注册)" {
  :播放 HIPAA 隐私声明;
  :收集基本信息 (姓名/生日/保险等);
  :存储到后端 DB (加密PHI);
  :生成 patient_id;
  :更新共享 State;
  :返回 Router;
}

-> Router 重新评估意图 (基于 State + 新输入);

fork
  partition "Report Agent (报告查询)" {
    :询问报告类型/时间;
    :后端查询报告 (patient_id);
    :LLM 通俗解释 (避免诊断);
    :TTS 播报总结;
    :处理追问;
    if (新意图检测?) then (如改约)
      :返回控制权给 Router;
    endif
  }
fork again
  partition "Booking Agent (预约管理)" {
    :查询当前预约 (patient_id);
    :后端查日历可用槽;
    :TTS 选项播报;
    :患者选择确认;
    :更新日历 + DB;
    :发送短信确认;
    if (新意图检测?) then (如查报告)
      :返回控制权给 Router;
    endif
  }
end fork

-> Router 检查会话结束?;
if (结束?) then (是)
  :TTS 道别;
  :结束通话;
else (否)
  :继续监听新输入;
  -> 循环到意图识别;
endif

stop

note bottom
  关键协作机制:
  - Router 作为中心, 动态路由
  - 共享 State: patient_id, 意图历史, 会话上下文
  - Agent间: 通过 Router/State 间接协作, 支持意图切换
  - 异常: 任意点可转人工 (未画出)
end note

@enduml
```

