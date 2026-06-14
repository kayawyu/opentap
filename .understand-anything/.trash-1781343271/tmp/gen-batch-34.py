import json, os

OUT_DIR = "/Users/yujiayou/CsharpProject/opentap/.understand-anything/intermediate"

# ===== PART 1: Files 1-13 =====

nodes_p1 = []
edges_p1 = []

# 1. Engine/UnparameterizableAttribute.cs
nodes_p1.append({
    "id": "file:Engine/UnparameterizableAttribute.cs",
    "type": "file", "name": "UnparameterizableAttribute.cs",
    "filePath": "Engine/UnparameterizableAttribute.cs",
    "summary": "定义一个属性，标记某个TestStep参数不可通过命令行被参数化（不可作为外部输入参数）。",
    "tags": ["attribute", "test-step", "metadata", "parameter"],
    "complexity": "simple"
})
nodes_p1.append({
    "id": "class:Engine/UnparameterizableAttribute.cs:UnparameterizableAttribute",
    "type": "class", "name": "UnparameterizableAttribute",
    "filePath": "Engine/UnparameterizableAttribute.cs", "lineRange": [6, 7],
    "summary": "标记属性：应用于TestStep参数，阻止其被命令行或其他外部输入方式参数化。",
    "tags": ["attribute", "test-step", "parameter", "metadata"],
    "complexity": "simple"
})
edges_p1.append({"source": "file:Engine/UnparameterizableAttribute.cs", "target": "class:Engine/UnparameterizableAttribute.cs:UnparameterizableAttribute", "type": "contains", "direction": "forward", "weight": 1.0})
edges_p1.append({"source": "file:Engine/UnparameterizableAttribute.cs", "target": "class:Engine/UnparameterizableAttribute.cs:UnparameterizableAttribute", "type": "exports", "direction": "forward", "weight": 0.8})

# 2. Engine/UnsweepableAttribute.cs
nodes_p1.append({
    "id": "file:Engine/UnsweepableAttribute.cs",
    "type": "file", "name": "UnsweepableAttribute.cs",
    "filePath": "Engine/UnsweepableAttribute.cs",
    "summary": "定义一个属性，标记某个对象在垃圾回收（sweep）过程中不可被清除，确保其生命周期持续。",
    "tags": ["attribute", "memory-management", "lifecycle", "metadata"],
    "complexity": "simple"
})
nodes_p1.append({
    "id": "class:Engine/UnsweepableAttribute.cs:UnsweepableAttribute",
    "type": "class", "name": "UnsweepableAttribute",
    "filePath": "Engine/UnsweepableAttribute.cs", "lineRange": [10, 11],
    "summary": "标记属性：阻止被标记的对象在OpenTAP的sweep垃圾回收机制中被清除。",
    "tags": ["attribute", "memory-management", "lifecycle", "metadata"],
    "complexity": "simple"
})
edges_p1.append({"source": "file:Engine/UnsweepableAttribute.cs", "target": "class:Engine/UnsweepableAttribute.cs:UnsweepableAttribute", "type": "contains", "direction": "forward", "weight": 1.0})
edges_p1.append({"source": "file:Engine/UnsweepableAttribute.cs", "target": "class:Engine/UnsweepableAttribute.cs:UnsweepableAttribute", "type": "exports", "direction": "forward", "weight": 0.8})

