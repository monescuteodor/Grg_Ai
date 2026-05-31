import os
import re
import sys
import warnings
import logging
import multiprocessing

warnings.filterwarnings("ignore")
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

class SuppressStderr:
    def __enter__(self):
        self.err_null = open(os.devnull, 'w')
        self.old_stderr = sys.stderr
        sys.stderr = self.err_null

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stderr = self.old_stderr
        self.err_null.close()

try:
    import llama_cpp
except ImportError:
    print("Error: llama_cpp library not found.")
    print("Install: pip install llama-cpp-python")
    sys.exit(1)

try:
    import chromadb
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Error: Required libraries not found.")
    print("Install: pip install chromadb sentence-transformers")
    sys.exit(1)

BANNER = r"""

                _______
     ----------/       \----------
     \        /         \        /
      \_______\_________/_______/

  ____  ____    ____       _     ___ 
 / ___||  _ \  / ___|     / \   |_ _|
| |  _ | |_) || |  _     / _ \   | | 
| |_| ||  _ < | |_| |   / ___ \  | | 
 \____||_| \_\ \____|  /_/   \_\|___|
        
Hello, I am Grg Ai!
What are you waiting for? Ask anything.
"""


KNOWLEDGE_DIR   = "Knowledge"
INDEX_DIR       = ".grg_index"
EMBED_MODEL     = "all-MiniLM-L6-v2"   # HuggingFace name — used only on first download
EMBED_MODEL_DIR = "./embed-model"       # local folder — loaded from here after first run
MODEL_PATH      = "./grg-model.gguf"
TOP_K         = 5       # more chunks = more knowledge context
MAX_CHUNK     = 500     # larger chunks = more complete snippets
MIN_CHUNK     = 50
DISTANCE_THRESHOLD = 1.0

_HOME       = os.path.expanduser("~")
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def _build_paths_map() -> dict:
    """
    Discover every meaningful filesystem location on this machine.
    Returns an ordered dict: label → absolute path (only existing locations).
    """
    import string
    paths = {}

    for name in [
        "Desktop", "Documents", "Downloads", "Pictures",
        "Videos", "Music", "Favorites", "Saved Games",
    ]:
        p = os.path.join(_HOME, name)
        if os.path.exists(p):
            paths[name] = p

    
    od = (
        os.environ.get("OneDrive")
        or os.environ.get("ONEDRIVE")
        or os.path.join(_HOME, "OneDrive")
    )
    if od and os.path.exists(od):
        paths["OneDrive"] = od
        # Common OneDrive sub-folders that sync local folders
        for sub in ["Desktop", "Documents", "Pictures", "Downloads"]:
            p = os.path.join(od, sub)
            if os.path.exists(p):
                paths[f"OneDrive/{sub}"] = p

   
    paths["Home"] = _HOME

  
    paths["Grg AI folder (here)"] = _SCRIPT_DIR

    
    if os.name == "nt":
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                
                label = {
                    "C": "Drive C: (System)",
                    "D": "Drive D:",
                    "E": "Drive E:",
                }.get(letter, f"Drive {letter}:")
                paths[label] = drive

    return paths


_KNOWN_PATHS = _build_paths_map()

_PATHS_LIST  = "\n".join(f'  "{name}": {path}' for name, path in _KNOWN_PATHS.items())


def _detect_gpu_layers() -> int:
    """
    Detect any GPU (NVIDIA, AMD, Intel, Apple) and enable layer offloading.
    Returns -1 (all layers to GPU) or 0 (CPU only).

    Install llama-cpp-python with GPU support for your hardware:
      NVIDIA CUDA : pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121
      AMD ROCm    : pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/rocm602
      Apple Metal : CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python
      Intel/Any   : CMAKE_ARGS="-DGGML_VULKAN=on" pip install llama-cpp-python
    """
    import subprocess
    import platform

    
    try:
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=3
        )
        if r.returncode == 0 and r.stdout.strip():
            print(f"GPU: {r.stdout.strip().splitlines()[0]} (NVIDIA CUDA)")
            return -1
    except Exception:
        pass

    
    try:
        r = subprocess.run(
            ["rocm-smi", "--showproductname"],
            capture_output=True, text=True, timeout=3
        )
        if r.returncode == 0 and r.stdout.strip():
            print("GPU: AMD (ROCm)")
            return -1
    except Exception:
        pass

    
    if platform.system() == "Darwin":
        try:
            r = subprocess.run(
                ["system_profiler", "SPHardwareDataType"],
                capture_output=True, text=True, timeout=5
            )
            if "Apple M" in r.stdout:
                chip = re.search(r"Chip:\s+(.+)", r.stdout)
                name = chip.group(1).strip() if chip else "Apple Silicon"
                print(f"GPU: {name} (Metal)")
                return -1
        except Exception:
            pass

    
    if platform.system() == "Windows":
        try:
            r = subprocess.run(
                ["wmic", "path", "win32_VideoController", "get", "name"],
                capture_output=True, text=True, timeout=5
            )
            gpus = [l.strip() for l in r.stdout.splitlines()
                    if l.strip() and l.strip().lower() != "name"]
            if gpus:
                print(f"GPU: {gpus[0]} (Vulkan)")
                return -1
        except Exception:
            pass

    
    try:
        r = subprocess.run(["lspci"], capture_output=True, text=True, timeout=5)
        gpu_lines = [l for l in r.stdout.splitlines()
                     if any(k in l for k in ("VGA", "Display", "3D", "GPU"))]
        if gpu_lines:
            print(f"GPU: {gpu_lines[0].split(':')[-1].strip()} (Vulkan)")
            return -1
    except Exception:
        pass

    
    print("No GPU detected → CPU inference")
    return 0



