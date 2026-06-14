#!/usr/bin/env python3
"""Generate batch-39 knowledge graph from structural extraction results."""
import json, os, math

os.chdir('/Users/yujiayou/CsharpProject/opentap')

with open(".understand-anything/tmp/ua-file-extract-results-39.json") as f:
    data = json.load(f)

# Accumulate nodes and edges
nodes = []
edges = []
seen_ids = set()

def add_node(node):
    if node['id'] not in seen_ids:
        seen_ids.add(node['id'])
        nodes.append(node)

def add_edge(edge):
    edges.append(edge)

# ---- Manual per-class/function summaries (Chinese) ----
# These provide richer context than auto-generated summaries

class_summaries = {
    "PackageAction": "包操作的抽象基类，实现 ICliAction 接口。提供日志、进度更新事件、错误事件及仓库令牌提取等公共基础设施，所有包 CLI 动作均直接或间接继承自此。",
    "PackageActionHelper": "提供 PackageAction 的静态辅助方法，包括从 CLI 上下文执行任意包操作、按预发布标签过滤包列表以及记录程序集版本信息。",
    "PackageActionHelpers": "包操作静态辅助类，提供包的快速解析、依赖与包定义收集、批量下载及规范文件名生成等核心工具方法。",
    "CacheAction": "清除本地包缓存目录的 CLI 动作，继承自 LockingPackageAction。",
    "PackageCreateAction": "包创建 CLI 动作，从工程目录或 package.xml 生成 .TapPackage 归档，处理文件路径、版本注入和依赖分析。",
    "PackageDownloadAction": "包下载 CLI 动作，从仓库解析并下载包及其依赖到本地输出路径。支持版本、架构、操作系统筛选和无缓存模式。",
    "ImageInstallAction": "镜像安装 CLI 动作，将 OpenTAP 部署镜像中的包集合并或复制到目标安装目录，支持 DryRun 预览。",
    "PackageInstallAction": "包安装 CLI 动作，完整的安装流程包括依赖解析、下载、兼容性检查、覆盖处理和许可证验证，是包管理器最核心的执行动作。",
    "IsolatedPackageAction": "隔离包操作抽象基类，继承自 LockingPackageAction，在隔离进程中执行变更操作以确保正在运行的 DLL 可被安全覆盖。",
    "PackageListAction": "包列表 CLI 动作，查询仓库中可用或已安装的包，支持多种过滤条件并以 Markdown 表格等格式输出。",
    "LockingPackageAction": "带互斥锁的包操作抽象基类，继承自 PackageAction，通过命名 Mutex 确保同一安装目录下的操作串行化。",
    "PackageExitCodes": "包 CLI 操作的退出码枚举（30-59），覆盖创建失败、无效定义、依赖错误、安装/卸载错误和 EULA 未接受等场景。",
    "PackageShowAction": "包详情展示 CLI 动作，显示包的元数据、依赖关系、包含的文件及插件信息，支持 Markdown 格式化输出。",
    "PackageTestAction": "包测试 CLI 动作，验证指定包是否存在于安装目录中并报告结果。",
    "PackageUninstallAction": "包卸载 CLI 动作，移除已安装包及其文件，检测反向依赖并处理用户交互确认。",
    "ContinueRequest": "卸载过程中的继续确认交互请求数据模型。",
    "UninstallRequest": "卸载过程中提示用户输入包名的交互请求数据模型。",
    "PackageCacheHelper": "本地包缓存管理类，提供缓存目录路径解析、缓存文件存取和清理功能，支持环境变量覆盖。",
    "PackageCompatibilityHelper": "语义化版本兼容性辅助类，提供 IsSatisfiedBy（兼容性匹配）、IsSuperSetOf（超集检测）及规格转换方法。",
    "PackageDefinitionSerializerPlugin": "PackageDef 对象的 XML 序列化/反序列化插件，将 package.xml 与 PackageDef 对象模型双向映射，同时处理命名空间设置。",
    "PackageDependencySerializerPlugin": "PackageDependency 对象的 XML 序列化/反序列化插件，负责依赖项的 XML 双向转换和版本格式兼容处理。",
    "PluginFile": "插件文件声明模型，描述 TapPackage 中包含的插件类型、名称、分组和可见性等元数据。",
    "PackageFile": "包文件声明模型，描述 TapPackage 中的物理文件条目，包含源路径、目标路径、插件引用和依赖序集信息。",
    "PackageDependency": "包依赖声明模型，包含包名称、版本约束和原始版本字符串，支持相等比较。",
    "ActionStep": "自定义操作步骤模型，定义包安装/卸载前后执行的外部程序（EXE）、参数和退出码处理规则。",
    "EulaAcceptanceDialog": "EULA 接受对话框，在安装时显示许可证文本并等待用户接受或拒绝。",
    "EULA": "最终用户许可协议数据模型，包含标识符和源文本。",
    "PackageDef": "包定义核心数据模型，是包系统中最重要的类。封装包的所有元数据：名称、版本、描述、依赖、文件列表、许可证、标签等。同时提供 XML 序列化/反序列化、哈希计算、文件系统查找等完整的包生命周期方法。",
    "Validation": "包验证规则基类，定义 IsValid 抽象方法用于自定义验证逻辑。",
    "FileExists": "文件存在性验证规则，检查指定路径的文件是否存在。",
    "NamespaceIgnorantXmlTextReader": "忽略命名空间的 XML 读取器，用于向后兼容读取旧版无命名空间的 package.xml 文件。",
    "ArchitectureHelper": "CPU 架构兼容性辅助类，检测主机架构、猜测基础架构并判断插件与主机或两个插件之间的架构兼容性。",
    "PackageFileSerializerPlugin": "PackageFile 对象的 XML 序列化/反序列化插件，处理包含插件声明的文件列表节点。",
    "PackageIconData": "包图标数据标记类，实现 ICustomPackageData 接口，用于在 package.xml 的 File 元素中嵌入图标资源。",
    "PackageIdentifier": "包四维标识符类，通过 Name、Version、Architecture、OS 四个属性唯一标识一个包实例，支持相等比较和哈希。",
    "PackageUninstallStep": "TestPlan 包卸载步骤，将包卸载操作嵌入测试计划流程。",
    "PackageInstallStep": "TestPlan 包安装步骤，将包安装操作嵌入测试计划流程，支持指定仓库和系统级安装。",
    "PackageManagerSettings": "包管理器全局设置类，管理仓库列表、本地缓存策略、不兼容包显示、更新检查和排序偏好等配置。",
    "RepositorySettingEntry": "单个仓库设置条目，封装仓库 URL、启用状态和管理器引用，支持绑定通知。",
    "IPackageDefSource": "包定义来源的标记接口。",
    "IFilePackageDefSource": "文件型包定义来源接口，标识从 .TapPackage 文件加载。",
    "FilePackageDefSource": "文件型包定义来源实现类。",
    "IRepositoryPackageDefSource": "仓库型包定义来源接口，标识从包仓库加载。",
    "HttpRepositoryPackageDefSource": "HTTP 仓库型包定义来源，包含仓库 URL 和直接下载地址。",
    "FileRepositoryPackageDefSource": "文件仓库型包定义来源，继承自 FilePackageDefSource 并实现仓库来源接口。",
    "XmlPackageDefSource": "XML 文件型包定义来源，从本地 package.xml 文件加载。",
    "InstalledPackageDefSource": "已安装包定义来源，继承自 XmlPackageDefSource，附加所属 Installation 信息。",
}

