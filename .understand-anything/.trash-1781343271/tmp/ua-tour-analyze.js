#!/usr/bin/env node
/**
 * Phase 1: Graph Topology Analysis for Tour Builder
 * Enhanced for C# project structure with configures/depends_on/contains/exports edges.
 */

const fs = require('fs');

// --- Argument parsing ---
const inputFile = process.argv[2];
const outputFile = process.argv[3];

if (!inputFile || !outputFile) {
  console.error('Usage: node ua-tour-analyze.js <input.json> <output.json>');
  process.exit(1);
}

let data;
try {
  data = JSON.parse(fs.readFileSync(inputFile, 'utf-8'));
} catch (e) {
  console.error('Failed to read/parse input file: ' + e.message);
  process.exit(1);
}

const nodes = data.nodes || [];
const edges = data.edges || [];
const layers = data.layers || [];

console.error(`Loaded ${nodes.length} nodes, ${edges.length} edges, ${layers.length} layers`);

// --- Build lookup maps ---
const nodeMap = new Map();
for (const node of nodes) {
  nodeMap.set(node.id, node);
}

// --- A. Fan-In & B. Fan-Out Ranking ---
const fanIn = new Map();
const fanOut = new Map();

for (const node of nodes) {
  fanIn.set(node.id, 0);
  fanOut.set(node.id, 0);
}

for (const edge of edges) {
  const src = edge.source;
  const tgt = edge.target;
  if (fanIn.has(tgt)) fanIn.set(tgt, (fanIn.get(tgt) || 0) + 1);
  if (fanOut.has(src)) fanOut.set(src, (fanOut.get(src) || 0) + 1);
}

const fanInRanking = Array.from(fanIn.entries())
  .filter(([, count]) => count > 0)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 20)
  .map(([id, count]) => {
    const node = nodeMap.get(id);
    return { id, fanIn: count, name: node ? node.name : id };
  });

const fanOutRanking = Array.from(fanOut.entries())
  .filter(([, count]) => count > 0)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 20)
  .map(([id, count]) => {
    const node = nodeMap.get(id);
    return { id, fanOut: count, name: node ? node.name : id };
  });

// --- C. Entry Point Candidates ---
const allFanOutValues = Array.from(fanOut.values()).filter(v => v > 0).sort((a, b) => a - b);
const allFanInValues = Array.from(fanIn.values()).filter(v => v > 0).sort((a, b) => a - b);

const fanOutTop10Threshold = allFanOutValues.length > 0
  ? allFanOutValues[Math.floor(allFanOutValues.length * 0.9)] : 0;
const fanInBottom25Threshold = allFanInValues.length > 0
  ? allFanInValues[Math.floor(allFanInValues.length * 0.25)] : 0;

const entryFilePatterns = [
  /^index\.ts$/i, /^index\.js$/i, /^main\.ts$/i, /^main\.js$/i,
  /^app\.ts$/i, /^app\.js$/i, /^server\.ts$/i, /^server\.js$/i,
  /^mod\.rs$/i, /^main\.go$/i, /^main\.py$/i, /^main\.rs$/i,
  /^manage\.py$/i, /^app\.py$/i, /^wsgi\.py$/i, /^asgi\.py$/i,
  /^run\.py$/i, /^__main__\.py$/i,
  /^Application\.java$/i, /^Main\.java$/i, /^Program\.cs$/i,
  /^config\.ru$/i, /^index\.php$/i, /^App\.swift$/i,
  /^Application\.kt$/i, /^main\.cpp$/i, /^main\.c$/i,
];

function scoreEntryPoint(node) {
  let score = 0;
  const name = node.name || '';
  const filePath = node.filePath || '';

  if (node.type === 'document') {
    if (name === 'README.md') {
      const fp = filePath.toLowerCase();
      if (fp === 'readme.md' || fp === './readme.md') score += 5;
    } else if (name.endsWith('.md')) {
      const fp = filePath.toLowerCase();
      if (fp === name || fp === './' + name || !fp.includes('/')) score += 2;
    }
    return score;
  }

  if (node.type !== 'file') return score;

  for (const pattern of entryFilePatterns) {
    if (pattern.test(name)) { score += 3; break; }
  }

  if (filePath) {
    const depth = filePath.split('/').filter(s => s.length > 0).length;
    if (depth <= 1) score += 1;
    const segments = filePath.toLowerCase().split('/').filter(s => s.length > 0);
    if (segments.length === 2 && segments[0] === 'src' &&
        entryFilePatterns.some(p => p.test(segments[1]))) score += 1;
  }

  const fOut = fanOut.get(node.id) || 0;
  if (fOut >= fanOutTop10Threshold && fOut > 0) score += 1;

  const fIn = fanIn.get(node.id) || 0;
  if (fIn <= fanInBottom25Threshold) score += 1;

  return score;
}