# 3. Engine/UserInput.cs
nodes_p1.append({
    "id": "file:Engine/UserInput.cs",
    "type": "file", "name": "UserInput.cs",
    "filePath": "Engine/UserInput.cs",
    "summary": "OpenTAP用户输入子系统，提供CLI交互式用户输入接口，支持管道输入、键盘读取、布局控制和输入验证。包含UserInput静态类、IUserInterface接口和CliUserInputInterface实现。",
    "tags": ["user-input", "cli", "interactive", "interface", "engine"],
    "complexity": "complex",
    "languageNotes": "使用BlockingCollection实现多线程安全输入队列，支持stdin管道读取与Console.ReadKey键盘读取两种模式。"
})
nodes_p1.append({
    "id": "class:Engine/UserInput.cs:UserInput",
    "type": "class", "name": "UserInput",
    "filePath": "Engine/UserInput.cs", "lineRange": [19, 62],
    "summary": "静态用户输入门面类，提供Request方法向用户请求输入数据，管理IUserInputInterface实现。",
    "tags": ["user-input", "static-class", "facade", "cli"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "class:Engine/UserInput.cs:IUserInterface",
    "type": "class", "name": "IUserInterface",
    "filePath": "Engine/UserInput.cs", "lineRange": [65, 73],
    "summary": "接口，定义对象属性变化时通知用户界面的回调方法。",
    "tags": ["interface", "user-input", "observer"],
    "complexity": "simple"
})
nodes_p1.append({
    "id": "class:Engine/UserInput.cs:IUserInputInterface",
    "type": "class", "name": "IUserInputInterface",
    "filePath": "Engine/UserInput.cs", "lineRange": [76, 83],
    "summary": "接口，定义请求用户输入数据的核心方法RequestUserInput，由具体UI实现。",
    "tags": ["interface", "user-input", "cli"],
    "complexity": "simple"
})
nodes_p1.append({
    "id": "class:Engine/UserInput.cs:LayoutAttribute",
    "type": "class", "name": "LayoutAttribute",
    "filePath": "Engine/UserInput.cs", "lineRange": [100, 128],
    "summary": "布局属性，控制用户输入界面中每个属性的显示模式（如普通行、多行文本）、行高和最小宽度。",
    "tags": ["attribute", "layout", "user-input", "ui"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "class:Engine/UserInput.cs:CliUserInputInterface",
    "type": "class", "name": "CliUserInputInterface",
    "filePath": "Engine/UserInput.cs", "lineRange": [134, 569],
    "summary": "命令行用户输入接口实现，提供基于Console的交互式参数输入，支持管道输入、超时控制、安全密码输入和多选菜单。",
    "tags": ["cli", "user-input", "interactive", "implementation"],
    "complexity": "complex",
    "languageNotes": "使用BlockingCollection<string>管理多线程输入行队列，通过Mutex保证输入请求的线程安全。"
})
nodes_p1.append({
    "id": "function:Engine/UserInput.cs:RequestUserInput",
    "type": "function", "name": "RequestUserInput",
    "filePath": "Engine/UserInput.cs", "lineRange": [257, 488],
    "summary": "核心方法：根据dataObject的注解和成员信息，逐字段向用户展示并请求CLI输入，支持布局、可用值列表、默认值和安全密码输入的复杂逻辑。",
    "tags": ["user-input", "cli", "interactive", "annotation-driven"],
    "complexity": "complex"
})
nodes_p1.append({
    "id": "function:Engine/UserInput.cs:StartKeyboardReader",
    "type": "function", "name": "StartKeyboardReader",
    "filePath": "Engine/UserInput.cs", "lineRange": [171, 214],
    "summary": "启动后台线程读取键盘输入（Console.ReadKey），将每行字符存入lines队列，支持退格编辑和Ctrl+C中断。",
    "tags": ["keyboard-input", "thread", "console", "input-queue"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/UserInput.cs:StartPipeReader",
    "type": "function", "name": "StartPipeReader",
    "filePath": "Engine/UserInput.cs", "lineRange": [218, 245],
    "summary": "启动后台线程从stdin管道读取字节流，按换行符分割后存入lines队列，支持从管道或重定向输入。",
    "tags": ["pipe-input", "stdin", "thread", "input-queue"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/UserInput.cs:awaitReadLine",
    "type": "function", "name": "awaitReadLine",
    "filePath": "Engine/UserInput.cs", "lineRange": [498, 532],
    "summary": "从输入队列中等待并取出一行文本，支持超时、安全模式（不显示回显）和EOF异常处理。",
    "tags": ["user-input", "async", "timeout", "secure-input"],
    "complexity": "moderate"
})

for cls_name in ["UserInput", "IUserInterface", "IUserInputInterface", "LayoutAttribute", "CliUserInputInterface"]:
    edges_p1.append({"source": "file:Engine/UserInput.cs", "target": f"class:Engine/UserInput.cs:{cls_name}", "type": "contains", "direction": "forward", "weight": 1.0})
    edges_p1.append({"source": "file:Engine/UserInput.cs", "target": f"class:Engine/UserInput.cs:{cls_name}", "type": "exports", "direction": "forward", "weight": 0.8})
for fn_name in ["RequestUserInput", "StartKeyboardReader", "StartPipeReader", "awaitReadLine"]:
    edges_p1.append({"source": "file:Engine/UserInput.cs", "target": f"function:Engine/UserInput.cs:{fn_name}", "type": "contains", "direction": "forward", "weight": 1.0})
    edges_p1.append({"source": "file:Engine/UserInput.cs", "target": f"function:Engine/UserInput.cs:{fn_name}", "type": "exports", "direction": "forward", "weight": 0.8})

# class containment within UserInput.cs
# CliUserInputInterface contains the functions
for fn in ["StartKeyboardReader", "StartPipeReader", "RequestUserInput", "awaitReadLine"]:
    edges_p1.append({"source": "class:Engine/UserInput.cs:CliUserInputInterface", "target": f"function:Engine/UserInput.cs:{fn}", "type": "contains", "direction": "forward", "weight": 1.0})

# 4. Engine/Utils/ExecutableFormatDetector.cs
nodes_p1.append({
    "id": "file:Engine/Utils/ExecutableFormatDetector.cs",
    "type": "file", "name": "ExecutableFormatDetector.cs",
    "filePath": "Engine/Utils/ExecutableFormatDetector.cs",
    "summary": "可执行文件格式检测器，通过读取PE/ELF/Mach-O文件头魔数来识别可执行文件的平台和格式。",
    "tags": ["executable-detection", "binary-analysis", "pe-format", "utility"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "class:Engine/Utils/ExecutableFormatDetector.cs:ExecutableFormatDetector",
    "type": "class", "name": "ExecutableFormatDetector",
    "filePath": "Engine/Utils/ExecutableFormatDetector.cs", "lineRange": [20, 135],
    "summary": "静态工具类，通过文件头魔数检测二进制可执行文件的格式（PE/ELF/Mach-O）和CPU架构。",
    "tags": ["executable-detection", "binary-analysis", "static-class", "utility"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/Utils/ExecutableFormatDetector.cs:Detect",
    "type": "function", "name": "Detect",
    "filePath": "Engine/Utils/ExecutableFormatDetector.cs", "lineRange": [22, 91],
    "summary": "检测给定文件流的可执行格式，通过读取首个字节判断是否为ELF/Mach-O/PE格式，并解析CPU架构。",
    "tags": ["executable-detection", "file-header", "magic-number", "cpu-arch"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/Utils/ExecutableFormatDetector.cs:IsDotNet",
    "type": "function", "name": "IsDotNet",
    "filePath": "Engine/Utils/ExecutableFormatDetector.cs", "lineRange": [93, 125],
    "summary": "检查PE文件是否包含.NET CLI头，从而判断是否为.NET托管可执行文件。",
    "tags": ["dotnet", "pe-header", "cli-header", "executable-detection"],
    "complexity": "moderate"
})
edges_p1.append({"source": "file:Engine/Utils/ExecutableFormatDetector.cs", "target": "class:Engine/Utils/ExecutableFormatDetector.cs:ExecutableFormatDetector", "type": "contains", "direction": "forward", "weight": 1.0})
edges_p1.append({"source": "file:Engine/Utils/ExecutableFormatDetector.cs", "target": "class:Engine/Utils/ExecutableFormatDetector.cs:ExecutableFormatDetector", "type": "exports", "direction": "forward", "weight": 0.8})
for fn in ["Detect", "IsDotNet"]:
    edges_p1.append({"source": "file:Engine/Utils/ExecutableFormatDetector.cs", "target": f"function:Engine/Utils/ExecutableFormatDetector.cs:{fn}", "type": "contains", "direction": "forward", "weight": 1.0})
    edges_p1.append({"source": "file:Engine/Utils/ExecutableFormatDetector.cs", "target": f"function:Engine/Utils/ExecutableFormatDetector.cs:{fn}", "type": "exports", "direction": "forward", "weight": 0.8})
for fn in ["Detect", "IsDotNet"]:
    edges_p1.append({"source": "class:Engine/Utils/ExecutableFormatDetector.cs:ExecutableFormatDetector", "target": f"function:Engine/Utils/ExecutableFormatDetector.cs:{fn}", "type": "contains", "direction": "forward", "weight": 1.0})

# 5. Engine/Utils/Utils2.cs
nodes_p1.append({
    "id": "file:Engine/Utils/Utils2.cs",
    "type": "file", "name": "Utils2.cs",
    "filePath": "Engine/Utils/Utils2.cs",
    "summary": "通用工具方法集合，提供循环依赖检测、函数绑定、排序检查和列表随机打乱等辅助功能。",
    "tags": ["utility", "helper", "algorithm", "dependency-check"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "class:Engine/Utils/Utils2.cs:Utils2",
    "type": "class", "name": "Utils2",
    "filePath": "Engine/Utils/Utils2.cs", "lineRange": [8, 76],
    "summary": "静态工具类，包含IsLooped（循环依赖检测）、Bind（偏函数绑定）、IsSortedBy（排序验证）和Shuffle（随机打乱）方法。",
    "tags": ["utility", "static-class", "helper", "algorithm"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/Utils/Utils2.cs:IsLooped",
    "type": "function", "name": "IsLooped",
    "filePath": "Engine/Utils/Utils2.cs", "lineRange": [10, 35],
    "summary": "使用栈遍历检测对象图中是否存在循环引用，通过HashSet跟踪已访问节点来判定环路。",
    "tags": ["cycle-detection", "graph", "dfs", "dependency-check"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/Utils/Utils2.cs:Shuffle",
    "type": "function", "name": "Shuffle",
    "filePath": "Engine/Utils/Utils2.cs", "lineRange": [64, 75],
    "summary": "使用Fisher-Yates洗牌算法对IList进行原地随机打乱。",
    "tags": ["shuffle", "random", "algorithm", "utility"],
    "complexity": "simple"
})
edges_p1.append({"source": "file:Engine/Utils/Utils2.cs", "target": "class:Engine/Utils/Utils2.cs:Utils2", "type": "contains", "direction": "forward", "weight": 1.0})
edges_p1.append({"source": "file:Engine/Utils/Utils2.cs", "target": "class:Engine/Utils/Utils2.cs:Utils2", "type": "exports", "direction": "forward", "weight": 0.8})
for fn in ["IsLooped", "Shuffle"]:
    edges_p1.append({"source": "file:Engine/Utils/Utils2.cs", "target": f"function:Engine/Utils/Utils2.cs:{fn}", "type": "contains", "direction": "forward", "weight": 1.0})
    edges_p1.append({"source": "file:Engine/Utils/Utils2.cs", "target": f"function:Engine/Utils/Utils2.cs:{fn}", "type": "exports", "direction": "forward", "weight": 0.8})
    edges_p1.append({"source": "class:Engine/Utils/Utils2.cs:Utils2", "target": f"function:Engine/Utils/Utils2.cs:{fn}", "type": "contains", "direction": "forward", "weight": 1.0})

# 6. Engine/ValidatingObject.cs
nodes_p1.append({
    "id": "file:Engine/ValidatingObject.cs",
    "type": "file", "name": "ValidatingObject.cs",
    "filePath": "Engine/ValidatingObject.cs",
    "summary": "OpenTAP验证框架，提供基类ValidatingObject支持属性和嵌入式对象的规则验证，以及ValidationRule、DelegateValidationRule和ValidationRuleCollection等验证规则体系。",
    "tags": ["validation", "rules-engine", "data-annotation", "engine"],
    "complexity": "complex",
    "languageNotes": "支持动态规则注入（DynamicRule），通过TypeData反射在运行时从嵌入式成员中收集验证规则并支持规则转发。"
})
nodes_p1.append({
    "id": "class:Engine/ValidatingObject.cs:ValidatingObject",
    "type": "class", "name": "ValidatingObject",
    "filePath": "Engine/ValidatingObject.cs", "lineRange": [20, 220],
    "summary": "可验证对象基类，管理ValidationRuleCollection，支持运行时从嵌入式成员和动态规则中更新验证规则，提供GetError获取聚合错误信息。",
    "tags": ["validation", "base-class", "rules-engine", "data-binding"],
    "complexity": "complex"
})
nodes_p1.append({
    "id": "class:Engine/ValidatingObject.cs:ValidationRule",
    "type": "class", "name": "ValidationRule",
    "filePath": "Engine/ValidatingObject.cs", "lineRange": [236, 263],
    "summary": "简单验证规则，包含IsValid判断条件、ErrorMessage错误消息和PropertyName属性名。",
    "tags": ["validation-rule", "data-annotation", "error-message"],
    "complexity": "simple"
})
nodes_p1.append({
    "id": "class:Engine/ValidatingObject.cs:DelegateValidationRule",
    "type": "class", "name": "DelegateValidationRule",
    "filePath": "Engine/ValidatingObject.cs", "lineRange": [268, 311],
    "summary": "委托式验证规则，ErrorMessage通过ErrorDelegate委托动态生成，支持运行时本地化错误消息。",
    "tags": ["validation-rule", "delegate", "dynamic-error", "localization"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "class:Engine/ValidatingObject.cs:ValidationRuleCollection",
    "type": "class", "name": "ValidationRuleCollection",
    "filePath": "Engine/ValidatingObject.cs", "lineRange": [316, 393],
    "summary": "验证规则集合，支持Add多种重载、Forward规则转发（将规则代理到子对象的成员），提供线程安全的规则更新键。",
    "tags": ["validation-rule-collection", "forwarding", "rule-management"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/ValidatingObject.cs:UpdateEmbeddedAndDynamicRules",
    "type": "function", "name": "UpdateEmbeddedAndDynamicRules",
    "filePath": "Engine/ValidatingObject.cs", "lineRange": [49, 110],
    "summary": "通过TypeData反射扫描嵌入式成员和DynamicMember，自动发现并注册验证规则到Rules集合中。",
    "tags": ["reflection", "dynamic-rules", "embedded-members", "validation"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/ValidatingObject.cs:GetError",
    "type": "function", "name": "GetError",
    "filePath": "Engine/ValidatingObject.cs", "lineRange": [115, 169],
    "summary": "聚合所有验证规则的错误信息，遍历规则列表并收集错误消息（包括转发规则的子对象错误），返回合并后的错误字符串。",
    "tags": ["validation", "error-aggregation", "rule-evaluation"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/ValidatingObject.cs:ThrowOnValidationError",
    "type": "function", "name": "ThrowOnValidationError",
    "filePath": "Engine/ValidatingObject.cs", "lineRange": [188, 200],
    "summary": "检查所有验证规则，如果任何规则未通过则抛出异常，支持忽略已禁用的属性。",
    "tags": ["validation", "exception", "error-checking"],
    "complexity": "moderate"
})

for cls_name in ["ValidatingObject", "ValidationRule", "DelegateValidationRule", "ValidationRuleCollection"]:
    edges_p1.append({"source": "file:Engine/ValidatingObject.cs", "target": f"class:Engine/ValidatingObject.cs:{cls_name}", "type": "contains", "direction": "forward", "weight": 1.0})
    edges_p1.append({"source": "file:Engine/ValidatingObject.cs", "target": f"class:Engine/ValidatingObject.cs:{cls_name}", "type": "exports", "direction": "forward", "weight": 0.8})
for fn_name in ["UpdateEmbeddedAndDynamicRules", "GetError", "ThrowOnValidationError"]:
    edges_p1.append({"source": "file:Engine/ValidatingObject.cs", "target": f"function:Engine/ValidatingObject.cs:{fn_name}", "type": "contains", "direction": "forward", "weight": 1.0})
    edges_p1.append({"source": "file:Engine/ValidatingObject.cs", "target": f"function:Engine/ValidatingObject.cs:{fn_name}", "type": "exports", "direction": "forward", "weight": 0.8})
for fn in ["UpdateEmbeddedAndDynamicRules", "GetError", "ThrowOnValidationError"]:
    edges_p1.append({"source": "class:Engine/ValidatingObject.cs:ValidatingObject", "target": f"function:Engine/ValidatingObject.cs:{fn}", "type": "contains", "direction": "forward", "weight": 1.0})

# 7. Engine/Verdict.cs
nodes_p1.append({
    "id": "file:Engine/Verdict.cs",
    "type": "file", "name": "Verdict.cs",
    "filePath": "Engine/Verdict.cs",
    "summary": "定义测试判决枚举Verdict，包含NotSet、Pass、Inconclusive、Fail、Aborted、Error六种测试结果状态。",
    "tags": ["enum", "verdict", "test-result", "test-execution"],
    "complexity": "simple"
})

# 8. Engine/Visa.cs
nodes_p1.append({
    "id": "file:Engine/Visa.cs",
    "type": "file", "name": "Visa.cs",
    "filePath": "Engine/Visa.cs",
    "summary": "VISA（Virtual Instrument Software Architecture）常量定义文件，包含完整的VISA属性常量、错误码、事件类型、接口类型、触发类型和协议常量，以及P/Invoke声明。",
    "tags": ["visa", "constants", "pinvoke", "instrumentation", "gpib"],
    "complexity": "complex",
    "languageNotes": "通过条件编译区分32位和64位平台，使用UnmanagedFunctionPointer委托声明VISA函数签名，包含数百个VI_ATTR_*和VI_ERROR_*常量。"
})
nodes_p1.append({
    "id": "class:Engine/Visa.cs:Visa",
    "type": "class", "name": "Visa",
    "filePath": "Engine/Visa.cs", "lineRange": [12, 786],
    "summary": "VISA静态类，定义所有VISA标准常量（属性ID、错误码、事件类型、接口/协议标识符），并在静态构造函数中通过VisaLibraryLoader加载原生VISA库函数。",
    "tags": ["visa", "constants", "static-class", "instrumentation"],
    "complexity": "complex",
    "languageNotes": "包含25+个VISA P/Invoke方法声明（viOpenDefaultRM、viFindRsrc、viRead、viWrite等），200+个属性常量，70+个错误码常量。"
})
edges_p1.append({"source": "file:Engine/Visa.cs", "target": "class:Engine/Visa.cs:Visa", "type": "contains", "direction": "forward", "weight": 1.0})
edges_p1.append({"source": "file:Engine/Visa.cs", "target": "class:Engine/Visa.cs:Visa", "type": "exports", "direction": "forward", "weight": 0.8})

# 9. Engine/VisaDeviceDiscovery.cs
nodes_p1.append({
    "id": "file:Engine/VisaDeviceDiscovery.cs",
    "type": "file", "name": "VisaDeviceDiscovery.cs",
    "filePath": "Engine/VisaDeviceDiscovery.cs",
    "summary": "VISA设备发现实现，通过VISA协议扫描和发现测试测量仪器（GPIB、TCP/IP、USB、PXI等接口），提供设备地址检测和别名解析。",
    "tags": ["visa", "device-discovery", "instrumentation", "gpib", "tcpip"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "class:Engine/VisaDeviceDiscovery.cs:VisaDeviceDiscovery",
    "type": "class", "name": "VisaDeviceDiscovery",
    "filePath": "Engine/VisaDeviceDiscovery.cs", "lineRange": [15, 178],
    "summary": "VISA设备发现类，通过VISA资源管理器扫描连接的各种仪器并获取设备地址列表，支持别名解析和异步检测队列。",
    "tags": ["visa", "device-discovery", "instrumentation"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/VisaDeviceDiscovery.cs:DetectDeviceAddresses",
    "type": "function", "name": "DetectDeviceAddresses",
    "filePath": "Engine/VisaDeviceDiscovery.cs", "lineRange": [120, 141],
    "summary": "异步检测指定类型的设备地址，将检测任务入队并等待完成，返回发现的设备地址数组。",
    "tags": ["device-detection", "async", "visa", "address-scanning"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/VisaDeviceDiscovery.cs:GetResourceManager",
    "type": "function", "name": "GetResourceManager",
    "filePath": "Engine/VisaDeviceDiscovery.cs", "lineRange": [158, 171],
    "summary": "获取VISA资源管理器会话，调用viOpenDefaultRM初始化VISA系统。",
    "tags": ["visa", "resource-manager", "session-management"],
    "complexity": "simple"
})
nodes_p1.append({
    "id": "function:Engine/VisaDeviceDiscovery.cs:updateDeviceAddresses",
    "type": "function", "name": "updateDeviceAddresses",
    "filePath": "Engine/VisaDeviceDiscovery.cs", "lineRange": [97, 118],
    "summary": "更新设备地址列表，通过viFindRsrc扫描资源，并为每个地址解析别名。",
    "tags": ["visa", "device-discovery", "address-update", "alias-resolution"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/VisaDeviceDiscovery.cs:getAliases",
    "type": "function", "name": "getAliases",
    "filePath": "Engine/VisaDeviceDiscovery.cs", "lineRange": [62, 92],
    "summary": "通过viParseRsrcEx解析给定地址的VISA别名，使用Semaphore实现超时保护。",
    "tags": ["visa", "alias-resolution", "timeout", "semaphore"],
    "complexity": "moderate"
})
edges_p1.append({"source": "file:Engine/VisaDeviceDiscovery.cs", "target": "class:Engine/VisaDeviceDiscovery.cs:VisaDeviceDiscovery", "type": "contains", "direction": "forward", "weight": 1.0})
edges_p1.append({"source": "file:Engine/VisaDeviceDiscovery.cs", "target": "class:Engine/VisaDeviceDiscovery.cs:VisaDeviceDiscovery", "type": "exports", "direction": "forward", "weight": 0.8})
for fn_name in ["DetectDeviceAddresses", "GetResourceManager", "updateDeviceAddresses", "getAliases"]:
    edges_p1.append({"source": "file:Engine/VisaDeviceDiscovery.cs", "target": f"function:Engine/VisaDeviceDiscovery.cs:{fn_name}", "type": "contains", "direction": "forward", "weight": 1.0})
    edges_p1.append({"source": "file:Engine/VisaDeviceDiscovery.cs", "target": f"function:Engine/VisaDeviceDiscovery.cs:{fn_name}", "type": "exports", "direction": "forward", "weight": 0.8})
    edges_p1.append({"source": "class:Engine/VisaDeviceDiscovery.cs:VisaDeviceDiscovery", "target": f"function:Engine/VisaDeviceDiscovery.cs:{fn_name}", "type": "contains", "direction": "forward", "weight": 1.0})

# 10. Engine/VisaFunctions.cs
nodes_p1.append({
    "id": "file:Engine/VisaFunctions.cs",
    "type": "file", "name": "VisaFunctions.cs",
    "filePath": "Engine/VisaFunctions.cs",
    "summary": "VISA函数委托结构体，定义所有VISA API的函数签名委托类型和对应的引用字段，供VisaLibraryLoader动态加载原生库函数指针。",
    "tags": ["visa", "delegate", "struct", "pinvoke", "instrumentation"],
    "complexity": "moderate",
    "languageNotes": "使用struct而非class定义VisaFunctions，包含25个delegate类型声明（ViOpenDefaultRmDelegate到ViUnlockDelegate）及其对应的函数指针字段。"
})
nodes_p1.append({
    "id": "class:Engine/VisaFunctions.cs:VisaFunctions",
    "type": "class", "name": "VisaFunctions",
    "filePath": "Engine/VisaFunctions.cs", "lineRange": [9, 344],
    "summary": "结构体，定义VISA标准API的所有函数委托签名（viOpenDefaultRM、viFindRsrc、viRead、viWrite等）及其对应的可赋值字段引用。",
    "tags": ["visa", "struct", "delegate", "function-pointer"],
    "complexity": "moderate"
})
edges_p1.append({"source": "file:Engine/VisaFunctions.cs", "target": "class:Engine/VisaFunctions.cs:VisaFunctions", "type": "contains", "direction": "forward", "weight": 1.0})
edges_p1.append({"source": "file:Engine/VisaFunctions.cs", "target": "class:Engine/VisaFunctions.cs:VisaFunctions", "type": "exports", "direction": "forward", "weight": 0.8})

# 11. Engine/VisaLibraryLoader.cs
nodes_p1.append({
    "id": "file:Engine/VisaLibraryLoader.cs",
    "type": "file", "name": "VisaLibraryLoader.cs",
    "filePath": "Engine/VisaLibraryLoader.cs",
    "summary": "VISA原生库加载器，在Windows/Linux/macOS上定位并加载VISA共享库（如visa32.dll、libvisa.so），通过LoadLibrary/GetProcAddress绑定所有VISA函数。",
    "tags": ["visa", "native-interop", "library-loader", "dlopen"],
    "complexity": "moderate",
    "languageNotes": "支持Windows的LoadLibrary/GetProcAddress和Linux/macOS的libdl，通过VisaFunctions结构体将所有函数指针统一封装。"
})
nodes_p1.append({
    "id": "class:Engine/VisaLibraryLoader.cs:VisaLibraryLoader",
    "type": "class", "name": "VisaLibraryLoader",
    "filePath": "Engine/VisaLibraryLoader.cs", "lineRange": [15, 141],
    "summary": "VISA库加载器类，根据操作系统平台搜索并加载VISA原生库，将函数指针绑定到VisaFunctions结构体的各个字段。",
    "tags": ["visa", "native-interop", "library-loader", "cross-platform"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/VisaLibraryLoader.cs:Load",
    "type": "function", "name": "Load",
    "filePath": "Engine/VisaLibraryLoader.cs", "lineRange": [66, 140],
    "summary": "加载VISA原生库：在Windows上通过win32 API加载，在Linux/macOS上搜索标准路径并通过libdl加载，然后将所有函数指针写入VisaFunctions。",
    "tags": ["visa", "native-loading", "cross-platform", "dlopen", "getprocaddress"],
    "complexity": "complex"
})
nodes_p1.append({
    "id": "function:Engine/VisaLibraryLoader.cs:viRead",
    "type": "function", "name": "viRead",
    "filePath": "Engine/VisaLibraryLoader.cs", "lineRange": [39, 48],
    "summary": "VISA读取包装方法，调用已加载的原生viRead函数从仪器读取数据到缓冲区。",
    "tags": ["visa", "read", "instrument-communication"],
    "complexity": "simple"
})
nodes_p1.append({
    "id": "function:Engine/VisaLibraryLoader.cs:viWrite",
    "type": "function", "name": "viWrite",
    "filePath": "Engine/VisaLibraryLoader.cs", "lineRange": [49, 58],
    "summary": "VISA写入包装方法，调用已加载的原生viWrite函数向仪器发送数据。",
    "tags": ["visa", "write", "instrument-communication"],
    "complexity": "simple"
})
edges_p1.append({"source": "file:Engine/VisaLibraryLoader.cs", "target": "class:Engine/VisaLibraryLoader.cs:VisaLibraryLoader", "type": "contains", "direction": "forward", "weight": 1.0})
edges_p1.append({"source": "file:Engine/VisaLibraryLoader.cs", "target": "class:Engine/VisaLibraryLoader.cs:VisaLibraryLoader", "type": "exports", "direction": "forward", "weight": 0.8})
for fn_name in ["Load", "viRead", "viWrite"]:
    edges_p1.append({"source": "file:Engine/VisaLibraryLoader.cs", "target": f"function:Engine/VisaLibraryLoader.cs:{fn_name}", "type": "contains", "direction": "forward", "weight": 1.0})
    edges_p1.append({"source": "file:Engine/VisaLibraryLoader.cs", "target": f"function:Engine/VisaLibraryLoader.cs:{fn_name}", "type": "exports", "direction": "forward", "weight": 0.8})
    edges_p1.append({"source": "class:Engine/VisaLibraryLoader.cs:VisaLibraryLoader", "target": f"function:Engine/VisaLibraryLoader.cs:{fn_name}", "type": "contains", "direction": "forward", "weight": 1.0})

# 12. Engine/WeakHashSet.cs
nodes_p1.append({
    "id": "file:Engine/WeakHashSet.cs",
    "type": "file", "name": "WeakHashSet.cs",
    "filePath": "Engine/WeakHashSet.cs",
    "summary": "基于弱引用的HashSet实现，使用WeakReference存储元素，允许GC自动回收不再使用的元素，防止内存泄漏。",
    "tags": ["weak-reference", "hashset", "memory-management", "collection"],
    "complexity": "simple"
})
nodes_p1.append({
    "id": "class:Engine/WeakHashSet.cs:WeakHashSet",
    "type": "class", "name": "WeakHashSet",
    "filePath": "Engine/WeakHashSet.cs", "lineRange": [6, 35],
    "summary": "弱引用HashSet泛型集合类，使用ConditionalWeakTable和List<WeakReference<T>>实现，Add方法自动复用已回收的槽位。",
    "tags": ["weak-reference", "hashset", "generic", "collection"],
    "complexity": "simple",
    "languageNotes": "利用ConditionalWeakTable控制键的生命周期，结合WeakReference实现自动GC清理。"
})
nodes_p1.append({
    "id": "function:Engine/WeakHashSet.cs:Add",
    "type": "function", "name": "Add",
    "filePath": "Engine/WeakHashSet.cs", "lineRange": [14, 25],
    "summary": "向WeakHashSet中添加元素，先查找可复用的空槽位（已被GC回收的引用），否则追加新的WeakReference。",
    "tags": ["weak-reference", "add", "slot-reuse", "gc-aware"],
    "complexity": "simple"
})
edges_p1.append({"source": "file:Engine/WeakHashSet.cs", "target": "class:Engine/WeakHashSet.cs:WeakHashSet", "type": "contains", "direction": "forward", "weight": 1.0})
edges_p1.append({"source": "file:Engine/WeakHashSet.cs", "target": "class:Engine/WeakHashSet.cs:WeakHashSet", "type": "exports", "direction": "forward", "weight": 0.8})
edges_p1.append({"source": "file:Engine/WeakHashSet.cs", "target": "function:Engine/WeakHashSet.cs:Add", "type": "contains", "direction": "forward", "weight": 1.0})
edges_p1.append({"source": "file:Engine/WeakHashSet.cs", "target": "function:Engine/WeakHashSet.cs:Add", "type": "exports", "direction": "forward", "weight": 0.8})
edges_p1.append({"source": "class:Engine/WeakHashSet.cs:WeakHashSet", "target": "function:Engine/WeakHashSet.cs:Add", "type": "contains", "direction": "forward", "weight": 1.0})

# 13. Engine/WorkQueue.cs
nodes_p1.append({
    "id": "file:Engine/WorkQueue.cs",
    "type": "file", "name": "WorkQueue.cs",
    "filePath": "Engine/WorkQueue.cs",
    "summary": "多线程工作队列，支持异步任务调度、并发控制、超时机制和性能监控，是OpenTAP内部任务执行的基础设施。",
    "tags": ["work-queue", "threading", "async", "concurrency", "engine"],
    "complexity": "complex",
    "languageNotes": "使用SemaphoreSlim控制并发度，通过CancellationTokenSource支持取消，利用Interlocked进行无锁计数。"
})
nodes_p1.append({
    "id": "class:Engine/WorkQueue.cs:WorkQueue",
    "type": "class", "name": "WorkQueue",
    "filePath": "Engine/WorkQueue.cs", "lineRange": [16, 282],
    "summary": "工作队列类，管理线程池和任务调度，支持EnqueueWork入队、Dequeue出队、Wait等待完成和Dispose释放资源。",
    "tags": ["work-queue", "threading", "task-scheduling", "concurrency"],
    "complexity": "complex"
})
nodes_p1.append({
    "id": "function:Engine/WorkQueue.cs:WorkerFunction",
    "type": "function", "name": "WorkerFunction",
    "filePath": "Engine/WorkQueue.cs", "lineRange": [110, 168],
    "summary": "工作线程主循环，等待信号量、出队任务并执行，跟踪执行耗时并更新平均时间统计。",
    "tags": ["worker-thread", "task-execution", "performance-tracking"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/WorkQueue.cs:EnqueueWork",
    "type": "function", "name": "EnqueueWork",
    "filePath": "Engine/WorkQueue.cs", "lineRange": [171, 196],
    "summary": "将工作项入队，增加并发计数器并在需要时启动新的工作线程，超过并发上限时阻塞等待。",
    "tags": ["enqueue", "thread-management", "backpressure"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/WorkQueue.cs:Dequeue",
    "type": "function", "name": "Dequeue",
    "filePath": "Engine/WorkQueue.cs", "lineRange": [220, 247],
    "summary": "从队列中取出工作项，等待信号量可用后从ConcurrentQueue中TryDequeue，减少并发计数。",
    "tags": ["dequeue", "concurrent", "semaphore"],
    "complexity": "moderate"
})
nodes_p1.append({
    "id": "function:Engine/WorkQueue.cs:Dispose",
    "type": "function", "name": "Dispose",
    "filePath": "Engine/WorkQueue.cs", "lineRange": [201, 208],
    "summary": "释放WorkQueue资源，取消所有等待中的工作线程并清理信号量。",
    "tags": ["dispose", "cleanup", "cancellation"],
    "complexity": "simple"
})
edges_p1.append({"source": "file:Engine/WorkQueue.cs", "target": "class:Engine/WorkQueue.cs:WorkQueue", "type": "contains", "direction": "forward", "weight": 1.0})
edges_p1.append({"source": "file:Engine/WorkQueue.cs", "target": "class:Engine/WorkQueue.cs:WorkQueue", "type": "exports", "direction": "forward", "weight": 0.8})
for fn_name in ["WorkerFunction", "EnqueueWork", "Dequeue", "Dispose"]:
    edges_p1.append({"source": "file:Engine/WorkQueue.cs", "target": f"function:Engine/WorkQueue.cs:{fn_name}", "type": "contains", "direction": "forward", "weight": 1.0})
    edges_p1.append({"source": "file:Engine/WorkQueue.cs", "target": f"function:Engine/WorkQueue.cs:{fn_name}", "type": "exports", "direction": "forward", "weight": 0.8})
    edges_p1.append({"source": "class:Engine/WorkQueue.cs:WorkQueue", "target": f"function:Engine/WorkQueue.cs:{fn_name}", "type": "contains", "direction": "forward", "weight": 1.0})

# Write part 1
part1 = {"nodes": nodes_p1, "edges": edges_p1}
with open(os.path.join(OUT_DIR, "batch-34-part-1.json"), "w", encoding="utf-8") as f:
    json.dump(part1, f, indent=2, ensure_ascii=False)

print(f"Part 1: {len(nodes_p1)} nodes, {len(edges_p1)} edges")

# ===== PART 2: Files 14-25 =====
nodes_p2 = []
edges_p2 = []

# 14. Engine/XmlError.cs
nodes_p2.append({
    "id": "file:Engine/XmlError.cs",
    "type": "file", "name": "XmlError.cs",
    "filePath": "Engine/XmlError.cs",
    "summary": "XML序列化错误表示类，在XML反序列化过程中捕获并包装异常信息，关联到具体的XML元素和行号。",
    "tags": ["xml", "serialization", "error-handling", "diagnostics"],
    "complexity": "simple"
})
nodes_p2.append({
    "id": "class:Engine/XmlError.cs:XmlError",
    "type": "class", "name": "XmlError",
    "filePath": "Engine/XmlError.cs", "lineRange": [8, 30],
    "summary": "XML错误类，持有异常对象和XML行信息，ToString方法格式化输出包含行号的错误消息。",
    "tags": ["xml", "serialization", "error-wrapping", "diagnostics"],
    "complexity": "simple"
})
edges_p2.append({"source": "file:Engine/XmlError.cs", "target": "class:Engine/XmlError.cs:XmlError", "type": "contains", "direction": "forward", "weight": 1.0})
edges_p2.append({"source": "file:Engine/XmlError.cs", "target": "class:Engine/XmlError.cs:XmlError", "type": "exports", "direction": "forward", "weight": 0.8})

# 15. Engine/XmlMessage.cs
nodes_p2.append({
    "id": "file:Engine/XmlMessage.cs",
    "type": "file", "name": "XmlMessage.cs",
    "filePath": "Engine/XmlMessage.cs",
    "summary": "XML序列化信息消息类，在XML加载过程中记录非错误的消息信息，关联到具体的XML元素。",
    "tags": ["xml", "serialization", "message", "diagnostics"],
    "complexity": "simple"
})
nodes_p2.append({
    "id": "class:Engine/XmlMessage.cs:XmlMessage",
    "type": "class", "name": "XmlMessage",
    "filePath": "Engine/XmlMessage.cs", "lineRange": [7, 29],
    "summary": "XML消息类，持有消息文本和XML元素引用，ToString方法格式化输出包含行号的消息。",
    "tags": ["xml", "serialization", "message", "diagnostics"],
    "complexity": "simple"
})
edges_p2.append({"source": "file:Engine/XmlMessage.cs", "target": "class:Engine/XmlMessage.cs:XmlMessage", "type": "contains", "direction": "forward", "weight": 1.0})
edges_p2.append({"source": "file:Engine/XmlMessage.cs", "target": "class:Engine/XmlMessage.cs:XmlMessage", "type": "exports", "direction": "forward", "weight": 0.8})

# 16. Installer/Assets/LogoSide.bmp
nodes_p2.append({
    "id": "file:Installer/Assets/LogoSide.bmp",
    "type": "file", "name": "LogoSide.bmp",
    "filePath": "Installer/Assets/LogoSide.bmp",
    "summary": "安装程序使用的侧边栏Logo位图资源（BMP格式）。",
    "tags": ["asset", "installer", "logo", "bitmap", "binary"],
    "complexity": "simple"
})

# 17. Installer/Assets/LogoTop.bmp
nodes_p2.append({
    "id": "file:Installer/Assets/LogoTop.bmp",
    "type": "file", "name": "LogoTop.bmp",
    "filePath": "Installer/Assets/LogoTop.bmp",
    "summary": "安装程序使用的顶部横幅Logo位图资源（BMP格式）。",
    "tags": ["asset", "installer", "logo", "bitmap", "binary"],
    "complexity": "simple"
})

# 18. Installer/Assets/Newtonsoft.Json.dll
nodes_p2.append({
    "id": "file:Installer/Assets/Newtonsoft.Json.dll",
    "type": "file", "name": "Newtonsoft.Json.dll",
    "filePath": "Installer/Assets/Newtonsoft.Json.dll",
    "summary": "Newtonsoft.Json（Json.NET）程序集文件，用于OpenTAP安装包中的JSON序列化/反序列化支持。",
    "tags": ["json", "dependency", "serialization", "binary", "third-party"],
    "complexity": "simple"
})

# 19. LinuxInstall/INSTALL.sh
nodes_p2.append({
    "id": "file:LinuxInstall/INSTALL.sh",
    "type": "file", "name": "INSTALL.sh",
    "filePath": "LinuxInstall/INSTALL.sh",
    "summary": "OpenTAP Linux自动安装脚本，检测.NET Core运行时依赖，解压TapPackage到~/.tap目录并创建bin目录快捷方式。",
    "tags": ["installer", "linux", "shell-script", "deployment"],
    "complexity": "simple"
})

# 20. LinuxInstall/README
nodes_p2.append({
    "id": "file:LinuxInstall/README",
    "type": "file", "name": "README",
    "filePath": "LinuxInstall/README",
    "summary": "OpenTAP Linux发行版说明文档，包含前置依赖（.NET 6.0、Ubuntu 16.04+）、自动/手动安装步骤和使用说明。",
    "tags": ["documentation", "linux", "installation", "readme"],
    "complexity": "simple"
})

# 21. LinuxInstall/package/Debian/control.in
nodes_p2.append({
    "id": "file:LinuxInstall/package/Debian/control.in",
    "type": "file", "name": "control.in",
    "filePath": "LinuxInstall/package/Debian/control.in",
    "summary": "Debian软件包控制文件模板，定义OpenTAP包的元数据（名称、版本占位符、依赖项如libc6-dev和libcurl4、架构amd64）。",
    "tags": ["debian", "packaging", "template", "configuration"],
    "complexity": "simple"
})

# 22. LinuxInstall/package/Debian/create-deb
nodes_p2.append({
    "id": "file:LinuxInstall/package/Debian/create-deb",
    "type": "file", "name": "create-deb",
    "filePath": "LinuxInstall/package/Debian/create-deb",
    "summary": "Debian软件包构建脚本，从TapPackage解压文件，生成DEBIAN/control和postinst文件，使用dpkg --build创建.deb安装包。",
    "tags": ["debian", "packaging", "build-script", "deployment"],
    "complexity": "moderate"
})

# 23. LinuxInstall/package/Debian/postinst.in
nodes_p2.append({
    "id": "file:LinuxInstall/package/Debian/postinst.in",
    "type": "file", "name": "postinst.in",
    "filePath": "LinuxInstall/package/Debian/postinst.in",
    "summary": "Debian软件包安装后脚本模板，创建opentap用户组、设置安装目录权限（g+rwxs粘滞位）并提示用户加入opentap组。",
    "tags": ["debian", "post-install", "template", "permissions"],
    "complexity": "simple"
})

# 24. LinuxInstall/tap.sh
nodes_p2.append({
    "id": "file:LinuxInstall/tap.sh",
    "type": "file", "name": "tap.sh",
    "filePath": "LinuxInstall/tap.sh",
    "summary": "OpenTAP Linux启动脚本，解析tap可执行文件的真实路径，检测dotnet运行时并执行tap.dll。",
    "tags": ["launcher", "linux", "shell-script", "entry-point"],
    "complexity": "simple"
})
nodes_p2.append({
    "id": "function:LinuxInstall/tap.sh:realpath",
    "type": "function", "name": "realpath",
    "filePath": "LinuxInstall/tap.sh", "lineRange": [13, 32],
    "summary": "自定义realpath实现，通过readlink递归解析符号链接，返回文件的绝对真实路径，包含无限循环检测。",
    "tags": ["path-resolution", "symlink", "utility", "shell-function"],
    "complexity": "moderate"
})
edges_p2.append({"source": "file:LinuxInstall/tap.sh", "target": "function:LinuxInstall/tap.sh:realpath", "type": "contains", "direction": "forward", "weight": 1.0})

# 25. nuget/OpenTAP.nuspec
nodes_p2.append({
    "id": "file:nuget/OpenTAP.nuspec",
    "type": "file", "name": "OpenTAP.nuspec",
    "filePath": "nuget/OpenTAP.nuspec",
    "summary": "NuGet包规范文件，定义OpenTAP包的元数据（id、版本、描述）、许可信息（MPL-2.0）和文件包含规则。",
    "tags": ["nuget", "packaging", "metadata", "configuration"],
    "complexity": "simple"
})

# Write part 2
part2 = {"nodes": nodes_p2, "edges": edges_p2}
with open(os.path.join(OUT_DIR, "batch-34-part-2.json"), "w", encoding="utf-8") as f:
    json.dump(part2, f, indent=2, ensure_ascii=False)

print(f"Part 2: {len(nodes_p2)} nodes, {len(edges_p2)} edges")
print(f"Total: {len(nodes_p1)+len(nodes_p2)} nodes, {len(edges_p1)+len(edges_p2)} edges")
