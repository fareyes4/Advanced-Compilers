#Franz Reyes
import sys, json
from collections import deque
#terminators
TERMS = {"br","jmp","ret"}
#split instrs into basic blocks
def form_blocks(instrs):
    blocks, cur = [], []
    for ins in instrs:
        if "label" in ins:
            if cur: blocks.append(cur); cur=[]
            cur.append(ins)
        else:
            cur.append(ins)
        if ins.get("op") in TERMS:
            blocks.append(cur); cur=[]
    if cur: blocks.append(cur)
    return blocks
#block name
def block_name(b, i):
    for ins in b:
        if "label" in ins: return ins["label"]
    return f"_B{i}"
#block label
def label_ix(blocks):
    ix = {}
    for i,b in enumerate(blocks):
        for ins in b:
            if "label" in ins: ix[ins["label"]] = i
    return ix
#build cfg from JSON program
def build_cfg_from_json(prog):
    f = prog["functions"][0]
    blocks = form_blocks(f["instrs"])
    names = [block_name(b,i) for i,b in enumerate(blocks)]
    lab = label_ix(blocks)
    succ = {n: [] for n in names}
    for i,b in enumerate(blocks):
        last = b[-1]
        here = names[i]
        op = last.get("op")
        if op == "jmp":
            t = last["labels"][0]
            succ[here].append(names[lab[t]])
        elif op == "br":
            t,f_ = last["labels"]
            succ[here] += [names[lab[t]], names[lab[f_]]]
        elif i+1 < len(blocks):
            succ[here].append(names[i+1])
    for k in succ: succ[k] = sorted(succ[k])
    return names, succ, names[0]

def get_path_lengths(cfg, entry):
    dist = {entry: 0}
    q = deque([entry])
    while q:
        u = q.popleft()
        for v in cfg.get(u, []):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
def reverse_postorder(cfg, entry):
    seen, post = set(), []
    def dfs(u):
        seen.add(u)
        for v in sorted(cfg.get(u, [])):
            if v not in seen: dfs(v)
        post.append(u)
    dfs(entry)
    return list(reversed(post))
def find_back_edges(cfg, entry):
    WHITE, GRAY, BLACK = 0,1,2
    color = {n: WHITE for n in cfg}
    back = []
    def dfs(u):
        color[u] = GRAY
        for v in sorted(cfg.get(u, [])):
            if color[v] == WHITE:
                dfs(v)
            elif color[v] == GRAY: 
                back.append((u,v))
        color[u] = BLACK
    dfs(entry)
    return back
def is_reducible(cfg, entry):
    reach = set()
    dq = deque([entry])
    while dq:
        u = dq.popleft()
        if u in reach: continue
        reach.add(u)
        dq.extend(cfg.get(u, []))
    adj = {u: [v for v in cfg.get(u, []) if v in reach] for u in reach}
    idx, low, on, st = {}, {}, set(), []
    out = []
    i = 0
    def sc(u):
        nonlocal i
        idx[u]=low[u]=i; i+=1
        st.append(u); on.add(u)
        for v in adj.get(u, []):
            if v not in idx:
                sc(v); low[u]=min(low[u], low[v])
            elif v in on:
                low[u]=min(low[u], idx[v])
        if low[u]==idx[u]:
            comp=set()
            while True:
                w=st.pop(); on.discard(w); comp.add(w)
                if w==u: break
            out.append(comp)
    for u in sorted(reach):
        if u not in idx: sc(u)
    preds = {u: [] for u in reach}
    for u in reach:
        for v in adj.get(u, []):
            preds[v].append(u)
    for S in out:
        if len(S)==1:
            s = next(iter(S))
            if s not in adj.get(s, []):
                continue
        entries = set()
        for v in S:
            for p in preds[v]:
                if p not in S:
                    entries.add(v)
        if len(entries) > 1:
            return False
    return True

def main():
    prog = json.load(sys.stdin)
    names, cfg, entry = build_cfg_from_json(prog)
    args = set(sys.argv[1:])
    if "--paths" in args:
        d = get_path_lengths(cfg, entry)
        for n in sorted(d, key=lambda x: (d[x], x)):
            print(f"{n} {d[n]}")
        return
    if "--rpo" in args:
        for n in reverse_postorder(cfg, entry):
            print(n)
        return
    if "--back" in args:
        for u,v in sorted(find_back_edges(cfg, entry)):
            print(f"{u}->{v}")
        return
    if "--reducible" in args:
        print("reducible" if is_reducible(cfg, entry) else "irreducible")
        return
    for n in names:
        succ = cfg[n]
        print(f'{n} -> {", ".join(succ) if succ else "∅"}')

if __name__ == "__main__":
    main()
