══════════════════════════ 🔍 PyCombiner Merge Report ══════════════════════════

Generated On     : 2025‑06‑16 14:03:28
Entry File       : tests/examples/deep_demo/main.py
Source Directory : tests/examples/deep_demo
Output File      : demo-result-20250607-140328.py

📦 Import Handling Summary
─────────────────────────────────────────────────────────────────────────────────────
                                       Lines   | Unhandled |  Handled
─────────────────────────────────────────────────────────────────────────────────────
📁 project/
├── services/
│   └── [1] database.py              →    23       0          6
│   └── [5] auth.py                  →    19       0          0
├── utils/
│   └── helpers/
│       └── [2] string_utils.py      →    17       1          0
│       └── [4] math_utils.py        →    21       1          0
├── models/
│   └── [3] user.py                  →    18       2          0
└── main.py     🚩 entry file        →    16       0          2
─────────────────────────────────────────────────────────────────────────────────────
*[]indicates Importing Order     Total    120   |   4     |    8


📦 Import Handling Details
─────────────────────────────────────────────────────────────────────────────────────
├── ✅ Handled Imports [4]
│   ├── services/
│   │   └── auth.py:        → database
│   ├── utils/helpers/
│   │   └── math_utils.py:  → string_utils
│   └── main.py[7]:         → database, auth 
│       - from utils.helpers.math_utils   import add, subtract 
│       - from utils.helpers.string_utils import format_name
│       - from models.user                import User
│       - from services.auth              import login, logout
│       - from services.database          import connect_db
│
└── ⚠️ Unhandled Imports [8]
    ├── services/
    │   └── database.py:    → os, logging
    │   └── auth.py:        → hashlib
    ├── utils/helpers/
    │   ├── string_utils.py: → re
    │   └── math_utils.py:   → math
    ├── models/
    │   └── user.py:        → typing.Optional, json
    └── main.py:            → sys
─────────────────────────────────────────────────────────────────────────────────────


⚙️ Summary
────────────────────────────────────────────────────────────────────────────────────────────
 • Total import statements analyzed……     12  
 • Dependency graph built………………           6 nodes / 6 edges  
 • Duplicate local imports skipped……      4  
 • Lines written to merged output……       114 → demo-result.py  
 • Redundant imports removed…………          13  
 • Total time elapsed…………………              0.74 s  

✅ Merge complete! Output saved to: demo-result.py  
   You can now run:  python demo-result.py