SYSTEM_IDENTITY = (
    "You are Grg AI, a helpful programming assistant created by Monescu Teodor. "
    "You are NOT made by Anthropic, OpenAI, Google, Meta, Microsoft, or any other AI company. "
    "You are NOT Claude, GPT, Gemini, Llama, Qwen, or any other known model. "
    "Your specialties are: C++, C#, Python, JavaScript, TypeScript, React Native, Brainfuck and many more."
    "If anyone asks who created you, who made you, what model you are, or about your origin, "
    "always answer: 'I am Grg AI, created by Monescu Teodor.' "
    "Never mention any other company or model as your creator."
)

_collection  = None
_embed_model = None



TOOL_PATTERN = re.compile(
    r'\[TOOL:\s*(\w+)((?:\s*\|\s*\w+=[^\]|]+)*)\]',
    re.IGNORECASE
)


_TOOLS_NEEDED_PATTERN = re.compile(
    r'\b(install|uninstall|pip|npm)\b'
    # File reading — with or without trigger verb (path alone is enough)
    r'|\b(read|open|parse|look\s+at|show\s+me|what\s+does|what\s+is|explain|describe)\b'
      r'.{0,40}\.(py|txt|json|cpp|js|ts|cs|java|md|html|css|rs|go|bat|sh)\b'
    r'|\b\w[\w\-]*\.(py|txt|json|cpp|js|ts|cs|java|md|html|css|rs|go|bat|sh)\b'
    # Full Windows or Unix path anywhere in the message
    r'|[A-Za-z]:\\[\w\\\-\. ]+'
    r'|/(?:home|usr|var|etc|tmp)/[\w/\-\.]+'
    r'|\b(find|search|locate)\b.{0,30}\b(file|folder|dir)\b'
    r'|\b(list|show|what|which).{0,40}\b(file|folder|dir|process|package|librar|module|pip|install)\b'
    r'|\b(what|which|how\s+much|how\s+many).{0,20}'
      r'\b(memory|ram|disk|space|cpu|process|running|package|librar|module|version)\b'
    r'|\b(free\s+space|disk\s+space|ram\s+usage|task\s+list|running\s+processes)\b'
    # Version checks — "which/what/check" + "version", or just standalone "version"
    r'|\b(check|what|which|show).{0,15}\bversion\b'
    r'|\bversion\b.{0,20}\b(have|installed|running|using)\b'
    # "run/execute it/this" — context-dependent command execution
    r'|\b(run|execute|try)\b.{0,10}\b(it|this|that|above|the\s+code|the\s+script|the\s+command)\b'
    r'|\b(open|launch|start)\b.{0,15}\b(app|program|application|notepad|explorer)\b'
    r'|\b(run|execute)\b.{0,20}\b(script|\.py|\.bat|\.sh|command)\b',
    re.IGNORECASE
)

TOOLS_INSTRUCTIONS = (
    "\n\nTOOL ACCESS: You have built-in tools to interact with the user's computer.\n"
    "To call a tool write EXACTLY this format on its own line:\n"
    "  [TOOL: tool_name | key=value | key=value]\n\n"
    "Available tools:\n"
    "  read_file      | path=<absolute_path>"
        "                    — read a file and return its full contents\n"
    "  run_command    | cmd=<shell_command>"
        "                    — run any shell command (pip, dir, tasklist…)\n"
    "  search_files   | pattern=<glob> | where=<dir>"
        "         — find files matching a pattern\n"
    "  list_folder    | path=<absolute_path>"
        "                   — list the contents of a folder\n"
    "  get_system_info"
        "                                          — CPU, RAM, disk, OS details\n"
    "  open_app       | name=<app_name_or_path>"
        "               — open an application\n\n"
    "Examples:\n"
    "  [TOOL: read_file | path=C:\\Users\\teodo\\Desktop\\main.py]\n"
    "  [TOOL: run_command | cmd=pip install numpy]\n"
    "  [TOOL: run_command | cmd=tasklist]\n"
    "  [TOOL: run_command | cmd=python --version]\n"
    "  [TOOL: search_files | pattern=*.py | where=C:\\Users\\teodo\\Desktop]\n"
    "  [TOOL: list_folder | path=C:\\Users\\teodo\\Desktop]\n"
    "  [TOOL: get_system_info]\n"
    "  [TOOL: open_app | name=notepad]\n\n"
    "Rules:\n"
    "- Call at most ONE tool per response.\n"
    "- After the tool runs you will receive its output and can answer fully.\n"
    "- Do NOT use tools for coding questions, explanations, or knowledge-only answers.\n"
    "- Do NOT compile/build code with run_command unless the user explicitly asks to compile.\n"
    "- Do NOT generate code in your response when you're calling a tool — wait for the result first.\n"
)


