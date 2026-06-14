---
created: 2026-06-14
tags:
  - GUI开发
  - 社区
  - github
---
# OpenTAP GitHub 项目全景

## OpenTAP 官方组织 (github.com/opentap)

共 **18 个项目**（含闭源 GUI 2个）。

### 🖥️ GUI 项目

| 项目 | 语言 | 开源 | 说明 |
|------|------|:---:|------|
| **[opentap/operator-panel](https://github.com/opentap/operator-panel)** | C# (WPF) | ✅ | 官方 Operator UI 示例，演示 WPF 构建运行界面 |
| **[StefanHolst/opentap-tui](https://github.com/StefanHolst/opentap-tui)** | C# (Terminal.Gui) | ✅ | 终端 UI，**最值得参考的 GUI 参考实现**，实现完整的 Annotation 绑定 |
| **Editor** (Package) | C# (WPF) | ❌ | Keysight 官方 Windows GUI 编辑器，`tap package install Editor` |
| **Editor X** (Package) | C# (跨平台) | ❌ | Keysight 跨平台编辑器，支持 Linux，`tap package install EditorX` |
| **Developer's System CE** (Package) | C# (WPF) | ❌ | 整合包 (Editor + SDK + 结果查看)，免费社区版 |

### 🔌 仪器与硬件插件

| 项目 | 语言 | 说明 |
|------|------|------|
| **[Keysight-Instrument-Plugins](https://github.com/opentap/Keysight-Instrument-Plugins)** | C# | Keysight 仪器插件合集（自动生成 SCPI） |
| **[Network-Analyzer](https://github.com/opentap/Network-Analyzer)** | C# | 网络分析仪（PNA/ENA/PXI/Streamline），最新 v0.7.4 |
| **[Signal-Source-Analyzer](https://github.com/opentap/Signal-Source-Analyzer)** | C# | Keysight SSA-X 信号源分析仪 |
| **[Keysight-DMX-VNA-OpenTap](https://github.com/opentap/Keysight-DMX-VNA-OpenTap)** | C# | DMX (S94601B) VNA 测试自动化 |
| **[PythonVisa](https://github.com/opentap/PythonVisa)** | C# | 透传 VISA 调用到 PyVISA/PyVISA-py |
| **[PSLab](https://github.com/opentap/PSLab)** | Python | PSLab (Pocket Science Lab) 仪器插件 |

### 🧩 扩展框架与工具

| 项目 | 语言 | 说明 |
|------|------|------|
| **[OpenTap.Python](https://github.com/OpenTAP/OpenTap.Python)** | C# | Python 集成，支持 Python 写 TestStep/Instrument/DUT |
| **[basic-mixins](https://github.com/opentap/basic-mixins)** | C# | 基础 Mixin：Limit、Repeat、Timeout、Dependency 等 |
| **[expressions](https://github.com/opentap/expressions)** | C# | 动态表达式引擎 |
| **[HTTP](https://github.com/opentap/HTTP)** | C# | Web API 测试插件 |
| **[Parquet](https://github.com/opentap/Parquet)** | C# | Parquet 文件格式结果输出 |
| **[MetricsAndAssets](https://github.com/opentap/MetricsAndAssets)** | C# | 指标（Poll/Push Metrics）和资产发现接口 |

### 📚 示例与教学

| 项目 | 语言 | 说明 |
|------|------|------|
| **[Demonstration](https://github.com/opentap/Demonstration)** | C# | 官方示例插件、TestStep、TestPlan |

### 🔧 CI/CD

| 项目 | 语言 | 说明 |
|------|------|------|
| **[setup-opentap](https://github.com/opentap/setup-opentap)** | JavaScript | GitHub Action，CI 中自动安装 OpenTAP |
| **[get-gitversion](https://github.com/opentap/get-gitversion)** | Shell | Git 版本号计算 Action |
| **[pr-version-comment](https://github.com/opentap/pr-version-comment)** | C# | PR 合入后自动评论 beta 版本号 |

### 🌐 社区 / 第三方

| 项目 | 语言 | 说明 |
|------|------|------|
| **[UCSC-Keysight/OpenTAP-Cobot-Plugin](https://github.com/UCSC-Keysight/OpenTAP-Cobot-Plugin)** | Python | 加州大学 × Keysight，UR3e 协作机器人 + 蜂窝天线测试 |

---

## GUI 项目深度对比

| 特性 | Editor (WPF) | Editor X | TUI | Operator Panel |
|------|:---:|:---:|:---:|:---:|
| **开源** | ❌ | ❌ | ✅ MIT | ✅ MIT |
| **平台** | Windows | Win/Linux | 全平台 | Windows |
| **框架** | WPF | — | Terminal.Gui | WPF |
| **编辑 TestPlan** | ✅ | ✅ | ✅ | ❌ |
| **拖拽步骤** | ✅ | ✅ | ❌ (键盘) | ❌ |
| **步骤属性编辑** | ✅ | ✅ | ✅ | ❌ |
| **运行 TestPlan** | ✅ | ✅ | ✅ | ✅ |
| **结果查看** | ✅ | ✅ | ✅ | ✅ |
| **包管理** | ✅ | ✅ | ✅ (tui-pm) | ❌ |
| **自定义面板** | ✅ | ❌ | ❌ | ❌ |
| **Input/Output 连线** | ✅ | ❌ | 手动 | ❌ |
| **Annotation 绑定** | ✅ | ✅ | ✅ (最完整参考) | ✅ |

---

## 自定义 GUI 开发参考顺序

1. **[StefanHolst/opentap-tui](https://github.com/StefanHolst/opentap-tui)** — 官推参考，`PropertiesView.cs` 展示了 Annotation → 控件的完整映射
2. **[opentap/operator-panel](https://github.com/opentap/operator-panel)** — WPF 版 Operator 场景的完整实现
3. **核心 API**: `AnnotationCollection.Annotate()` → `IPropEditProvider` → `IUserInputInterface`
4. **推荐框架**: Avalonia (跨平台) 或 Terminal.Gui (终端)

---

## 安装命令速查

```bash
# GUI
tap package install Editor                # WPF 编辑器 (Windows)
tap package install EditorX               # 跨平台编辑器
tap package install "Developer's System CE" -y  # 完整套装
tap package install TUI                   # 终端 UI

# 插件
tap package install "Basic Mixins"        # 基础 Mixin
tap package install Expressions           # 表达式引擎
tap package install Python                # Python 支持
tap package install HTTP                  # Web API
tap package install CSV                   # CSV 输出
tap package install "REST API"            # REST 接口
```

## 相关笔记

- [[GUI开发总览]] — GUI 生态总览与框架选择
- [[TUI架构分析]] — TUI 源码架构详解
- [[架构概览]] — OpenTAP 整体架构
- [[OpenTAP-vs-TestStand]] — 与 TestStand 的对比

## 参考

- GitHub 组织: [github.com/OpenTAP](https://github.com/OpenTAP)
- 包仓库: [packages.opentap.io](https://packages.opentap.io)
- 论坛: [forum.opentap.io](https://forum.opentap.io)
