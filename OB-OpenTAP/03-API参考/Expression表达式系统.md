---
created: 2026-06-14
tags:
  - API参考
  - expression
  - 动态表达式
---
# Expression 表达式系统

## 概述

Expression 系统允许用户在测试步骤设置中**直接使用数学表达式和函数**，实现动态配置。由 `opentap/expressions` 插件提供。

```bash
tap package install Expressions
```

## 基本语法

### 数值计算

```
10 * 60              → 600
2 ^ 8                → 256
(1 + 2) * 3          → 9
sin(π / 2)           → 1
```

### 字符串插值

```
// 字符串属性中用 {} 嵌入表达式
BANDwidth {2000 * 1000000 / 10}
// → "BANDwidth 200000000"

// 带 $ 前缀显式声明
$"The number is {1 + 2}."
// → "The number is 3."
```

### 引用其他步骤的输出

```
// 用 @ 引用
The result was {@Scpi Step.Response}

// 转义含特殊字符的名称
@'Step (2).Power [dBm]' * 0.001
```

## 运算符

| 类别 | 运算符 | 说明 |
|------|--------|------|
| 算术 | `+` `-` `*` `/` `^` | 加减乘除幂 |
| 比较 | `<` `<=` `>` `>=` `==` `!=` | 比较运算 |
| 逻辑 | `&&` `\|\|` | 短路的 AND/OR |

## 常用函数

| 函数 | 说明 |
|------|------|
| `abs(v)` | 绝对值 |
| `sqrt(x)` | 平方根 |
| `exp(x)` | e^x |
| `log(x, base)` | 对数 |
| `log10(x)` / `log2(x)` | 常用对数 |
| `sin(v)` / `cos(v)` / `tan(v)` | 三角函数 |
| `asin(v)` / `acos(v)` / `atan(v)` | 反三角函数 |
| `floor(v)` / `ceiling(v)` / `round(v)` | 取整 |
| `max(a,b)` / `min(a,b)` | 最值（2-4参数） |
| `sign(v)` | 符号函数 |
| `env(name)` | 读取环境变量 |
| `empty(text)` | 空字符串检测 |
| `number(text)` | 文本转数字 |
| `number(text, n, [sep])` | 按分隔符取第 n 个数字 |

## 常量

- `π` 或 `pi` — 圆周率
- `e` — 自然常数

## 自定义函数（扩展）

```csharp
public class ExpressionFunctionProviderExample : IExpressionFunctionProvider
{
    class CustomMethods
    {
        public static bool string_is_empty(string str) => string.IsNullOrEmpty(str);
        public static double nth_number(string str, int index) =>
            double.Parse(str.Split(',').ElementAtOrDefault(index) ?? "0");
        public static double π => Math.PI;
    }

    static readonly MethodInfo[] extraMethods;
    static readonly PropertyInfo[] extraProperties;

    static ExpressionFunctionProviderExample()
    {
        extraMethods = typeof(CustomMethods)
            .GetMethods(BindingFlags.Static | BindingFlags.Public);
        extraProperties = typeof(CustomMethods)
            .GetProperties(BindingFlags.Static | BindingFlags.Public);
    }

    public IEnumerable<MemberInfo> GetMembers() =>
        extraMethods.Concat<MemberInfo>(extraProperties);
}
```

## GUI 中使用

在属性编辑器中直接输入表达式，OpenTAP 会在运行时计算：

- 数字属性: `10 * 60`
- 字符串属性: `BANDwidth {2000 * 1000000 / 10}`
- 可引用步骤输出: `@StepName.OutputName`

## 相关笔记

- [[TestStep详解]] — Input/Output 与 Expression 的区别
- [[Input输出系统]] — 步骤间数据传递的另一机制
- [[Mixin系统]] — Expression 常与 Mixin 配合使用

## 参考

- 仓库: [github.com/opentap/expressions](https://github.com/opentap/expressions)
- 文档: [doc/Developer Guide/Test Step/Readme.md](doc/Developer Guide/Test Step/Readme.md) (Expressions 节)
