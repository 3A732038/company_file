#!/usr/bin/env python3
"""轉檔 worker(python-UNO)。獨立 process 執行,避免 uno 的 import hook 干擾 web 層。

用法:worker.py <input> <output.pdf> [soffice_port]

修正最常見的跑版:文字框因字型/行高差異往下長,撐破投影片下緣或疊到其他圖形;
作法是把這類「自動長高」的文字框(含群組內)改成「固定高度 + 縮小文字以符合」。
"""
import os
import sys
import time
import subprocess

import uno
from com.sun.star.beans import PropertyValue
from com.sun.star.drawing.TextFitToSizeType import AUTOFIT
from com.sun.star.awt import Size

SOFFICE_PORT = sys.argv[3] if len(sys.argv) > 3 else os.environ.get("SOFFICE_PORT", "2002")
MARGIN = int(os.environ.get("BOTTOM_MARGIN", "200"))   # 1/100 mm,底部安全邊距
_PROFILE = "file:///tmp/louser"


def _prop(name, value):
    p = PropertyValue()
    p.Name = name
    p.Value = value
    return p


def _resolve_desktop():
    ctx = uno.getComponentContext()
    resolver = ctx.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", ctx)
    remote = resolver.resolve(
        "uno:socket,host=localhost,port=%s;urp;StarOffice.ComponentContext" % SOFFICE_PORT)
    return remote.ServiceManager.createInstanceWithContext(
        "com.sun.star.frame.Desktop", remote)


def _listener_alive():
    try:
        _resolve_desktop()
        return True
    except Exception:
        return False


def _ensure_listener():
    if _listener_alive():
        return
    subprocess.Popen(
        ["soffice", "--headless", "--invisible", "--nodefault", "--norestore",
         "--nologo", "-env:UserInstallation=" + _PROFILE,
         "--accept=socket,host=localhost,port=%s;urp;" % SOFFICE_PORT],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        if _listener_alive():
            return
        time.sleep(1)
    raise RuntimeError("soffice listener failed to start")


def _fix_shape(shape, slide_h, counter):
    """遞迴處理單一圖形;群組則往內鑽。"""
    try:
        if shape.supportsService("com.sun.star.drawing.GroupShape"):
            for k in range(shape.Count):
                _fix_shape(shape.getByIndex(k), slide_h, counter)
            return
    except Exception:
        pass

    try:
        if not shape.supportsService("com.sun.star.drawing.Text"):
            return
        if not hasattr(shape, "TextFitToSize"):
            return
        if not getattr(shape, "TextAutoGrowHeight", False):
            return

        size = shape.Size
        pos = shape.Position
        new_h = size.Height
        limit = slide_h - MARGIN
        if pos.Y + size.Height > limit:          # 已超出投影片下緣 -> 夾回來
            new_h = max(500, limit - pos.Y)

        try:
            shape.TextAutoGrowHeight = False
        except Exception:
            pass
        shape.TextFitToSize = AUTOFIT             # 改為「縮小文字以符合」
        if new_h != size.Height:
            shape.Size = Size(size.Width, new_h)
        counter[0] += 1
    except Exception:
        pass


def convert(in_path, out_path):
    _ensure_listener()
    desktop = _resolve_desktop()
    doc = desktop.loadComponentFromURL(
        "file://" + in_path, "_blank", 0, (_prop("Hidden", True),))
    try:
        pages = doc.DrawPages
        slide_h = pages.getByIndex(0).Height
        counter = [0]
        for i in range(pages.Count):
            page = pages.getByIndex(i)
            for j in range(page.Count):
                _fix_shape(page.getByIndex(j), slide_h, counter)
        doc.storeToURL("file://" + out_path,
                       (_prop("FilterName", "impress_pdf_Export"),))
        return counter[0]
    finally:
        doc.close(False)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: worker.py <input> <output.pdf> [soffice_port]", file=sys.stderr)
        sys.exit(2)
    n = convert(sys.argv[1], sys.argv[2])
    print("fixed %d text boxes -> %s" % (n, sys.argv[2]))
