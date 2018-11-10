from IPython.lib.pretty import pretty as _pretty
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic, line_cell_magic
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.getipython import get_ipython
from itertools import zip_longest

sh = InteractiveShell.instance()

def pretty(obj):
        import numpy as np
        if isinstance(obj, np.ndarray):
            return np.array2string(obj, separator=", ")
        else:
            return _pretty(obj)

@magics_class
class BrMagics(Magics): 
    """从内嵌类Magics, 定义自己的类iceBrMagics"""
    
    @line_magic("C")
    def _C(self,line):
        """格式化打印多个数组,数组之间用分号隔开,两个分号表示           换行,%C a;b;;c """
        global results
        from itertools import zip_longest
        pos = line.find(" ")
        
        try:
            gap = int(line[:pos])
            line = line[pos+1:]
        except ValueError:
            gap = 2
        
        for idx, sec in enumerate(line.split(";;")):
            if idx > 0:
                print
            codes = [x.strip() for x in sec.split(";")]
            results = [[code] for code in codes]

            for i, code in enumerate(codes):
                results[i].extend(pretty(sh.ev(code)).split("\n"))

            results = [list(row) for row in zip(*list(zip_longest(*results, fillvalue="")))]
            #print(results)

            for i, col in enumerate(results):
                width = max(len(row) for row in col)
                col.insert(1, "-"*width)
                col[0] = col[0].center(width)
                col[2:] = [row.ljust(width) for row in col[2:]]

            for row in zip(*results):  #将result解开
                print((" "*gap).join(row))
                
get_ipython().register_magics(BrMagics)