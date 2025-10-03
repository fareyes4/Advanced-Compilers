#Franz Reyes
import sys, json
from form_blocks import form_blocks
import cfg
from df import Analysis, df_worklist, fmt

def expr_key(i):
    if "dest" in i and i.get("args"):
        return (i["op"], tuple(i["args"]))
    return None

def build_ae_analysis(blocks):
    name_of = {id(b): n for n, b in blocks.items()}
    U = set()
    for b in blocks.values():
        for i in b:
            k = expr_key(i)
            if k:
                U.add(k)
    dvars = {n: {i["dest"] for i in b if "dest" in i} for n, b in blocks.items()}
    def make_gen(b):
        later = set()
        g = set()
        for i in reversed(b):
            k = expr_key(i)
            if k and not any(a in later for a in i.get("args", [])):
                g.add(k)
            if "dest" in i:
                later.add(i["dest"])
        return g
    GEN = {n: make_gen(b) for n, b in blocks.items()}
    def make_kill(n):
        k = set()
        D = dvars[n]
        if D:
            for (op, args) in U:
                if any(a in D for a in args):
                    k.add((op, args))
        return k
    KILL = {n: make_kill(n) for n in blocks}
    def meet(vals):
        vals = list(vals)
        if not vals:
            return set()
        out = set(U)
        for s in vals:
            out &= s
        return out
    def transfer(block, IN):
        n = name_of[id(block)]
        return GEN[n] | (IN - KILL[n])
    return Analysis(True, init=set(U), merge=meet, transfer=transfer)

def main():
    prog = json.load(sys.stdin)
    for f in prog["functions"]:
        blocks = cfg.block_map(form_blocks(f["instrs"]))
        cfg.add_terminators(blocks)
        ana = build_ae_analysis(blocks)
        IN, OUT = df_worklist(blocks, ana)
        for n in blocks:
            def show(S):
                if not S:
                    return "∅"
                return ", ".join(f"{op}({', '.join(args)})" for op, args in sorted(S))
            print(f"{n}:")
            print("  in:  ", show(IN[n]))
            print("  out: ", show(OUT[n]))
if __name__ == "__main__":
    main()