# Special function summaries for key methods
func_summaries = {
    "PackageAction.cs:ExtractRepositoryTokens": "从仓库参数列表中提取认证令牌信息并保存到 AuthenticationSettings。支持 --repository 参数中的 token=value 格式及 URL 中的用户信息。",
    "PackageAction.cs:FilterPreRelease": "按预发布标签过滤包列表，将匹配的预发布版本分组并按语义版本排序取最新。",
    "PackageActionHelpers.cs:TriviallyResolvePackage": "快速解析单个包：在仓库中查找，若无依赖则直接返回。",
    "PackageActionHelpers.cs:GatherPackagesAndDependencyDefs": "收集包及依赖定义的完整信息，处理文件路径、仓库查询和依赖递归解析，返回待下载的包列表。",
    "PackageActionHelpers.cs:DownloadPackages": "批量下载包文件到目标目录，支持进度回调和缓存跳跃。",
    "PackageActionHelpers.cs:GetQualifiedFileName": "为包生成规范文件名：{Name}.{Version}.{OS}-{Architecture}.TapPackage。",
    "LockedExecute": "在获取安装目录互斥锁或隔离进程保护后执行的实际操作逻辑，由于类继承层次中的具体动作实现。",
    "Execute": "CLI 动作入口方法，从命令行参数上下文触发执行。",
    "Create.cs:Process": "包创建的核心流程：加载 package.xml、分析依赖、收集文件、注入版本信息并生成最终的 .TapPackage 归档。",
    "Create.cs:GetRealFilePath": "根据路径、版本和扩展名生成实际输出文件路径。",
    "Create.cs:GetRealFilePathFromName": "根据包名、版本和扩展名生成实际输出文件路径。",
    "Install.cs:DoExecute": "执行完整的安装流程：解析包规范、收集依赖、下载、解压、运行安装脚本并记录安装状态。",
    "Install.cs:UninstallExisting": "在安装前卸载与待安装包冲突的已有版本。",
    "Install.cs:ReorderPackages": "根据依赖关系对包列表进行拓扑排序，确保依赖包在被依赖包之前安装。",
    "Install.cs:CheckForOverwrittenPackages": "检测安装是否会覆盖其他已安装包的文件并提示用户确认。",
    "List.cs:PrintVersionsReadable": "以 Markdown 表格格式输出包的版本列表。",
    "List.cs:PrintReadable": "以 Markdown 表格格式输出包列表，区分已安装和未安装状态。",
    "Show.cs:ParseDescription": "解析包描述中的分节格式（## Section），将其拆分为键值对。",
    "Show.cs:AddWritePair": "向输出缓存中添加键值对。",
    "Show.cs:WritePairs": "将所有缓存的键值对以对齐格式写入输出。",
    "Show.cs:GetPackageDef": "从目标安装目录中加载包的 PackageDef 信息。",
    "Show.cs:GetPackageInfo": "获取包的完整信息，包括元数据、依赖关系和包含的文件列表。",
    "Show.cs:WordWrap": "将长文本按指定宽度进行自动换行。",
    "Show.cs:DisableHttpRepositories": "临时禁用 HTTP 仓库以支持离线模式查询。",
    "Uninstall.cs:DoExecute": "执行完整的卸载流程：查找已安装包、检查依赖关系、删除文件并更新安装记录。",
    "Uninstall.cs:GetPaths": "获取指定包在安装目录下的所有文件路径列表。",
    "Uninstall.cs:CheckPackageAndDependencies": "检查待卸载包是否被其他已安装包依赖，返回受影响的包列表。",
    "IsolatedPackageAction.cs:TryFindParentInstallation": "查找包含指定目录的父级安装目录。",
    "IsolatedPackageAction.cs:GetChangeId": "获取安装目录的变更计数器。",
    "IsolatedPackageAction.cs:IncrementChangeId": "递增安装目录的变更计数器（标记安装状态变化）。",
    "IsolatedPackageAction.cs:RunIsolated": "在隔离进程中执行指定的包操作。",
    "LockingPackageAction.cs:GetLocalInstallationDir": "获取当前可执行文件所在的安装目录路径。",
    "LockingPackageAction.cs:GuessHostOS": "根据当前运行时环境猜测主机操作系统类型。",
    "LockingPackageAction.cs:GetMutex": "为指定安装目录创建或获取命名 Mutex。",
    "PackageFile.cs:PackageDef.FromXml": "从 XML 流反序列化为 PackageDef 对象。",
    "PackageFile.cs:PackageDef.SaveTo": "将单个 PackageDef 序列化为 XML 并写入流。",
    "PackageFile.cs:PackageDef.SaveManyTo": "将多个 PackageDef 对象批量序列化为 XML 流。",
    "PackageFile.cs:PackageDef.ManyFromXml": "从 XML 流批量反序列化多个 PackageDef 对象。",
    "PackageFile.cs:PackageDef.FromPackage": "从 .TapPackage 文件中加载 PackageDef。",
    "PackageFile.cs:PackageDef.FromPackages": "从多个 .TapPackage 文件中加载 PackageDef 列表。",
    "PackageFile.cs:PackageDef.ValidateXml": "根据 XSD Schema 验证 package.xml 文件的合法性。",
    "PackageFile.cs:PackageDef.GetXmlSchema": "获取嵌入的 package.xsd Schema 以进行 XML 验证。",
    "PackageFile.cs:PackageDef.FindPackageDefinitions": "扫描目录查找所有 package.xml 文件并加载。",
    "PackageFile.cs:PackageDef.GetMetadataFromPackage": "从 .TapPackage 归档中提取 package.xml 元数据文件。",
    "PackageFile.cs:PackageDef.ComputeHash": "计算包定义的 SHA256 哈希值并缓存。",
    "PackageFile.cs:ArchitectureHelper.CompatibleWith": "判断插件是否与主机 CPU 架构兼容。",
    "PackageFile.cs:ArchitectureHelper.PluginsCompatible": "判断两个插件之间的 CPU 架构是否兼容。",
    "PackageFile.cs:ArchitectureHelper.GuessBaseArchitecture": "根据主机架构猜测基础架构（如 x64 -> x86 兼容性映射）。",
    "PackageFile.cs:EulaAcceptanceDialog.OpenEula": "显示 EULA 许可证对话框并等待用户接受。",
    "PackageCompatibilityHelper.cs:IsSatisfiedBy": "检查包版本是否满足指定的版本约束条件。",
    "PackageCompatibilityHelper.cs:IsSuperSetOf": "检查一个版本约束是否为另一个的超集。",
    "PackageCompatibilityHelper.cs:AsCompatibleSpecifier": "将语义化版本转换为兼容性规格。",
    "PackageCompatibilityHelper.cs:AsExactSpecifier": "将语义化版本转换为精确匹配规格。",
    "PackageDefinitionSerializerPlugin.cs:Deserialize": "将 XML 节点反序列化为 PackageDef 对象（入口在 PackageDefinitionSerializerPlugin 类中）。",
    "PackageDefinitionSerializerPlugin.cs:Serialize": "将 PackageDef 对象序列化为 XML 节点。",
    "PackageDefinitionSerializerPlugin.cs:SetAllNamespaces": "批量设置 XML 元素及其子元素的命名空间。",
    "PackageFileSerializerPlugin.cs:Deserialize": "将 XML 节点反序列化为 PackageFile 对象。",
    "PackageFileSerializerPlugin.cs:Serialize": "将 PackageFile 对象序列化为 XML 节点。",
    "PackageIdentifier.cs:GetHashCode": "基于 Name、Version、Architecture、OS 四个属性计算哈希码以实现字典查找。",
    "PackageIdentifier.cs:Equals": "比较两个 PackageIdentifier 是否在四个维度上完全相等。",
    "PackageInstallStep.cs:Run": "执行 TestPlan 步骤中的包操作（安装或卸载）。",
    "PackageManagerSettings.cs:GetEnabledRepositories": "获取当前启用的仓库列表，可被命令行指定的仓库 URL 覆盖。",
    "PackageCacheHelper.cs:GetCacheFilePath": "获取指定包的缓存文件路径。",
    "PackageCacheHelper.cs:CachePackage": "将包文件复制到缓存目录。",
    "PackageCacheHelper.cs:ClearCache": "清空本地包缓存目录。",
}

