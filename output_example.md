══════════════════════════ 🔍 PyCombiner Merge Report v1.2.0 ══════════════════════════

Generated On     : 2025‑06‑16 14:03:28
Entry File       : tests/examples/deep_demo/main.py
Source Directory : tests/examples/deep_demo
Output File      : demo-result.py

📦 Files Discovered (6)
────────────────────────────────────────────────────────────────────────────────────────────
 #  File                                               Lines  Internal Imports
────────────────────────────────────────────────────────────────────────────────────────────
 1  main.py                                            16     7
    └─ Unhandled imports: sys

 2  services/database.py                               23     0
    └─ Unhandled imports: os, logging

 3  utils/helpers/string_utils.py                      17     0
    └─ Unhandled imports: re

 4  models/user.py                                     18     0
    └─ Unhandled imports: typing.Optional, json

 5  utils/helpers/math_utils.py                        21     0
    └─ Unhandled imports: math

 6  services/auth.py                                   19     1
    └─ Unhandled imports: hashlib
────────────────────────────────────────────────────────────────────────────────────────────
 Total Lines: 114   |   Functions/Methods: 25   |   Classes: 2

📚 Imports in Entry File (main.py)
────────────────────────────────────────────────────────────────────────────────────────────
from utils.helpers.math_utils import add, subtract  
from utils.helpers.string_utils import format_name  
from models.user import User  
from services.auth import login, logout  
from services.database import connect_db  

📈 Dependency Tree
────────────────────────────────────────────────────────────────────────────────────────────
main.py  
├─ utils.helpers.math_utils  
├─ utils.helpers.string_utils  
├─ services.database  
├─ services.auth  
│  └─ models.user  
└─ models.user  

🧩 Merge Order (Topological Sort)
────────────────────────────────────────────────────────────────────────────────────────────
 1. services/database.py  
 2. utils/helpers/string_utils.py  
 3. models/user.py  
 4. utils/helpers/math_utils.py  
 5. services/auth.py  
 6. main.py ← entry file is merged last  

⚙️ Summary
────────────────────────────────────────────────────────────────────────────────────────────
 • Total import statements analyzed…… 12  
 • Dependency graph built……………… 6 nodes / 6 edges  
 • Duplicate local imports skipped…… 4  
 • Lines written to merged output…… 114 → demo-result.py  
 • Redundant imports removed………… 13  
 • Total time elapsed………………… 0.74 s  

✅ Merge complete! Output saved to: demo-result.py  
   You can now run:  python demo-result.py
