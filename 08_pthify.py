import os
import sys

if len(sys.argv) != 2:
    print(f"usage - {sys.argv[0]} filename.py")
    sys.exit(1)

site_packages_path = os.path.abspath(
    os.path.join(
        sys.executable,
        f'../../lib/python3.{sys.version_info.minor}/site-packages'
    )
)
pth_path = os.path.join(site_packages_path, 'aaaa_hack.pth')

if sys.argv[1] == 'clear':
    if os.path.exists(pth_path):
        os.remove(pth_path)
    sys.stdout.write(".pth cleared\n")
    sys.exit(0)

code_path = sys.argv[1]
with open(code_path) as f:
    code = f.read()

pth_code = f'import sys; exec({repr(code)})'
with open(pth_path, 'w') as f:
    f.write(pth_code)

sys.stdout.write(".pth set\n")
