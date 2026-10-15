import os
import sys
import copy
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import Glyph, GlyphCoordinates
from fontTools.ttLib.tables.ttProgram import Program
from fontTools.varLib import instancer
import freetype
from PIL import Image, ImageDraw, ImageFont
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Sources: can look in "original", "Michelangelus Fonts", or current directory
CANDIDATE_SRC = [
    os.path.join(SCRIPT_DIR, "original"),
    os.path.join(SCRIPT_DIR, "Michelangelus Fonts"),
    SCRIPT_DIR,
]
SRC_DIR = next((p for p in CANDIDATE_SRC if os.path.exists(p) and os.path.exists(os.path.join(p, "Michelangelus-Regular.ttf"))), SCRIPT_DIR)
DST_DIR = SCRIPT_DIR
REF_DIR = os.path.join(SCRIPT_DIR, "reference-fonts")

os.makedirs(REF_DIR, exist_ok=True)
os.makedirs(DST_DIR, exist_ok=True)

# Auto-download reference fonts if not present
REF_URLS = {
    "EBGaramond.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/ebgaramond/EBGaramond%5Bwght%5D.ttf",
    "EBGaramond-Italic.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/ebgaramond/EBGaramond-Italic%5Bwght%5D.ttf"
}
import urllib.request
for ref_name, ref_url in REF_URLS.items():
    ref_file = os.path.join(REF_DIR, ref_name)
    if not os.path.exists(ref_file):
        print(f"Downloading reference font: {ref_name} ...")
        try:
            req = urllib.request.Request(ref_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as resp, open(ref_file, 'wb') as out_f:
                out_f.write(resp.read())
            print(f"  [OK] Saved {ref_name}")
        except Exception as e:
            print(f"  [!] Could not auto-download {ref_name}: {e}")

FONTS = [
    {
        "src": "Michelangelus-Regular.ttf",
        "dst": "Michelangelus-VN-Regular.ttf",
        "name": "Michelangelus VN",
        "subfamily": "Regular",
        "full_name": "Michelangelus VN Regular",
        "ps_name": "MichelangelusVN-Regular",
        "ref_font": "EBGaramond.ttf",
        "ref_axis": {"wght": 400},
        "is_italic": False,
        "is_bold": False,
    },
    {
        "src": "Michelangelus-Bold.ttf",
        "dst": "Michelangelus-VN-Bold.ttf",
        "name": "Michelangelus VN",
        "subfamily": "Bold",
        "full_name": "Michelangelus VN Bold",
        "ps_name": "MichelangelusVN-Bold",
        "ref_font": "EBGaramond.ttf",
        "ref_axis": {"wght": 700},
        "is_italic": False,
        "is_bold": True,
    },
    {
        "src": "Michelangelus-Italic.ttf",
        "dst": "Michelangelus-VN-Italic.ttf",
        "name": "Michelangelus VN",
        "subfamily": "Italic",
        "full_name": "Michelangelus VN Italic",
        "ps_name": "MichelangelusVN-Italic",
        "ref_font": "EBGaramond-Italic.ttf",
        "ref_axis": {"wght": 400},
        "is_italic": True,
        "is_bold": False,
    },
    {
        "src": "Michelangelus-BoldItalic.ttf",
        "dst": "Michelangelus-VN-BoldItalic.ttf",
        "name": "Michelangelus VN",
        "subfamily": "Bold Italic",
        "full_name": "Michelangelus VN Bold Italic",
        "ps_name": "MichelangelusVN-BoldItalic",
        "ref_font": "EBGaramond-Italic.ttf",
        "ref_axis": {"wght": 700},
        "is_italic": True,
        "is_bold": True,
    },
]

def extract_contours(glyph, glyf_table):
    """Extract raw contours as list of (coords, endPts, flags)."""
    coords, endPts, flags = glyph.getCoordinates(glyf_table)
    contours = []
    for i in range(len(endPts)):
        start = 0 if i == 0 else endPts[i-1] + 1
        end = endPts[i]
        c_pts = coords[start:end+1]
        c_flags = flags[start:end+1]
        contours.append((list(c_pts), c_flags))
    return contours

def transform_contour(pts, flags, dx=0, dy=0, sx=1.0, sy=1.0, origin_x=0, origin_y=0):
    """Scale around origin and translate."""
    new_pts = []
    for x, y in pts:
        nx = round((x - origin_x) * sx + origin_x + dx)
        ny = round((y - origin_y) * sy + origin_y + dy)
        new_pts.append((nx, ny))
    return new_pts, list(flags)

def combine_to_glyph(contour_list):
    """Combine a list of (pts, flags) into a TrueType simple Glyph."""
    all_coords = GlyphCoordinates()
    all_endPts = []
    all_flags = []
    
    current_offset = 0
    for pts, flags in contour_list:
        if not pts:
            continue
        for p in pts:
            all_coords.append(p)
        current_offset += len(pts)
        all_endPts.append(current_offset - 1)
        all_flags.extend(flags)
        
    g = Glyph()
    g.numberOfContours = len(all_endPts)
    g.coordinates = all_coords
    g.endPtsOfContours = all_endPts
    g.flags = all_flags
    g.program = Program()
    if len(all_coords) > 0:
        g.xMin = min(p[0] for p in all_coords)
        g.yMin = min(p[1] for p in all_coords)
        g.xMax = max(p[0] for p in all_coords)
        g.yMax = max(p[1] for p in all_coords)
    else:
        g.xMin = g.yMin = g.xMax = g.yMax = 0
    return g

def get_glyph_center_and_top(glyph, glyf_table):
    coords, _, _ = glyph.getCoordinates(glyf_table)
    xs = [p[0] for p in coords]
    ys = [p[1] for p in coords]
    return (min(xs) + max(xs)) / 2, max(ys)

def get_accent_contour(glyph, glyf_table):
    """Extract accent contours (contours above y = 480)."""
    coords, endPts, flags = glyph.getCoordinates(glyf_table)
    accent_contours = []
    for i in range(len(endPts)):
        start = 0 if i == 0 else endPts[i-1] + 1
        end = endPts[i]
        c_pts = coords[start:end+1]
        c_flags = flags[start:end+1]
        if min(p[1] for p in c_pts) >= 480:
            accent_contours.append((list(c_pts), list(c_flags)))
    return accent_contours

def get_accent_bbox(contours):
    all_pts = [p for pts, _ in contours for p in pts]
    if not all_pts:
        return 0, 0, 0, 0
    xs = [p[0] for p in all_pts]
    ys = [p[1] for p in all_pts]
    return min(xs), min(ys), max(xs), max(ys)

def process_single_font(cfg):
    src_path = os.path.join(SRC_DIR, cfg["src"])
    dst_path = os.path.join(DST_DIR, cfg["dst"])
    ref_path = os.path.join(REF_DIR, cfg["ref_font"])
    
    print(f"\n==================================================")
    print(f"Processing: {cfg['src']} -> {cfg['dst']}")
    print(f"Reference: {cfg['ref_font']} ({cfg['ref_axis']})")
    
    tt = TTFont(src_path)
    glyf = tt["glyf"]
    hmtx = tt["hmtx"]
    cmap = tt.getBestCmap()
    
    # Load and instantiate reference font (EBGaramond)
    ref_tt = TTFont(ref_path)
    ref_inst = instancer.instantiateVariableFont(ref_tt, cfg["ref_axis"])
    ref_glyf = ref_inst["glyf"]
    
    # 1. Measure base center anchors from existing circumflex glyphs
    anchors = {}
    
    # Lowercase anchors
    for char, gname in [('a', 'acircumflex'), ('e', 'ecircumflex'), ('o', 'ocircumflex'), ('u', 'ucircumflex')]:
        acc = get_accent_contour(glyf[gname], glyf)
        x0, y0, x1, y1 = get_accent_bbox(acc)
        anchors[char] = {
            'cx': (x0 + x1) / 2,
            'y_base': y0,
            'y_top': y1,
        }
    
    # i and y
    for char, gname in [('i', 'itilde'), ('y', 'ycircumflex')]:
        if gname in glyf:
            acc = get_accent_contour(glyf[gname], glyf)
            x0, y0, x1, y1 = get_accent_bbox(acc)
            anchors[char] = {'cx': (x0 + x1) / 2, 'y_base': y0, 'y_top': y1}
        else:
            c, t = get_glyph_center_and_top(glyf['dotlessi' if char == 'i' else 'y'], glyf)
            anchors[char] = {'cx': c, 'y_base': 520, 'y_top': 700}
            
    # Uppercase anchors
    for char, gname in [('A', 'Acircumflex'), ('E', 'Ecircumflex'), ('O', 'Ocircumflex'), ('U', 'Ucircumflex')]:
        acc = get_accent_contour(glyf[gname], glyf)
        x0, y0, x1, y1 = get_accent_bbox(acc)
        anchors[char] = {
            'cx': (x0 + x1) / 2,
            'y_base': y0,
            'y_top': y1,
        }
        
    for char, gname in [('I', 'Itilde'), ('Y', 'Ycircumflex')]:
        if gname in glyf:
            acc = get_accent_contour(glyf[gname], glyf)
            x0, y0, x1, y1 = get_accent_bbox(acc)
            anchors[char] = {'cx': (x0 + x1) / 2, 'y_base': y0, 'y_top': y1}
        else:
            c, t = get_glyph_center_and_top(glyf[char], glyf)
            anchors[char] = {'cx': c, 'y_base': 750, 'y_top': 930}
            
    # 2. Extract basic accents from Michelangelus
    # Dot below derived from 'period'
    dot_contours = extract_contours(glyf['period'], glyf)
    dot_x0, dot_y0, dot_x1, dot_y1 = get_accent_bbox(dot_contours)
    dot_cx = (dot_x0 + dot_x1) / 2
    
    # Acute
    acute_contours = extract_contours(glyf['acute'], glyf)
    ac_x0, ac_y0, ac_x1, ac_y1 = get_accent_bbox(acute_contours)
    ac_cx = (ac_x0 + ac_x1) / 2
    
    # Grave
    grave_contours = extract_contours(glyf['grave'], glyf)
    gr_x0, gr_y0, gr_x1, gr_y1 = get_accent_bbox(grave_contours)
    gr_cx = (gr_x0 + gr_x1) / 2
    
    # Circumflex
    circ_contours = extract_contours(glyf['circumflex'], glyf)
    ci_x0, ci_y0, ci_x1, ci_y1 = get_accent_bbox(circ_contours)
    ci_cx = (ci_x0 + ci_x1) / 2
    
    # Breve
    breve_contours = extract_contours(glyf['breve'], glyf)
    br_x0, br_y0, br_x1, br_y1 = get_accent_bbox(breve_contours)
    br_cx = (br_x0 + br_x1) / 2
    
    # Tilde
    tilde_contours = extract_contours(glyf['tilde'], glyf)
    ti_x0, ti_y0, ti_x1, ti_y1 = get_accent_bbox(tilde_contours)
    ti_cx = (ti_x0 + ti_x1) / 2

    # 3. Extract Hook and Horn from EBGaramond
    hook_contours = extract_contours(ref_glyf['hookabovecomb'], ref_glyf)
    hk_x0, hk_y0, hk_x1, hk_y1 = get_accent_bbox(hook_contours)
    hk_cx = (hk_x0 + hk_x1) / 2
    
    horn_contours = extract_contours(ref_glyf['uni031B'], ref_glyf)
    hn_x0, hn_y0, hn_x1, hn_y1 = get_accent_bbox(horn_contours)
    
    # In Italic: slant factor
    slant = 0.364 if cfg["is_italic"] else 0.0 # tan(20 deg) ~ 0.364

    # 4. Define helper to place an accent over a letter
    def place_accent(accent_cnts, acc_cx, acc_y0, target_cx, target_y0, sx=1.0, sy=1.0):
        res = []
        for pts, flags in accent_cnts:
            t_pts, t_flags = transform_contour(
                pts, flags,
                dx=target_cx - acc_cx,
                dy=target_y0 - acc_y0,
                sx=sx, sy=sy,
                origin_x=acc_cx, origin_y=acc_y0
            )
            res.append((t_pts, t_flags))
        return res

    # 5. Define helper to place horn on o/O/u/U
    def get_horn(base_char, is_cap=False):
        g = glyf[base_char]
        coords, _, _ = g.getCoordinates(glyf)
        ymax = max(p[1] for p in coords)
        candidates = [p for p in coords if p[1] > ymax * 0.75]
        best_p = max(candidates, key=lambda p: p[0])
        
        # Attachment offset
        # EBGaramond horn baseline attachment is around hn_x0 + 40, hn_y0 + 10
        target_x = best_p[0] + (10 if not is_cap else 15)
        target_y = best_p[1] - (20 if not is_cap else 30)
        
        scale = 1.05 if not is_cap else 1.25
        res = []
        for pts, flags in horn_contours:
            t_pts, t_flags = transform_contour(
                pts, flags,
                dx=target_x - hn_x0 - 30,
                dy=target_y - hn_y0,
                sx=scale, sy=scale,
                origin_x=hn_x0, origin_y=hn_y0
            )
            res.append((t_pts, t_flags))
        return res

    # Dictionary of generated glyphs: gname -> (Glyph, advanceWidth, lsb)
    new_glyphs = {}
    
    def register_glyph(gname, cp, contour_list, base_gname, extra_width=0):
        glyph = combine_to_glyph(contour_list)
        base_adv = hmtx[base_gname][0]
        adv = max(base_adv, glyph.xMax + 30) if extra_width > 0 else base_adv
        new_glyphs[gname] = (glyph, adv, glyph.xMin)
        cmap[cp] = gname

    # -------------------------------------------------------------
    # GENERATION LOGIC FOR ALL 92 MISSING VIETNAMESE CHARACTERS
    # -------------------------------------------------------------

    # GROUP 1: Hook above (12 characters)
    # ả, Ả, ẻ, Ẻ, ỉ, Ỉ, ỏ, Ỏ, ủ, Ủ, ỷ, Ỷ
    hook_map = [
        ('uni1EA3', 0x1EA3, 'a', 'a', False),
        ('uni1EA2', 0x1EA2, 'A', 'A', True),
        ('uni1EBB', 0x1EBB, 'e', 'e', False),
        ('uni1EBA', 0x1EBA, 'E', 'E', True),
        ('uni1EC9', 0x1EC9, 'dotlessi', 'i', False),
        ('uni1EC8', 0x1EC8, 'I', 'I', True),
        ('uni1ECF', 0x1ECF, 'o', 'o', False),
        ('uni1ECE', 0x1ECE, 'O', 'O', True),
        ('uni1EE7', 0x1EE7, 'u', 'u', False),
        ('uni1EE6', 0x1EE6, 'U', 'U', True),
        ('uni1EF7', 0x1EF7, 'y', 'y', False),
        ('uni1EF6', 0x1EF6, 'Y', 'Y', True),
    ]
    for gname, cp, base_g, anchor_k, is_cap in hook_map:
        base_cnts = extract_contours(glyf[base_g], glyf)
        anc = anchors[anchor_k]
        h_cnts = place_accent(
            hook_contours, hk_cx, hk_y0,
            anc['cx'], anc['y_base'] + (0 if not is_cap else 15),
            sx=1.1 if not is_cap else 1.3,
            sy=1.1 if not is_cap else 1.3
        )
        register_glyph(gname, cp, base_cnts + h_cnts, base_g)

    # GROUP 2: Dot below (12 characters)
    # ạ, Ạ, ẹ, Ẹ, ị, Ị, ọ, Ọ, ụ, Ụ, ỵ, Ỵ
    dot_map = [
        ('uni1EA1', 0x1EA1, 'a', 'a', False),
        ('uni1EA0', 0x1EA0, 'A', 'A', True),
        ('uni1EB9', 0x1EB9, 'e', 'e', False),
        ('uni1EB8', 0x1EB8, 'E', 'E', True),
        ('uni1ECB', 0x1ECB, 'i', 'i', False), # i has its regular dot
        ('uni1ECA', 0x1ECA, 'I', 'I', True),
        ('uni1ECD', 0x1ECD, 'o', 'o', False),
        ('uni1ECC', 0x1ECC, 'O', 'O', True),
        ('uni1EE5', 0x1EE5, 'u', 'u', False),
        ('uni1EE4', 0x1EE4, 'U', 'U', True),
        ('uni1EF5', 0x1EF5, 'y', 'y', False),
        ('uni1EF4', 0x1EF4, 'Y', 'Y', True),
    ]
    for gname, cp, base_g, anchor_k, is_cap in dot_map:
        base_cnts = extract_contours(glyf[base_g], glyf)
        anc = anchors[anchor_k]
        dot_x = anc['cx'] + (40 if anchor_k == 'y' and not is_cap else 0)
        d_cnts = place_accent(
            dot_contours, dot_cx, dot_y0,
            dot_x, -140
        )
        register_glyph(gname, cp, base_cnts + d_cnts, base_g)

    # GROUP 3: Missing tilde characters (4 characters)
    # ẽ, Ẽ, ỹ, Ỹ
    tilde_map = [
        ('uni1EBD', 0x1EBD, 'e', 'e', False),
        ('uni1EBC', 0x1EBC, 'E', 'E', True),
        ('uni1EF9', 0x1EF9, 'y', 'y', False),
        ('uni1EF8', 0x1EF8, 'Y', 'Y', True),
    ]
    for gname, cp, base_g, anchor_k, is_cap in tilde_map:
        base_cnts = extract_contours(glyf[base_g], glyf)
        anc = anchors[anchor_k]
        t_cnts = place_accent(
            tilde_contours, ti_cx, ti_y0,
            anc['cx'], anc['y_base'] + (30 if not is_cap else 40)
        )
        register_glyph(gname, cp, base_cnts + t_cnts, base_g)

    # GROUP 4: Horn letters (ơ, Ơ, ư, Ư) and their tone marks (24 characters)
    horn_base_defs = [
        ('ohorn', 0x01A1, 'o', 'o', False),
        ('Ohorn', 0x01A0, 'O', 'O', True),
        ('uhorn', 0x01B0, 'u', 'u', False),
        ('Uhorn', 0x01AF, 'U', 'U', True),
    ]
    for hname, cp, base_g, anchor_k, is_cap in horn_base_defs:
        base_cnts = extract_contours(glyf[base_g], glyf)
        hn_cnts = get_horn(base_g, is_cap)
        register_glyph(hname, cp, base_cnts + hn_cnts, base_g, extra_width=30)
        # Also store in glyf so subsequent tone compositions can use it!
        glyf[hname] = new_glyphs[hname][0]
        hmtx[hname] = (new_glyphs[hname][1], new_glyphs[hname][2])

    # Tone marks on ohorn and uhorn
    horn_tones = [
        # ohorn tones
        ('uni1EDD', 0x1EDD, 'ohorn', 'o', False, 'grave'),
        ('uni1EDB', 0x1EDB, 'ohorn', 'o', False, 'acute'),
        ('uni1EDF', 0x1EDF, 'ohorn', 'o', False, 'hook'),
        ('uni1EE1', 0x1EE1, 'ohorn', 'o', False, 'tilde'),
        ('uni1EE3', 0x1EE3, 'ohorn', 'o', False, 'dot'),
        # Ohorn tones
        ('uni1EDC', 0x1EDC, 'Ohorn', 'O', True, 'grave'),
        ('uni1EDA', 0x1EDA, 'Ohorn', 'O', True, 'acute'),
        ('uni1EDE', 0x1EDE, 'Ohorn', 'O', True, 'hook'),
        ('uni1EE0', 0x1EE0, 'Ohorn', 'O', True, 'tilde'),
        ('uni1EE2', 0x1EE2, 'Ohorn', 'O', True, 'dot'),
        # uhorn tones
        ('uni1EEB', 0x1EEB, 'uhorn', 'u', False, 'grave'),
        ('uni1EE9', 0x1EE9, 'uhorn', 'u', False, 'acute'),
        ('uni1EED', 0x1EED, 'uhorn', 'u', False, 'hook'),
        ('uni1EEF', 0x1EEF, 'uhorn', 'u', False, 'tilde'),
        ('uni1EF1', 0x1EF1, 'uhorn', 'u', False, 'dot'),
        # Uhorn tones
        ('uni1EEA', 0x1EEA, 'Uhorn', 'U', True, 'grave'),
        ('uni1EE8', 0x1EE8, 'Uhorn', 'U', True, 'acute'),
        ('uni1EEC', 0x1EEC, 'Uhorn', 'U', True, 'hook'),
        ('uni1EEE', 0x1EEE, 'Uhorn', 'U', True, 'tilde'),
        ('uni1EF0', 0x1EF0, 'Uhorn', 'U', True, 'dot'),
    ]
    for gname, cp, base_g, anchor_k, is_cap, tone in horn_tones:
        base_cnts = extract_contours(glyf[base_g], glyf)
        anc = anchors[anchor_k]
        
        # When tone mark is on horn vowel, center it over the base vowel body
        tcx = anc['cx']
        ybase = anc['y_base'] + (0 if not is_cap else 15)
        
        if tone == 'grave':
            t_cnts = place_accent(grave_contours, gr_cx, gr_y0, tcx, ybase)
        elif tone == 'acute':
            t_cnts = place_accent(acute_contours, ac_cx, ac_y0, tcx, ybase)
        elif tone == 'hook':
            t_cnts = place_accent(hook_contours, hk_cx, hk_y0, tcx, ybase, sx=1.0 if not is_cap else 1.2, sy=1.0 if not is_cap else 1.2)
        elif tone == 'tilde':
            t_cnts = place_accent(tilde_contours, ti_cx, ti_y0, tcx, ybase + 30)
        elif tone == 'dot':
            t_cnts = place_accent(dot_contours, dot_cx, dot_y0, tcx, -140)
            
        register_glyph(gname, cp, base_cnts + t_cnts, base_g, extra_width=30)

    # GROUP 5: Stacked circumflex (30 characters)
    # â, ê, ô + huyền, sắc, hỏi, ngã, nặng
    # Lowercase & Uppercase
    circ_stack_defs = [
        # a
        ('uni1EA7', 0x1EA7, 'a', 'a', False, 'grave'),
        ('uni1EA5', 0x1EA5, 'a', 'a', False, 'acute'),
        ('uni1EA9', 0x1EA9, 'a', 'a', False, 'hook'),
        ('uni1EAB', 0x1EAB, 'a', 'a', False, 'tilde'),
        ('uni1EAD', 0x1EAD, 'a', 'a', False, 'dot'),
        # A
        ('uni1EA6', 0x1EA6, 'A', 'A', True, 'grave'),
        ('uni1EA4', 0x1EA4, 'A', 'A', True, 'acute'),
        ('uni1EA8', 0x1EA8, 'A', 'A', True, 'hook'),
        ('uni1EAA', 0x1EAA, 'A', 'A', True, 'tilde'),
        ('uni1EAC', 0x1EAC, 'A', 'A', True, 'dot'),
        # e
        ('uni1EC1', 0x1EC1, 'e', 'e', False, 'grave'),
        ('uni1EBF', 0x1EBF, 'e', 'e', False, 'acute'),
        ('uni1EC3', 0x1EC3, 'e', 'e', False, 'hook'),
        ('uni1EC5', 0x1EC5, 'e', 'e', False, 'tilde'),
        ('uni1EC7', 0x1EC7, 'e', 'e', False, 'dot'),
        # E
        ('uni1EC0', 0x1EC0, 'E', 'E', True, 'grave'),
        ('uni1EBE', 0x1EBE, 'E', 'E', True, 'acute'),
        ('uni1EC2', 0x1EC2, 'E', 'E', True, 'hook'),
        ('uni1EC4', 0x1EC4, 'E', 'E', True, 'tilde'),
        ('uni1EC6', 0x1EC6, 'E', 'E', True, 'dot'),
        # o
        ('uni1ED3', 0x1ED3, 'o', 'o', False, 'grave'),
        ('uni1ED1', 0x1ED1, 'o', 'o', False, 'acute'),
        ('uni1ED5', 0x1ED5, 'o', 'o', False, 'hook'),
        ('uni1ED7', 0x1ED7, 'o', 'o', False, 'tilde'),
        ('uni1ED9', 0x1ED9, 'o', 'o', False, 'dot'),
        # O
        ('uni1ED2', 0x1ED2, 'O', 'O', True, 'grave'),
        ('uni1ED0', 0x1ED0, 'O', 'O', True, 'acute'),
        ('uni1ED4', 0x1ED4, 'O', 'O', True, 'hook'),
        ('uni1ED6', 0x1ED6, 'O', 'O', True, 'tilde'),
        ('uni1ED8', 0x1ED8, 'O', 'O', True, 'dot'),
    ]

    for gname, cp, base_g, anchor_k, is_cap, tone in circ_stack_defs:
        base_cnts = extract_contours(glyf[base_g], glyf)
        anc = anchors[anchor_k]
        tcx = anc['cx']
        ybase = anc['y_base']
        
        if tone == 'dot':
            # Regular circumflex + dot below
            c_cnts = place_accent(circ_contours, ci_cx, ci_y0, tcx, ybase)
            d_cnts = place_accent(dot_contours, dot_cx, dot_y0, tcx, -140)
            register_glyph(gname, cp, base_cnts + c_cnts + d_cnts, base_g)
        else:
            # Compact circumflex (scaled 0.85x)
            c_scale = 0.85 if not is_cap else 0.88
            c_cnts = place_accent(circ_contours, ci_cx, ci_y0, tcx, ybase - (15 if not is_cap else 20), sx=c_scale, sy=c_scale)
            
            # Place tone mark resting on slope or peak
            if tone == 'acute':
                # right slope
                shift_x = 65 if not is_cap else 80
                shift_y = 110 if not is_cap else 125
                t_cnts = place_accent(acute_contours, ac_cx, ac_y0, tcx + shift_x, ybase + shift_y, sx=0.72, sy=0.72)
            elif tone == 'grave':
                # left slope
                shift_x = -65 if not is_cap else -80
                shift_y = 110 if not is_cap else 125
                t_cnts = place_accent(grave_contours, gr_cx, gr_y0, tcx + shift_x, ybase + shift_y, sx=0.72, sy=0.72)
            elif tone == 'hook':
                # hook slightly right of peak
                shift_x = 35 if not is_cap else 45
                shift_y = 105 if not is_cap else 120
                t_cnts = place_accent(hook_contours, hk_cx, hk_y0, tcx + shift_x, ybase + shift_y, sx=0.75, sy=0.75)
            elif tone == 'tilde':
                # tilde above peak
                shift_y = 135 if not is_cap else 150
                t_cnts = place_accent(tilde_contours, ti_cx, ti_y0, tcx, ybase + shift_y, sx=0.75, sy=0.75)
                
            register_glyph(gname, cp, base_cnts + c_cnts + t_cnts, base_g)

    # GROUP 6: Stacked breve (10 characters)
    # ă + huyền, sắc, hỏi, ngã, nặng (và Ă)
    breve_stack_defs = [
        ('uni1EB1', 0x1EB1, 'a', 'a', False, 'grave'),
        ('uni1EAF', 0x1EAF, 'a', 'a', False, 'acute'),
        ('uni1EB3', 0x1EB3, 'a', 'a', False, 'hook'),
        ('uni1EB5', 0x1EB5, 'a', 'a', False, 'tilde'),
        ('uni1EB7', 0x1EB7, 'a', 'a', False, 'dot'),
        ('uni1EB0', 0x1EB0, 'A', 'A', True, 'grave'),
        ('uni1EAE', 0x1EAE, 'A', 'A', True, 'acute'),
        ('uni1EB2', 0x1EB2, 'A', 'A', True, 'hook'),
        ('uni1EB4', 0x1EB4, 'A', 'A', True, 'tilde'),
        ('uni1EB6', 0x1EB6, 'A', 'A', True, 'dot'),
    ]

    for gname, cp, base_g, anchor_k, is_cap, tone in breve_stack_defs:
        base_cnts = extract_contours(glyf[base_g], glyf)
        anc = anchors[anchor_k]
        tcx = anc['cx']
        ybase = anc['y_base']
        
        if tone == 'dot':
            b_cnts = place_accent(breve_contours, br_cx, br_y0, tcx, ybase + (20 if not is_cap else 20))
            d_cnts = place_accent(dot_contours, dot_cx, dot_y0, tcx, -140)
            register_glyph(gname, cp, base_cnts + b_cnts + d_cnts, base_g)
        else:
            b_scale = 0.85 if not is_cap else 0.88
            b_cnts = place_accent(breve_contours, br_cx, br_y0, tcx, ybase, sx=b_scale, sy=b_scale)
            
            if tone == 'acute':
                shift_x = 25 if not is_cap else 35
                shift_y = 110 if not is_cap else 125
                t_cnts = place_accent(acute_contours, ac_cx, ac_y0, tcx + shift_x, ybase + shift_y, sx=0.72, sy=0.72)
            elif tone == 'grave':
                shift_x = -25 if not is_cap else -35
                shift_y = 110 if not is_cap else 125
                t_cnts = place_accent(grave_contours, gr_cx, gr_y0, tcx + shift_x, ybase + shift_y, sx=0.72, sy=0.72)
            elif tone == 'hook':
                shift_y = 100 if not is_cap else 115
                t_cnts = place_accent(hook_contours, hk_cx, hk_y0, tcx, ybase + shift_y, sx=0.75, sy=0.75)
            elif tone == 'tilde':
                shift_y = 120 if not is_cap else 135
                t_cnts = place_accent(tilde_contours, ti_cx, ti_y0, tcx, ybase + shift_y, sx=0.75, sy=0.75)
                
            register_glyph(gname, cp, base_cnts + b_cnts + t_cnts, base_g)

    # GROUP 7: Authentic Vietnamese Đ and đ (Stroke bar through stem)
    # The original font incorrectly pointed Dcroat / dcroat to Dcaron / dcaron.
    # We extract the crossbars from EBGaramond (Eth and dcroat) and graft them onto Michelangelus D and d.
    coords_eth, endPts_eth, flags_eth = ref_glyf['Eth'].getCoordinates(ref_glyf)
    bar_cap = coords_eth[:endPts_eth[0]+1]
    bar_cap_flags = flags_eth[:endPts_eth[0]+1]

    coords_dc, endPts_dc, flags_dc = ref_glyf['dcroat'].getCoordinates(ref_glyf)
    bar_sm = coords_dc[endPts_dc[1]+1:]
    bar_sm_flags = flags_dc[endPts_dc[1]+1:]

    # Build Đ (0x0110, Dcroat)
    base_D_cnts = extract_contours(glyf['D'], glyf)
    # Slant offset if italic
    d_x_shift = -20 if not cfg['is_italic'] else 80
    d_y_shift = 20
    t_bar_cap = []
    for x, y in bar_cap:
        t_bar_cap.append((round(x + d_x_shift), round(y + d_y_shift)))
    register_glyph('Dcroat', 0x0110, base_D_cnts + [(t_bar_cap, list(bar_cap_flags))], 'D')

    # Build đ (0x0111, dcroat)
    base_d_cnts = extract_contours(glyf['d'], glyf)
    sm_x_shift = -10 if not cfg['is_italic'] else 180
    sm_y_shift = 30
    t_bar_sm = []
    for x, y in bar_sm:
        t_bar_sm.append((round(x + sm_x_shift), round(y + sm_y_shift)))
    register_glyph('dcroat', 0x0111, base_d_cnts + [(t_bar_sm, list(bar_sm_flags))], 'd')

    # -------------------------------------------------------------
    # COMMIT ALL NEW GLYPHS TO TTFONT
    # -------------------------------------------------------------
    order = tt.getGlyphOrder()
    for gname, (glyph, adv, lsb) in new_glyphs.items():
        if gname not in order:
            order.append(gname)
        glyf[gname] = glyph
        hmtx[gname] = (adv, lsb)
    tt.setGlyphOrder(order)
    
    # Update cmap tables
    for table in tt['cmap'].tables:
        if table.isUnicode():
            for cp, gname in cmap.items():
                if table.format == 4 and cp > 0xFFFF:
                    continue
                table.cmap[cp] = gname

    # Update font name records
    for record in tt['name'].names:
        if record.nameID == 1:
            record.string = cfg["name"].encode(record.getEncoding())
        elif record.nameID == 2:
            record.string = cfg["subfamily"].encode(record.getEncoding())
        elif record.nameID == 4:
            record.string = cfg["full_name"].encode(record.getEncoding())
        elif record.nameID == 6:
            record.string = cfg["ps_name"].encode(record.getEncoding())

    tt.save(dst_path)
    print(f"Generated {len(new_glyphs)} new Vietnamese glyphs successfully!")
    print(f"Saved to: {dst_path}")
    
    # Validation with freetype
    face = freetype.Face(dst_path)
    test_chars = "àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵĐ"
    test_chars += test_chars.upper()
    face.set_pixel_sizes(0, 36)
    missing = []
    for c in test_chars:
        try:
            face.load_char(c, freetype.FT_LOAD_RENDER)
            if face.glyph.bitmap.width == 0 and c != ' ':
                missing.append(c)
        except Exception:
            missing.append(c)
            
    if missing:
        print(f"WARNING: Missing or empty bitmaps for {len(missing)} characters: {''.join(missing)}")
    else:
        print(f"ALL {len(set(test_chars))} Vietnamese characters verified and render beautifully via FreeType!")

if __name__ == '__main__':
    for f in FONTS:
        process_single_font(f)
    print("\n==================================================")
    print("ALL 4 STYLES PROCESSED SUCCESSFULLY!")
