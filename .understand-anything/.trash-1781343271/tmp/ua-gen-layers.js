#!/usr/bin/env node
/**
 * Generate layers.json by assigning every file node to exactly one layer.
 * Uses directory-based assignment with (root) split by node type.
 */
const fs = require('fs');

const INPUT_PATH = process.argv[2];
const OUTPUT_PATH = process.argv[3];

if (!INPUT_PATH || !OUTPUT_PATH) {
  console.error('Usage: node gen-layers.js <input-nodes.json> <layers.json>');
  process.exit(1);
}

const nodes = JSON.parse(fs.readFileSync(INPUT_PATH, 'utf8'));

function getTopLevelDir(fp) {
  const parts = fp.split('/');
  return parts.length > 1 ? parts[0] : '(root)';
}

// Layer definitions with directory assignments
const layerDefs = [
  {
    id: 'layer:engine',
    name: '核心引擎层',
    description: 'OpenTAP 核心引擎，提供测试执行、序列化、CLI 解析、插件加载、日志记录和设置管理等基础能力',
    directories: ['Engine'],
    dirFilter: null
  },
  {
    id: 'layer:package',
    name: '包管理层',
    description: 'OpenTAP 包管理系统，处理测试包的创建、解析、缓存、安装和版本管理',
    directories: ['Package'],
    dirFilter: null
  },
  {
    id: 'layer:plugins',
    name: '插件与 SDK 层',
    description: '内置测试步骤插件（Sweep、Delay、Wait 等）以及面向插件开发者的 SDK 示例和参考实现',
    directories: ['BasicSteps', 'sdk'],
    dirFilter: null
  },
  {
    id: 'layer:entry',
    name: '入口点层',
    description: '命令行接口入口点和自动升级器，提供 `tap` 命令的启动和版本升级机制',
    directories: ['Cli', 'tap', 'Tap.Upgrader'],
    dirFilter: null
  },
  {
    id: 'layer:test',
    name: '测试层',
    description: '引擎和包管理的单元测试，以及集成测试计划文件（.TapPlan）',
    directories: ['Engine.UnitTests', 'Package.UnitTests', 'tests'],
    dirFilter: null
  },
  {
    id: 'layer:shared',
    name: '共享工具层',
    description: '跨项目使用的共享代码和辅助工具，包括程序集信息和通用基础类',
    directories: ['Shared'],
    dirFilter: null
  },
  {
    id: 'layer:infrastructure',
    name: '基础设施层',
    description: 'Docker 容器定义、CI/CD 工作流（GitHub Actions）、安装程序、Linux 安装脚本、NuGet 打包规范和 .NET 项目模板',
    directories: ['docker', '.github', 'Installer', 'LinuxInstall', 'nuget', 'templates'],
    dirFilter: null
  },
  {
    id: 'layer:documentation',
    name: '文档层',
    description: '项目技术文档，包括开发者指南、API 参考、用户手册和基于 VitePress 构建的文档站点',
    directories: ['doc'],
    dirFilter: null,
    extraFromRoot: ['document']  // document type nodes from root
  },
  {
    id: 'layer:config',
    name: '项目配置层',
    description: '项目根级配置文件，包括 MSBuild 属性、解决方案文件、版本管理和包清单',
    directories: ['.claude'],
    dirFilter: null,
    extraFromRoot: ['config', 'file']  // config and file type nodes from root (except documents)
  }
];

// Build node assignment
const layerAssignments = {};
for (const layer of layerDefs) {
  layerAssignments[layer.id] = [];
}

// Determine root document node IDs
const rootDocIds = new Set();
const rootConfigIds = new Set();
for (const node of nodes) {
  const dir = getTopLevelDir(node.filePath);
  if (dir === '(root)' && node.type === 'document') {
    rootDocIds.add(node.id);
  }
  if (dir === '(root)' && node.type !== 'document') {
    rootConfigIds.add(node.id);
  }
}

// Assign nodes to layers
for (const node of nodes) {
  const dir = getTopLevelDir(node.filePath);
  let assigned = false;

  for (const layer of layerDefs) {
    // Check directory match
    if (layer.directories && layer.directories.includes(dir)) {
      layerAssignments[layer.id].push(node.id);
      assigned = true;
      break;
    }

    // Check extraFromRoot
    if (dir === '(root)' && layer.extraFromRoot) {
      if (layer.extraFromRoot.includes(node.type)) {
        layerAssignments[layer.id].push(node.id);
        assigned = true;
        break;
      }
    }
  }

  if (!assigned) {
    console.error(`WARNING: Unassigned node: ${node.id} (${node.filePath}, type: ${node.type})`);
  }
}

// Build output
const output = [];
for (const layer of layerDefs) {
  const nodeIds = layerAssignments[layer.id];
  // Sort node IDs for consistency
  nodeIds.sort();
  output.push({
    id: layer.id,
    name: layer.name,
    description: layer.description,
    nodeIds
  });
}

// Verify total count
const totalAssigned = output.reduce((sum, l) => sum + l.nodeIds.length, 0);
console.error(`Total nodes: ${nodes.length}, Assigned: ${totalAssigned}`);
if (totalAssigned !== nodes.length) {
  console.error('ERROR: Node count mismatch!');
  process.exit(1);
}

// Print per-layer counts
for (const layer of output) {
  console.error(`  ${layer.id}: ${layer.nodeIds.length} nodes`);
}

fs.writeFileSync(OUTPUT_PATH, JSON.stringify(output, null, 2));
console.error(`Layers written to ${OUTPUT_PATH}`);
