import pathlib
import re
import shutil
from tkinter.messagebox import showinfo, showerror
from tkinter.filedialog import askdirectory
import xml.etree.ElementTree as ET
import zipfile


def main():
    try:
        path = pathlib.Path(askdirectory(mustexist=True))
        out = path / "output"
        out.mkdir()
        vr = out / "$VROtherBooks"
        vr.mkdir()
        ar = out / "archivo"
        ar.mkdir()
        for z in path.glob("*.zip"):
            with zipfile.ZipFile(z) as lz:
                lz.extractall(out)
            title, author = parse(z)
            with zipfile.ZipFile(z) as lz:
                vrb = vr / to_filename(title)
                lz.extractall(vrb)
                vrbd = list(vrb.glob("*"))[0]
                for vrbf in vrb.glob("*/*"):
                    vrbf.rename(vrb / vrbf.name)
                vrbd.rmdir()
            with zipfile.ZipFile(z) as lz:
                au = ar / to_filename_preserve_comma(author)
                au.mkdir(exist_ok=True)
                shutil.copy(z, au / (to_filename(title) + ".zip"))
            print(title, author)
        showinfo("Finished")
    except Exception as e:
        showerror(str(e))
        raise e

def parse(path: pathlib.Path):
    with zipfile.ZipFile(path) as z:
        ncc_html = sorted([f for f in z.namelist() if f.endswith("ncc.html")])[0]
        ncc_html = z.read(ncc_html)
        xml = ET.fromstring(ncc_html)
        meta = {e.get("name"): e.get("content") for e in xml.find("{http://www.w3.org/1999/xhtml}head").findall("{http://www.w3.org/1999/xhtml}meta")}
        title = meta["dc:title"]
        author = meta["dc:creator"]
        return title, author


def to_filename(s):
    return re.sub(r"\W+", " ", s).strip()


def to_filename_preserve_comma(s):
    return re.sub(r"[^\w,]+", " ", s).strip()



if __name__ == "__main__":
    main()
