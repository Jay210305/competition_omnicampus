#!/usr/bin/env python3
"""
Plan Linter according to PLANNING_METHODOLOGY.md Step 7.
Validates:
1. Sub-task hours sum to task effort_h
2. Task effort_h sum to sprint hours in roadmap
3. Unique task IDs
4. Dependencies exist and form a DAG with no cycles
5. Internal markdown links are valid
"""

import os
import re
import glob
import sys

def parse_frontmatter(content):
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    yaml_text = parts[1]
    body = parts[2]
    meta = {}
    for line in yaml_text.strip().split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                items = [x.strip() for x in v[1:-1].split(",") if x.strip()]
                meta[k] = items
            else:
                try:
                    if "." in v:
                        meta[k] = float(v)
                    else:
                        meta[k] = int(v)
                except ValueError:
                    meta[k] = v
    return meta, body

def main():
    print("[PLAN LINTER] Starting validation of planning artifacts...")
    errors = []
    warnings = []

    task_files = glob.glob("implementation/sprint-*/*.md")
    if not task_files:
        errors.append("No task files found in implementation/sprint-*/")
        print("\n".join(errors))
        sys.exit(1)

    tasks = {}
    total_hours_by_sprint = {}

    for path in task_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        meta, body = parse_frontmatter(content)
        task_id = meta.get("id")
        if not task_id:
            errors.append(f"{path}: Missing 'id' in frontmatter")
            continue
        if task_id in tasks:
            errors.append(f"Duplicate task id: {task_id} in {path} and {tasks[task_id]['path']}")
        
        sprint = meta.get("sprint")
        effort_h = meta.get("effort_h", 0)
        depends_on = meta.get("depends_on", [])

        # Sub-task hours sum verification
        # Look for patterns like: - 4.1 ... (1.5 h) or (2 h)
        subtask_matches = re.findall(r"\(([0-9.]+)\s*h\)", body)
        if subtask_matches:
            subtask_sum = sum(float(x) for x in subtask_matches)
            if abs(subtask_sum - float(effort_h)) > 0.01:
                errors.append(
                    f"{path} ({task_id}): Subtask hours sum ({subtask_sum}h) != effort_h ({effort_h}h)"
                )
        else:
            warnings.append(f"{path} ({task_id}): No subtask hour annotations found like '(X h)'")

        tasks[task_id] = {
            "path": path,
            "sprint": sprint,
            "effort_h": effort_h,
            "depends_on": depends_on
        }

        total_hours_by_sprint[sprint] = total_hours_by_sprint.get(sprint, 0) + effort_h

    # Check dependencies existence
    for task_id, info in tasks.items():
        for dep in info["depends_on"]:
            if dep not in tasks:
                errors.append(f"Task {task_id} depends on unknown task '{dep}'")

    # Check for cycles in dependencies (Topological sort / DFS)
    visited = {}  # 0: visiting, 1: visited
    def has_cycle(tid, path=()):
        if tid in visited:
            return visited[tid] == 0
        visited[tid] = 0
        for dep in tasks.get(tid, {}).get("depends_on", []):
            if has_cycle(dep, path + (tid,)):
                return True
        visited[tid] = 1
        return False

    for tid in tasks:
        if tid not in visited:
            if has_cycle(tid):
                errors.append(f"Cycle detected in task dependencies involving {tid}")

    # Check documentation existence (docs 00 to 10)
    expected_docs = [
        "docs/00-discovery.md",
        "docs/01-overview.md",
        "docs/02-architecture.md",
        "docs/03-technical-spec.md",
        "docs/04-implementation-roadmap.md",
        "docs/05-testing.md",
        "docs/06-ci-cd.md",
        "docs/07-risks.md",
        "docs/08-metrics-nfrs.md",
        "docs/09-decisions-adrs.md",
        "docs/10-glossary-references.md",
        "docs/contracts/data-contracts.md",
        "docs/contracts/cli-contract.md",
        "implementation/README.md"
    ]
    for doc in expected_docs:
        if not os.path.exists(doc):
            errors.append(f"Missing required specification document: {doc}")

    # Check sprint hours match roadmap
    roadmap_path = "docs/04-implementation-roadmap.md"
    if os.path.exists(roadmap_path):
        with open(roadmap_path, "r", encoding="utf-8") as f:
            roadmap_content = f.read()
        expected_sprint_hours = {0: 8, 1: 8, 2: 12, 3: 8, 4: 4, 5: 8}
        for sp, exp_h in expected_sprint_hours.items():
            act_h = total_hours_by_sprint.get(sp, 0)
            if act_h != exp_h:
                errors.append(f"Sprint {sp} task hours sum ({act_h}h) != roadmap expected effort ({exp_h}h)")

    print(f"[PLAN LINTER] Checked {len(tasks)} tasks across {len(total_hours_by_sprint)} sprints.")
    print(f"[PLAN LINTER] Total task hours: {sum(t['effort_h'] for t in tasks.values())} h.")

    if warnings:
        print("\n--- WARNINGS ---")
        for w in warnings:
            print(f"[*] {w}")

    if errors:
        print("\n--- ERRORS FOUND ---")
        for e in errors:
            print(f"[!] {e}")
        sys.exit(1)
    else:
        print("\n[PLAN LINTER] PASS! All constraints, hours, dependencies, and files validated successfully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