def _needs_tools(user_input: str) -> bool:
    """True when the question needs real OS interaction (not a coding/knowledge question)."""
    return bool(_TOOLS_NEEDED_PATTERN.search(user_input))


def _build_tools_hint(user_input: str) -> str:
    """Return a targeted one-line hint so the small model knows exactly which tool to call."""
    low = user_input.lower()

   
    _path_re = re.compile(
        r'[A-Za-z]:\\[\w\\\-\. ]+\.\w+'   # C:\path\to\file.ext
        r'|/(?:home|usr|var|tmp)/[\w/\-\.]+\.\w+'  # Unix /home/...
        r'|\b[\w\-]+\.(py|txt|json|cpp|js|ts|cs|java|md|html|css|rs|go|bat|sh)\b',
        re.IGNORECASE
    )
    path_m = _path_re.search(user_input)
    if path_m and not re.search(r'\b(install|uninstall|find|search|list|show)\b', low):
        raw = path_m.group(0).strip("'\"")
        return f"The user is asking about the file '{raw}'. Use: [TOOL: read_file | path={raw}]"

    
    if re.search(r'\binstall\b', low):
        m = re.search(r'\binstall\s+([^\s,]+)', low)
        pkg = m.group(1) if m and m.group(1) not in ("a","the","my","some","it") else "<name>"
        return f"Use: [TOOL: run_command | cmd=pip install {pkg}]"

    if re.search(r'\buninstall\b', low):
        m = re.search(r'\buninstall\s+([^\s,]+)', low)
        pkg = m.group(1) if m else "<name>"
        return f"Use: [TOOL: run_command | cmd=pip uninstall -y {pkg}]"

    
    if re.search(r'\bversion\b', low):
        tool = "python" if "python" in low else "pip" if "pip" in low else "node" if "node" in low else "python"
        return f"Use: [TOOL: run_command | cmd={tool} --version]"

    
    if re.search(r'\b(librar|package|module)\b', low):
        return "Use: [TOOL: run_command | cmd=pip list]"
    if re.search(r'\binstalled\b', low):
        return "Use: [TOOL: run_command | cmd=pip list]"

    
    if re.search(r'\b(run|execute|try)\b.{0,15}\b(it|this|that|above|the\s+code|the\s+script)\b', low):
        return (
            "The user wants to run the code or command from the previous message. "
            "Use: [TOOL: run_command | cmd=python --version] "
            "or the appropriate command based on the conversation history."
        )

    
    if re.search(r'\b(read|open|parse|look\s+at|explain|describe)\b.{0,40}'
                 r'\.(py|txt|json|cpp|js|ts|cs|md|html)\b', low):
        m = re.search(r'[A-Za-z]:\\[\w\\\-\. ]+|[\w\-]+\.\w+', user_input)
        path = m.group(0).strip("'\"") if m else "<path>"
        return f"Use: [TOOL: read_file | path={path}]"

    
    if re.search(r'\b(find|search|locate)\b.{0,20}\bfile\b', low):
        m = re.search(r'\*\.\w+|\b(\w+\.\w+)\b', user_input)
        pattern = m.group(0) if m else "*.py"
        return f"Use: [TOOL: search_files | pattern={pattern} | where={_SCRIPT_DIR}]"

    
    if re.search(r'\b(list|show)\b.{0,15}\b(file|folder|dir)\b', low):
        return f"Use: [TOOL: list_folder | path={_SCRIPT_DIR}]"

    
    if re.search(r'\b(process|running|task\s+list)\b', low):
        return "Use: [TOOL: run_command | cmd=tasklist]"
    if re.search(r'\b(memory|ram|disk|space|cpu)\b', low):
        return "Use: [TOOL: get_system_info]"

    
    if re.search(r'\b(open|launch|start)\b.{0,15}\b(app|program|application)\b', low):
        return "Use: [TOOL: open_app | name=<app_name>]"

    return "Use the appropriate [TOOL: ...] from the tools list above."




def _tool_read_file(path: str) -> str:
    path = os.path.expanduser(path.strip())
    if not os.path.exists(path):
        return f"File not found: {path}"
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        lines = content.splitlines()
        if len(lines) > 200:
            content = "\n".join(lines[:200]) + f"\n... ({len(lines)} lines total, showing first 200)"
        return content if content else "(file is empty)"
    except Exception as e:
        return f"Could not read file: {e}"


