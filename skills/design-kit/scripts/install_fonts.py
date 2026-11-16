#!/usr/bin/env python3
"""design-kit 폰트 설치 — 무료(OFL) 폰트를 받아 이 컴퓨터에 설치한다. 맥 · 윈도우 · 리눅스 공용.

  python3 install_fonts.py --check "Inter Tight" Pretendard        설치돼 있는지만 본다
  python3 install_fonts.py "Inter Tight" Pretendard --dry-run       무엇을 설치할지 보여 주기만
  python3 install_fonts.py "Inter Tight" Pretendard                 설치
  python3 install_fonts.py "Inter Tight" --weights 300,400,600       굵기 지정 (기본 400,500,600,700)
  python3 install_fonts.py "Inter Tight" --out ./fonts              설치하지 않고 폴더에 파일만 만든다
  python3 install_fonts.py "Inter Tight" --variable                 가변 폰트 파일 그대로 설치 (웹 · 디자인 툴용)

윈도우에서는 python3 대신 py -3 (또는 python).

- 폰트 출처: Google Fonts 공식 저장소(github.com/google/fonts) · Pretendard 는 npm 공식 배포본.
  전부 SIL Open Font License 등 무료 라이선스 폰트만 받는다. 상용 폰트는 받지 않는다.
- PowerPoint · Word 는 가변 폰트(한 파일에 모든 굵기)를 잘 못 다루고 파일에 포함도 못 한다.
  그래서 기본은 가변 폰트에서 굵기별 고정 파일(400 · 500 · 600 · 700 …)을 만들어 설치한다(fontTools 필요).
  이름은 맥 · 윈도우에서 똑같이 잡히게 맞춘다: 400 → "Inter Tight" Regular, 700 → "Inter Tight" Bold,
  그 밖 → "Inter Tight SemiBold" 같은 별도 이름(오피스 글꼴 목록에 그대로 보이는 이름).
- 설치 위치(관리자 권한 필요 없음): 맥 ~/Library/Fonts · 윈도우 %LOCALAPPDATA%\\Microsoft\\Windows\\Fonts(+ 사용자 레지스트리)
  · 리눅스 ~/.local/share/fonts. 이미 있는 폰트는 건너뛴다.
- 설치 뒤에는 PowerPoint · Word · 브라우저를 다시 시작해야 새 폰트가 보인다.
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.parse
import urllib.request
from pathlib import Path

sys.dont_write_bytecode = True
try:
    sys.stdout.reconfigure(errors="replace")
except Exception:  # noqa: BLE001
    pass

IS_WIN = os.name == "nt"
IS_MAC = sys.platform == "darwin"
GF_RAW = "https://raw.githubusercontent.com/google/fonts/main"
PRETENDARD = "https://registry.npmjs.org/pretendard/-/pretendard-1.3.9.tgz"
WEIGHT_NAMES = {100: "Thin", 200: "ExtraLight", 300: "Light", 400: "Regular", 500: "Medium",
                600: "SemiBold", 700: "Bold", 800: "ExtraBold", 900: "Black"}
DEFAULT_WEIGHTS = [400, 500, 600, 700]


def say(msg=""):
    print(msg, flush=True)


def die(msg, code=1):
    say("[멈춤] " + msg)
    sys.exit(code)


# ── 경로 ───────────────────────────────────────────────────
def cache_dir():
    base = Path(os.environ.get("LOCALAPPDATA", "")) if IS_WIN else Path.home() / ".cache"
    d = base / "design-kit" / "fonts"
    d.mkdir(parents=True, exist_ok=True)
    return d


def user_font_dir():
    if IS_MAC:
        return Path.home() / "Library" / "Fonts"
    if IS_WIN:
        return Path(os.environ["LOCALAPPDATA"]) / "Microsoft" / "Windows" / "Fonts"
    return Path.home() / ".local" / "share" / "fonts"


def all_font_dirs():
    dirs = [user_font_dir()]
    if IS_MAC:
        dirs += [Path("/Library/Fonts"), Path("/System/Library/Fonts")]
    elif IS_WIN:
        dirs += [Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"]
    else:
        dirs += [Path("/usr/share/fonts"), Path("/usr/local/share/fonts"), Path.home() / ".fonts"]
    return [d for d in dirs if d.is_dir()]


# ── 받기 ───────────────────────────────────────────────────
def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "design-kit-font-installer"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def cached(url, name):
    p = cache_dir() / name
    if not p.exists() or p.stat().st_size == 0:
        p.write_bytes(fetch(url))
    return p


def gf_dir(family):
    return re.sub(r"[^a-z0-9]", "", family.lower())


def gf_metadata(family):
    """Google Fonts 저장소에서 METADATA.pb 를 읽어 (라이선스 폴더, 글꼴 목록, 축 목록)."""
    d = gf_dir(family)
    for lic in ("ofl", "apache", "ufl"):
        try:
            text = fetch(f"{GF_RAW}/{lic}/{d}/METADATA.pb").decode("utf-8")
        except Exception:  # noqa: BLE001
            continue
        fonts = []
        for block in re.findall(r"fonts \{(.*?)\n\}", text, re.S):
            style = re.search(r'style: "(\w+)"', block)
            weight = re.search(r"weight: (\d+)", block)
            fname = re.search(r'filename: "([^"]+)"', block)
            if fname and (not style or style.group(1) == "normal"):
                fonts.append({"file": fname.group(1), "weight": int(weight.group(1)) if weight else 400})
        axes = {}
        for block in re.findall(r"axes \{(.*?)\}", text, re.S):
            tag = re.search(r'tag: "(\w+)"', block)
            lo = re.search(r"min_value: ([\d.]+)", block)
            hi = re.search(r"max_value: ([\d.]+)", block)
            if tag and lo and hi:
                axes[tag.group(1)] = (float(lo.group(1)), float(hi.group(1)))
        official = re.search(r'^name: "([^"]+)"', text, re.M)
        return lic, d, fonts, axes, (official.group(1) if official else family)
    return None


# ── 이름 맞추기 · 고정 굵기 만들기 ──────────────────────────────
def need_fonttools():
    try:
        import fontTools  # noqa: F401
        return True
    except ImportError:
        return False


def set_names(font, family, weight):
    """맥 · 윈도우 오피스에서 같은 이름으로 잡히게 이름표를 정리한다."""
    style = WEIGHT_NAMES.get(weight, str(weight))
    ribbi = weight in (400, 700)
    legacy_family = family if ribbi else f"{family} {style}"
    legacy_style = ("Bold" if weight == 700 else "Regular") if ribbi else "Regular"
    full = f"{family} {style}" if style != "Regular" else family
    ps = re.sub(r"[^A-Za-z0-9-]", "", f"{family.replace(' ', '')}-{style}")
    name = font["name"]
    for nid in (16, 17, 21, 22, 25):
        name.removeNames(nameID=nid)
    for nid, val in ((1, legacy_family), (2, legacy_style), (3, f"{ps};design-kit"), (4, full), (6, ps)):
        name.setName(val, nid, 3, 1, 0x409)
        name.setName(val, nid, 1, 0, 0)
    if not ribbi:
        for nid, val in ((16, family), (17, style)):
            name.setName(val, nid, 3, 1, 0x409)
            name.setName(val, nid, 1, 0, 0)
    if "OS/2" in font:
        os2 = font["OS/2"]
        os2.usWeightClass = weight
        sel = os2.fsSelection & ~0b1100001  # italic(0) · bold(5) · regular(6) 비트 정리
        sel |= (1 << 5) if weight == 700 else (1 << 6)
        os2.fsSelection = sel
    if "head" in font:
        font["head"].macStyle = 1 if weight == 700 else 0
    return f"{ps}.ttf", full


def make_static(var_path, family, weights, axes, out_dir):
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    made = []
    lo, hi = axes.get("wght", (400, 400))
    for w in weights:
        if not lo <= w <= hi:
            say(f"  - {family} {w}: 이 폰트의 굵기 범위({int(lo)}~{int(hi)}) 밖이라 건너뜀")
            continue
        vf = TTFont(str(var_path))
        limits = {tag: None for tag in axes}   # 다른 축은 기본값으로 고정
        limits["wght"] = w
        inst = instancer.instantiateVariableFont(vf, limits)
        fname, full = set_names(inst, family, w)
        dst = out_dir / fname
        inst.save(str(dst))
        made.append((dst, full))
    return made


# ── 폰트 하나 준비 ─────────────────────────────────────────
def prepare(family, weights, variable, out_dir):
    """설치할 파일들을 out_dir 에 만든다 → [(파일, 이름)]"""
    if family.lower().replace(" ", "") in ("pretendard", "pretendardvariable"):
        tgz = cached(PRETENDARD, "pretendard-1.3.9.tgz")
        made = []
        with tarfile.open(tgz) as t:
            for w in weights:
                style = WEIGHT_NAMES.get(w)
                member = f"package/dist/public/static/Pretendard-{style}.otf"
                try:
                    data = t.extractfile(member).read()
                except (KeyError, AttributeError):
                    say(f"  - Pretendard {w}: 배포본에 없어 건너뜀")
                    continue
                dst = out_dir / f"Pretendard-{style}.otf"
                dst.write_bytes(data)
                made.append((dst, f"Pretendard {style}" if style != "Regular" else "Pretendard"))
        return made

    meta = gf_metadata(family)
    if not meta:
        say(f"  - {family}: Google Fonts 에서 찾지 못했습니다(이름 철자 확인). 건너뜀")
        return []
    lic, d, fonts, axes, official = meta
    made = []
    var_files = [f for f in fonts if "[" in f["file"]]
    if var_files:
        f = var_files[0]
        src = cached(f"{GF_RAW}/{lic}/{d}/{urllib.parse.quote(f['file'])}", f["file"])
        if variable:
            dst = out_dir / f["file"]
            shutil.copyfile(src, dst)
            return [(dst, f"{official} (가변)")]
        if not need_fonttools():
            die("굵기별 파일을 만들려면 fontTools 가 필요합니다: python3 -m pip install --user fonttools "
                "(윈도우 py -3 -m pip install --user fonttools) · 또는 --variable 로 가변 폰트를 그대로 설치", 3)
        return make_static(src, official, weights, axes, out_dir)
    # 이미 굵기별 파일로 나뉘어 있는 폰트
    by_weight = {f["weight"]: f["file"] for f in fonts}
    wanted = weights if len(by_weight) > 1 else list(by_weight)   # 단일 굵기 폰트는 그것 하나
    for w in wanted:
        if w not in by_weight:
            say(f"  - {official} {w}: 제공되지 않는 굵기라 건너뜀")
            continue
        fname = by_weight[w]
        src = cached(f"{GF_RAW}/{lic}/{d}/{urllib.parse.quote(fname)}", fname)
        dst = out_dir / fname
        shutil.copyfile(src, dst)
        style = WEIGHT_NAMES.get(w, str(w))
        made.append((dst, official if style == "Regular" else f"{official} {style}"))
    return made


# ── 설치 여부 확인 ─────────────────────────────────────────
_installed = None


def installed_names():
    """설치된 글꼴의 이름들(소문자). fontTools 가 없으면 파일 이름으로 대신한다."""
    global _installed
    if _installed is not None:
        return _installed
    names = set()
    if not IS_WIN and not IS_MAC and shutil.which("fc-list"):
        r = subprocess.run(["fc-list", ":", "family", "fullname"], capture_output=True, text=True)
        for line in r.stdout.splitlines():
            for part in re.split(r"[,:]", line):
                if part.strip():
                    names.add(part.strip().lower())
    has_ft = need_fonttools()
    for d in all_font_dirs():
        for p in d.rglob("*"):
            if p.suffix.lower() not in (".ttf", ".otf", ".ttc"):
                continue
            names.add(re.sub(r"[-_]", " ", p.stem).lower())
            if not has_ft:
                continue
            try:
                from fontTools.ttLib import TTCollection, TTFont
                fonts = TTCollection(str(p), lazy=True).fonts if p.suffix.lower() == ".ttc" else [TTFont(str(p), lazy=True)]
                for f in fonts:
                    for nid in (1, 4, 16):
                        n = f["name"].getDebugName(nid)
                        if n:
                            names.add(n.lower())
            except Exception:  # noqa: BLE001
                pass
    _installed = names
    return names


def is_installed(family):
    key = family.lower()
    compact = key.replace(" ", "")
    return any(n == key or n.replace(" ", "") == compact or n.startswith(key + " ") for n in installed_names())


# ── 설치 ───────────────────────────────────────────────────
def install_file(path, full_name):
    dst_dir = user_font_dir()
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / path.name
    shutil.copyfile(path, dst)
    if IS_WIN:
        import winreg
        kind = "OpenType" if path.suffix.lower() == ".otf" else "TrueType"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows NT\CurrentVersion\Fonts",
                             0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, f"{full_name} ({kind})", 0, winreg.REG_SZ, str(dst))
        winreg.CloseKey(key)
        try:
            import ctypes
            ctypes.windll.gdi32.AddFontResourceW(str(dst))
        except Exception:  # noqa: BLE001
            pass
    return dst


def notify_font_change():
    if IS_WIN:
        try:
            import ctypes
            ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001D, 0, 0, 0x0002, 1000, None)
        except Exception:  # noqa: BLE001
            pass
    elif not IS_MAC and shutil.which("fc-cache"):
        subprocess.run(["fc-cache", "-f"], capture_output=True)


# ── 실행 ───────────────────────────────────────────────────
def main():
    argv = sys.argv[1:]

    def take(flag):
        if flag in argv:
            i = argv.index(flag)
            v = argv[i + 1] if i + 1 < len(argv) else None
            del argv[i:i + 2]
            return v
        return None

    weights_arg = take("--weights")
    out = take("--out")
    flags = {a for a in argv if a.startswith("--")}
    families = [a for a in argv if not a.startswith("--")]
    if not families:
        die('폰트 이름을 주세요. 예: python3 install_fonts.py "Inter Tight" Pretendard')
    weights = [int(x) for x in weights_arg.split(",")] if weights_arg else DEFAULT_WEIGHTS

    if "--check" in flags:
        result = {f: is_installed(f) for f in families}
        for f, ok in result.items():
            say(f"{'설치됨' if ok else '없음  '}  {f}")
        say(json.dumps(result, ensure_ascii=False))
        return

    todo = []
    for f in families:
        if not out and "--force" not in flags and is_installed(f):
            say(f"건너뜀: {f} (이미 설치돼 있음)")
        else:
            todo.append(f)
    if not todo:
        say("설치할 폰트가 없습니다.")
        return

    place = Path(out).expanduser() if out else user_font_dir()
    if "--dry-run" in flags:
        mode = "가변 폰트 그대로" if "--variable" in flags else f"굵기별 파일 {','.join(map(str, weights))}"
        say(f"설치 예정 ({mode}) → {place}")
        for f in todo:
            say(f"  - {f}")
        return

    work = Path(out).expanduser() if out else cache_dir() / "build"
    work.mkdir(parents=True, exist_ok=True)
    total = []
    for f in todo:
        say(f"{f} 준비 중…")
        made = prepare(f, weights, "--variable" in flags, work)
        for path, full in made:
            if out:
                say(f"  만듦: {path}  ({full})")
            else:
                dst = install_file(path, full)
                say(f"  설치: {dst.name}  ({full})")
        total += made
    if not out:
        notify_font_change()
        say(f"\n끝: {len(total)}개 파일 → {user_font_dir()}")
        say("PowerPoint · Word · 브라우저를 다시 시작해야 새 폰트가 보입니다.")
    else:
        say(f"\n끝: {len(total)}개 파일 → {work}  (설치는 하지 않았습니다)")


if __name__ == "__main__":
    main()
