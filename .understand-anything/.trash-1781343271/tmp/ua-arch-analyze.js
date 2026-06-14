#!/usr/bin/env node
/**
 * OpenTAP Architecture Layer Analyzer - Phase 1 Script
 *
 * Reads fileNodes and allEdges from input JSON, computes structural patterns,
 * and writes results JSON.
 *
 * For .NET C# projects, the primary dependency edges are:
 * - depends_on: csproj project references
 * - tested_by: test → code under test
 * - configures: config → code
 * - related: cross-file associations
 * - deploys: service/deployment → code
 * - documents: document → code
 * - imports: explicit import directives (JS/C# using)
 */

const fs = require('fs');

const INPUT_PATH = process.argv[2];
const OUTPUT_PATH = process.argv[3];

if (!INPUT_PATH || !OUTPUT_PATH) {
  console.error('Usage: node ua-arch-analyze.js <input.json> <output.json>');
  process.exit(1);
}

// ─── Read Input ───────────────────────────────────────────────────────────
let inputData;
try {
  inputData = JSON.parse(fs.readFileSync(INPUT_PATH, 'utf8'));
} catch (e) {
  console.error(`Failed to read input: ${e.message}`);
  process.exit(1);
}

const fileNodes = inputData.fileNodes;
const allEdges = inputData.allEdges;
const importEdges = inputData.importEdges || [];

if (!fileNodes || !Array.isArray(fileNodes)) {
  console.error('Invalid input: fileNodes array missing');
  process.exit(1);
}

// ─── Build File Node ID Set ───────────────────────────────────────────────
const fileNodeIdSet = new Set(fileNodes.map(n => n.id));
const fileNodeMap = new Map(fileNodes.map(n => [n.id, n]));

// ─── Filter to File-Level Edges Only ──────────────────────────────────────
// Edges where BOTH source AND target are in the fileNodes set are file-level.
// Sub-file edges have targets like "class:..." or "function:..." which are not in fileNodes.
const fileLevelEdges = (allEdges || []).filter(
  e => fileNodeIdSet.has(e.source) && fileNodeIdSet.has(e.target)
);

const importOnlyEdges = (importEdges || []).filter(
  e => fileNodeIdSet.has(e.source) && fileNodeIdSet.has(e.target)
);

// Log filtering stats
const subFileTypes = (allEdges || []).filter(
  e => !(fileNodeIdSet.has(e.source) && fileNodeIdSet.has(e.target))
);
console.error(`Total edges in input: ${(allEdges || []).length}`);
console.error(`File-level edges: ${fileLevelEdges.length}`);
console.error(`Sub-file edges filtered out: ${subFileTypes.length}`);

// ─── A. Directory Grouping ────────────────────────────────────────────────
function getTopLevelDir(filePath) {
  const parts = filePath.split('/');
  if (parts.length <= 1) return '(root)';
  return parts[0];
}

const directoryGroups = {};
for (const node of fileNodes) {
  const dir = getTopLevelDir(node.filePath);
  if (!directoryGroups[dir]) {
    directoryGroups[dir] = [];
  }
  directoryGroups[dir].push(node.id);
}

// ─── B. Node Type Grouping ────────────────────────────────────────────────
const nodeTypeGroups = {};
const nodeTypeCounts = {};
for (const node of fileNodes) {
  const type = node.type || 'unknown';
  if (!nodeTypeGroups[type]) {
    nodeTypeGroups[type] = [];
  }
  nodeTypeGroups[type].push(node.id);
  nodeTypeCounts[type] = (nodeTypeCounts[type] || 0) + 1;
}

// ─── C. Import Adjacency Matrix (using file-level depends_on and imports) ─
// For C# projects, the key dependency relationship is "depends_on" (project refs).
// It also includes "imports" for JS files.
// We'll compute fan-in/fan-out for ALL file-level edge types.

const fileFanIn = {};
const fileFanOut = {};

for (const node of fileNodes) {
  fileFanIn[node.id] = 0;
  fileFanOut[node.id] = 0;
}