# ---- Create all nodes and edges ----
for r in data['results']:
    path = r['path']
    cat = r['fileCategory']
    lines = r['totalLines']

    if cat == 'config':
        node_type = 'config'
        node_id = f"config:{path}"
    else:
        node_type = 'file'
        node_id = f"file:{path}"

    name = path.split('/')[-1]

    # Map summaries
    if path == "Package/PackageSchema.xsd":
        summary = "包定义 XML Schema（XSD），定义 package.xml 的合法结构和元素约束，包括 File、Dependencies、Description、EULA 等复杂类型定义。"
        tags = ["configuration", "schema-definition", "xml", "validation", "package"]
        complexity = "moderate"
    elif path == "Package/PackageCompatibilityHelper.cs":
        summary = "包版本兼容性辅助类，提供语义化版本的兼容性判断、超集检测和规格转换方法。"
        tags = ["utility", "package", "version", "compatibility", "semver"]
        complexity = "moderate"
    elif path == "Package/PackageIconData.cs":
        summary = "包图标数据标记类，实现 ICustomPackageData 接口，用于在 package.xml 的 File 节点中嵌入图标信息。"
        tags = ["data-model", "package", "icon", "marker-class"]
        complexity = "simple"
    elif path == "Package/PackageActions/CacheAction.cs":
        summary = "包缓存管理 CLI 动作，清除本地包缓存目录中的所有缓存文件。"
        tags = ["cli-action", "package", "cache", "cleanup"]
        complexity = "simple"
    elif path == "Package/PackageActions/Test.cs":
        summary = "包测试 CLI 动作，检查指定包是否存在于安装目录中并报告存在性结果。"
        tags = ["cli-action", "package", "test", "validation"]
        complexity = "simple"
    elif path == "Package/PackageActions/PackageExitCodes.cs":
        summary = "定义包 CLI 操作的退出码枚举（范围 30-59），覆盖创建失败、无效定义、依赖错误、安装/卸载错误和 EULA 未接受等场景。"
        tags = ["enum", "package", "exit-code", "error-handling"]
        complexity = "simple"
    elif path == "Package/PackageInstallHelpers/PackageInstallStep.cs":
        summary = "定义包安装和卸载的 TestPlan 步骤类，支持在测试计划流程中嵌入包管理操作。"
        tags = ["testplan-step", "package", "install", "uninstall"]
        complexity = "simple"
    elif path == "Package/PackageSource/IPackageSource.cs":
        summary = "定义包定义来源的接口层级体系：IPackageDefSource 及各实现类（文件、HTTP 仓库、文件仓库、XML、已安装），用于标识包定义的加载来源。"
        tags = ["interface", "package", "source", "repository", "abstraction"]
        complexity = "simple"
    elif path == "Package/PackageAction.cs":
        summary = "定义包操作抽象基类 PackageAction（实现 ICliAction）及静态辅助类 PackageActionHelper，提供进度更新事件、错误事件、仓库令牌提取和预发布版本过滤等公共功能。"
        tags = ["api-handler", "abstract-class", "package", "cli-action", "base-class"]
        complexity = "complex"
    elif path == "Package/PackageActionHelpers.cs":
        summary = "提供包操作的静态辅助方法：快速包解析、依赖与包定义收集、批量下载及规范文件名生成，是安装流程的核心工具类。"
        tags = ["utility", "package", "dependency-resolution", "download", "helper"]
        complexity = "complex"
    elif path == "Package/PackageActions/Create.cs":
        summary = "包创建 CLI 动作，从工程目录或 XML 描述文件生成 .TapPackage 归档，处理文件路径、版本注入和依赖分析。"
        tags = ["cli-action", "package", "create", "build"]
        complexity = "complex"
    elif path == "Package/PackageActions/Download.cs":
        summary = "包下载 CLI 动作，从仓库解析并下载包及其依赖到本地输出路径，支持版本、架构和操作系统筛选。"
        tags = ["cli-action", "package", "download", "repository"]
        complexity = "complex"
    elif path == "Package/PackageActions/ImageInstall.cs":
        summary = "镜像安装 CLI 动作，将 OpenTAP 部署镜像中的包集合并或复制到目标安装目录，支持 DryRun 预览模式。"
        tags = ["cli-action", "package", "image", "install", "merge"]
        complexity = "complex"
    elif path == "Package/PackageActions/Install.cs":
        summary = "包安装 CLI 动作，完整的安装流程包括依赖解析、下载、兼容性检查、覆盖控制、许可证验证和安装状态记录，是包管理器最核心的动作。"
        tags = ["cli-action", "package", "install", "dependency", "main-action"]
        complexity = "complex"
    elif path == "Package/PackageActions/List.cs":
        summary = "包列表 CLI 动作，查询仓库中可用或已安装的包及其版本，以 Markdown 表格格式输出，支持多种过滤条件。"
        tags = ["cli-action", "package", "list", "repository", "query"]
        complexity = "complex"
    elif path == "Package/PackageActions/Show.cs":
        summary = "包详情展示 CLI 动作，以 Markdown 格式输出包的元数据、依赖关系、文件列表和插件信息，支持离线模式。"
        tags = ["cli-action", "package", "show", "info", "markdown"]
        complexity = "complex"
    elif path == "Package/PackageActions/Uninstall.cs":
        summary = "包卸载 CLI 动作，移除已安装包及其文件，检测反向依赖关系并处理用户交互确认和强制选项。"
        tags = ["cli-action", "package", "uninstall", "cleanup", "dependency"]
        complexity = "complex"
    elif path == "Package/PackageActions/IsolatedPackageAction.cs":
        summary = "隔离包操作抽象基类，继承自 LockingPackageAction，提供变更 ID 跟踪和隔离进程执行支持，用于需要覆盖运行时 DLL 的安装/卸载操作。"
        tags = ["abstract-class", "package", "isolation", "base-class", "cli-action"]
        complexity = "moderate"
    elif path == "Package/PackageActions/LockingPackageAction.cs":
        summary = "带互斥锁的包操作抽象基类，继承自 PackageAction，通过命名 Mutex 确保同一安装目录下的包操作串行执行，防止并发冲突。"
        tags = ["abstract-class", "package", "locking", "base-class", "concurrency"]
        complexity = "moderate"
    elif path == "Package/PackageCacheHelper.cs":
        summary = "本地包缓存管理类，提供缓存目录路径解析、文件存取和清理功能，支持通过环境变量覆盖缓存位置。"
        tags = ["utility", "package", "cache", "storage"]
        complexity = "moderate"
    elif path == "Package/PackageDefinitionSerializerPlugin.cs":
        summary = "包定义 XML 序列化/反序列化插件集，将 PackageDef 和 PackageDependency 对象与 package.xml 格式双向映射，处理命名空间和版本格式兼容。"
        tags = ["serialization", "package", "xml", "plugin", "serializer"]
        complexity = "complex"
    elif path == "Package/PackageFile.cs":
        summary = "包系统的核心定义文件，包含 PackageDef（包元数据）、PackageFile（文件列表）、PluginFile（插件声明）、PackageDependency（依赖）、ActionStep（自定义步骤）和 ArchitectureHelper（架构兼容）等 11 个类，是包数据模型的中央枢纽。"
        tags = ["data-model", "package", "core", "xml", "serialization"]
        complexity = "complex"
    elif path == "Package/PackageFileSerializerPlugin.cs":
        summary = "PackageFile 对象的 XML 序列化/反序列化插件，处理包含插件声明的文件列表节点与 XML 的双向转换。"
        tags = ["serialization", "package", "xml", "plugin", "serializer"]
        complexity = "complex"
    elif path == "Package/PackageIdentifier.cs":
        summary = "包四维标识符类（Name + Version + Architecture + OS），支持多构造函数重载、相等比较和哈希计算，用于在集合中唯一标识包实例。"
        tags = ["data-model", "package", "identifier", "version"]
        complexity = "moderate"
    elif path == "Package/PackageManagerSettings.cs":
        summary = "包管理器全局设置类，管理仓库列表及其启用状态、缓存策略、不兼容包显示、更新检查和排序偏好。"
        tags = ["configuration", "package", "settings", "repository"]
        complexity = "complex"
    else:
        summary = f"C# 源代码文件，属于 OpenTAP 包管理子系统。"
        tags = ["package", "csharp"]
        if lines > 200:
            complexity = "complex"
        elif lines > 50:
            complexity = "moderate"
        else:
            complexity = "simple"

    file_node = {
        "id": node_id,
        "type": node_type,
        "name": name,
        "filePath": path,
        "summary": summary,
        "tags": tags,
        "complexity": complexity
    }
    add_node(file_node)

    # Handle code files
    if cat == 'code':
        file_exports_list = r.get('exports', [])
        classes = r.get('classes', [])
        functions = r.get('functions', [])
        export_names = {e['name'] for e in file_exports_list}

        # Collect class method names to avoid duplicating
        class_method_names = set()
        for cls in classes:
            for m in cls.get('methods', []):
                class_method_names.add(m)

        # Create class nodes
        for cls in classes:
            cls_name = cls['name']
            cls_methods = cls.get('methods', [])
            cls_props = cls.get('properties', [])
            cls_lines = cls['endLine'] - cls['startLine'] + 1

            # Significance filter: 2+ methods OR 20+ lines OR exported
            if not (len(cls_methods) >= 2 or cls_lines >= 20 or cls_name in export_names):
                continue

            cls_id = f"class:{path}:{cls_name}"
            cls_summary = class_summaries.get(cls_name, f"定义于 {name} 中，包含 {len(cls_methods)} 个方法、{len(cls_props)} 个属性。")

            cls_node = {
                "id": cls_id,
                "type": "class",
                "name": cls_name,
                "filePath": path,
                "lineRange": [cls['startLine'], cls['endLine']],
                "summary": cls_summary,
                "tags": ["class", "package"],
                "complexity": "complex" if cls_lines >= 100 else ("moderate" if cls_lines >= 40 else "simple")
            }
            add_node(cls_node)

            # contains edge
            add_edge({"source": node_id, "target": cls_id, "type": "contains", "direction": "forward", "weight": 1.0})

            # exports edge
            if cls_name in export_names:
                add_edge({"source": node_id, "target": cls_id, "type": "exports", "direction": "forward", "weight": 0.8})

        # Create function nodes (standalone, not class methods)
        for func in functions:
            name_f = func['name']
            if name_f in class_method_names:
                continue

            func_lines = func['endLine'] - func['startLine'] + 1

            # Significance: 10+ lines OR exported (but skip trivial 1-2 liners unless exported)
            if func_lines < 3 and name_f not in export_names:
                continue
            if func_lines < 10 and name_f not in export_names:
                continue

            func_id = f"function:{path}:{name_f}"
            params_str = ', '.join(func.get('params', []))

            # Look up per-function summary
            func_key = f"{path}:{name_f}"
            func_summary = func_summaries.get(func_key)
            if func_summary is None:
                func_summary = func_summaries.get(name_f)  # try name-only (for LockedExecute, Execute, etc.)
            if func_summary is None:
                func_summary = f"参数 ({params_str})，共 {func_lines} 行。"

            func_node = {
                "id": func_id,
                "type": "function",
                "name": name_f,
                "filePath": path,
                "lineRange": [func['startLine'], func['endLine']],
                "summary": func_summary,
                "tags": ["function", "package"],
                "complexity": "complex" if func_lines >= 80 else ("moderate" if func_lines >= 30 else "simple")
            }
            add_node(func_node)

            # contains edge
            add_edge({"source": node_id, "target": func_id, "type": "contains", "direction": "forward", "weight": 1.0})

            # exports edge
            if name_f in export_names:
                add_edge({"source": node_id, "target": func_id, "type": "exports", "direction": "forward", "weight": 0.8})

