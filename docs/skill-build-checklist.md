# Agent Skill 从 0 到发布 Checklist

> 方法论来源：JuneYaooo/lineage-skill（Capture → Cite → Compress → Connect → Codify → Coach → Practice → Consolidate → Transfer → Graduate）+ nihaisha-nishi-tcm 工程实践 + Anthropic skill-creator 官方规范。
> 使用方式：每阶段完成后核对「产物」和「验收标准」，全部打勾才进入下一阶段。标注 [CKA] 的条目是首发项目的具体实例，其余通用。
> 三个项目的定位：CKA（公开首发，Mentor 模式）→ 八年级英语（私有家用，复用架构）→ 交付方法论（主打，Expert+Consultant 模式）。

---

## 阶段 0：选题与边界（0.5 天，纸面工作）

### 任务
- [ ] 用能力雷达四标准过一遍选题：高密度素材 / 有明确"老师" / 痛点尖锐 / 版权可控
- [ ] 确认素材授权。[CKA] kubernetes.io 文档 = CC BY 4.0；CNCF curriculum repo 公开。红线：不碰 Killer.sh 题库、不碰真题回忆（违反 NDA），所有练习题原创
- [ ] 选角色模式：expert（查证）/ mentor（带练）/ consultant（诊断建议）/ practitioner（模板产出）。[CKA] mentor——实操考试，查证模式没有价值
- [ ] 写下安全与范围边界（一段话）。[CKA] "备考辅助，不保证通过；判卷基于本地环境，与真实考试环境可能有版本差异；不提供真题"
- [ ] 定目标用户和触发场景清单（≥10 条用户会说的原话，中英双语），这是后面 description 的原料

### 产物
- `docs/DECISIONS.md`：选题评分、角色选择、边界声明、触发场景清单

### 验收标准
- 版权结论有出处链接，不是"应该没问题"
- 边界声明能回答："这个 skill 明确不做什么？"

---

## 阶段 1：采集层 Capture（CKA 约 3-5 天）

### 任务
- [ ] 建仓库骨架：`SKILL.md` / `references/` / `scripts/` / `assets/` / `docs/`（对齐 skill-creator 官方结构）
- [ ] 拉取源材料并版本固定。[CKA] clone kubernetes/website 指定 release 分支，记录 K8s 版本号（考纲跟版本走，写进 manifest）
- [ ] 视频/音频类：ASR 转写带时间戳（你的 SenseVoice 管线）；视频跑 vision 标记板书/演示片段，选帧压 WebP。[CKA] 无视频，跳过
- [ ] PDF 类：OCR 逐物理页建记录，空白页也记录（保证页码引用永远对齐）
- [ ] 能力与配置分离：所有外部 provider 走环境变量（API_KEY / BASE_URL / MODEL），不写死，不提交 .env
- [ ] 每个采集步骤幂等：产物存在且输入未变则跳过，进度写入 progress json

### 产物
- `data/`（gitignore）：原始素材 + 采集产物 + `source-manifest.json`（来源、版本、日期、license）

### 验收标准
- 断点重跑不会重复昂贵操作
- manifest 里每个来源都有 license 字段
- 仓库里没有任何 secret 和 .env

---

## 阶段 2：证据层 Cite（CKA 约 3-5 天）——先证据后综合，顺序不能反

### 任务
- [ ] 定义证据 ID 规范：稳定 doc_id + 定位符，禁止本机绝对路径。示例：`pdf-evidence:<doc_id>#p<page>`、`k8s-docs:<path>#<anchor>`、截图用仓库内相对路径 + 时间戳
- [ ] 生成证据卡（evidence-cards.jsonl 一行一卡：id、来源、定位符、原文摘录、模块标签）
- [ ] 建 provenance 标签体系，MVP 四级：`direct_source` / `source_grounded_synthesis` / `cross_source_synthesis` / `unsupported`
- [ ] 冲突保留规则：来源矛盾时双方及条件都记录，禁止拉平成假共识。[CKA] 不同 K8s 版本行为差异按版本标注，不合并
- [ ] 建勘误记录文件 `correction-decisions.md`：每次修正记录"原文/改为/依据/日期"。[CKA] ASR 无此问题，但文档版本更新的 diff 决策记在这里

