---
created: 2026-06-14
tags:
  - API参考
  - mixin
  - 扩展
---
# Mixin 系统

## 概述

Mixin（混入）是一种向现有步骤**动态注入功能**的机制。来自面向对象编程中的 "mix-in" 概念——可以混入其他类的扩展。

在 OpenTAP 中，Mixin 为 TestStep 添加：
- 新的可配置设置
- 生命周期钩子（PreRun / PostRun）
- 可复用的功能块

## 核心插件

| 包 | 内容 |
|----|------|
| **Basic Mixins** | Limit（上下限判定）、Repeat、Timeout、Dependency |
| **Expressions** | Number、Text Mixin |

```bash
tap package install "Basic Mixins"
tap package install Expressions
```

## 使用方式（终端用户）

1. 在 GUI 中右键点击步骤设置区域 → "Add Mixin"
2. 选择 Mixin 类型
3. Mixin 的新设置出现在步骤属性面板中
4. 右键 Mixin 的设置 → "Remove Mixin" 移除

## Mixin 类型（生命周期钩子）

| 接口 | 触发时机 |
|------|----------|
| `ITestStepPreRunMixin` | 步骤 Run() 之前 |
| `ITestStepPostRunMixin` | 步骤 Run() 之后 |
| `ITestPlanPreRunMixin` | TestPlan PreRun 阶段 |
| `ITestPlanPostRunMixin` | TestPlan PostRun 阶段 |

## 编写简单 Mixin

```csharp
// 步骤 1: 定义 Mixin 类
public class EmbeddingClassMixin : ITestStepPostRunMixin
{
    [Display("Some Setting")]
    public string SomeSetting { get; set; } = "123";

    static readonly TraceSource log = Log.CreateSource("test");

    public void OnPostRun(TestStepPostRunEventArgs eventArgs)
    {
        log.Info($"OnPostRun executed. SomeSetting = {SomeSetting}");
    }
}

// 步骤 2: 在 TestStep 中嵌入
public class EmbedderTestStep : TestStep
{
    [EmbedProperties]
    public EmbeddingClassMixin Embed { get; } = new EmbeddingClassMixin();
}
```

## 编写可发现的 Mixin（IMixinBuilder）

让 Mixin 出现在 GUI 的 "Add Mixin" 菜单中：

```csharp
[Display("My Mixin", "This is an example of a mixin.")]
[MixinBuilder(typeof(ITestStepParent))]  // 指定支持的目标类型
public class MyMixinBuilder : IMixinBuilder
{
    public string MemberName { get; set; } = "";

    public void Initialize(ITypeData type)
    {
        // 初始化设置，避免命名冲突
    }

    public MixinMemberData ToDynamicMember(ITypeData targetType)
    {
        return new MixinMemberData(this, () => new EmbeddingClassMixin())
        {
            Name = "MyMixinBuilder:" + MemberName,
            TypeDescriptor = TypeData.FromType(typeof(EmbeddingClassMixin)),
            Attributes = new object[]
            {
                new DisplayAttribute(MemberName),
                new EmbedPropertiesAttribute()
            },
            DeclaringType = TypeData.FromType(typeof(ITestStep))
        };
    }
}
```

## Mixin vs 继承 vs 组合

| 方式 | 优点 | 缺点 |
|------|------|------|
| **Mixin** | 运行时动态添加，用户可选 | 实现复杂（需要 IMixinBuilder） |
| **继承** | 简单直接 | 类型膨胀，不灵活 |
| **组合（EmbedProperties）** | 代码复用 | 无法动态添加/移除 |

推荐：用 `[EmbedProperties]` 直接嵌入来复用代码（组合），用 `IMixinBuilder` 来让用户可选的 Mixin。

## 常见 Mixin

| Mixin | 功能 |
|-------|------|
| Limit Mixin | 为步骤输出添加上下限判定 |
| Repeat Mixin | 步骤自动重复执行 |
| Timeout Mixin | 步骤超时控制 |
| Dependency Mixin | 资源 Open/Close 顺序控制 |
| Number/Text Mixin | 添加数字/文本设置 |

## 相关笔记

- [[TestStep详解]] — Mixin 的作用目标
- [[Annotation系统]] — Mixin 通过 Annotation 暴露设置到 GUI
- [[Expression表达式系统]] — Expression 常与 Mixin 配合

## 参考

- 仓库: [github.com/opentap/basic-mixins](https://github.com/opentap/basic-mixins)
- 仓库: [github.com/opentap/expressions](https://github.com/opentap/expressions)
- 文档: [doc/Developer Guide/Test Step/Readme.md](doc/Developer Guide/Test Step/Readme.md) (Mixins 节)