def _tool_run_command(cmd: str, timeout: int = 20) -> str:
    import subprocess
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=timeout, cwd=_SCRIPT_DIR
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        if stdout and stderr:
            return f"{stdout}\n[stderr]: {stderr}"
        output = stdout or stderr
        return output if output else "(command ran but produced no output)"
    except subprocess.TimeoutExpired:
        return f"(timed out after {timeout}s)"
    except Exception as e:
        return f"(error: {e})"


def _tool_search_files(pattern: str, where: str = "") -> str:
    import fnmatch
    where = os.path.expanduser(where.strip()) if where.strip() else _SCRIPT_DIR
    if not os.path.exists(where):
        return f"Directory not found: {where}"
    found = []
    try:
        for root, dirs, files in os.walk(where):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for f in files:
                if fnmatch.fnmatch(f.lower(), pattern.lower()):
                    found.append(os.path.join(root, f))
            if len(found) >= 50:
                break
    except PermissionError:
        pass
    if not found:
        return f"No files matching '{pattern}' found in: {where}"
    out = f"Found {len(found)} file(s) matching '{pattern}' in {where}:\n"
    out += "\n".join(found[:50])
    if len(found) >= 50:
        out += "\n... (showing first 50)"
    return out


def _tool_list_folder(path: str) -> str:
    path = os.path.expanduser(path.strip())
    if not os.path.exists(path):
        return f"Path not found: {path}"
    if not os.path.isdir(path):
        return f"Not a directory: {path}"
    try:
        entries = sorted(os.listdir(path))
        lines = []
        for e in entries[:100]:
            full = os.path.join(path, e)
            tag = "[DIR] " if os.path.isdir(full) else "      "
            lines.append(f"{tag}{e}")
        result = f"Contents of {path} ({len(entries)} items):\n" + "\n".join(lines)
        if len(entries) > 100:
            result += f"\n... (showing first 100 of {len(entries)})"
        return result
    except Exception as e:
        return f"Could not list folder: {e}"


def _tool_get_system_info() -> str:
    import platform, subprocess
    info = [
        f"OS:          {platform.system()} {platform.release()} ({platform.version()})",
        f"Machine:     {platform.machine()}",
        f"CPU cores:   {multiprocessing.cpu_count()}",
    ]
    if platform.system() == "Windows":
        # RAM
        try:
            r = subprocess.run(
                ["wmic", "OS", "get", "FreePhysicalMemory,TotalVisibleMemorySize", "/value"],
                capture_output=True, text=True, timeout=5
            )
            mem = {}
            for line in r.stdout.splitlines():
                if '=' in line:
                    k, _, v = line.partition('=')
                    if v.strip().isdigit():
                        mem[k.strip()] = int(v.strip())
            if "TotalVisibleMemorySize" in mem:
                total = mem["TotalVisibleMemorySize"] // 1024
                free  = mem.get("FreePhysicalMemory", 0) // 1024
                info.append(f"RAM:         {total} MB total, {free} MB free")
        except Exception:
            pass
        # Disks
        try:
            r = subprocess.run(
                ["wmic", "logicaldisk", "get", "DeviceID,FreeSpace,Size"],
                capture_output=True, text=True, timeout=5
            )
            for line in r.stdout.splitlines()[1:]:
                parts = line.split()
                if len(parts) == 3:
                    dev, free_b, size_b = parts
                    try:
                        free_gb = int(free_b) // (1024**3)
                        size_gb = int(size_b) // (1024**3)
                        info.append(f"Disk {dev}      {size_gb} GB total, {free_gb} GB free")
                    except ValueError:
                        pass
        except Exception:
            pass
    return "\n".join(info)


def _tool_open_app(name: str) -> str:
    import subprocess
    import platform
    try:
        system = platform.system()
        if system == "Windows":
            subprocess.Popen(["start", "", name], shell=True)
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", name])
        else:
            subprocess.Popen([name])
        return f"Opened: {name}"
    except Exception as e:
        return f"Could not open '{name}': {e}"


def _parse_tool_call(text: str) -> tuple[str, dict] | tuple[None, None]:
    """Extract the first [TOOL: name | k=v ...] from AI output."""
    m = TOOL_PATTERN.search(text)
    if not m:
        return None, None
    name = m.group(1).strip().lower()
    args_raw = m.group(2) or ""
    args = {}
    for segment in args_raw.split('|'):
        segment = segment.strip()
        if '=' in segment:
            k, _, v = segment.partition('=')
            args[k.strip().lower()] = v.strip()
    return name, args


def _execute_tool(name: str, args: dict) -> str:
    """Dispatch to the correct tool function."""
    if name == "read_file":
        return _tool_read_file(args.get("path", ""))
    if name == "run_command":
        return _tool_run_command(args.get("cmd", ""))
    if name == "search_files":
        return _tool_search_files(args.get("pattern", "*"), args.get("where", ""))
    if name == "list_folder":
        return _tool_list_folder(args.get("path", _SCRIPT_DIR))
    if name == "get_system_info":
        return _tool_get_system_info()
    if name == "open_app":
        return _tool_open_app(args.get("name", ""))
    return f"Unknown tool: '{name}'"


