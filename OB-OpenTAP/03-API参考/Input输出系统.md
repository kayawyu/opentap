---
created: 2026-06-14
tags:
  - API参考
  - input
  - output
  - 数据传递
---
# Input / Output 系统

## 概述

Input/Output 系统是 OpenTAP 中**步骤间数据传递**的机制。一个步骤通过 `[Output]` 发布数据，另一个步骤通过 `Input<T>` 消费数据。

## 基本模式

```csharp
// ═══ 步骤 A: 产生数据 ═══
public class GenerateData : TestStep
{
    [Output]
    [Display("测量电压")]
    public double MeasuredVoltage { get; private set; }

    public override void Run()
    {
        MeasuredVoltage = 3.3;
        UpgradeVerdict(Verdict.Pass);
    }
}

// ═══ 步骤 B: 消费数据 ═══
public class ConsumeData : TestStep
{
    [Display("输入电压")]
    public Input<double> InputVoltage { get; set; }

    public ConsumeData()
    {
        InputVoltage = new Input<double>();
    }

    public override void Run()
    {
        double v = InputVoltage.Value;  // 阻塞等待上游产出
        Log.Info($"电压: {v} V");
    }
}
```

## Output 属性

```csharp
// 默认: Availability = AfterRun (Run 完成后可用)
[Output]
public double Value1 { get; private set; }

// BeforeRun: PrePlanRun 后可用
[Output(Availability = OutputAvailability.BeforeRun)]
public double Value2 { get; private set; }

// AfterDefer: Defer 任务完成后可用
[Output(Availability = OutputAvailability.AfterDefer)]
public double Value3 { get; private set; }
```

| Availability | 可用时机 |
|---|---|
| `BeforeRun` | PrePlanRun 后即可用 |
| `AfterRun` | Run() 完成后可用（默认） |
| `AfterDefer` | Defer 任务完成后可用 |

## 类型兼容性矩阵

| Input → / Output ↓ | Number | String | Boolean | Instrument | DUT |
|---------------------|--------|--------|---------|------------|-----|
| Number | ✅ | ✅ | ✅ | ❌ | ❌ |
| String | ✅ | ✅ | ✅ | ❌ | ❌ |
| Boolean | ✅ | ✅ | ✅ | ❌ | ❌ |
| Instrument | ❌ | ❌ | ❌ | ✅ (及子类) | ❌ |
| DUT | ❌ | ❌ | ❌ | ❌ | ✅ |

## 连接方式

### 方式1: GUI 右键连接

1. 右键点击要赋值的属性 → "Assign Output"
2. 选择输出范围（TestPlan 级别、父步骤级别等）
3. 选择具体的 Output 属性

### 方式2: 直接连接任何兼容设置

Output 不仅限于 `Input<T>`，可以连接到任何兼容类型的设置：
- 数字 Output → 数字设置
- 字符串 Output → Dialog 的文本
- Verdict Output → If 步骤的条件

## 参数化（Parameterization）

多个步骤的同一设置可以通过参数化统一管理：

```
TestPlan
├── Frequency (参数化到 TestPlan)  ← 外部参数
├── SignalGenerator
│   └── Frequency → 引用 TestPlan.Frequency
└── SignalAnalyzer
    └── Frequency → 引用 TestPlan.Frequency
```

```bash
# CLI 中设置外部参数
tap run test.TapPlan -e "Frequency=10MHz"
```

Sweep 步骤利用参数化实现扫参：
- **Sweep Parameter** — 按值表遍历参数
- **Sweep Parameter Range** — 按范围和步长遍历参数

## 相关笔记

- [[TestStep详解]] — Input/Output 的完整代码示例
- [[Expression表达式系统]] — 用表达式引用 Output: `@StepName.OutputName`
- [[TestPlan与生命周期]] — Output Available 时机

## 参考

- 源码: [Engine/Input.cs](Engine/Input.cs), [Engine/OutputAttribute.cs](Engine/OutputAttribute.cs)
- 文档: [doc/Developer Guide/Test Step/Readme.md](doc/Developer Guide/Test Step/Readme.md) (Inputs and Outputs 节)
