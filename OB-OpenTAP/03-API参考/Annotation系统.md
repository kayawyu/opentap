---
created: 2026-06-14
tags:
  - API参考
  - annotation
  - GUI
  - UI
---
# Annotation 系统

## 概述

Annotation 系统是 OpenTAP 的**动态 UI 生成引擎**。它提供一种灵活的方式来描述对象与用户之间的交互，使得同一个模型可以驱动 WPF GUI、终端 TUI、JSON Web API 等多种界面。

> **核心价值**: 写一次插件代码，所有 GUI 自动适配，无需为每种 UI 框架单独编写绑定代码。

## 核心概念

```
对象 (TestStep, ComponentSettings, ...)
    │
    ▼
AnnotationCollection.Annotate(obj)
    │
    ▼
注解集合 (Annotations)
    ├── IDisplayAnnotation       → 名称、描述、分组
    ├── IStringValueAnnotation   → 文本可编辑值
    ├── IAvailableValuesAnnotation → 下拉选择
    ├── IBoolValueAnnotation     → 布尔/复选框
    ├── IMembersAnnotation       → 子成员（递归展开）
    ├── IEnabledAnnotation       → 是否可用
    ├── IAccessAnnotation        → 可见性控制
    ├── IErrorAnnotation         → 验证错误
    ├── IMultiSelect             → 多选
    ├── IBasicCollectionAnnotation → 表格/数据网格
    └── MenuAnnotation           → 右键菜单项
```

## 同一个对象，多种 UI

```
TestStep (C# 对象)
    │
    AnnotationCollection
    │
    ├── WPF Editor ───→ 窗口控件（TextBox, ComboBox, DataGrid）
    ├── TUI ─────────→ 终端控件（Terminal.Gui）
    └── REST API ────→ JSON Schema
```

## 常用注解类型

| 接口 | 说明 | UI 映射 |
|------|------|---------|
| `IStringValueAnnotation` | 可编辑的文本值 | TextBox / 单行输入 |
| `IStringReadOnlyValueAnnotation` | 只读文本值 | Label / 禁用输入 |
| `IAvailableValuesAnnotation` | 可选值列表 | ComboBox / 下拉框 |
| `ISuggestedValuesAnnotation` | 建议值（可自定义） | ComboBox(可编辑) |
| `IMultiSelect` | 多选 | CheckList |
| `IDisplayAnnotation` | 名称/描述/分组/排序 | 标签、工具提示 |
| `IEnabledAnnotation` | 是否可编辑 | IsEnabled 绑定 |
| `IAccessAnnotation` | 可见/可写 | IsVisible / IsReadOnly |
| `IErrorAnnotation` | 验证错误 | 错误提示 |
| `IBasicCollectionAnnotation` | 集合 | DataGrid / 表格 |
| `IMembersAnnotation` | 子成员 | 展开/子树 |

## 使用方式

### 获取注解

```csharp
// 一行代码获得完整 UI 模型
var annotations = AnnotationCollection.Annotate(myTestStep);

// 获取可编辑的成员
var members = annotations.Get<IMembersAnnotation>()?.Members;

// 获取显示名称
var name = annotations.Get<IDisplayAnnotation>()?.Name;

// 获取字符串值
var value = annotations.Get<IStringValueAnnotation>()?.Value;
```

### 自定义 Annotator

```csharp
// 实现 IAnnotator 为特定类型提供自定义注解
public class MyTypeAnnotator : IAnnotator
{
    public double Priority => 1;  // 控制注解顺序

    public void Annotate(AnnotationCollection annotations)
    {
        // 为对象添加自定义注解
        if (annotations.Source is MyType obj)
        {
            // 添加自定义的可用值等
        }
    }
}
```

## 在 GUI 中使用 Annotation

以 opentap-tui 为例的模式：

```csharp
// 1. 获取注解
var annotations = AnnotationCollection.Annotate(selectedStep);
var members = annotations.Get<IMembersAnnotation>()?.Members;

// 2. 遍历成员，按注解类型路由到对应 UI 控件
foreach (var member in members)
{
    if (member.Get<IStringValueAnnotation>() != null)
        CreateTextBox(member);    // → 文本输入
    else if (member.Get<IAvailableValuesAnnotation>() != null)
        CreateComboBox(member);   // → 下拉选择
    else if (member.Get<IMultiSelect>() != null)
        CreateMultiSelect(member); // → 多选列表
    else if (member.Get<IMembersAnnotation>() != null)
        CreateSubTree(member);    // → 递归展开
}
```

完整的参考实现在 [StefanHolst/opentap-tui](https://github.com/StefanHolst/opentap-tui) 的 `PropertiesView.cs` 中。

## 设计原则

1. **描述性而非命令式** — 注解描述"是什么"，而非"怎么渲染"
2. **UI 无关** — 不依赖任何特定 GUI 框架
3. **可扩展** — 通过 `IAnnotator` 插件扩展注解类型
4. **不推荐自定义注解** — 自定义注解会破坏跨 UI 兼容性，如需新增应发起社区讨论

## 相关笔记

- [[GUI开发总览]] — OpenTAP GUI 生态总览
- [[TUI架构分析]] — TUI 如何使用 Annotation 系统
- [[TestStep详解]] — TestStep 的属性即注解源
- [[Mixin系统]] — Mixin 通过注解添加动态属性

## 参考

- 文档: [doc/Developer Guide/Annotations/Readme.md](doc/Developer Guide/Annotations/Readme.md)
- 源码: [Engine/Annotations/Annotation.cs](Engine/Annotations/Annotation.cs)
- TUI 参考: [StefanHolst/opentap-tui — PropertiesView.cs](https://github.com/StefanHolst/opentap-tui/blob/main/OpenTAP.TUI/Views/PropertiesView.cs)
