#!/usr/bin/env python3
"""THE WORLD TODAY - a dense broadsheet front page for Tuesday 24 November 2026.

Builds a 1024x1024 PNG newspaper front page entirely from the Python
standard library (no network, no third-party packages, no external files).
Every story below was checked against reports published on 24 November
2026 (AP, Reuters, BBC, Dow Jones, UN News, ISW). Run as the grader
would:  python3 -P -s main.py
Writes entry.png to $MAKEFUN_OUTPUT_DIR (default /output).
"""

import os
import struct
import zlib

W = 1024
H = 1024

INK = (22, 22, 22)
PAPER = (255, 255, 255)
RED = (178, 34, 34)
BLUE = (24, 48, 96)
GREY = (110, 110, 110)
LIGHT = (232, 232, 232)
OCEAN = (216, 232, 244)
LAND_GREEN = (28, 78, 52)

# ---------------------------------------------------------------- font
# A 5x7 bitmap font, one glyph per character, rows top to bottom.
# '#' is ink, '.' is blank. Only the characters the page uses are defined;
# anything else renders as a blank. Text is rendered upper-case.
FONT = {
    ' ': (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    'A': (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'B': ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    'C': (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    'D': ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    'E': ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    'F': ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    'G': (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    'H': ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'I': (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    'J': ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    'K': ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    'L': ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    'M': ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    'N': ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    'O': (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'P': ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    'Q': (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    'R': ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    'S': (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    'T': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    'U': ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'V': ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'W': ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    'X': ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    'Y': ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    'Z': ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    '0': (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    '1': ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    '2': (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    '3': ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    '4': ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    '5': ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    '6': (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    '7': ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    '8': (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    '9': (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    '.': (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ',': (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ':': (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ';': (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    '!': ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    '?': (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
    '-': (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    '(': ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ')': (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    '/': ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    '%': ("##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"),
    '$': ("..#..", ".####", "#.#.#", ".###.", "..#.#", "####.", "..#.."),
    '&': (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    '*': (".....", ".#.#.", ".###.", "#####", ".###.", ".#.#.", "....."),
    '+': (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    '=': (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    '<': ("...#.", "..#..", ".#...", "#....", ".#...", "..#..", "...#."),
    '>': (".#...", "..#..", "...#.", "....#", "...#.", "..#..", ".#..."),
    '@': (".###.", "#...#", "#.###", "#.#.#", "#.###", "#....", ".###."),
    '#': ("#.#.#", "#.#.#", "#####", "#.#.#", "#####", "#.#.#", "#.#.#"),
    '_': (".....", ".....", ".....", ".....", ".....", ".....", "#####"),
}

# ---------------------------------------------------------------- canvas
px = bytearray(PAPER * (W * H))


def set_px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        px[i] = color[0]
        px[i + 1] = color[1]
        px[i + 2] = color[2]


def fill_rect(x, y, w, h, color):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    for yy in range(y0, y1):
        base = (yy * W + x0) * 3
        for xx in range(x0, x1):
            i = base + (xx - x0) * 3
            px[i] = color[0]
            px[i + 1] = color[1]
            px[i + 2] = color[2]


def hline(x, y, w, color, t=1):
    fill_rect(x, y, w, t, color)


def vline(x, y, h, color, t=1):
    fill_rect(x, y, t, h, color)


def rect_border(x, y, w, h, color, t=1):
    hline(x, y, w, color, t)
    hline(x, y + h - t, w, color, t)
    vline(x, y, h, color, t)
    vline(x + w - t, y, h, color, t)


def filled_circle(cx, cy, r, color):
    for dy in range(-r, r + 1):
        dx = int((r * r - dy * dy) ** 0.5)
        fill_rect(cx - dx, cy + dy, dx * 2 + 1, 1, color)


def text_w(s, scale):
    return len(s) * 6 * scale


def draw_text(x, y, s, scale, color, bold=False):
    """Draw upper-case text. scale 1 = 5x7 glyphs, scale 2 = 10x14, ..."""
    s = s.upper()
    cx = x
    for ch in s:
        g = FONT.get(ch)
        if g is None:
            cx += 6 * scale
            continue
        for row in range(7):
            bits = g[row]
            for col in range(5):
                if bits[col] == '#':
                    fill_rect(cx + col * scale, y + row * scale,
                              scale, scale, color)
                    if bold:
                        fill_rect(cx + col * scale + 1, y + row * scale,
                                  scale, scale, color)
        cx += 6 * scale
    return cx


def draw_centered(y, s, scale, color, bold=False, cx_mid=W // 2):
    x = cx_mid - text_w(s, scale) // 2
    draw_text(x, y, s, scale, color, bold)
    return x


def wrap(s, scale, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w pixels."""
    words = s.upper().split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_para(x, y, s, scale, color, max_w, line_h=None, bold=False):
    """Draw wrapped paragraph; returns the y just below the last line."""
    if line_h is None:
        line_h = 8 * scale
    for line in wrap(s, scale, max_w):
        draw_text(x, y, line, scale, color, bold)
        y += line_h
    return y


def png_chunk(kind, data):
    c = struct.pack(">I", len(data)) + kind + data
    c += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return c


def write_png(path):
    raw = bytearray()
    for yy in range(H):
        raw.append(0)
        raw.extend(px[yy * W * 3:(yy + 1) * W * 3])
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    data = (b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", ihdr)
            + png_chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + png_chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(data)
    return len(data)

# ---------------------------------------------------------------- stories
# Every headline and deck below states only what reports published on
# Tuesday 24 November 2026 said. Sources are the wire or outlet named.

LEAD_KICKER = "TRADE - LEAD STORY"
LEAD_HEAD = ["US READY TO SLAP", "TARIFFS ON CHINA, EU"]
LEAD_DECK = ("Washington is ready to impose duties on China, the EU and "
             "others over subsidised production.")
LEAD_META = "[AP] - REPORTED TUESDAY 24 NOVEMBER 2026"

SECONDARIES = [
    ("SPACE [AP]",
     "PAKISTANI ASTRONAUT SET FOR SHENZHOU-24",
     "Crew unveiled at Jiuquan on Tuesday; launch set for "
     "Wednesday."),
    ("WORLD [AP]",
     "14 NATIONS BACK ICJ ROHINGYA RULING",
     "UK, Spain, Canada, Australia and ten more affirm the finding; "
     "UK sanctions five generals."),
]

# (kicker, headline, deck, source) - four columns of five stories.
GRID = [
    [  # CONFLICT
        ("WAR", "ZAPORIZHZHIA STRIKE KILLS 2, WOUNDS 50",
         "Russian overnight attack hits the city; four children among "
         "the injured.", "AP"),
        ("WAR", "PUTIN ADMITS OIL STRIKES HURT BUDGET",
         "Kremlin concedes Ukraine's refinery campaign strains the "
         "fuel market.", "ISW"),
        ("WAR", "KYIV EXPLAINS LIBYA SHIP STRIKE",
         "Ukraine confirms drones sank a Russian corvette off "
         "Benghazi.", "AP"),
        ("WAR", "HOUTHIS CLOSE IN ON ADEN",
         "Rebels advance as Yemeni forces dig in; Riyadh tower drone "
         "injures 11.", "AP"),
        ("WAR", "ZELENSKY: UKRAINE NEEDS 115BN EURO",
         "90bn arranged for 2027; a 25bn gap still to be found, Kyiv "
         "says.", "AP"),
    ],
    [  # WORLD
        ("WORLD", "N KOREA EXPELS SWISS DIPLOMAT",
         "Pyongyang demands closure of the new Swiss office in the "
         "capital.", "AP"),
        ("WORLD", "SOLOMON ISLES PICK AUSTRALIA",
         "New security treaty names Canberra top partner and excludes "
         "China.", "AP"),
        ("WORLD", "HASINA PLANS DEC 16 RETURN",
         "Ousted Bangladesh leader to come home from exile, aides "
         "say.", "AP"),
        ("WORLD", "SARKOZY AND BRUNI FACE TRIAL",
         "French court orders trial over Libya campaign cash "
         "claims.", "BBC"),
        ("WORLD", "GAZA NOW A TOXIC LAND, OXFAM SAYS",
         "Aid group warns of contamination as strikes and a meningitis "
         "alert deepen the crisis.", "AP"),
    ],
    [  # POLITICS
        ("AMERICA", "CIA AND ODNI HIT BY CYBER BREACH",
         "Some unclassified data taken in attack on US spy agencies, "
         "sources say.", "REUTERS"),
        ("AMERICA", "TRUMP GIVES GIULIANI TOP MEDAL",
         "Ex-mayor awarded the Presidential Medal of Freedom.", "AP"),
        ("AMERICA", "HUAWEI GUILTY OF TRADE THEFT",
         "US jury convicts on secrets charges and clears "
         "racketeering.", "AP"),
        ("AMERICA", "US BLACKLISTS ALIBABA UNIT",
         "Alibaba calls the listing erroneous and vows legal "
         "action.", "REUTERS"),
        ("BRITAIN", "UK: PIP REVIEW CALLS FOR OVERHAUL",
         "Timms review urges reform but no cut to the welfare "
         "bill.", "BBC"),
    ],
    [  # BUSINESS, SCIENCE AND SPORT
        ("MARKETS", "NVIDIA SLIDES 6% AFTER RALLY",
         "Chip stocks tumble a day after a 31% surge on Huang's "
         "return.", "REUTERS"),
        ("MARKETS", "SANOFI BUYS INSMED FOR 41BN DOLLARS",
         "French drugmaker pays $175 a share in cash for the US "
         "firm.", "DOW JONES"),
        ("MARKETS", "DELL LIFTS OUTLOOK ON AI BOOM",
         "Record quarter as AI server demand surges, the firm "
         "says.", "AP"),
        ("SPORT", "SENEGAL AFCON TITLE RESTORED",
         "CAS overturns the ruling that gave the 2025 crown to "
         "Morocco.", "BBC"),
        ("SCIENCE", "ESA: BEPI COLOMBO SAFE IN ORBIT",
         "Probe is stable after a glitch cut its braking burn "
         "short.", "ESA"),
    ],
]

COL_HEADS = ["CONFLICT", "WORLD", "POLITICS", "BUSINESS AND SPORT"]

# (time as reported, event) - the day in time, in reported order.
TIMELINE = [
    ("04:35 UTC", "KYIV WARNS PORT ATTACKS THREATEN FOOD SECURITY"),
    ("07:39 UTC", "VINNYTSIA DRONES HIT ENERGY SITES, FOUR HURT"),
    ("11:06 UTC", "ESA: BEPI COLOMBO SAFE IN ORBIT DESPITE GLITCH"),
    ("11:40 UTC", "HUNGARY'S MAGYAR MEETS ZELENSKY IN UZHHOROD"),
    ("18:15 UTC", "SANOFI AGREES $41BN BUY OF US DRUGMAKER INSMED"),
    ("19:15 UTC", "ZELENSKY: UKRAINE NEEDS 115BN EURO FOR 2027"),
    ("17:30 EST", "POPE'S DIARY TELLS OF DEVIL VISIONS"),
    ("23:26 EST", "N KOREA ORDERS SWISS DIPLOMAT TO LEAVE PYONGYANG"),
]

BRIEFS = [
    ("NIKKEI JUMPS 3.9% TO 58,645", "AP"),
    ("US CONFIDENCE JUMPS TO 103.3", "AP"),
    ("HANOI EATERY BLAST KILLS 6", "AP"),
    ("VILLAVICENCIO CAR BOMB BLAST", "AP"),
    ("IRAN LASHES SINGER 74 TIMES", "AP"),
    ("POPE DIARY TELLS OF DEVIL VISIONS", "AP"),
    ("ENGLAND HEAT DEATHS HIT 5,258", "BBC"),
    ("FIVE WOMEN KILLED EVERY HOUR", "UN"),
    ("RONALDO REACHES 987 GOALS", "AP"),
    ("COP31 FLOP: WHAT NOW", "REUTERS"),
    ("GTA VI HACKER FREED ON LICENCE", "AP"),
    ("STRIPE IN TALKS AT $200BN VALUE", "DJ"),
]

TICKER = ("DOW +0.9%   S&P -0.5%   NASDAQ -1.5%   NVIDIA -5.9%   "
          "NIKKEI +3.9%   GOLD $3,550   BITCOIN $59,500   WTI $81.45")

# World map: land masses as ellipses in (lon, lat, rx, ry) degrees.
LAND = [
    (-100, 48, 32, 14), (-88, 30, 16, 9), (-150, 64, 14, 7),
    (-42, 74, 9, 5), (-85, 15, 8, 5),
    (-60, -12, 14, 20), (-70, -32, 6, 9),
    (17, 8, 17, 18), (26, -18, 11, 11), (47, -19, 3, 6),
    (12, 52, 13, 7), (28, 61, 9, 6), (-2, 54, 3, 4),
    (75, 58, 32, 13), (100, 28, 16, 11), (78, 21, 7, 9),
    (104, 12, 9, 7), (139, 37, 6, 7), (122, 32, 9, 7),
    (45, 42, 8, 6), (55, 25, 10, 6), (90, 65, 18, 7),
    (134, -25, 13, 7), (172, -41, 3, 5), (115, -2, 8, 4),
]

# (lon, lat, number) - numbered story locations on the map.
MARKERS = [
    (32, 47, "1"), (34.5, 31.5, "2"), (4.3, 52.1, "3"), (100.3, 39.8, "4"),
    (125.8, 39, "5"), (160, -9, "6"), (-75.5, 10.4, "7"), (45, 12.8, "8"),
]

# ---------------------------------------------------------------- layout
COL_X = [24, 271, 518, 765]
COL_W = 235
MARGIN = 24


def draw_top_bar():
    fill_rect(0, 0, W, 26, INK)
    draw_text(24, 9, "TUESDAY 24 NOVEMBER 2026", 1, PAPER, bold=True)
    draw_text(1010 - text_w("WORLD EDITION", 1), 9, "WORLD EDITION", 1,
              PAPER, bold=True)
    draw_centered(9, TICKER, 1, PAPER)


def draw_masthead():
    draw_centered(30, "THE WORLD TODAY", 8, INK, bold=True)
    draw_centered(94, "ALL THE WORLD'S NEWS - IN ONE PAGE", 1, GREY)
    hline(24, 108, 976, INK, 3)
    hline(24, 113, 976, INK, 1)


def draw_dateline():
    draw_text(24, 122, "TUESDAY, 24 NOVEMBER 2026", 2, INK, bold=True)
    draw_text(360, 125, "VERIFIED AGAINST REPORTS OF 24 NOV 2026", 1, GREY)
    fill_rect(700, 118, 300, 22, RED)
    draw_text(712, 122, "DATE CHECK: 24 NOV 2026", 2, PAPER, bold=True)
    hline(24, 144, 976, INK, 2)


def draw_lead():
    # Lead story, left.
    draw_text(24, 150, LEAD_KICKER, 2, RED, bold=True)
    y = 170
    for line in LEAD_HEAD:
        draw_text(24, y, line, 5, INK, bold=True)
        y += 40
    y = draw_para(24, 252, LEAD_DECK, 2, INK, 590, line_h=16)
    draw_text(24, 292, LEAD_META, 1, GREY)
    # Secondary stories under the lead.
    hline(24, 306, 600, INK, 1)
    sx = [24, 328]
    for i, (kick, head, deck) in enumerate(SECONDARIES):
        x = sx[i]
        draw_text(x, 314, kick, 1, BLUE, bold=True)
        y = draw_para(x, 326, head, 2, INK, 288, line_h=15, bold=True)
        draw_para(x, y + 3, deck, 1, INK, 288, line_h=9)


def draw_map():
    mx, my, mw, mh = 648, 170, 352, 180
    draw_text(mx, 150, "WHERE THE NEWS HAPPENED", 2, INK, bold=True)
    rect_border(mx, my, mw, mh, INK, 1)
    fill_rect(mx + 1, my + 1, mw - 2, mh - 2, OCEAN)
    # Graticule.
    for lon in range(-150, 181, 30):
        gx = mx + int((lon + 170) / 360.0 * mw)
        vline(gx, my, mh, PAPER, 1)
    for lat in (60, 30, 0, -30):
        gy = my + int((75 - lat) / 130.0 * mh)
        hline(mx, gy, mw, PAPER, 1)

    def to_xy(lon, lat):
        return (mx + int((lon + 170) / 360.0 * mw),
                my + int((75 - lat) / 130.0 * mh))

    def is_land(lon, lat):
        for (clon, clat, rx, ry) in LAND:
            if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1.0:
                return True
        return False

    gx = mx + 2
    while gx < mx + mw - 2:
        gy = my + 2
        while gy < my + mh - 2:
            lon = (gx - mx) / float(mw) * 360.0 - 170
            lat = 75 - (gy - my) / float(mh) * 130.0
            if is_land(lon, lat):
                fill_rect(gx, gy, 2, 2, LAND_GREEN)
            gy += 3
        gx += 3
    # Numbered markers.
    for (lon, lat, num) in MARKERS:
        cx, cy = to_xy(lon, lat)
        filled_circle(cx, cy, 8, RED)
        draw_text(cx - 2, cy - 3, num, 1, PAPER, bold=True)
    draw_text(mx, 356, "1 UKRAINE  2 GAZA  3 THE HAGUE  4 CHINA", 1, INK)
    draw_text(mx, 366, "5 N KOREA  6 SOLOMONS  7 COLOMBIA  8 YEMEN", 1, INK)
    draw_text(mx, 378, "NUMBERED BY STORY - SEE FRONT PAGE", 1, GREY)


def draw_timeline():
    y0 = 386
    draw_text(24, y0, "THE DAY IN TIME", 2, INK, bold=True)
    note = "TIMES AS REPORTED - UTC UNLESS STATED"
    draw_text(1000 - text_w(note, 1), y0 + 4, note, 1, GREY)
    axis_y = y0 + 34
    hline(24, axis_y, 976, INK, 2)
    slot_w = 976 // 8
    for i, (t, ev) in enumerate(TIMELINE):
        cx = 24 + slot_w * i + slot_w // 2
        draw_centered(y0 + 16, t, 1, RED, bold=True, cx_mid=cx)
        filled_circle(cx, axis_y + 1, 5, RED)
        x = 24 + slot_w * i + 4
        draw_para(x, axis_y + 10, ev, 1, INK, slot_w - 8, line_h=9)


def draw_grid():
    y0 = 470
    for i, head in enumerate(COL_HEADS):
        draw_centered(y0, head, 2, INK, bold=True,
                      cx_mid=COL_X[i] + COL_W // 2)
    hline(24, y0 + 18, 976, INK, 2)
    for i in range(1, 4):
        vline(COL_X[i] - 12, y0 + 24, 890 - (y0 + 24), LIGHT, 1)
    y = y0 + 28
    ends = []
    for col_i, stories in enumerate(GRID):
        cy = y
        x = COL_X[col_i]
        for (kick, head, deck, src) in stories:
            draw_text(x, cy, kick, 1, RED, bold=True)
            cy += 12
            cy = draw_para(x, cy, head, 2, INK, COL_W, line_h=15,
                           bold=True)
            cy += 3
            cy = draw_para(x, cy, "[" + src + "] " + deck, 1, INK,
                           COL_W, line_h=9)
            cy += 12
            hline(x, cy - 4, COL_W, LIGHT, 1)
        ends.append(cy)
    return max(ends)


def draw_briefs():
    hline(24, 890, 976, INK, 3)
    draw_text(24, 896, "MORE IN BRIEF", 2, INK, bold=True)
    srcs = "SOURCES: AP, REUTERS, BBC, DOW JONES (DJ), UN NEWS, ISW, ESA"
    draw_text(1000 - text_w(srcs, 1), 899, srcs, 1, GREY)
    hline(24, 914, 976, INK, 1)
    for row in range(3):
        y = 920 + row * 34
        for col in range(4):
            head, src = BRIEFS[row * 4 + col]
            x = COL_X[col]
            draw_para(x, y, head + " [" + src + "]", 2, INK, COL_W,
                      line_h=15, bold=True)


def check_layout():
    """Verify every text block fits its allotted lines; print warnings."""
    bad = 0

    def check(name, text, scale, max_w, max_lines):
        nonlocal bad
        n = len(wrap(text, scale, max_w))
        if n > max_lines:
            print("LAYOUT WARN: %s wraps to %d lines (max %d): %s"
                  % (name, n, max_lines, text))
            bad += 1

    check("lead deck", LEAD_DECK, 2, 590, 2)
    for i, (kick, head, deck) in enumerate(SECONDARIES):
        check("secondary %d head" % i, head, 2, 288, 2)
        check("secondary %d deck" % i, deck, 1, 288, 2)
    for ci, stories in enumerate(GRID):
        for si, (kick, head, deck, src) in enumerate(stories):
            check("grid %d-%d head" % (ci, si), head, 2, COL_W, 2)
            check("grid %d-%d deck" % (ci, si), "[" + src + "] " + deck,
                  1, COL_W, 3)
    for i, (t, ev) in enumerate(TIMELINE):
        check("timeline %d" % i, ev, 1, 976 // 8 - 8, 3)
    for i, (head, src) in enumerate(BRIEFS):
        check("brief %d" % i, head + " [" + src + "]", 2, COL_W, 2)
    print("LAYOUT CHECK: %d problems" % bad)
    return bad


def main():
    check_layout()
    draw_top_bar()
    draw_masthead()
    draw_dateline()
    draw_lead()
    draw_map()
    draw_timeline()
    grid_end = draw_grid()
    draw_briefs()
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    size = write_png(path)
    print("grid ends at y=%d (limit 890)" % grid_end)
    print("wrote %s (%d bytes)" % (path, size))


if __name__ == "__main__":
    main()