// Map from source dir to target dir for imports/depends_on
const dirImportsFrom = {};  // dir → Set of dirs it imports from
const dirImportsBy = {};    // dir → Set of dirs that import from it
const interGroupCount = {}; // "fromDir->toDir" → count

for (const edge of fileLevelEdges) {
  // Fan-out for source, fan-in for target
  fileFanOut[edge.source] = (fileFanOut[edge.source] || 0) + 1;
  fileFanIn[edge.target] = (fileFanIn[edge.target] || 0) + 1;

  // Inter-group tracking (for all edge types)
  const srcNode = fileNodeMap.get(edge.source);
  const tgtNode = fileNodeMap.get(edge.target);
  if (!srcNode || !tgtNode) continue;

  const srcDir = getTopLevelDir(srcNode.filePath);
  const tgtDir = getTopLevelDir(tgtNode.filePath);
  if (srcDir === tgtDir) continue; // skip intra-group for inter-group count

  const key = `${srcDir}->${tgtDir}`;
  interGroupCount[key] = (interGroupCount[key] || 0) + 1;

  if (!dirImportsFrom[srcDir]) dirImportsFrom[srcDir] = new Set();
  if (!dirImportsBy[tgtDir]) dirImportsBy[tgtDir] = new Set();
  dirImportsFrom[srcDir].add(tgtDir);
  dirImportsBy[tgtDir].add(srcDir);
}

// Compute total fan-in/top fan-in (top 20)
const topFanIn = Object.entries(fileFanIn)
  .filter(([, v]) => v > 0)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 20)
  .map(([k, v]) => ({ file: k, fanIn: v }));

const topFanOut = Object.entries(fileFanOut)
  .filter(([, v]) => v > 0)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 20)
  .map(([k, v]) => ({ file: k, fanOut: v }));

const fileFanInOut = {};
for (const e of topFanIn) fileFanInOut[e.file] = { fanIn: e.fanIn };
for (const e of topFanOut) {
  if (!fileFanInOut[e.file]) fileFanInOut[e.file] = {};
  fileFanInOut[e.file].fanOut = e.fanOut;
}

// ─── D. Cross-Category Dependency Analysis ────────────────────────────────
const crossCategory = {}; // "fromType->toType" → { edgeType → count }
for (const edge of fileLevelEdges) {
  const srcNode = fileNodeMap.get(edge.source);
  const tgtNode = fileNodeMap.get(edge.target);
  if (!srcNode || !tgtNode) continue;

  const fromType = srcNode.type;
  const toType = tgtNode.type;
  const key = `${fromType}->${toType}`;
  if (!crossCategory[key]) crossCategory[key] = {};
  crossCategory[key][edge.type] = (crossCategory[key][edge.type] || 0) + 1;
}

// Flatten to output format
const crossCategoryEdges = [];
for (const [key, typeCounts] of Object.entries(crossCategory)) {
  const [fromType, toType] = key.split('->');
  for (const [edgeType, count] of Object.entries(typeCounts)) {
    crossCategoryEdges.push({ fromType, toType, edgeType, count });
  }
}
crossCategoryEdges.sort((a, b) => b.count - a.count);

// ─── E. Inter-Group Edge Frequency (all edge types) ──────────────────────
const interGroupImports = Object.entries(interGroupCount)
  .map(([key, count]) => {
    const [from, to] = key.split('->');
    return { from, to, count };
  })
  .sort((a, b) => b.count - a.count);

// ─── F. Intra-Group Density ───────────────────────────────────────────────
const intraGroupDensity = {};
for (const [dir, nodeIds] of Object.entries(directoryGroups)) {
  const nodeIdSet = new Set(nodeIds);
  let internalEdges = 0;
  let totalEdges = 0;

  for (const edge of fileLevelEdges) {
    const srcNode = fileNodeMap.get(edge.source);
    const tgtNode = fileNodeMap.get(edge.target);
    if (!srcNode || !tgtNode) continue;

    const srcDir = getTopLevelDir(srcNode.filePath);
    const tgtDir = getTopLevelDir(tgtNode.filePath);

    const srcInGroup = srcDir === dir;
    const tgtInGroup = tgtDir === dir;

    if (srcInGroup || tgtInGroup) {
      totalEdges++;
      if (srcInGroup && tgtInGroup) {
        internalEdges++;
      }
    }
  }

  const density = totalEdges > 0 ? internalEdges / totalEdges : 0;
  intraGroupDensity[dir] = { internalEdges, totalEdges, density };
}

