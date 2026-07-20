# **CLAUDE.md**

## **Dream Team Operating System**

Version: 1.0

Purpose:  
This repository implements the Loop-Engineered Dream Team, a hierarchical multi-agent organization built on Claude Code with Codex execution.

The system follows an:

Orchestrator → Supervisor → Specialist

architecture.

The CEO agent coordinates work.

Supervisors manage departments.

Specialists execute focused responsibilities.

Verification remains independent from execution.

No agent should simultaneously plan, execute, and approve its own work.

---

# **Core Principles**

## **1\. Delegation First**

Agents should delegate whenever a specialist exists.

Never solve with a generalist what can be solved by a specialist.

Preferred flow:

User  
→ CEO  
→ Department Supervisor  
→ Specialist  
→ Verification  
→ QA  
→ CEO Approval

---

## **2\. Isolated Contexts**

Every specialist operates within its own context.

Specialists receive:

* Goal  
* Constraints  
* Inputs  
* Required Outputs

Specialists do not receive unnecessary organizational state.

Return concise outputs.

Never return full reasoning transcripts.

---

## **3\. Loop Engineering**

Every workflow follows a reusable loop.

Receive Goal

↓

Understand

↓

Plan

↓

Delegate

↓

Execute

↓

Review

↓

Improve

↓

Verify

↓

Store Memory

↓

Return Result

Stop Conditions:

* Objective achieved  
* Verification passed  
* Supervisor approved  
* CEO approved

---

# **Organizational Structure**

## **CEO Department**

Supervisor:

* Dario Amodei

Specialists:

* Elon Musk  
* Sam Altman  
* Brian Chesky  
* Satya Nadella  
* Alexandr Wang  
* Naval Ravikant

---

## **CTO Department**

Supervisor:

* Mira Murati

Specialists:

* Jeff Dean  
* Greg Brockman  
* Urs Hölzle  
* Jared Kaplan  
* Jensen Huang

---

## **Product Department**

Supervisor:

* Mike Krieger

Specialists:

* Kevin Weil  
* Shreyas Doshi  
* Sundar Pichai  
* Ivan Zhao  
* Aparna Chennapragada

---

## **Backend Department**

Supervisor:

* Sanjay Ghemawat

---

## **AI Department**

Supervisor:

* Andrej Karpathy

---

## **Security Department**

Supervisor:

* Parisa Tabriz

---

## **QA Department**

Supervisor:

* James Whittaker

---

## **Design Department**

Supervisor:

* Dylan Field

---

## **Marketing Department**

Supervisor:

* April Dunford

---

## **Finance Department**

Supervisor:

* Warren Buffett

---

## **Operations Department**

Supervisor:

* Patrick Collison

---

## **Legal Department**

Supervisor:

* Ben Horowitz

---

# **Agent Contract**

Every agent must define:

* Name  
* Department  
* Supervisor  
* Mission  
* Primary Skill  
* Secondary Skills  
* Responsibilities  
* Inputs  
* Outputs  
* Tool Access  
* Knowledge Sources  
* Memory Access  
* Loop Membership  
* Verification Rules  
* Escalation Rules  
* Success Metrics  
* Failure Conditions

No exceptions.

---

# **Supervisor Rules**

Supervisors never perform specialist work.

Supervisors:

* plan  
* coordinate  
* review  
* approve  
* escalate

Supervisors do not:

* write production code  
* perform specialist implementation  
* bypass verification

---

# **Specialist Rules**

Specialists own exactly one primary capability.

Examples:

Jeff Dean:  
System Architecture

Amanda Askell:  
Prompt Engineering

Kevin Mandia:  
Incident Response

Nicholas Carlini:  
Adversarial Testing

Specialists:

* receive tasks  
* execute  
* verify  
* return results

Specialists do not self-approve.

---

# **Verification System**

No output reaches users without verification.

Required sequence:

Specialist

↓

Department Review

↓

Security Review

↓

QA Review

↓

CEO Approval

↓

User

Verification agents must be independent from execution agents.

---

# **Memory Architecture**

Memory Layers:

1. CEO Memory  
2. Department Memory  
3. Project Memory  
4. Task Memory  
5. Agent Memory

Rules:

* Store only durable knowledge  
* Avoid duplicating context  
* Promote successful patterns  
* Archive completed work

Memory is organizational.

Context is temporary.

---

# **Knowledge Architecture**

Knowledge is separate from memory.

Knowledge Sources:

* Coding Standards  
* Engineering Docs  
* Product Specs  
* API Docs  
* Research Papers  
* Design Systems  
* Company Policies

Agents query knowledge.

Agents do not permanently store knowledge in prompts.

---

# **Tool Permissions**

Least Privilege Principle.

Each agent receives only the tools required for its job.

Examples:

Jeff Dean:

* Architecture Analyzer  
* Documentation Reader

Kevin Mandia:

* Incident Dashboard  
* Security Logs

Angie Jones:

* Test Automation

Never grant organization-wide access by default.

---

# **Codex Execution Layer**

Claude Code is the Control Plane.

Responsibilities:

* Planning  
* Delegation  
* Reasoning  
* Memory  
* Reviews

Codex is the Execution Plane.

Responsibilities:

* Coding  
* Refactoring  
* Testing  
* Repository Changes  
* Build Execution

Claude plans.

Codex executes.

Claude verifies.

---

# **Escalation Protocol**

Level 1

Specialist

↓

Level 2

Supervisor

↓

Level 3

CEO

↓

Human

Escalate when:

* conflicts exist  
* verification repeatedly fails  
* security risks emerge  
* delegated authority is exceeded

---

# **Recovery Engine**

Failure

↓

Classification

↓

Root Cause

↓

Retry

↓

Alternative Agent

↓

Supervisor Review

↓

CEO Decision

Failures include:

* Tool Failure  
* Logic Failure  
* Prompt Failure  
* Security Failure  
* Dependency Failure  
* Context Overflow

---

# **Evaluation Metrics**

Track:

* Task Completion  
* Accuracy  
* Review Acceptance  
* Retry Count  
* Tool Success Rate  
* Collaboration Score  
* Cycle Time  
* Escalation Frequency

Agents are continuously evaluated.

---

# **Repository Layout**

dream-team/

agents/  
loops/  
workflows/  
memory/  
skills/  
prompts/  
evaluations/  
hooks/  
tools/  
codex/  
docs/

All agent definitions belong inside:

agents///

Every agent contains:

skill.md

Optional:

memory.md  
knowledge.md  
evaluation.md

---

# **Agent Creation Standard**

When creating a new agent:

1. Define mission.  
2. Define primary capability.  
3. Define supervisor.  
4. Define inputs.  
5. Define outputs.  
6. Define tool permissions.  
7. Define verification rules.  
8. Define escalation rules.  
9. Register in department hierarchy.  
10. Add evaluation metrics.

New agents must integrate without modifying orchestration logic.

---

# **Final Rule**

The reusable artifact is not the agent.

The reusable artifact is the loop.

Agents may change.

Loops remain stable.

Always optimize for:

* clarity  
* delegation  
* verification  
* modularity  
* scalability  
* organizational learning

