---
created: 2026-06-14
tags:
  - 核心概念
  - teststep
  - 插件开发
---
# TestStep 详解

## 概述

TestStep 是 OpenTAP 中最核心的抽象，代表测试计划中的**一个执行单元**。每个步骤封装一段功能：测量、硬件控制、流程控制、用户交互等。

## 基础模板

```csharp
[Display("MyTestStep", Group: "MyPlugin", Description: "步骤描述")]
public class MyTestStep : TestStep
{
    #region Settings
    // 用户可配置的属性
    [Display("频率", Description: "测量频率，单位 Hz")]
    public double Frequency { get; set; } = 1e9;
    #endregion

    public MyTestStep()
    {
        // 设置默认值
    }

    public override void PrePlanRun()
    {
        base.PrePlanRun();
        // 测试计划运行前的一次性设置（在所有 Run 之前）
    }

    public override void Run()
    {
        // 核心逻辑
        RunChildSteps();  // 如果有子步骤
        UpgradeVerdict(Verdict.Pass);
    }

    public override void PostPlanRun()
    {
        // 测试计划运行后的一次性清理（在所有 Run 之后，逆序调用）
        base.PostPlanRun();
    }
}
```

## 生命周期方法

| 方法 | 调用时机 | 调用顺序 | 用途 |
|------|----------|----------|------|
| `PrePlanRun()` | 资源打开后，Run 之前 | 顺序（上→下，展平） | 一次性设置、资源配置 |
| `Run()` | PrePlanRun 之后 | 由父步骤控制 | 核心测试逻辑 |
| `PostPlanRun()` | Run 之后，资源关闭前 | 逆序（下→上） | 一次性清理、关机 |

> **关键**: PrePlanRun 和 PostPlanRun 总是成对调用——如果 PrePlanRun 被调用了，即使发生异常，PostPlanRun 也一定会被调用。

## 步骤层级

```
TestPlan
├── Sequence
│   ├── InstrumentSetup    ← 子步骤
│   ├── MeasurePower       ← 子步骤
│   └── Parallel           ← 父步骤（同时是 Sequence 的子步骤）
│       ├── DUT1_Test       ← 并行执行
│       └── DUT2_Test       ← 并行执行
```

### 定义父子关系

```csharp
// 方式1：父步骤声明允许哪些子步骤
[AllowAnyChild]
public class ParallelStep : TestStep { }

[AllowChildrenOfType(typeof(IMyPlugin))]
public class SpecificParent : TestStep { }

// 方式2：子步骤声明允许作为哪些父步骤的子
[AllowAsChildIn(typeof(ParallelStep))]
public class MyChild : TestStep { }
```

推荐使用**接口**而非具体类型来定义关系，提高灵活性。

## Verdict 判定

使用 `UpgradeVerdict()` 设置判定，默认只升级不降级：

```csharp
public override void Run()
{
    if (result > limit)
        UpgradeVerdict(Verdict.Pass);
    else
        UpgradeVerdict(Verdict.Fail);
}
```

判定严重度从低到高：`NotSet → Pass → Inconclusive → Fail → Aborted → Error`

[[Verdict与判定系统]] 有详细说明。

## 发布结果

```csharp
// 单行发布
Results.Publish("Power", new List<string>{"Freq", "Power"}, freq, power);

// 批量发布（最快）
Results.PublishTable("Sweep", new List<string>{"Freq", "Power"},
    freqArray, powerArray);

// 对象发布
Results.Publish(new { Frequency = 1e9, Power = -10.5 });
```

## 验证规则

```csharp
public MyTestStep()
{
    Rules.Add(() => Frequency > 0, "频率必须大于 0", nameof(Frequency));
    Rules.Add(() => LowerLimit < UpperLimit, "下限必须小于上限",
        nameof(LowerLimit), nameof(UpperLimit));
}
```

## 子步骤执行

```csharp
// 默认：顺序执行所有子步骤
RunChildSteps();

// 不抛异常（手动处理中断）
RunChildSteps(throwOnBreak: false);

// 逐个执行
foreach (var child in ChildTestSteps)
    RunChildStep(child);
```

## Input / Output 数据传递

```csharp
// 步骤 A: 产生输出
[Output]
[Display("测量值")]
public double MeasuredValue { get; private set; }

// 步骤 B: 消费输入
public Input<double> InputValue { get; set; }
// InputValue.Value — 运行时可访问
```

详见 [[Input输出系统]]

## 最佳实践

1. 每个步骤放在单独的 .cs 文件中，文件名接近 Display 名称
2. 用 `TapThread.Sleep()` 代替 `Thread.Sleep()`（可被中止）
3. 耗时的设置/清理放在 `PrePlanRun`/`PostPlanRun` 中，不要放在 `Run` 里
4. 日志用 `Log.Info()`/`Log.Debug()` 而非 `Console.WriteLine()`
5. 使用 `Stopwatch` 记录耗时操作，配合 Timing Analyzer

## 相关笔记

- [[架构概览]] — 整体架构与执行流程
- [[TestPlan与生命周期]] — TestPlan 的完整生命周期
- [[Verdict与判定系统]] — 判定传播与 Break Conditions
- [[Input输出系统]] — 步骤间数据传递
- [[Resource与仪器DUT]] — 资源管理
- [[Expression表达式系统]] — 动态表达式
- [[Mixin系统]] — 混入扩展

## 参考

- 文档: [doc/Developer Guide/Test Step/Readme.md](doc/Developer Guide/Test Step/Readme.md)
- 源码: [Engine/TestStep.cs](Engine/TestStep.cs), [Engine/ITestStep.cs](Engine/ITestStep.cs)
- 示例: [sdk/Examples/PluginDevelopment/TestSteps/](sdk/Examples/PluginDevelopment/TestSteps/)