// ─── G. Directory Pattern Matching ────────────────────────────────────────
const directoryPatterns = {
  'routes': 'api', 'api': 'api', 'controllers': 'api', 'endpoints': 'api', 'handlers': 'api',
  'services': 'service', 'core': 'service', 'lib': 'service', 'domain': 'service', 'logic': 'service',
  'models': 'data', 'db': 'data', 'data': 'data', 'persistence': 'data', 'repository': 'data', 'entities': 'data',
  'components': 'ui', 'views': 'ui', 'pages': 'ui', 'ui': 'ui', 'layouts': 'ui', 'screens': 'ui',
  'middleware': 'middleware', 'plugins': 'middleware', 'interceptors': 'middleware', 'guards': 'middleware',
  'utils': 'utility', 'helpers': 'utility', 'common': 'utility', 'shared': 'utility', 'tools': 'utility',
  'config': 'config', 'constants': 'config', 'env': 'config', 'settings': 'config',
  '__tests__': 'test', 'test': 'test', 'tests': 'test', 'spec': 'test', 'specs': 'test',
  'types': 'types', 'interfaces': 'types', 'schemas': 'types', 'contracts': 'types', 'dtos': 'types',
  'hooks': 'hooks', 'store': 'state', 'state': 'state', 'reducers': 'state', 'actions': 'state', 'slices': 'state',
  'assets': 'assets', 'static': 'assets', 'public': 'assets',
  'migrations': 'data',
  'management': 'config', 'commands': 'config',
  'templatetags': 'utility',
  'signals': 'service',
  'serializers': 'api',
  'cmd': 'entry',
  'internal': 'service',
  'pkg': 'utility',
  'src/main/java': 'service', 'src/test/java': 'test',
  'dto': 'types', 'request': 'types', 'response': 'types',
  'entity': 'data', 'controller': 'api', 'routers': 'api',
  'composables': 'service',
  'blueprints': 'api',
  'mailers': 'service', 'jobs': 'service', 'channels': 'service',
  'bin': 'entry',
  'docs': 'documentation', 'documentation': 'documentation', 'wiki': 'documentation',
  'deploy': 'infrastructure', 'deployment': 'infrastructure', 'infra': 'infrastructure', 'infrastructure': 'infrastructure',
  '.github': 'ci-cd', '.gitlab': 'ci-cd', '.circleci': 'ci-cd',
  'k8s': 'infrastructure', 'kubernetes': 'infrastructure', 'helm': 'infrastructure', 'charts': 'infrastructure',
  'terraform': 'infrastructure', 'tf': 'infrastructure',
  'docker': 'infrastructure',
  'sql': 'data', 'database': 'data', 'schema': 'data',
};

// Additional file-level patterns
const filePatterns = {
  // Test file patterns
  test: [/\.test\./, /\.spec\./, /^test_/, /_test\.go$/, /Test\.java$/, /_spec\.rb$/, /Test\.php$/, /Tests?\.cs$/],
  // TypeScript declaration files
  types: [/\.d\.ts$/],
  // Entry point files
  entry: [/\/index\.ts$/, /\/index\.js$/, /\/__init__\.py$/, /\/manage\.py$/,
          /\/main\.go$/, /\/main\.rs$/, /\/lib\.rs$/, /\/Application\.java$/,
          /\/Program\.cs$/, /\/config\.ru$/,
          /wsgi\.py$/, /asgi\.py$/],
};

const patternMatches = {};

