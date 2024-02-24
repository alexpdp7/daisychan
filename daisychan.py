import pathlib
from tkinter.filedialog import askdirectory
import xml.etree.ElementTree as ET
import zipfile


def main():
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
            lz.extractall(vr / title)
        with zipfile.ZipFile(z) as lz:
            au = ar / author
            au.mkdir(exist_ok=True)
            lz.extractall(au / title)
        print(title, author)


def parse(path: pathlib.Path):
    with zipfile.ZipFile(path) as z:
        ncc_html = sorted([f for f in z.namelist() if f.endswith("ncc.html")])[0]
        ncc_html = z.read(ncc_html)
        xml = ET.fromstring(ncc_html)
        meta = {e.get("name"): e.get("content") for e in xml.find("{http://www.w3.org/1999/xhtml}head").findall("{http://www.w3.org/1999/xhtml}meta")}
        title = meta["dc:title"]
        author = meta["dc:creator"]
        return title, author



if __name__ == "__main__":
    main()