### 产物
- `references/evidence/`：evidence-cards.jsonl + index.md + correction-decisions.md

### 验收标准
- 随机抽 10 张证据卡，凭定位符能在源材料里 30 秒内找到原文
- 无重复 ID、无悬空引用（写个 validate 脚本查）

---

## 阶段 3：蒸馏层 Compress + Connect（CKA 约 5-7 天）

### 任务
- [ ] 每模块一个 Markdown，单文件 <500 行，>300 行加目录。[CKA] 按考纲域拆：troubleshooting(30%) / cluster-architecture(25%) / services-networking(20%) / workloads(15%) / storage(10%)
- [ ] 建多入口索引：术语入口 / 白话入口 / 场景入口。[CKA] 白话入口 = "Pod 起不来怎么查"→ 分水岭诊断树；场景入口 = 按考试任务类型
- [ ] 写 `references/index.md` 路由表，三列：文件 / 用途 / 何时打开
- [ ] 每条综合性结论回填 provenance 标签和证据引用
- [ ] 跑一轮内容审计 `references/audit/content-audit.md`：来源等级、覆盖边界、高风险表述检查
- [ ] [Mentor 模式] 建能力图 CapabilityGraph：能力节点 + 前置依赖边，无环。[CKA] 例：`kubectl 基础` → `Deployment 排障` → `集群级 troubleshooting`

### 产物
- `references/*.md` 蒸馏模块 + index.md 路由表 + audit 报告
- [Mentor] `references/capability-graph.md`

### 验收标准
- 冷启动测试：只给 Claude index.md，问 5 个典型问题，它能路由到正确文件
- 每个模块文件独立可读，不依赖读过其他文件
- 能力图无环、无悬空引用

---

## 阶段 4：检索与练习层（CKA 约 5-7 天）

### 任务（检索——所有模式通用）
- [ ] 写轻量检索脚本（零依赖、零网络、确定性）：领域词典分词 + filler 剥离（"帮我""查一下"）+ 简单打分排序
- [ ] 重资产（向量库/大数据集）单独分发（HF Dataset），SKILL.md 里封死自动下载："用户要求使用 ≠ 授权下载"。[CKA] 第一版不需要 RAG，跳过

### 任务（练习——Mentor 模式）
- [ ] 练习库：每个能力节点 ≥1 题，按考纲权重分布，全部原创。[CKA] 题目 = 场景描述 + 初始集群状态 manifest + 目标状态
- [ ] 判卷脚本：本地 kind/k3s 起题目环境，脚本化验收目标状态（kubectl 断言），输出 rubric 级结果。[CKA] 这是本项目最大的差异化，也是你 K8s 老本行
- [ ] H0–H4 分级提示：H0 无提示 → H4 手把手。每题预写提示阶梯
- [ ] 学习者状态外置：练习记录 append-only 事件流（JSONL/SQLite），掌握度从事件重建，绝不存进 skill 的 references/（复用你 Hearthstone 管线架构）
- [ ] 掌握度规则：一次成功 ≠ 掌握；每次成功最多推进一级；换场景 H0 成功才算迁移

### 产物
- `scripts/search_*.py` + `scripts/grade_*.sh|py`
- `references/practice-bank/`（题目）+ 提示阶梯
- 学习者状态目录约定文档（外部路径，不入库）

### 验收标准
- 检索脚本对 10 个含噪音的自然语言查询返回正确 top3
- [CKA] 随机抽 3 题：kind 环境 3 分钟内起好，判卷脚本对"正确解/错误解/部分解"三种情况判定准确
- 仓库里 grep 不到任何学习者真实数据

---

## 阶段 5：SKILL.md 编写 Codify（2-3 天）