// Match directory names against patterns
for (const dir of Object.keys(directoryGroups)) {
  const lowerDir = dir.toLowerCase();

  // First try exact directory name match
  if (directoryPatterns[lowerDir]) {
    patternMatches[dir] = directoryPatterns[lowerDir];
    continue;
  }

  // Try partial match
  for (const [pattern, label] of Object.entries(directoryPatterns)) {
    if (lowerDir.includes(pattern)) {
      patternMatches[dir] = label;
      break;
    }
  }

  // Check file-level patterns for files in this directory
  if (!patternMatches[dir]) {
    const nodeIds = directoryGroups[dir];
    for (const nid of nodeIds) {
      const node = fileNodeMap.get(nid);
      if (!node) continue;
      const fpath = node.filePath;
      const fname = node.name;

      // Check test patterns
      if (fname.match(/\.test\./) || fname.match(/\.spec\./) ||
          fname.match(/^test_/) || fname.match(/_test\.go$/) ||
          fname.match(/Test\.java$/) || fname.match(/_spec\.rb$/) ||
          fname.match(/Test\.php$/) || fname.match(/Tests?\.cs$/)) {
        patternMatches[dir] = 'test';
        break;
      }

      // Check entry point patterns
      if (fname === 'Program.cs' || fname === 'Main.cs' ||
          fname === 'index.ts' || fname === 'index.js' ||
          fname === '__init__.py' || fname === 'main.go' ||
          fname === 'main.rs' || fname === 'lib.rs') {
        patternMatches[dir] = 'entry';
        break;
      }

      // Check types pattern
      if (fname.match(/\.d\.ts$/)) {
        patternMatches[dir] = 'types';
        break;
      }
    }
  }

  // .NET specific patterns
  if (!patternMatches[dir]) {
    if (dir.match(/UnitTest/i)) {
      patternMatches[dir] = 'test';
    } else if (dir.match(/\.csproj$/i) || dir === 'Directory.Build.props' ||
               dir === '.gitversion') {
      patternMatches[dir] = 'config';
    }
  }
}

// ─── H. Deployment Topology Detection ─────────────────────────────────────
const deploymentTopology = {
  hasDockerfile: false,
  hasCompose: false,
  hasK8s: false,
  hasTerraform: false,
  hasCI: false,
  infraFiles: []
};