const entryPointCandidates = nodes
  .map(node => ({
    id: node.id,
    score: scoreEntryPoint(node),
    name: node.name,
    summary: node.summary
  }))
  .filter(e => e.score > 0)
  .sort((a, b) => b.score - a.score)
  .slice(0, 5);

// --- D. BFS Traversal (Enhanced) ---
// Build bidirectional adjacency for structural edges
const forwardAdj = new Map();   // source -> Set of targets
const reverseAdj = new Map();   // target -> Set of sources

function addEdge(adj, from, to) {
  if (!adj.has(from)) adj.set(from, new Set());
  adj.get(from).add(to);
}

// Edge types to follow FORWARD in BFS:
const forwardEdgeTypes = new Set([
  'contains', 'exports', 'calls', 'depends_on', 'configures',
  'inherits', 'implements', 'deploys', 'imports', 'related', 'documents'
]);

// Edge types to follow in REVERSE in BFS (e.g., going from a file up to its project):
const reverseEdgeTypes = new Set([
  'configures', 'contains', 'tested_by'
]);

for (const edge of edges) {
  const src = edge.source;
  const tgt = edge.target;

  if (forwardEdgeTypes.has(edge.type)) {
    addEdge(forwardAdj, src, tgt);
  }
  if (reverseEdgeTypes.has(edge.type)) {
    addEdge(reverseAdj, tgt, src);
  }
}

// Find the best code entry point for BFS:
// Prefer the actual main entry point (tap/Program.cs) which is known to be the app entry
let topCodeEntry = null;
// First try file:tap/Program.cs explicitly since it's the documented entry point
if (nodeMap.has('file:tap/Program.cs')) {
  topCodeEntry = 'file:tap/Program.cs';
} else if (nodeMap.has('file:Cli/TapEntry.cs')) {
  topCodeEntry = 'file:Cli/TapEntry.cs';
}

// Fallback: use entryPointCandidates
if (!topCodeEntry) {
  for (const candidate of entryPointCandidates) {
    const node = nodeMap.get(candidate.id);
    if (node && node.type === 'file') {
      topCodeEntry = candidate.id;
      break;
    }
  }
}

let bfsTraversal = null;
if (topCodeEntry) {
  const visited = new Set();
  const order = [];
  const depthMap = {};
  const byDepth = {};

  const queue = [{ id: topCodeEntry, depth: 0 }];
  visited.add(topCodeEntry);

  while (queue.length > 0) {
    const { id, depth } = queue.shift();

    // Only include file/csproj/runtimeconfig/solution types in traversal output
    // (skip intermediate class/function nodes for cleaner output)
    const node = nodeMap.get(id);
    const isStructuralNode = node && (
      node.type === 'file' || node.type === 'config' ||
      node.type === 'document' || node.type === 'service' ||
      node.type === 'pipeline' || node.type === 'resource'
    );

    if (isStructuralNode || !id.includes(':')) {
      // Always add the start node, but for others only add structural nodes
    }

    // Always track in order/depthMap even for non-structural nodes
    // so we can use them as stepping stones
    order.push(id);
    depthMap[id] = depth;

    // For BFS output, only show structural nodes at each depth
    if (isStructuralNode) {
      if (!byDepth[depth]) byDepth[depth] = [];
      byDepth[depth].push(id);
    }

    // Get forward neighbors
    const fwdNeighbors = forwardAdj.get(id);
    if (fwdNeighbors) {
      for (const neighbor of fwdNeighbors) {
        if (!visited.has(neighbor) && nodeMap.has(neighbor)) {
          visited.add(neighbor);
          queue.push({ id: neighbor, depth: depth + 1 });
        }
      }
    }

    // Get reverse neighbors (for going "up" the hierarchy)
    const revNeighbors = reverseAdj.get(id);
    if (revNeighbors) {
      for (const neighbor of revNeighbors) {
        if (!visited.has(neighbor) && nodeMap.has(neighbor)) {
          visited.add(neighbor);
          queue.push({ id: neighbor, depth: depth + 1 });
        }
      }
    }
  }

  // Filter byDepth to only include structural nodes that were reached directly
  // Recompute byDepth from the order
  const cleanByDepth = {};
  for (const id of order) {
    const d = depthMap[id];
    const nd = nodeMap.get(id);
    if (nd && (nd.type === 'file' || nd.type === 'config' ||
        nd.type === 'document' || nd.type === 'service' ||
        nd.type === 'pipeline' || nd.type === 'resource')) {
      if (!cleanByDepth[d]) cleanByDepth[d] = [];
      cleanByDepth[d].push(id);
    }
  }

  bfsTraversal = {
    startNode: topCodeEntry,
    order,
    depthMap,
    byDepth: cleanByDepth,
  };
}

