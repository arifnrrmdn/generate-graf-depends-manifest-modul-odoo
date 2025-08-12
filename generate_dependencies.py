import os
import ast
from graphviz import Digraph
from collections import defaultdict

# Path ke folder addons lokal
ADDONS_PATH = "/home/ariev/Developments/odoo12-docker-dev/addons"
OUTPUT_DIAGRAM = "/home/ariev/Developments/tools-koleksi-dependensi-manifest-modul-odoo/output"

# Dictionary untuk menyimpan hubungan dependensi
dependencies = {}

# Loop semua folder di addons path
for module_name in os.listdir(ADDONS_PATH):
    manifest_path = os.path.join(ADDONS_PATH, module_name, "__manifest__.py")
    if os.path.isfile(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            try:
                manifest_data = ast.literal_eval(f.read())
                depends = manifest_data.get("depends", [])
                dependencies[module_name] = depends
            except Exception as e:
                print(f"Gagal membaca {manifest_path}: {e}")

# Balik mapping jadi dependensi -> list modul yg tergantung
reverse_deps = defaultdict(list)
all_modules = set(dependencies.keys())

for module, deps in dependencies.items():
    for dep in deps:
        reverse_deps[dep].append(module)

# Siapkan set modul eksternal (yang tidak ada di addons lokal)
external_modules = set(reverse_deps.keys()) - all_modules

# Buat graf
dot = Digraph(comment="Odoo Module Dependencies (dependensi -> modul)", format="png")
dot.attr(rankdir="LR", fontsize="10")

# Tambahkan node lokal dan eksternal
for module in sorted(all_modules):
    dot.node(module, module)
for ext_mod in sorted(external_modules):
    dot.node(ext_mod, ext_mod, style="dashed", color="gray")

# Tambahkan edges dari dependensi ke modul yang tergantung, urut alfabet
for dep in sorted(reverse_deps.keys()):
    for mod in sorted(reverse_deps[dep]):
        dot.edge(dep, mod)

# Simpan dan render
output_file = os.path.join(OUTPUT_DIAGRAM, "odoo_dependencies_reversed_sorted")
dot.render(output_file, view=False)

print(f"Graf dependensi tersimpan di {output_file}.png")

# Output teks format dependensi -> modul, urut berdasarkan dependensi dan modul
print("\nDaftar dependensi (format dependensi -> modul), terurut:")
for dep in sorted(reverse_deps.keys()):
    for mod in sorted(reverse_deps[dep]):
        print(f"{dep} -> {mod}")
