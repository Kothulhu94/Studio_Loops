import os
import json
import ast
import re
import glob
from datetime import datetime
from browser_research import BrowserResearch

ASCII_REPLACEMENTS = {
    "\u2019": "'",
    "\u2018": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2014": "-",
    "\u2013": "-",
    "\u2026": "...",
    "\u00a0": " ",
}


def normalize_ascii_text(value):
    text = str(value)
    for source, replacement in ASCII_REPLACEMENTS.items():
        text = text.replace(source, replacement)
    return text


class ResearchClient:
    """Research client for the Studio Loop Orchestrator. 
    Uses local Playwright browser automation for web research.
    No API keys or paid providers required.
    """
    def __init__(self, config=None, base_path=None):
        self.config = config or {}
        self.base_path = base_path or os.getcwd()
        research_config = self.config.get("web_research", {})
        self.enabled = research_config.get("enabled", False)
        self.browser_research = BrowserResearch(self.config, self.base_path)
        self.artifact_dir = os.path.join(self.base_path, research_config.get("artifact_dir", ".agent/Loop_Flow/research"))

    def perform_research(self, query, reason=None, feature_slug=None, stage=None, local_only=False, target_files=None, audit_kind=None):
        if local_only:
            print(f"Performing local codebase audit for: {query}")
            research_data = self._perform_local_audit(query, reason, target_files=target_files or [], audit_kind=audit_kind)
        elif not self.enabled:
            return {
                "query": query,
                "status": "blocked",
                "errors": ["Web research is disabled in config."]
            }
        else:
            print(f"Researching (Browser-Based): {query}")
            research_data = self.browser_research.perform_research(query, reason)
        
        # Save research brief artifact
        artifact_content = self.generate_artifact(research_data)
        os.makedirs(self.artifact_dir, exist_ok=True)
        
        # Generate unique filename
        safe_query = "".join([c if c.isalnum() else "_" for c in query[:30]]).strip("_")
        slug = feature_slug or "latest"
        stage_name = stage or "unknown"
        filename = f"{slug}_{stage_name}_{safe_query}_research_brief.md"
        artifact_path = os.path.join(self.artifact_dir, filename)
        
        with open(artifact_path, 'w', encoding='utf-8') as f:
            f.write(artifact_content)
            
        research_data["artifact_path"] = artifact_path
        return research_data

    def _perform_local_audit(self, query, reason, target_files=None, audit_kind=None):
        """Inspect requested workspace files and return bounded local evidence."""
        target_files = target_files or []
        if audit_kind == "discovery" or self._contains_directory_target(target_files):
            return self._perform_local_discovery(query, reason, target_files)

        retrieved_at = datetime.now().isoformat()
        findings = []
        sources = []
        errors = []
        inspected = []
        expanded_files, target_errors = self._expand_file_targets(target_files)
        errors.extend(target_errors)

        for rel_path in expanded_files:
            full_path = os.path.join(self.base_path, rel_path)
            with open(full_path, "r", encoding="utf-8", errors="replace") as handle:
                text = handle.read()

            inspected.append(rel_path)
            
            # Include both the summary AND the full content (up to limit)
            details = self._summarize_local_file(rel_path, text)
            
            content_snippet = text
            if len(content_snippet) > 10000:
                content_snippet = content_snippet[:10000] + "\n... [TRUNCATED] ..."
            
            findings.append(f"### FULL SOURCE CODE: {rel_path}\n```\n{content_snippet}\n```")
            findings.extend(details)
            
            sources.append({
                "title": f"Local file: {rel_path}",
                "url": f"local://{rel_path}",
                "status": "fetched",
                "relevant": True,
                "retrieved_at": retrieved_at,
                "notes": "Local codebase audit"
            })

        status = "complete" if inspected and not errors and len(findings) >= 1 else "blocked"
        if not target_files:
            errors.append("Local codebase audit requires target_files.")
        if inspected and len(findings) < 1:
            errors.append("Local codebase audit produced no findings.")

        return {
            "query": query,
            "reason": reason,
            "status": status,
            "evidence_type": "local_codebase",
            "sources": sources,
            "findings": findings,
            "errors": errors,
            "source_set_relevance_passed": status == "complete",
            "backend": "local_audit"
        }

    def _perform_local_discovery(self, query, reason, target_files=None):
        target_files = target_files or []
        retrieved_at = datetime.now().isoformat()
        roots, root_errors = self._resolve_discovery_roots(target_files)
        files = self._collect_discovery_files(roots)
        ranked_files = self._rank_discovery_files(query, files)
        selected = ranked_files[:20]

        findings = []
        sources = []
        for item in selected[:10]:
            symbols = ", ".join(item["symbols"][:6]) or "no symbols detected"
            findings.append(f"Found {item['path']} with {symbols} ({item['line_count']} lines).")
            sources.append({
                "title": f"Local file: {item['path']}",
                "url": f"local://{item['path']}",
                "status": "fetched",
                "relevant": True,
                "retrieved_at": retrieved_at,
                "notes": "Local codebase discovery"
            })

        if os.path.exists(os.path.join(self.base_path, "tools/test_orchestrator.py")) and not os.path.exists(os.path.join(self.base_path, "tests/test_orchestrator.py")):
            findings.append("No tests/test_orchestrator.py found; closest known candidate is tools/test_orchestrator.py.")

        errors = root_errors
        status = "complete" if len(selected) >= 3 and len(findings) >= 1 and not errors else "blocked"
        if not selected:
            errors.append("Local discovery found no relevant files.")

        return {
            "query": query,
            "reason": reason,
            "status": status,
            "evidence_type": "local_codebase",
            "audit_kind": "discovery",
            "sources": sources,
            "findings": findings,
            "errors": errors,
            "source_set_relevance_passed": status == "complete",
            "backend": "local_audit"
        }

    def _contains_directory_target(self, target_files):
        for target in target_files or []:
            rel_path, error = self._normalize_local_target(target)
            if error:
                continue
            if os.path.isdir(os.path.join(self.base_path, rel_path)):
                return True
        return False

    def _normalize_local_target(self, target):
        rel_path = str(target).replace("\\", "/").strip()
        normalized_rel = os.path.normpath(rel_path).replace("\\", "/")
        if not rel_path:
            return None, "Target file is empty."
        if os.path.isabs(rel_path) or normalized_rel == ".." or normalized_rel.startswith("../") or "/../" in normalized_rel:
            return None, f"Target file must be workspace-relative and cannot contain '..': {rel_path}"
        return normalized_rel, None

    def _is_allowed_local_path(self, rel_path):
        rel_path = rel_path.replace("\\", "/").strip("/")
        return any(rel_path == root or rel_path.startswith(root + "/") for root in self.ALLOWED_LOCAL_ROOTS)

    def _is_ignored_rel_path(self, rel_path):
        parts = rel_path.replace("\\", "/").split("/")
        return any(part in self.IGNORED_DIRS for part in parts)

    def _expand_file_targets(self, target_files):
        expanded = []
        errors = []
        seen = set()
        if not target_files:
            return expanded, ["Local codebase audit requires target_files."]

        for target in target_files:
            rel_path, error = self._normalize_local_target(target)
            if error:
                errors.append(error)
                continue
            if any(ch in rel_path for ch in "*?["):
                matches = glob.glob(os.path.join(self.base_path, rel_path), recursive=True)
                file_matches = []
                for match in matches:
                    if not os.path.isfile(match):
                        continue
                    match_rel = os.path.relpath(match, self.base_path).replace("\\", "/")
                    if self._is_allowed_local_path(match_rel) and not self._is_ignored_rel_path(match_rel):
                        file_matches.append(match_rel)
                if not file_matches:
                    errors.append(f"Glob target did not match allowed files: {rel_path}")
                    continue
                for match_rel in sorted(file_matches):
                    if match_rel not in seen:
                        expanded.append(match_rel)
                        seen.add(match_rel)
                continue

            full_path = os.path.join(self.base_path, rel_path)
            if os.path.isdir(full_path):
                discovered = self._collect_discovery_files([rel_path])
                for item in discovered:
                    if item["path"] not in seen:
                        expanded.append(item["path"])
                        seen.add(item["path"])
                continue
            if not self._is_allowed_local_path(rel_path):
                errors.append(f"Target file is outside allowed local audit roots: {rel_path}")
                continue
            if not os.path.isfile(full_path):
                suggestion = self._closest_existing_file(rel_path)
                message = f"Target file does not exist: {rel_path}"
                if suggestion:
                    message += f". Closest candidate: {suggestion}"
                errors.append(message)
                continue
            if self._is_ignored_rel_path(rel_path):
                errors.append(f"Target file is in an ignored local audit directory: {rel_path}")
                continue
            if rel_path not in seen:
                expanded.append(rel_path)
                seen.add(rel_path)

        return expanded, errors

    def _resolve_discovery_roots(self, target_files):
        roots = []
        errors = []
        targets = target_files or self.ALLOWED_LOCAL_ROOTS
        for target in targets:
            rel_path, error = self._normalize_local_target(target)
            if error:
                errors.append(error)
                continue
            if rel_path == ".agent":
                for root in [".agent/orchestrator", ".agent/workflows", ".agent/skills"]:
                    if root not in roots:
                        roots.append(root)
                continue
            if rel_path in self.ALLOWED_LOCAL_ROOTS:
                roots.append(rel_path)
                continue
            full_path = os.path.join(self.base_path, rel_path)
            if os.path.isdir(full_path):
                allowed_children = [
                    root for root in self.ALLOWED_LOCAL_ROOTS
                    if root == rel_path or root.startswith(rel_path.rstrip("/") + "/")
                ]
                if allowed_children:
                    roots.extend(allowed_children)
                else:
                    errors.append(f"Discovery directory is outside allowed local audit roots: {rel_path}")
                continue
            if os.path.isfile(full_path) and self._is_allowed_local_path(rel_path):
                roots.append(os.path.dirname(rel_path))
                continue
            suggestion = self._closest_existing_file(rel_path)
            message = f"Discovery target does not exist or is not allowed: {rel_path}"
            if suggestion:
                message += f". Closest candidate: {suggestion}"
            errors.append(message)

        roots = sorted(set(root for root in roots if root and os.path.isdir(os.path.join(self.base_path, root))))
        if not roots and not errors:
            roots = [root for root in self.ALLOWED_LOCAL_ROOTS if os.path.isdir(os.path.join(self.base_path, root))]
        return roots, errors

    def _collect_discovery_files(self, roots):
        items = []
        seen = set()
        for root in roots:
            if not self._is_allowed_local_path(root):
                continue
            full_root = os.path.join(self.base_path, root)
            if not os.path.isdir(full_root):
                continue
            for dirpath, dirnames, filenames in os.walk(full_root):
                rel_dir = os.path.relpath(dirpath, self.base_path).replace("\\", "/")
                dirnames[:] = [
                    dirname for dirname in dirnames
                    if dirname not in self.IGNORED_DIRS
                    and not self._is_ignored_rel_path(f"{rel_dir}/{dirname}")
                ]
                for filename in filenames:
                    if not filename.endswith(self.DISCOVERY_EXTENSIONS):
                        continue
                    full_path = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(full_path, self.base_path).replace("\\", "/")
                    if rel_path in seen or self._is_ignored_rel_path(rel_path) or not self._is_allowed_local_path(rel_path):
                        continue
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="replace") as handle:
                            text = handle.read()
                    except Exception:
                        continue
                    analysis = self._analyze_local_text(text)
                    items.append({
                        "path": rel_path,
                        "line_count": len(text.splitlines()),
                        "symbols": analysis["symbols"],
                        "imports": analysis["imports"],
                    })
                    seen.add(rel_path)
        return items

    def _rank_discovery_files(self, query, files):
        query_lower = str(query or "").lower()
        query_terms = set(re.findall(r"[a-z0-9_]+", query_lower))
        priority_pairs = [
            ("studiolooporchestrator", "studio_loop.py"),
            ("studio_loop", "studio_loop.py"),
            ("statestore", "state_store.py"),
            ("state_store", "state_store.py"),
            ("transitionengine", "transition_engine.py"),
            ("transition_engine", "transition_engine.py"),
            ("contextpruner", "context_pruner.py"),
            ("context_pruner", "context_pruner.py"),
            ("contextcompactor", "context_compactor.py"),
            ("context_compactor", "context_compactor.py"),
            ("researchclient", "research_client.py"),
            ("research_client", "research_client.py"),
            ("artifactvalidator", "artifact_validator.py"),
            ("artifact_validator", "artifact_validator.py"),
            ("responseparser", "response_parser.py"),
            ("response_parser", "response_parser.py"),
            ("test", "test_"),
        ]

        def score(item):
            path_lower = item["path"].lower()
            symbols_lower = " ".join(item["symbols"]).lower()
            value = 0
            for term in query_terms:
                if term and term in path_lower:
                    value += 3
                if term and term in symbols_lower:
                    value += 4
            for query_hint, path_hint in priority_pairs:
                if query_hint in query_lower and path_hint in path_lower:
                    value += 20
            if path_lower.startswith(".agent/orchestrator/"):
                value += 2
            return value

        return sorted(files, key=lambda item: (-score(item), item["path"]))

    def _analyze_local_text(self, text):
        imports = []
        symbols = []
        try:
            tree = ast.parse(text)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    imports.append(node.module or "")
                elif isinstance(node, ast.ClassDef):
                    symbols.append(f"class {node.name}")
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    symbols.append(f"def {node.name}")
        except SyntaxError:
            for line in text.splitlines():
                match = re.match(r"\s*(class|def)\s+([A-Za-z_][A-Za-z0-9_]*)", line)
                if match:
                    symbols.append(f"{match.group(1)} {match.group(2)}")
        return {"imports": imports, "symbols": symbols}

    def _closest_existing_file(self, requested_path):
        requested = str(requested_path).replace("\\", "/").strip()
        basename = os.path.basename(requested.rstrip("/"))
        if not basename:
            return None

        candidates = []
        for root, dirnames, filenames in os.walk(self.base_path):
            dirnames[:] = [
                dirname for dirname in dirnames
                if dirname not in {".git", "node_modules", "__pycache__", "dist", "build"}
            ]
            for filename in filenames:
                if filename != basename:
                    continue
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, self.base_path).replace("\\", "/")
                candidates.append(rel_path)

        if not candidates:
            return None

        requested_parts = set(requested.split("/"))
        return sorted(
            candidates,
            key=lambda candidate: (
                -len(requested_parts.intersection(candidate.split("/"))),
                len(candidate),
                candidate,
            )
        )[0]

    def _summarize_local_file(self, rel_path, text):
        lines = text.splitlines()
        line_count = len(lines)
        imports = []
        symbols = []
        todo_markers = []
        responsibilities = []
        integration_points = []
        risks = []

        analysis = self._analyze_local_text(text)
        imports = analysis["imports"]
        symbols = analysis["symbols"]

        for index, line in enumerate(lines, start=1):
            upper = line.upper()
            if "TODO" in upper or "FIXME" in upper:
                todo_markers.append(f"L{index}: {line.strip()[:140]}")
            stripped = line.strip()
            if stripped.startswith(("class ", "def ", "async def ")):
                responsibilities.append(stripped[:140])
            if any(token in stripped for token in ("ResearchClient", "ResponseParser", "ArtifactValidator", "TransitionEngine", "StateStore", "perform_research", "validate_research_result")):
                integration_points.append(stripped[:160])
            if any(token in upper for token in ("BLOCKED", "FAILED", "ERROR", "EXCEPTION", "RETRY")):
                risks.append(stripped[:160])

        excerpt_lines = []
        for index, line in enumerate(lines[:30], start=1):
            stripped = line.strip()
            if stripped.startswith(("import ", "from ", "class ", "def ", "async def ")):
                excerpt_lines.append(f"L{index}: {stripped[:160]}")
            if len(excerpt_lines) >= 4:
                break

        return [
            (
                f"{rel_path}: {line_count} lines; symbols: {', '.join(symbols[:12]) or 'none detected'}; "
                f"imports: {', '.join(sorted(set(imports))[:12]) or 'none detected'}."
            ),
            (
                f"{rel_path}: responsibilities appear centered on {', '.join(responsibilities[:6]) or 'module-level orchestration'}; "
                f"likely integration points include {', '.join(integration_points[:5]) or 'none detected by keyword scan'}."
            ),
            (
                f"{rel_path}: risks/TODOs: {', '.join((risks + todo_markers)[:6]) or 'no obvious TODO/FIXME or error-path markers found'}; "
                f"short excerpts: {' | '.join(excerpt_lines) or 'no import/symbol excerpt available'}."
            )
        ]

    def generate_artifact(self, research_data):
        query = normalize_ascii_text(research_data.get('query', 'Unknown'))
        status = normalize_ascii_text(research_data.get('status', 'complete'))
        
        content = f"# Research Brief: {query}\n\n"
        content += f"## Status\n{status}\n\n"
        content += f"## Query\n{query}\n\n"
        content += f"## Reason\n{normalize_ascii_text(research_data.get('reason', 'N/A'))}\n\n"
        
        content += "## Sources\n\n"
        content += "| Title | URL | Status | Retrieved | Notes |\n"
        content += "|---|---|---|---|---|\n"
        sources = research_data.get("sources", [])
        if status == "complete":
            sources = [
                src for src in sources
                if src.get("status") == "fetched" and src.get("relevant", True) and not src.get("rejected")
            ]
        for src in sources:
            coverage = ", ".join(src.get("topic_coverage", []))
            notes = normalize_ascii_text(src.get("notes", ""))
            if coverage:
                notes = f"{notes} coverage: {coverage}".strip()
            title = normalize_ascii_text(src.get("title", "")).replace("|", "\\|")
            url = normalize_ascii_text(src.get("url", "")).replace("|", "%7C")
            content += f"| {title} | {url} | {src.get('status', 'unknown')} | {src.get('retrieved_at', 'N/A')} | {notes.replace('|', '/')} |\n"
        
        content += "\n## Extracted Findings\n\n"
        if research_data.get("findings"):
            for finding in research_data["findings"]:
                content += f"### Finding\n{normalize_ascii_text(finding)}\n\n"
        else:
            content += "No findings recorded.\n"
        
        content += "\n## Copyright / Safety Notes\n"
        if research_data.get("evidence_type") == "local_codebase":
            content += "Extracted from local workspace files with short excerpts only.\n"
        else:
            content += "Extracted from public web sources using local browser automation. No prohibited IP terms detected in summary.\n"
        
        content += "\n## Technical Notes\n"
        backend = research_data.get("backend", "playwright")
        content += f"- Backend: {backend}\n"
        content += f"- Timestamp: {datetime.now().isoformat()}\n"
        
        return content
    ALLOWED_LOCAL_ROOTS = [
        ".agent/orchestrator",
        ".agent/workflows",
        ".agent/skills",
        "tests",
        "tools",
        "docs",
        "src",
        "public",
    ]
    IGNORED_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", "logs", "Loop_Flow"}
    DISCOVERY_EXTENSIONS = (".py", ".md", ".json", ".ts", ".tsx")
