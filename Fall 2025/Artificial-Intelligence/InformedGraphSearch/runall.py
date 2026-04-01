import subprocess

searchers = ["AStarGraphSearcher", "BiAStarGraphSearcher", "UCGraphSearcher"]

problems = [108, 14, 1234, 333, 55555, 1176, 15210, 4444]

for problem in problems:
    for searcher in searchers:
        problem_path = f"problems/graph-{problem}.txt"
        print(f"\n***   Running {searcher} on {problem_path}   ***")
        subprocess.run(
            ["python3", "main-nogui.py", problem_path, searcher]
        )