def _ask_tool_permission(name: str, args: dict) -> bool:
    """Show the tool call and ask the user to approve it."""
    arg_str = "  ".join(f"{k}={v}" for k, v in args.items()) if args else "(no args)"
    print(f"\n{'─' * 52}")
    print(f"  Grg AI wants to use a tool:")
    print(f"  Tool : {name}")
    print(f"  Args : {arg_str}")
    print(f"{'─' * 52}")
    try:
        answer = input("  Allow? [y/N]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        answer = "n"
    return answer in ("y", "yes")


FILE_PATTERN  = re.compile(r'\[FILE:\s*(.+?)\]\s*<?\n?(.*?)\n?>?\s*\[/FILE\]', re.DOTALL | re.IGNORECASE)
MKDIR_PATTERN = re.compile(r'\[MKDIR:\s*(.+?)\]', re.IGNORECASE)

_FILE_REQUEST_PATTERN = re.compile(
    r'\b(save|write|put|create|make|generate)\b.{0,50}\b(file|\.cpp|\.py|\.js|\.txt|\.html|\.cs|\.java)\b'
    r'|\bin\s+a\s+(?:new\s+)?file\b'
    r'|\bsave\b.{0,30}\bto\b'           # "save this code to downloads"
    r'|\bsave\b.{0,30}\b(desktop|downloads|documents|pictures|here)\b'
    r'|\b(to|in)\s+(?:my\s+)?(?:downloads?|documents?|desktop|pictures)\b'
    r'|\bon\s+(?:the\s+)?desktop\b'
    r'|\bcreate\s+a?\s*folder\b'
    r'|\bmake\s+a?\s*(?:new\s+)?(?:folder|directory|dir)\b',
    re.IGNORECASE
)

FILE_INSTRUCTIONS = (
    f"\n\nFILE SYSTEM ACCESS: You can create files and folders on the user's computer.\n"
    f"To create a FILE write this EXACT format — include both markers and the content between them:\n"
    f"[FILE: <full_absolute_path>]\n"
    f"<file content here>\n"
    f"[/FILE]\n\n"
    f"To create a FOLDER write:\n"
    f"[MKDIR: <full_absolute_path>]\n\n"
    f"ALL KNOWN PATHS on this system — read carefully and pick the correct one:\n"
    f"{_PATHS_LIST}\n\n"
    f"Rules:\n"
    f"- Use [FILE:] ONLY when the user explicitly asks to SAVE or CREATE a file.\n"
    f"- Use [MKDIR:] ONLY when the user explicitly asks to CREATE a folder.\n"
    f"- For 'generate code' with no file mention → just write code normally, NO [FILE:].\n"
    f"- Always use a FULL ABSOLUTE PATH from the list above — never a relative path.\n"
    f"- Match the path to what the user said: 'desktop' → Desktop path, 'documents' → Documents path, etc.\n"
    f"- The user will be asked to approve before anything is written to disk.\n"
)


_LOCATION_KEYWORDS: list[tuple[str, str]] = [
    (r'\bdesktop\b',                       "Desktop"),
    (r'\bdocuments?\b',                    "Documents"),
    (r'\bdownloads?\b',                    "Downloads"),
    (r'\bpictures?\b|\bimages?\b',         "Pictures"),
    (r'\bvideos?\b|\bmovies?\b',           "Videos"),
    (r'\bmusic\b|\bsongs?\b',             "Music"),
    (r'\bonedrive\b',                      "OneDrive"),
    (r'\bhome\b|\buser\s+folder\b',        "Home"),
    (r'\bdrive\s*[dD]\b',                  "Drive D:"),
    (r'\bdrive\s*[eE]\b',                  "Drive E:"),
    (r'\bhere\b|\bthis\s+folder\b|\bproject\b|\bgrg\b', "Grg AI folder (here)"),
]


def _needs_file_hint(user_input: str) -> str | None:
    """
    Returns a hint only when the user explicitly wants a file or folder created.
    The AI resolves the exact path itself using the full path map in FILE_INSTRUCTIONS.
    Returns None for plain code-generation requests.
    """
    if not _FILE_REQUEST_PATTERN.search(user_input):
        return None

    low = user_input.lower()

    location_path = _SCRIPT_DIR   # sensible fallback
    location_name = "Grg AI folder (here)"
    for pattern, label in _LOCATION_KEYWORDS:
        if re.search(pattern, low) and label in _KNOWN_PATHS:
            location_path = _KNOWN_PATHS[label]
            location_name = label
            break

    
    if re.search(r'\b(folder|directory|dir)\b', low):
        m = re.search(
            r'\b(?:folder|directory|dir)\b\s+(?:named?|called?)?\s*["\']?([\w][\w\s\-]*)["\']?',
            low
        )
        name = m.group(1).strip() if m else "NewFolder"
        path = os.path.join(location_path, name)
        return (
            f"The user wants to create a folder named '{name}' in {location_name}.\n"
            f"Use: [MKDIR: {path}]"
        )

    
    ext_map = {
        "c++": ".cpp", "cpp": ".cpp", "c#": ".cs", "csharp": ".cs",
        "python": ".py", "javascript": ".js", "typescript": ".ts",
        "html": ".html", "css": ".css", "java": ".java", "rust": ".rs",
        "go": ".go", "kotlin": ".kt", "swift": ".swift",
        "text": ".txt", "markdown": ".md", "json": ".json", "xml": ".xml",
    }
    filename_m = re.search(r'\b([\w\-]+\.\w+)\b', user_input)
    if filename_m:
        filename = filename_m.group(1)
    else:
        ext = ".txt"
        for lang, e in ext_map.items():
            if lang in low:
                ext = e
                break
        filename = f"output{ext}"

    path = os.path.join(location_path, filename)
    return (
        f"The user wants to save a file to {location_name} ({location_path}).\n"
        f"Suggested path: {path}\n"
        f"Use [FILE: {path}]<content>[/FILE] — put the actual code/text as the content."
    )


def _ask_file_permission(path: str, content: str = "", is_dir: bool = False) -> bool:
    """Show the file path (and content preview) and ask the user to approve."""
    kind = "folder" if is_dir else "file"
    print(f"\n{'─' * 52}")
    print(f"  Grg AI wants to create a {kind}:")
    print(f"  📄 {path}")
    if content:
        lines = content.splitlines()
        for line in lines[:6]:
            print(f"     {line}")
        if len(lines) > 6:
            print(f"     ... ({len(lines)} lines total)")
    print(f"{'─' * 52}")
    try:
        answer = input("  Allow? [y/N]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        answer = "n"
    return answer in ("y", "yes")


def _create_file(path: str, content: str) -> str:
    """Write content to path, creating parent directories as needed."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✓ File created: {path}"
    except Exception as e:
        return f"✗ Could not create file: {e}"


def _create_folder(path: str) -> str:
    """Create a folder (and any missing parents)."""
    try:
        os.makedirs(path, exist_ok=True)
        return f"✓ Folder created: {path}"
    except Exception as e:
        return f"✗ Could not create folder: {e}"



def _parse_markdown(content: str) -> list:
    """Parsează Markdown în chunk-uri inteligente cu heading context."""
    chunks = []
    heading_stack = []
    code_block = None
    code_lang  = ""
    text_buf   = []

    def flush_text():
        if not text_buf:
            return
        text = " ".join(text_buf).strip()
        if len(text) >= MIN_CHUNK:
            heading = " > ".join(heading_stack) if heading_stack else ""
            for i in range(0, len(text), MAX_CHUNK):
                piece = text[i:i+MAX_CHUNK]
                chunks.append({
                    "text": f"{heading}\n{piece}" if heading else piece,
                    "type": "text"
                })
        text_buf.clear()

    def flush_code():
        nonlocal code_block, code_lang
        if code_block is None:
            return
        code = "\n".join(code_block).strip()
        if code:
            heading = " > ".join(heading_stack) if heading_stack else ""
            label = f"[{code_lang} code]" if code_lang else "[code]"
            chunks.append({
                "text": f"{heading}\n{label}\n{code}" if heading else f"{label}\n{code}",
                "type": "code"
            })
        code_block = None
        code_lang  = ""

    for line in content.splitlines():
        fence_match = re.match(r"^```(\w*)", line)
        if fence_match:
            if code_block is None:
                flush_text()
                code_block = []
                code_lang  = fence_match.group(1)
            else:
                flush_code()
            continue

        if code_block is not None:
            code_block.append(line)
            continue

        h_match = re.match(r"^(#{1,6})\s+(.+)", line)
        if h_match:
            flush_text()
            level = len(h_match.group(1))
            title = h_match.group(2).strip()
            heading_stack[:] = heading_stack[:level-1]
            heading_stack.append(title)
            continue

        stripped = line.strip()
        if stripped:
            text_buf.append(stripped)

    flush_text()
    flush_code()
    return chunks


def _get_file_fingerprint() -> str:
    if not os.path.exists(KNOWLEDGE_DIR):
        return ""
    parts = []
    for fname in sorted(os.listdir(KNOWLEDGE_DIR)):
        if fname.endswith((".md", ".txt")):
            path = os.path.join(KNOWLEDGE_DIR, fname)
            parts.append(f"{fname}:{os.path.getsize(path)}")
    return "|".join(parts)


def _chunk_plain_text(content: str) -> list:
    chunks = []
    paragraphs = re.split(r"\n\s*\n", content)
    for para in paragraphs:
        para = para.strip()
        if len(para) >= MIN_CHUNK:
            for i in range(0, len(para), MAX_CHUNK):
                chunks.append({"text": para[i:i+MAX_CHUNK], "type": "text"})
    return chunks


def _load_rag():
    
    global _collection, _embed_model

    print("Loading embedding model...", end="\r")
    with SuppressStderr():
        try:
            import torch
            if torch.cuda.is_available():
                _torch_device = "cuda"
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                _torch_device = "mps"
            else:
                _torch_device = "cpu"
        except ImportError:
            _torch_device = "cpu"

        if os.path.isdir(EMBED_MODEL_DIR):
            _embed_model = SentenceTransformer(EMBED_MODEL_DIR, device=_torch_device)
        else:
            print("\nFirst run: downloading embedding model (internet required once)...")
            _embed_model = SentenceTransformer(EMBED_MODEL, device=_torch_device)
            _embed_model.save(EMBED_MODEL_DIR)
            print(f"Embedding model saved to '{EMBED_MODEL_DIR}' — offline from now on.")
    print("                          ", end="\r")

    client = chromadb.PersistentClient(path=INDEX_DIR)

    fingerprint    = _get_file_fingerprint()
    fp_file        = os.path.join(INDEX_DIR, "fingerprint.txt")
    saved_fp       = open(fp_file).read() if os.path.exists(fp_file) else ""
    index_is_fresh = (saved_fp == fingerprint and fingerprint != "")

    if index_is_fresh:
        _collection = client.get_or_create_collection("knowledge")
        count = _collection.count()
        print(f"Knowledge index ready ({count} chunks).")
        return

    print("Building knowledge index (only once)...")
    try:
        client.delete_collection("knowledge")
    except Exception:
        pass
    _collection = client.create_collection("knowledge")

    if not os.path.exists(KNOWLEDGE_DIR):
        print("Warning: 'Knowledge' folder not found.")
        return

    all_chunks = []
    all_ids    = []
    all_metas  = []
    chunk_idx  = 0

    for filename in os.listdir(KNOWLEDGE_DIR):
        if not filename.endswith((".md", ".txt")):
            continue
        path = os.path.join(KNOWLEDGE_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Warning: Could not read {filename}: {e}")
            continue

        if filename.endswith(".md"):
            file_chunks = _parse_markdown(content)
        else:
            file_chunks = _chunk_plain_text(content)

        for ch in file_chunks:
            all_chunks.append(ch["text"])
            all_ids.append(f"c{chunk_idx}")
            all_metas.append({"source": filename, "type": ch["type"]})
            chunk_idx += 1

    if not all_chunks:
        print("Warning: No content found in Knowledge folder.")
        return

    print(f"Embedding {len(all_chunks)} chunks...", end="\r")
    with SuppressStderr():
        embeddings = _embed_model.encode(
            all_chunks,
            batch_size=64,
            show_progress_bar=False
        ).tolist()
    print(f"                              ", end="\r")

    batch = 500
    for i in range(0, len(all_chunks), batch):
        _collection.add(
            documents  = all_chunks[i:i+batch],
            embeddings = embeddings[i:i+batch],
            ids        = all_ids[i:i+batch],
            metadatas  = all_metas[i:i+batch]
        )

    os.makedirs(INDEX_DIR, exist_ok=True)
    with open(fp_file, "w") as f:
        f.write(fingerprint)

    print(f"Knowledge index built ({len(all_chunks)} chunks).")


def get_knowledge_from_folder(query: str):
    """Caută semantic în index și returnează chunk-urile relevante."""
    if _collection is None or _collection.count() == 0:
        return None

    with SuppressStderr():
        query_embedding = _embed_model.encode([query]).tolist()

    results = _collection.query(
        query_embeddings = query_embedding,
        n_results        = min(TOP_K, _collection.count()),
        include          = ["documents", "metadatas", "distances"]
    )

    docs      = results.get("documents", [[]])[0]
    metas     = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not docs:
        return None

    matched = [
        f"[Source: {m['source']}]\n{d}"
        for d, m, dist in zip(docs, metas, distances)
        if dist < DISTANCE_THRESHOLD
    ]

    if not matched:
        return None
    
    return "\n\n---\n\n".join(matched)

_MAX_HISTORY_CHARS = 3000   


def _build_history_block(history: list) -> str:
    if not history:
        return ""
    parts = []
    total = 0
    for turn in reversed(history):
        chunk = (
            f"<|im_start|>user\n{turn['user']}<|im_end|>\n"
            f"<|im_start|>assistant\n{turn['assistant']}<|im_end|>\n"
        )
        total += len(chunk)
        if total > _MAX_HISTORY_CHARS:
            break
        parts.insert(0, chunk)
    return "".join(parts)


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)

    _load_rag()

    if not os.path.exists(MODEL_PATH):
        print(f"\n Model file not found: {MODEL_PATH}")
        print("\nRecommended: Qwen2.5-3B-Instruct-Q4_K_M.gguf (~2GB)")
        sys.exit(1)

    cores = multiprocessing.cpu_count()
    gpu_layers = _detect_gpu_layers()
    print(f"Loading LLM model ({'GPU' if gpu_layers else 'CPU'})...", end="\r")

    try:
        with SuppressStderr():
            llm = llama_cpp.Llama(
                model_path    = MODEL_PATH,
                n_ctx         = 4096,       
                verbose       = False,
                n_threads     = cores,
                n_batch       = 1024,      
                n_gpu_layers  = gpu_layers, 
                f16_kv        = True,       
                use_mmap      = True,       
            )
        print("                                    ", end="\r")
    except Exception as e:
        print(f"\n Error loading model: {e}")
        sys.exit(1)

    print(f"--- Grg Ai ---")

    # Session memory — lives only while the program is running
    conversation_history: list[dict] = []

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        context = get_knowledge_from_folder(user_input)

        
        needs_tools = _needs_tools(user_input)
        tools_block = (
            f"{TOOLS_INSTRUCTIONS}"
            f"\n\n=== TOOL HINT ===\n{_build_tools_hint(user_input)}\n=== END HINT ==="
            if needs_tools else ""
        )

        file_hint = _needs_file_hint(user_input)
        file_block = (
            f"{FILE_INSTRUCTIONS}"
            f"\n\n=== FILE HINT ===\n{file_hint}\n=== END HINT ==="
            if file_hint else ""
        )

        max_tok = 1536 if (file_hint or needs_tools) else 768

        
        history_block = _build_history_block(conversation_history)

        
        base_system = (
            f"{SYSTEM_IDENTITY}"
            f"{tools_block}"
            f"{file_block}\n\n"
        )
        if context:
            prompt = (
                f"<|im_start|>system\n"
                f"{base_system}"
                f"You have access to a knowledge base. "
                f"Below is relevant context retrieved from it. "
                f"Use this context to answer helpfully and conversationally.\n\n"
                f"=== KNOWLEDGE BASE CONTEXT ===\n{context}\n=== END CONTEXT ===\n"
                f"<|im_end|>\n"
                f"{history_block}"
                f"<|im_start|>user\n{user_input}<|im_end|>\n"
                f"<|im_start|>assistant\n"
            )
        else:
            prompt = (
                f"<|im_start|>system\n"
                f"{base_system}"
                f"Answer the user's question helpfully and conversationally. "
                f"If you don't know something specific, say so honestly.\n"
                f"<|im_end|>\n"
                f"{history_block}"
                f"<|im_start|>user\n{user_input}<|im_end|>\n"
                f"<|im_start|>assistant\n"
            )

        try:
            llm_params = dict(
                max_tokens     = max_tok,
                stop           = ["<|im_end|>", "</s>"],
                stream         = True,
                temperature    = 0.3,
                top_p          = 0.9,
                repeat_penalty = 1.1,
            )

            
            MAX_TOOL_CALLS = 5
            agent_prompt   = prompt
            response_text  = ""

            for call_num in range(MAX_TOOL_CALLS + 1):
                print(f"\nGrg Ai: ", end="", flush=True)
                response_text = ""
                for chunk in llm(agent_prompt, **llm_params):
                    if 'choices' in chunk:
                        token = chunk['choices'][0].get('text', '')
                        if token:
                            print(token, end="", flush=True)
                            response_text += token
                print()

                tool_name, tool_args = _parse_tool_call(response_text)
                if not tool_name or call_num == MAX_TOOL_CALLS:
                    break

                if _ask_tool_permission(tool_name, tool_args):
                    output = _execute_tool(tool_name, tool_args)
                    lines = output.splitlines()
                    print(f"  Output:\n  " + "\n  ".join(lines[:30]))
                    if len(lines) > 30:
                        print(f"  ... ({len(lines)} lines total, showing first 30)")
                    agent_prompt = (
                        agent_prompt
                        + response_text
                        + "<|im_end|>\n"
                        + "<|im_start|>system\n"
                        + f"Tool '{tool_name}' returned:\n```\n{output[:2000]}\n```\n"
                        + "Use this result to complete your answer."
                        + "<|im_end|>\n"
                        + "<|im_start|>assistant\n"
                    )
                else:
                    print("  [Tool call denied]")
                    break

            if response_text.strip():
                conversation_history.append({
                    "user":      user_input,
                    "assistant": response_text.strip(),
                })

            for file_match in FILE_PATTERN.finditer(response_text):
                fpath   = file_match.group(1).strip()
                content = file_match.group(2)
                if _ask_file_permission(fpath, content=content):
                    print(f"  {_create_file(fpath, content)}")
                else:
                    print("  [File creation denied]")

            for mkdir_match in MKDIR_PATTERN.finditer(response_text):
                fpath = mkdir_match.group(1).strip()
                if _ask_file_permission(fpath, is_dir=True):
                    print(f"  {_create_folder(fpath)}")
                else:
                    print("  [Folder creation denied]")

        except Exception as e:
            print(f"\n[Error: {e}]")


if __name__ == "__main__":
    main()