from ruamel.yaml import YAML
from collections.abc import Iterable
yaml = YAML(typ='safe')

def tex_recur(i, e="enumerate", tdepth=0):
    def tabitize(s, tdepth=0):
        return "".join(("\t"*tdepth, s,))# "\n"))

    if isinstance(i, str):
        return tabitize(f"\\item {i}", tdepth=tdepth)
    else:
        o = []
        o.append(tabitize(f"\\begin{{{e}}}", tdepth=tdepth))
        for item in i:
            o.append(tex_recur(item, e, tdepth=(tdepth+1)))
        o.append(tabitize(f"\\end{{{e}}}", tdepth=tdepth))
        return "\n".join(o)

def yml_to_tex(i):
    return data_to_tex(
        yaml.load(i)
    )

def data_to_tex(i, e="enumerate", depth=0):
    def sectioning(s, depth=0):
        return f"\\{'sub'*depth}section{{{k}}}"

    if isinstance(i, dict):
        o = []
        for k, v in i.items():
            o.append(sectioning(k, depth=depth))
            if isinstance(v, str):
                o.append(f"\t{v}")
            elif isinstance(v, dict):
                o.append(data_to_tex(v, e=e, depth=depth+1))
            elif isinstance(v, Iterable):
                o.append(tex_recur(v, e=e))
            else:
                o.append(f"\t{v}")
        return "\n".join(o)
    if isinstance(i, list):
        return tex_recur(i, e=e)
    else:
        return i

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('infiles', metavar='I', type=str, nargs='*',
                        help='yaml infiles to be converted to LaTeX'
                        )
    parser.add_argument("-o", "--stdout",  
                        help="print output to STDOUT", 
                        action="store_true")
    parser.add_argument("-i", "--itemize", 
                        help="put items in itemized list", 
                        action="store_true")
    ARGS = parser.parse_args()
    #change this if you want to add filter functionality
    assert ARGS.infiles, "you need to supply an input file!"

    if ARGS.itemize:
        e = "itemize"
    else:
        e = "enumerate"

    for infile in ARGS.infiles:
        i = yaml.load(open(infile).read())
        latex = data_to_tex(i, e=e)
        if ARGS.stdout:
            print(latex)
        else:
            outfile = ".".join(
                (
                infile.split(".")[0],
                "tex"
                )
            )
            open(outfile, "a").write(latex)
