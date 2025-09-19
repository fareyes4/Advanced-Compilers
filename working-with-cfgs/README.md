Franz Reyes
Working with CFGs assignment. I reused my intro CFG code and added four features: shortest paths, reverse postorder, back edges, and reducibility. Everything uses Bril JSON.
The code reads a Bril JSON program from stdin, splits it into basic blocks, builds the CFG, it uses labels start blocks; br/jmp/ret end blocks, fallthrough goes to the next block, then prints edges by default or runs the feature.
How to run on a single file
python3 src/cfg.py < tests/edges/branch.json
python3 src/cfg.py --paths < tests/paths/branch.json
python3 src/cfg.py --rpo < tests/rpo/loop.json
python3 src/cfg.py --back < tests/back/loop.json
python3 src/cfg.py --reducible < tests/reducible/irreducible.json
Tests
turnt tests/edges/*.json
turnt tests/paths/*.json
turnt tests/rpo/*.json
turnt tests/back/*.json
turnt tests/reducible/*.json
I used ChatGPT as a source to help fix some test errors and to come up with simple test cases.
