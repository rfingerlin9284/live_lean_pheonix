#!/usr/bin/env python3
import os,py_compile

engine_path = 'oanda/oanda_trading_engine.py'
print('🔧 Initiating Syntax Repair on OANDA Engine...')

if not os.path.exists(engine_path):
    print(f"❌ FATAL ERROR: Trading engine file not found at '{engine_path}'.")
    raise SystemExit(1)

with open(engine_path,'r') as f:
    lines = f.readlines()

fixed_lines = []
changed = 0
for i,line in enumerate(lines):
    fixed_lines.append(line)
    # Detect function def lines at top indentation within class or module
    stripped = line.strip()
    if stripped.startswith('def ') and stripped.endswith(':'):
        # Get indent level
        indent_len = len(line) - len(line.lstrip())
        # Check next non-empty line
        j = i+1
        while j < len(lines) and lines[j].strip() == '':
            j += 1
        if j >= len(lines):
            # EOF after def -> insert pass
            indent = ' '*(indent_len+4)
            fixed_lines.append(f"{indent}pass\n")
            changed += 1
            print(f"  - 🛠️  Inserted pass after trailing def at line {i+1}")
        else:
            next_line = lines[j]
            next_indent = len(next_line) - len(next_line.lstrip())
            # If next line indentation is not greater than def's indent, insert pass
            if next_indent <= indent_len:
                indent = ' '*(indent_len+4)
                fixed_lines.append(f"{indent}pass\n")
                changed += 1
                print(f"  - 🛠️  Fixed empty or unindented def body at line {i+1} (next line {j+1})")

# Write back only if we changed anything
if changed > 0:
    backup = engine_path + '.bak.indent'
    os.rename(engine_path, backup)
    print(f"Backup of original written to {backup}")
    with open(engine_path,'w') as f:
        f.writelines(fixed_lines)
    print(f"Wrote repaired file ({changed} changes)")
else:
    print('No obvious indentation issues detected. Manual review may be required.')

# Verify syntax
try:
    py_compile.compile(engine_path, doraise=True)
    print('✅ Syntax Verification PASSED.')
except py_compile.PyCompileError as e:
    print('❌ Syntax Verification FAILED:')
    print(e)
    # If failed, restore backup
    if os.path.exists(backup):
        os.rename(backup, engine_path)
        print('Restored backup after failed compile')

print('\n🚀 Repair attempt complete.')