for (const node of fileNodes) {
  const fpath = node.filePath;
  const fname = node.name;

  if (fname.includes('Dockerfile')) {
    deploymentTopology.hasDockerfile = true;
    deploymentTopology.infraFiles.push(node.id);
  }
  if (fname.includes('docker-compose')) {
    deploymentTopology.hasCompose = true;
    deploymentTopology.infraFiles.push(node.id);
  }
  if (fpath.match(/\.github\/workflows/)) {
    deploymentTopology.hasCI = true;
    deploymentTopology.infraFiles.push(node.id);
  }
  if (fname.match(/\.yml$/) && fpath.includes('.github/workflows')) {
    deploymentTopology.hasCI = true;
  }
  if (fname.match(/k8s|kubernetes|helm/i)) {
    deploymentTopology.hasK8s = true;
    deploymentTopology.infraFiles.push(node.id);
  }
  if (fname.match(/\.tf$/)) {
    deploymentTopology.hasTerraform = true;
    deploymentTopology.infraFiles.push(node.id);
  }

  // NuGet spec files, installer scripts, etc.
  if (fpath.match(/^nuget\//) || fpath.match(/\.nuspec$/) ||
      fpath.match(/^Installer\//) || fpath.match(/^LinuxInstall\//)) {
    if (!deploymentTopology.infraFiles.includes(node.id)) {
      deploymentTopology.infraFiles.push(node.id);
    }
  }
}

// ─── I. Data Pipeline Detection ──────────────────────────────────────────
const dataPipeline = {
  schemaFiles: [],
  migrationFiles: [],
  dataModelFiles: [],
  apiHandlerFiles: []
};

for (const node of fileNodes) {
  const fpath = node.filePath;
  const fname = node.name;

  if (fname.match(/\.sql$/)) {
    dataPipeline.schemaFiles.push(node.id);
  }
  if (fname.match(/\.graphql$/) || fname.match(/\.gql$/)) {
    dataPipeline.schemaFiles.push(node.id);
  }
  if (fname.match(/\.proto$/)) {
    dataPipeline.schemaFiles.push(node.id);
  }
  if (fpath.match(/migration/i) && fname.match(/\.sql$/)) {
    dataPipeline.migrationFiles.push(node.id);
  }
  if (fpath.match(/(models|entities|schema|db)\//i) && fname.match(/\.(cs|ts|js|py)$/)) {
    dataPipeline.dataModelFiles.push(node.id);
  }
}

// ─── J. Documentation Coverage ────────────────────────────────────────────
const docCoverage = {
  groupsWithDocs: 0,
  totalGroups: Object.keys(directoryGroups).length,
  coverageRatio: 0,
  undocumentedGroups: []
};

// Check for README.md or any .md file in each group
// Also check document-type nodes that reference code
const docNodes = fileNodes.filter(n => n.type === 'document');
const docRefTargets = new Set();

for (const edge of fileLevelEdges) {
  const srcNode = fileNodeMap.get(edge.source);
  const tgtNode = fileNodeMap.get(edge.target);
  if (srcNode && srcNode.type === 'document' && edge.type === 'documents') {
    if (tgtNode) {
      const dir = getTopLevelDir(tgtNode.filePath);
      docRefTargets.add(dir);
    }
  }
}

for (const [dir, nodeIds] of Object.entries(directoryGroups)) {
  const hasReadme = nodeIds.some(nid => {
    const node = fileNodeMap.get(nid);
    return node && node.name && node.name.toLowerCase() === 'readme.md';
  });
  const hasDocRef = docRefTargets.has(dir);
  const hasDocNode = nodeIds.some(nid => {
    const node = fileNodeMap.get(nid);
    return node && node.type === 'document';
  });

  if (hasReadme || hasDocNode || hasDocRef) {
    docCoverage.groupsWithDocs++;
  } else {
    docCoverage.undocumentedGroups.push(dir);
  }
}

docCoverage.coverageRatio = docCoverage.totalGroups > 0
  ? docCoverage.groupsWithDocs / docCoverage.totalGroups
  : 0;

// ─── K. Dependency Direction ──────────────────────────────────────────────
const dependencyDirection = [];
for (const entry of interGroupImports) {
  const { from, to, count } = entry;
  // Find reverse direction
  const reverseKey = `${to}->${from}`;
  const reverseEntry = interGroupImports.find(e => e.from === to && e.to === from);
  const reverseCount = reverseEntry ? reverseEntry.count : 0;

  if (count > reverseCount) {
    dependencyDirection.push({
      dependent: from,
      dependsOn: to,
      dominantCount: count,
      reverseCount: reverseCount
    });
  }
}

// Sort by dominance
dependencyDirection.sort((a, b) => (b.dominantCount - b.reverseCount) - (a.dominantCount - a.reverseCount));

// ─── Compute File Stats ──────────────────────────────────────────────────
const filesPerGroup = {};
for (const [dir, nodeIds] of Object.entries(directoryGroups)) {
  filesPerGroup[dir] = nodeIds.length;
}

// ─── Build Output ─────────────────────────────────────────────────────────
const output = {
  scriptCompleted: true,
  directoryGroups,
  nodeTypeGroups,
  crossCategoryEdges,
  interGroupImports,
  intraGroupDensity,
  patternMatches,
  deploymentTopology,
  dataPipeline,
  docCoverage,
  dependencyDirection,
  fileStats: {
    totalFileNodes: fileNodes.length,
    filesPerGroup,
    nodeTypeCounts
  },
  fileFanIn: Object.fromEntries(
    Object.entries(fileFanIn)
      .filter(([, v]) => v > 0)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 30)
  ),
  fileFanOut: Object.fromEntries(
    Object.entries(fileFanOut)
      .filter(([, v]) => v > 0)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 30)
  )
};

// ─── Write Output ─────────────────────────────────────────────────────────
try {
  fs.writeFileSync(OUTPUT_PATH, JSON.stringify(output, null, 2));
  console.error(`Output written to ${OUTPUT_PATH}`);
  console.error(`File nodes: ${fileNodes.length}`);
  console.error(`File-level edges: ${fileLevelEdges.length}`);
  console.error(`Directory groups: ${Object.keys(directoryGroups).length}`);
} catch (e) {
  console.error(`Failed to write output: ${e.message}`);
  process.exit(1);
}