# ---- Stats ----
print(f"Total nodes: {len(nodes)}")
print(f"Total edges: {len(edges)}")

# ---- Partition ----
node_count = len(nodes)
edge_count = len(edges)
if node_count <= 60 and edge_count <= 120:
    parts = 1
else:
    parts = math.ceil(max(node_count / 60, edge_count / 120))

print(f"Parts needed: {parts}")

# Sort files alphabetically
files_sorted = sorted(set(n['filePath'] for n in nodes if n.get('filePath')), key=lambda x: x)

chunk_size = math.ceil(len(files_sorted) / parts)
file_to_part = {}
for i, fp in enumerate(files_sorted):
    file_to_part[fp] = (i // chunk_size) + 1

for p in range(1, parts + 1):
    fps = [fp for fp, pp in sorted(file_to_part.items(), key=lambda x: x[0]) if pp == p]
    print(f"  Part {p}: {len(fps)} files - {fps}")

# Helper: extract filePath from node id
def get_file_path(node):
    fp = node.get('filePath')
    if fp:
        return fp
    nid = node['id']
    # class:path:Name or function:path:Name
    for prefix in ['class:', 'function:']:
        if nid.startswith(prefix):
            rest = nid[len(prefix):]
            idx = rest.rfind(':')
            if idx > 0:
                return rest[:idx]
            return rest
    # file:path, config:path etc.
    for prefix in ['file:', 'config:', 'document:', 'service:', 'table:', 'endpoint:', 'pipeline:', 'schema:', 'resource:']:
        if nid.startswith(prefix):
            return nid[len(prefix):]
    return None

# Write each part
os.makedirs(".understand-anything/intermediate", exist_ok=True)

for part_idx in range(1, parts + 1):
    part_files = {fp for fp, p in file_to_part.items() if p == part_idx}

    part_nodes = []
    for node in nodes:
        fp = get_file_path(node)
        if fp and fp in part_files:
            part_nodes.append(node)

    part_node_ids = {n['id'] for n in part_nodes}

    part_edges = []
    for edge in edges:
        src_id = edge['source']
        src_fp = get_file_path({'id': src_id})
        if src_fp and src_fp in part_files:
            part_edges.append(edge)

    if parts == 1:
        fname = ".understand-anything/intermediate/batch-39.json"
    else:
        fname = f".understand-anything/intermediate/batch-39-part-{part_idx}.json"

    output = {"nodes": part_nodes, "edges": part_edges}
    with open(fname, 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Validate
    part_ids = {n['id'] for n in part_nodes}
    for edge in part_edges:
        if edge['source'] not in part_ids:
            print(f"  WARNING: edge source {edge['source']} not in part {part_idx} nodes")
        # target may be in a different part - that's OK for cross-part edges

    print(f"  Part {part_idx}: {fname} -> {len(part_nodes)} nodes, {len(part_edges)} edges")

print("Done!")
