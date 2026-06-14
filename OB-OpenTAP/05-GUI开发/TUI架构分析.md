---
created: 2026-06-14
tags:
  - GUI开发
  - tui
  - 源码分析
---
# TUI 架构分析

## 概述

[opentap-tui](https://github.com/StefanHolst/opentap-tui) 是 OpenTAP 的**终端文本用户界面**，也是**官方推荐的自定义 GUI 参考实现**。使用 Terminal.Gui (gui.cs) 框架。

- **仓库**: [github.com/StefanHolst/opentap-tui](https://github.com/StefanHolst/opentap-tui)
- **UI 框架**: Terminal.Gui (git submodule)
- **入口**: `tap tui` / `tap tui-pm` / `tap tui-results`

## 架构概览

```
TuiAction (抽象基类)
├── TUI         → 主编辑器 (TestPlan 编辑+运行)
├── TuiPm       → 包管理器 (安装/卸载/浏览)
└── TuiResults  → 结果查看器 (历史运行记录)
```

## 源码结构

```
OpenTAP.TUI/
├── OpenTAP.TUI.cs          # MainWindow + TUI 入口
├── TuiAction.cs            # 抽象基类: Terminal.Gui 初始化 + 异常恢复
├── TuiPm.cs                # 包管理器 CLI Action
├── TuiResults.cs           # 结果查看器 CLI Action
├── TuiUserInput.cs         # IUserInputInterface 实现
├── TuiSettings.cs          # TUI 设置持久化
├── KeyMapper.cs            # 快捷键映射
│
├── Views/                  # 可复用视图组件
│   ├── PropertiesView.cs   # ★ 核心: Annotation → 终端控件
│   ├── TestPlanView.cs     # ★ 步骤树 (TreeView<ITestStep>)
│   ├── LogPanelView.cs     # 实时日志面板
│   ├── TreeView.cs         # 通用树形控件
│   ├── DatagridView.cs     # 表格视图
│   ├── SelectorView.cs     # 列表选择器
│   └── Recovery.cs         # 崩溃恢复
│
├── Windows/                # 弹窗/子窗口
│   ├── NewPluginWindow.cs  # 新增步骤/插件选择
│   ├── EditWindow.cs       # 编辑对话框基类
│   ├── PackageManagerWindow.cs
│   ├── ResultsWindow.cs
│   ├── ComponentSettingsWindow.cs
│   ├── ResourceSettingsWindow.cs
│   ├── ConnectionSettingsWindow.cs
│   └── RunExplorerWindow.cs
│
├── PropEditProviders/      # Annotation → 控件映射
│   ├── IPropEditProvider.cs      # interface: Order + Edit()
│   ├── BooleanEditProvider.cs    # IBoolean → CheckBox
│   ├── EnumEditProvider.cs       # IAvailableValues → ComboBox
│   ├── DataGridEditProvider.cs   # IBasicCollection → DataGrid
│   ├── MultiSelectProvider.cs    # IMultiSelect → 多选列表
│   ├── ActionProvider.cs         # IMethod → Button
│   ├── DefaultEditProvider.cs    # IStringValue → TextBox (fallback)
│   └── ...
│
└── Annotations/            # 自定义 Annotation 类型
    ├── IResultColumnAnnotation.cs
    └── KeyEventAnnotation.cs
```

## 核心流程

### 1. Annotation → UI 控件映射

```csharp
// PropertiesView.cs 核心流程
void LoadProperties(object obj)
{
    var annotations = AnnotationCollection.Annotate(obj);
    var members = annotations.Get<IMembersAnnotation>()?.Members;

    foreach (var member in members)
    {
        // 按 Order 排序遍历所有 IPropEditProvider
        foreach (var provider in editProviders.OrderBy(p => p.Order))
        {
            var view = provider.Edit(member, isReadOnly);
            if (view != null)
            {
                treeView.Add(view);  // 添加到 UI 树
                break;               // 第一个匹配即停止
            }
        }
    }
}
```

### 2. 新增步骤

```csharp
// NewPluginWindow.cs
var types = TypeData.GetDerivedTypes(typeof(TestStep))
    .Where(x => x.CanCreateInstance)
    .Where(x => x.GetAttribute<BrowsableAttribute>()?.Browsable ?? true)
    .Where(x => TestStepList.AllowChild(parentType, x));
// 展示为分组树，用户选择后实例化并添加到步骤树
```

### 3. 用户输入处理

```csharp
// TuiUserInput.cs
public void RequestUserInput(object dataObject, TimeSpan Timeout, bool modal)
{
    var annotations = AnnotationCollection.Annotate(dataObject);
    var dialog = new EditWindow(title) { ... };
    var propertiesView = new PropertiesView();
    propertiesView.LoadProperties(dataObject, true);
    propertiesView.Submit += () => { Application.Current.Running = false; };
    dialog.Add(propertiesView);
    Application.Run(dialog);  // 模态弹窗
}
```

### 4. 主窗口布局

```
┌ OpenTAP TUI ───────────────────────────────────┐
│ [F9] File  Edit  Bench  Settings  Tools  Help  │
├────────────────────────────────────────────────┤
│ ┌ TestPlan [F6] ──────┐ ┌ Settings [F7] ────┐ │
│ │ 步骤树形结构          │ │ 选中步骤的动态属性 │ │
│ │                      │ │                   │ │
│ └──────────────────────┘ └───────────────────┘ │
├────────────────────────────────────────────────┤
│ ┌ Log Panel [F8] ────────────────────────────┐ │
│ │ 实时日志输出                                 │ │
│ └─────────────────────────────────────────────┘ │
├────────────────────────────────────────────────┤
│ [F1] TestPlan Settings  [F2] Insert New Step   │
└────────────────────────────────────────────────┘
```

## 关键设计决策

| 决策 | 说明 |
|------|------|
| **禁用鼠标** | `Application.IsMouseDisabled = true`，纯键盘操作 |
| **崩溃恢复** | `Recovery.cs` 自动保存，下次启动恢复 |
| **IUserInputInterface 替换** | `UserInput.SetInterface(new TuiUserInput())` 接管 CLI 交互 |
| **日志重定向** | 移除 ConsoleTraceListener 防覆盖 UI，日志输出到底部面板 |
| **自定义快捷键** | `KeyMapper.cs` + `KeyTypes` 枚举，用户可定制 |

## 如何基于 TUI 构建自定义 GUI

```csharp
// 1. 选一个 UI 框架 (Avalonia / Blazor / ...)

// 2. 复用 Annotation → 控件映射模式
var annotations = AnnotationCollection.Annotate(myStep);
foreach (var member in annotations.Get<IMembersAnnotation>().Members)
{
    // 映射到你的框架控件:
    // IStringValueAnnotation → <TextBox />
    // IBoolValueAnnotation   → <CheckBox />
    // IAvailableValuesAnnotation → <ComboBox />
    // ...
}

// 3. 实现 IUserInputInterface
class MyUserInput : IUserInputInterface
{
    void RequestUserInput(object data, TimeSpan timeout, bool modal)
    {
        // 在你的 GUI 中弹窗
    }
}
UserInput.SetInterface(new MyUserInput());

// 4. 列出可用步骤类型
var types = TypeData.GetDerivedTypes(typeof(TestStep))
    .Where(x => x.CanCreateInstance && x.Browsable);

// 5. 执行 TestPlan
await plan.Execute();
```

## 相关笔记

- [[Annotation系统]] — Annotation 驱动 UI 的机制
- [[GUI开发总览]] — 所有 GUI 选项对比
- [[IUserInputInterface详解]] — 用户交互接口
- [[插件开发入门]] — 插件开发基础

## 参考

- [github.com/StefanHolst/opentap-tui](https://github.com/StefanHolst/opentap-tui)
- [doc/Developer Guide/Annotations/Readme.md](doc/Developer%20Guide/Annotations/Readme.md)
