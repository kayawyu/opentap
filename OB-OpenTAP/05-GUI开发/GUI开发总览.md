---
created: 2026-06-14
tags:
  - GUI开发
  - overview
  - editor
  - tui
---
# GUI 开发总览

## OpenTAP GUI 生态

OpenTAP 提供**多种 GUI 前端**，适用于不同的场景：

| GUI | 类型 | 平台 | 开源 | 安装 |
|-----|------|------|------|------|
| **Editor** (Developer's System) | WPF 桌面 | Windows | ❌ (免费) | `tap package install Editor` |
| **Editor X** | 跨平台桌面 | Win/Linux | ❌ (免费) | `tap package install EditorX` |
| **TUI** | 终端文本 UI | 全平台 | ✅ MIT | `tap package install TUI` |
| **Operator Panel** | WPF 桌面 | Windows | ✅ MIT | [github.com/opentap/operator-panel](https://github.com/opentap/operator-panel) |

## 各 GUI 功能对比

| 功能 | Editor (WPF) | Editor X | TUI | Operator Panel |
|------|:---:|:---:|:---:|:---:|
| TestPlan 编辑 | ✅ | ✅ | ✅ | ❌ |
| 拖拽步骤 | ✅ | ✅ | ❌ (键盘) | ❌ |
| 步骤属性编辑 | ✅ | ✅ | ✅ | ❌ |
| 运行 TestPlan | ✅ | ✅ | ✅ | ✅ |
| 结果查看 | ✅ | ✅ | ✅ | ✅ |
| 包管理 | ✅ | ✅ | ✅ (tui-pm) | ❌ |
| 自定义面板 | ✅ (DockablePanel) | ❌ | ❌ | ❌ |
| Input/Output 连线 | ✅ (右键) | ❌ | 手动 | ❌ |
| 多选移动 | ✅ | ❌ | ✅ | ❌ |

## 核心 GUI 架构

```
┌──────────────────────────────────────────────┐
│              OpenTAP Engine                   │
│  TestStep / TestPlan / PluginManager / ...    │
├──────────────────────────────────────────────┤
│        Annotation System (中间层)             │
│  AnnotationCollection.Annotate(obj)           │
│  → IStringValue, IAvailableValues, ...        │
├──────────────────────────────────────────────┤
│  GUI 框架 (WPF / Terminal.Gui / Avalonia)    │
│  Annotation → UI 控件映射                     │
├──────────────────────────────────────────────┤
│  IUserInputInterface (用户输入抽象)           │
│  GUI 实现此接口处理对话框/弹窗               │
└──────────────────────────────────────────────┘
```

所有 GUI 共享同一套 Annotation 层，这意味着：
- **插件开发者**无需为不同 GUI 写绑定代码
- **GUI 开发者**可以用任意框架实现界面，只需处理 Annotation

## 开发自定义 GUI 的关键接口

| 接口 | 用途 | 实现示例 |
|------|------|----------|
| `AnnotationCollection.Annotate()` | 获取对象的 UI 描述 | `PropertiesView.cs` in TUI |
| `IUserInputInterface` | 处理用户输入弹窗 | `TuiUserInput.cs` |
| `TypeData.GetDerivedTypes()` | 列出所有可用步骤类型 | `NewPluginWindow.cs` in TUI |
| `TestStepList.AllowChild()` | 检查父子步骤兼容性 | `TestPlanView.cs` in TUI |
| `ComponentSettings.GetCurrent()` | 读取设置 | `ComponentSettingsWindow.cs` in TUI |
| `TestPlan.Execute()` | 执行测试计划 | `TestPlanView.cs` in TUI |

## 开发自定义 GUI 的建议路线

1. **首选参考**: [StefanHolst/opentap-tui](https://github.com/StefanHolst/opentap-tui) — 最完整的参考实现
2. **WPF 参考**: [opentap/operator-panel](https://github.com/opentap/operator-panel) — WPF 示例
3. **文档**: [doc/Developer Guide/Annotations/Readme.md](doc/Developer%20Guide/Annotations/Readme.md)
4. **理解核心**: `AnnotationCollection.Annotate()` → `IPropEditProvider` 模式

## Gui 框架选择

| 框架 | 适合场景 | 成本 |
|------|----------|------|
| **Avalonia** | 跨平台桌面 GUI，最接近 WPF 体验 | 中 |
| **Terminal.Gui** | 终端 UI，SSH/容器友好 | 低 |
| **Blazor Hybrid** | Web 技术栈 | 中 |
| **Electron + C# Backend** | 丰富前端生态 | 高 |
| **WPF** | Windows 桌面 | 低 |

## 相关笔记

- [[Annotation系统]] — 动态 UI 生成核心
- [[TUI架构分析]] — TUI 源码架构详解
- [[TestStep详解]] — 步骤开发
- [[插件开发入门]] — 插件开发

## 参考

- [github.com/StefanHolst/opentap-tui](https://github.com/StefanHolst/opentap-tui)
- [github.com/opentap/operator-panel](https://github.com/opentap/operator-panel)
- [doc/User Guide/Editors/Readme.md](doc/User%20Guide/Editors/Readme.md)
