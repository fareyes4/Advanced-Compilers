#Franz Reyes
import sys, json
from form_blocks import form_blocks
import cfg
from df import Analysis, df_worklist, union, fmt

def build_rd_analysis(blocks):
    name_of = {id(b): n for n, b in blocks.items()}
    defs = {}
    for n, block in blocks.items():
        for i, instr in enumerate(block):
            d = instr.get("dest")
            if d is not None:
                defs.setdefault(d, set()).add(f"{n}:{i}")
    def transfer(block, in_set):
        bname = name_of[id(block)]
        last = {}
        for i, instr in enumerate(block):
            d = instr.get("dest")
            if d is not None:
                last[d] = f"{bname}:{i}"
        gen = set(last.values())
        kill = set()
        for v, myd in last.items():
            kill |= (defs.get(v, set()) - {myd})
        return gen | (in_set - kill)
    return Analysis(
        forward=True,
        init=set(),
        merge=union,
        transfer=transfer,
    )
def main():
    prog = json.load(sys.stdin)
    for f in prog["functions"]:
        blocks = cfg.block_map(form_blocks(f["instrs"]))
        cfg.add_terminators(blocks)
        ana = build_rd_analysis(blocks)
        inn, out = df_worklist(blocks, ana)
        for n in blocks:
            print(f"{n}:")
            print("  in: ", fmt(inn[n]))
            print("  out:", fmt(out[n]))
if __name__ == "__main__":
    main()