### 任务
- [ ] frontmatter description：触发词穷举（双语、别名、场景短语），写得"pushy"——官方明确说 Claude 倾向 undertrigger。[CKA] 覆盖：CKA、K8s 认证、kubectl、troubleshooting、etcd 备份、考试模拟、"帮我练一道题"……
- [ ] Scope：一句话用途 + 边界声明（阶段 0 的产出）
- [ ] Workflow：识别入口 → 按路由表加载 → 按任务类型选固定回答骨架。[CKA] 骨架：出题（场景+环境+计时）/ 判卷（rubric 结果+一个主要瓶颈+最小有效提示）/ 讲解（概念+例+反例+两道检验题）
- [ ] Product invariants：硬规则清单——引用必带定位符 / 不暴露绝对路径 / 证据不足明说 gap / [CKA] 不提供真题、不代做考试
- [ ] 全文 <500 行，超了就加层级下沉到 references/

### 产物
- `SKILL.md` 定稿

### 验收标准
- 通过官方 `skill-creator/scripts/quick_validate.py`
- description 单独拿出来给一个没看过项目的人读，能准确说出"什么时候会用到它"

---

## 阶段 6：评测与发布（3-5 天）

### 任务（对齐 skill-creator 官方流程）
- [ ] 写 ≥10 个测试 prompt（覆盖各入口 + 2 个不应触发的负例），跑 claude-with-skill，人工过一遍结果
- [ ] 触发评测：正例应触发、负例不应触发；有条件跑官方 description 优化 loop（需 Claude Code 的 `claude -p`）
- [ ] 迭代：改 SKILL.md → 重跑测试 → 直到满意
- [ ] 打包：`package_skill.py` 出 `.skill` 文件 + `install_as_skill.sh` + 一段"丢给 agent 就能装"的安装 prompt
- [ ] README 即落地页：能做什么 / 适合场景表（必须含"不适合"行）/ 模块清单 / ≥5 个使用示例 prompt / 更新记录 / 安全与版权声明。加英文镜像 README.en.md
- [ ] `agents/openai.yaml` 兼容 Codex 生态
- [ ] 发布前最后一遍 grep：绝对路径 / secret / 学习者数据 / 版权红线内容
- [ ] 发布渠道：GitHub + 你的小红书选题（"我把 CKA 备考做成了 Claude skill"天然是好内容）+ r/kubernetes、LINUX DO

### 产物
- 公开 repo + `.skill` 包 + 双语 README

### 验收标准
- 一个新用户按 README 安装 prompt，10 分钟内完成安装并跑通第一个示例
- 10 个测试 prompt 触发率 ≥8/10，负例 0 触发

---

## 阶段 7：运营与毕业（持续）

- [ ] 更新节奏：README 顶部放"建议定期回来看更新"（学 nihaisha）；[CKA] 跟 CNCF 考纲版本，考纲变更 = 一次 minor release
- [ ] Issue 模板引导反馈类型：术语勘误 / 证据补充 / 检索体验
- [ ] [CKA] 自己的备考数据就是第一份运营素材：通过考试后写"用自己的 skill 备考 CKA 的 N 天记录"
- [ ] 抽象复盘：做完第一个后,记录哪些环节手工痛苦、值得脚本化——第二个项目（英语 skill）复用架构时决定自动化投入；第三个项目（交付方法论）前把这份 checklist 修订成你自己的 lineage 方法

---

## 附：三项目复用地图

| 资产 | CKA（首发） | 八年级英语（私有） | 交付方法论（主打） |
| --- | --- | --- | --- |
| 证据卡 + provenance 体系 | 新建 | 直接复用 | 直接复用 |
| 轻量检索脚本 | 新建 | 换词典复用 | 换词典复用 |
| 练习库 + 判卷 + H0-H4 | 新建（kubectl 断言判卷） | 复用架构（换成听写/选择题判卷） | 大部分不需要 |
| 学习者状态事件流 | 移植自 Hearthstone 管线 | 直接复用 | 不需要 |
| 素材蒸馏 | k8s 文档（结构现成） | 教材（注意版权，仅私有） | vault-distill 审讯式提纯（工作量最大） |
| 发布 | 公开双语 | 不发布 | 公开双语 + Upwork 获客 |
