---
created: 2026-06-14
tags:
  - GUI开发
  - 自定义GUI
  - Avalonia
  - WPF
---
# 自定义 GUI 开发指南

## 背景

OpenTAP 官方 GUI（Editor / Editor X）均为闭源（免费），社区有两个开源参考实现：TUI（终端）和 Operator Panel（WPF）。如果需要在 macOS/Linux 上使用图形化 GUI，或需要深度定制，可以考虑自建。

## 开发难度评估

| 目标 | 难度 | 预估工时（单人全职） | 说明 |
|------|:---:|:---:|------|
| 轻量 TestPlan 运行器 | 低 | 2-4 周 | 解析 .TapPlan + 调用 TestPlan.Execute() + 显示结果 |
| 完整编辑器（替代 Editor） | 高 | 3-6 月 | 步骤增删改、Input/Output 连线、Annotation 完整绑定 |
| 产线 Operator 面板 | 中 | 1-2 月 | 加载计划、运行、显示结果和判定 |

## 框架选择

| 框架 | 跨平台 | .NET 原生 | UI 开发效率 | 适合场景 |
|------|:---:|:---:|:---:|------|
| **Avalonia UI** | ✅ | ✅ | 高 (XAML) | 跨平台桌面 GUI，最接近 WPF 体验 |
| **Terminal.Gui** | ✅ | ✅ | 中 | 终端 UI，SSH/容器友好 |
| **Blazor Hybrid** | ✅ | ✅ | 高 (HTML/CSS) | Web 技术栈团队 |
| **MAUI** | ✅ | ✅ | 中 | 微软官方方案，macOS 支持待完善 |
| **WPF** | ❌ | ✅ | 高 (XAML) | 仅 Windows 桌面 |
| **Electron + C# Backend** | ✅ | ❌ | 高 | 前端生态丰富，IPC 开销大 |

### 推荐: Avalonia UI

- 跨平台（Win/Mac/Linux），与 OpenTAP 跨平台定位一致
- XAML 语法与 WPF 相似，学习曲线低
- 纯 .NET，可与 OpenTAP 共享进程，零 IPC 开销

## 核心架构模式

```
┌──────────────────────────────────────────────┐
│              OpenTAP Engine                   │
│  (同进程引用 OpenTap.dll)                     │
├──────────────────────────────────────────────┤
│        Annotation System                      │
│  AnnotationCollection.Annotate(obj)           │
├──────────────────────────────────────────────┤
│        UI 绑定层 (手动桥接)                   │
│  IStringValueAnnotation → TextBox             │
│  IAvailableValuesAnnotation → ComboBox        │
│  IBoolValueAnnotation → CheckBox              │
│  IMembersAnnotation → 递归子树               │
│  IErrorAnnotation → 验证错误提示             │
├──────────────────────────────────────────────┤
│        GUI Framework                          │
│  Avalonia / Terminal.Gui / WPF / Blazor       │
└──────────────────────────────────────────────┘
```

## 开发路线图（以 Avalonia 为例）

### Phase 1: 基础框架 (1-2 周)
- [ ] Avalonia 项目搭建，引用 OpenTap.dll
- [ ] 主窗口布局（步骤树 + 属性面板 + 日志）
- [ ] `AnnotationCollection.Annotate()` → Avalonia 控件映射
- [ ] 加载 .TapPlan 文件，展示步骤树

### Phase 2: 编辑功能 (2-4 周)
- [ ] 添加/删除/移动步骤
- [ ] 属性编辑（Annotation → 控件双向绑定）
- [ ] 步骤验证（Rules 错误提示）
- [ ] 保存 .TapPlan

### Phase 3: 运行与监控 (2-3 周)
- [ ] TestPlan.Execute() 集成
- [ ] 实时日志输出
- [ ] Verdict 实时更新
- [ ] Break / Abort 控制

