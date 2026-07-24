# DECISIONS.md — 选题与边界（阶段 0）

> 本文件对应 `docs/skill-build-checklist.md` 阶段 0 的全部产物。后续阶段如需变更选题、角色或边界，先改这里，再改 SKILL.md。

---

## 1. 能力雷达四标准评分

| 标准 | 评分（1-5） | 说明 |
| --- | --- | --- |
| 高密度素材 | 5 | kubernetes.io 官方文档 + CNCF 官方 curriculum，结构化程度高，五域细目现成 |
| 有明确"老师" | 5 | 本人 K8s 运维老本行，判卷脚本（kind + kubectl 断言）是可复用的专业积累 |
| 痛点尖锐 | 5 | CKA 是纯实操考试，考的是"手速+准确率"，市面上缺少可反复批改的本地练习环境 |
| 版权可控 | 4 | 文档和考纲均有明确开放授权，唯一约束是不能碰 Killer.sh 题库和真题回忆 |

**结论：选题通过，四项均达标。**

---

## 2. 选题结论

- **项目**：CKA（Certified Kubernetes Administrator）备考 Mentor skill
- **角色模式**：`mentor`（带练）
- **理由**：CKA 是纯实操考试（kubectl 命令 + 集群操作），核心痛点是"反复练习 + 即时反馈"，不是"查证事实"。`expert` 模式（查证）对这类技能没有价值；`consultant`/`practitioner` 也不匹配"陪练到通过"的核心诉求。

---

## 3. 版权依据

| 素材 | 授权 | 出处链接 |
| --- | --- | --- |
| kubernetes.io 官方文档 | CC BY 4.0 | https://github.com/kubernetes/website/blob/main/LICENSE （站点页脚同样声明 CC BY 4.0，见 https://kubernetes.io/docs/reference/ ） |
| CNCF curriculum（CKA_Curriculum） | 公开发布，CC-BY 4.0+ | https://github.com/cncf/curriculum （root README 明确写明 "The Curriculum is available under the CC-BY 4.0+ License"，链接 https://creativecommons.org/licenses/by/4.0/ ） |

**红线（不可触碰）：**
1. 不碰 Killer.sh 题库（付费商业题库，无授权）。
2. 不复述/不收录任何真实考试原题或考生回忆（违反 Linux Foundation 考试 NDA）。
3. 仓库内所有练习题必须原创——基于考纲能力点自行设计场景，禁止照搬任何第三方题库措辞或场景描述。

---

## 4. 边界声明

> 本 skill 是 CKA 备考辅助工具，**不保证通过考试**。判卷基于本地 kind/k3s 环境，与真实考试环境（PSI 远程监考平台、特定 Kubernetes 版本、特定网络插件等）可能存在版本或行为差异，请以官方文档为准。本 skill **不提供、不复述任何真实考试题目**，所有练习题均为原创，仅用于训练同等能力点。本 skill 模拟"open book"规则：陪练/答疑过程中只允许引用 kubernetes.io 官方文档内容，不引用/不代做超出该范围的信息源。

明确不做的事：
- 不提供真题或题库内容
- 不代考生答题、不替代真实考试
- 不承诺通过率或分数
- 不脱离 kubernetes.io 文档范围做延伸查证（角色是 mentor，不是 expert）

---

## 5. 目标用户

准备参加 CKA 认证考试的 Kubernetes 学习者/运维工程师，已具备基础 kubectl 操作能力，需要系统性刷题 + 实操判卷 + 薄弱点诊断。

---

## 6. 触发场景清单（≥10 条，中英双语）

### 中文（用户原话）
1. "帮我出一道 CKA 的 troubleshooting 题"
2. "我 kubectl 老是记不住 RBAC 相关的命令，能不能带我练几道"
3. "帮我模拟一次 CKA 考试环境"
4. "这道题我做完了，帮我判一下卷"
5. "Pod 一直起不来，帮我分析一下怎么排查"
6. "CKA 考试都考哪些内容，权重怎么分布"
7. "我要考 CKA，不知道从哪开始复习"
8. "etcd 备份恢复这块我总是出错，能出题让我练练吗"
9. "网络策略（NetworkPolicy）我看不太懂，能不能用例子教我"
10. "给我一个 CKA 分域的学习路线图"
11. "这题我卡住了，能不能给个提示，不要直接给答案"
12. "帮我检查一下我搭的 kubeadm 高可用集群配置对不对"

### English (verbatim user phrasing)
1. "Give me a CKA troubleshooting practice question"
2. "Can you drill me on kubectl commands for RBAC?"
3. "Simulate a CKA exam environment for me"
4. "I finished this task, can you grade my solution?"
5. "My pod won't start, help me debug it step by step"
6. "What are the CKA exam domains and their weights?"
7. "I'm studying for CKA, where should I start?"
8. "I keep messing up etcd backup and restore, quiz me on it"
9. "Can you explain NetworkPolicy with an example?"
10. "Give me a study roadmap broken down by CKA domain"
11. "I'm stuck on this task, give me a hint but not the answer"
12. "Check whether my kubeadm HA control plane setup is correct"

---

## 7. 变更记录

| 日期 | 变更 | 依据 |
| --- | --- | --- |
| 2026-07-24 | 初版，完成阶段 0 全部产物 | 首次执行 checklist |