// --- E. Non-Code File Inventory ---
const nonCodeFiles = {
  documentation: [],
  infrastructure: [],
  data: [],
  config: [],
};

for (const node of nodes) {
  const entry = { id: node.id, name: node.name, summary: node.summary || '', type: node.type };
  switch (node.type) {
    case 'document':
      nonCodeFiles.documentation.push(entry);
      break;
    case 'service':
    case 'pipeline':
    case 'resource':
      nonCodeFiles.infrastructure.push(entry);
      break;
    case 'table':
    case 'schema':
    case 'endpoint':
      nonCodeFiles.data.push(entry);
      break;
    case 'config':
      nonCodeFiles.config.push(entry);
      break;
  }
}

// --- F. Tightly Coupled Clusters ---
const pairEdges = new Map();
const edgeSet = new Set();

for (const edge of edges) {
  edgeSet.add(`${edge.source}->${edge.target}`);
}

for (const edge of edges) {
  const reverse = `${edge.target}->${edge.source}`;
  if (edgeSet.has(reverse)) {
    const pair = [edge.source, edge.target].sort().join('|');
    pairEdges.set(pair, (pairEdges.get(pair) || 0) + 1);
  }
}

const clusters = [];
const usedNodes = new Set();
const sortedPairs = Array.from(pairEdges.entries())
  .sort((a, b) => b[1] - a[1]);

for (const [pairKey, edgeCount] of sortedPairs) {
  const pairNodes = pairKey.split('|');
  let targetCluster = null;
  for (const cluster of clusters) {
    const matchingNodes = pairNodes.filter(n => cluster.nodeSet.has(n));
    if (matchingNodes.length >= 1 && cluster.nodes.length < 5) {
      targetCluster = cluster;
      break;
    }
  }

  if (targetCluster) {
    for (const n of pairNodes) {
      if (!targetCluster.nodeSet.has(n)) {
        targetCluster.nodeSet.add(n);
        targetCluster.nodes.push(n);
      }
    }
    targetCluster.edgeCount += edgeCount;
  } else {
    const newNodeSet = new Set(pairNodes);
    if (!pairNodes.some(n => usedNodes.has(n))) {
      const newCluster = {
        nodes: pairNodes,
        nodeSet: newNodeSet,
        edgeCount: edgeCount,
      };
      clusters.push(newCluster);
      for (const n of pairNodes) usedNodes.add(n);
    }
  }
}

const filteredClusters = clusters
  .filter(c => c.nodes.length >= 2)
  .sort((a, b) => b.edgeCount - a.edgeCount)
  .slice(0, 10)
  .map(c => ({ nodes: c.nodes, edgeCount: c.edgeCount }));

// --- G. Layer List ---
const layersOutput = {
  count: layers.length,
  list: layers,
};

// --- H. Node Summary Index ---
const nodeSummaryIndex = {};
for (const node of nodes) {
  nodeSummaryIndex[node.id] = {
    name: node.name,
    type: node.type,
    summary: node.summary || '',
  };
}

// --- Assemble output ---
const output = {
  scriptCompleted: true,
  entryPointCandidates,
  fanInRanking,
  fanOutRanking,
  bfsTraversal,
  nonCodeFiles,
  clusters: filteredClusters,
  layers: layersOutput,
  nodeSummaryIndex,
  totalNodes: nodes.length,
  totalEdges: edges.length,
};

try {
  fs.writeFileSync(outputFile, JSON.stringify(output, null, 2), 'utf-8');
  console.error('Analysis complete. Output written to ' + outputFile);
  console.error(`  Entry point candidates: ${entryPointCandidates.length}`);
  console.error(`  Fan-in top: ${fanInRanking.length}`);
  console.error(`  Fan-out top: ${fanOutRanking.length}`);
  console.error(`  BFS start: ${bfsTraversal ? bfsTraversal.startNode : 'none'}`);
  console.error(`  BFS nodes visited: ${bfsTraversal ? bfsTraversal.order.length : 0}`);
  console.error(`  BFS structural nodes at depths: ${
    bfsTraversal ? Object.keys(bfsTraversal.byDepth).map(d => d + ':' + bfsTraversal.byDepth[d].length).join(', ') : 'none'
  }`);
  console.error(`  Non-code docs: ${nonCodeFiles.documentation.length}`);
  console.error(`  Non-code infra: ${nonCodeFiles.infrastructure.length}`);
  console.error(`  Non-code data: ${nonCodeFiles.data.length}`);
  console.error(`  Non-code config: ${nonCodeFiles.config.length}`);
  console.error(`  Clusters: ${filteredClusters.length}`);
  console.error(`  Layers: ${layers.length}`);
} catch (e) {
  console.error('Failed to write output: ' + e.message);
  process.exit(1);
}