### Phase 4: 高级功能 (3-6 周)
- [ ] Input/Output 连线可视化
- [ ] 拖拽步骤
- [ ] 包管理集成
- [ ] Bench 设置面板
- [ ] 参数化支持
- [ ] Expression/Mixin 支持

## 关键 API 速查

```csharp
// 1. 列出所有可用步骤
var stepTypes = TypeData.GetDerivedTypes(typeof(TestStep))
    .Where(x => x.CanCreateInstance && x.Browsable);

// 2. 获取步骤的 UI 模型
var annotations = AnnotationCollection.Annotate(myStep);
var members = annotations.Get<IMembersAnnotation>()?.Members;

// 3. 检查步骤是否可以放在某父步骤下
bool canAdd = TestStepList.AllowChild(parentType, childType);

// 4. 执行测试计划
var planRun = plan.Execute();

// 5. 注册用户输入处理器
UserInput.SetInterface(new MyUserInputHandler());

// 6. 读取设置
var engineSettings = EngineSettings.Current;
var instrumentSettings = InstrumentSettings.Current;
```

## Annotation → Avalonia 控件映射参考

| Annotation 接口 | Avalonia 控件 | 绑定方向 |
|----------------|-------------|:---:|
| `IStringValueAnnotation` | `TextBox` | 双向 |
| `IBoolValueAnnotation` | `CheckBox` | 双向 |
| `IAvailableValuesAnnotation` | `ComboBox` | 双向 |
| `IMultiSelect` | `ListBox` (多选) | 双向 |
| `IMembersAnnotation` | 递归生成子树 | — |
| `IErrorAnnotation` | `TextBlock` (红色) | 单向 |
| `IDisplayAnnotation` | `Label` / `ToolTip` | 单向 |
| `IEnabledAnnotation` | `IsEnabled` 绑定 | 单向 |
| `IAccessAnnotation` | `IsVisible` 绑定 | 单向 |
| `IBasicCollectionAnnotation` | `DataGrid` | 双向 |
| `IMethodAnnotation` | `Button` | 命令 |

## 实现 IUserInputInterface

```csharp
public class MyUserInput : IUserInputInterface
{
    public void RequestUserInput(object dataObject, TimeSpan timeout, bool modal)
    {
        // 1. 获取 UI 模型
        var annotations = AnnotationCollection.Annotate(dataObject);
        var members = annotations.Get<IMembersAnnotation>()?.Members;

        // 2. 在 GUI 中创建弹窗
        var dialog = new Window { ... };
        var panel = GeneratePropertyPanel(members);  // 复用映射逻辑
        dialog.Content = panel;

        // 3. 寻找 Submit 按钮
        var submitMember = members.FirstOrDefault(m =>
            m.Get<SubmitAttribute>() != null);
        if (submitMember != null)
        {
            // 添加确认按钮，点击时调用 submitMember.Get<IMethodAnnotation>().Invoke()
        }

        // 4. 显示对话框
        dialog.ShowDialog();
    }
}

// 应用启动时注册
UserInput.SetInterface(new MyUserInput());
```

## 难点与对策

| 难点 | 对策 |
|------|------|
| **Annotation 绑定非标准** | 没有现成的 MVVM 绑定，需手动写桥接代码（参考 TUI 的 `PropEditProviders/`） |
| **插件热加载** | 监听文件系统变化，调用 `PluginManager.SearchAsync()` |
| **TestPlan 大文件** | 步骤树虚拟化渲染 |
| **线程安全** | Annotation 操作必须在 `TapThread.MainThread` 执行 |
| **跨平台兼容** | 避免 Windows 专有 API，使用 .NET 跨平台 API |
| **IUserInputInterface 模态** | 需要在 GUI 框架中正确实现模态弹窗 |

## 相关笔记

- [[GUI开发总览]] — 所有 GUI 选项对比
- [[TUI架构分析]] — TUI 源码架构（最佳参考）
- [[Annotation系统]] — Annotation 驱动 UI 的完整机制
- [[GitHub项目列表]] — 所有相关仓库
- [[插件开发入门]] — 插件开发基础
