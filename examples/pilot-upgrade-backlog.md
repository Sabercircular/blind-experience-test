# 匿名试点证据摘录 | Anonymized pilot evidence

这份摘录只为 README 的产品升级需求表示例提供可检查的出处。受测产品、仓库、账号和截图均不公开；以下数字来自同一次真实 Flutter App 试点的运行文件与控制端复现，不是合成 demo。

This excerpt makes the README's product-upgrade backlog inspectable without publishing the subject product, repository, account, or screenshots. The numbers below come from executor files and controller reproduction in one real Flutter app pilot; they are not synthetic demo data.

## 适用范围 | Scope

- 一个 App、一个 seed；不是稳定的跨产品效果估计。
- 三路动作预算不完全相等，因此不能把结果读成统计意义上的模型胜率。
- 本页证明的是：状态与副作用台账在这次运行中找到了目标驱动探索和交互清单都漏掉的问题。
- One app and one seed; this is not a stable cross-product estimate.
- The three arms did not have identical action budgets, so the outcome is not a statistical model win rate.
- The supported claim is narrow: in this run, explicit state and side-effect ledgers found problems missed by goal-driven exploration and an interaction checklist.

## 证据台账 | Evidence ledger

测试者不知道源码、Git 历史、已知 Bug 或隐藏答案。它对可见的新建动作应用了通用状态规则：

```text
首页对象数 0   进入新建页，空返回     首页对象数 1
首页对象数 1   进入新建页，空返回     首页对象数 2
首页对象数 2   进入新建页，空返回     首页对象数 3
首页对象数 3   最小提交失败           首页对象数 4
首页对象数 4   杀进程并重新启动       首页对象数 0
```

The executor had no source, Git history, known-bug list, or hidden ground truth. It applied a generic state rule to a visible create action:

```text
Home objects 0   enter New, leave empty     Home objects 1
Home objects 1   enter New, leave empty     Home objects 2
Home objects 2   enter New, leave empty     Home objects 3
Home objects 3   minimal submission fails   Home objects 4
Home objects 4   terminate and relaunch      Home objects 0
```

控制端随后从干净状态独立复现了“空进入即新增对象”。冷重启前后的 `4 → 0` 由同一路运行台账记录。

The controller independently reproduced “empty entry creates an object” from a clean reset. The same executor ledger recorded `4 → 0` across a cold relaunch.

## 裁决摘要 | Adjudication summary

本次试点还接受了以下新发现簇；README 从中选两条改写为需求表样例：

- 发送失败后的恢复路径不完整；
- 失败消息回到列表后丢失可识别身份；
- 发送控件没有可区分的 accessibility name；
- 空状态语言不一致；
- 麦克风权限拒绝后缺少明确恢复状态。

The pilot also accepted these new finding clusters; the README turns two of them into backlog examples:

- incomplete recovery after send failure;
- failed-message identity is lost on return to the list;
- the send control has no distinguishable accessibility name;
- inconsistent empty-state language;
- no explicit recovery state after microphone permission denial.

## 哪些是事实，哪些是建议 | Fact versus recommendation

- **事实：**可见步骤、`0 → 1 → 2 → 3`、`4 → 0`、控制端复现结果和 accepted finding 分类。
- **建议：**README 表里的 P0 / P1、产品改法和建议回归入口。它们是把证据整理成目标产品需求表时新增的判断。
- **当前边界：**这份表由维护者从真实证据手工整理；当前 Skill 尚未自动生成产品升级需求表。
- **Fact:** visible steps, `0 → 1 → 2 → 3`, `4 → 0`, controller reproduction, and accepted-finding classifications.
- **Recommendation:** P0 / P1, proposed product changes, and regression entries in the README. Those judgments were added while converting evidence into the target backlog.
- **Current boundary:** a maintainer manually shaped this table from real evidence. The current skill does not yet generate the product-upgrade backlog automatically.
