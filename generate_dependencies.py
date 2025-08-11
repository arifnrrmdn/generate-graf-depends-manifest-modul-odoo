import os
import ast
from graphviz import Digraph

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

# Buat graf
dot = Digraph(comment="Odoo Module Dependencies", format="png")
dot.attr(rankdir="LR", fontsize="10")

# Tambahkan semua node
all_modules = set(dependencies.keys())
external_modules = set()

for module, deps in dependencies.items():
    dot.node(module, module)  # Node untuk modul lokal
    for dep in deps:
        if dep not in all_modules:  # Modul eksternal
            external_modules.add(dep)

# Tambahkan node eksternal dengan warna berbeda
for ext_mod in external_modules:
    dot.node(ext_mod, ext_mod, style="dashed", color="gray")

# Tambahkan edges
for module, deps in dependencies.items():
    for dep in deps:
        dot.edge(dep, module)  # Tetap hubungkan meskipun eksternal

# Simpan dan render
output_file = os.path.join(OUTPUT_DIAGRAM, "odoo_dependencies_full")
dot.render(output_file, view=False)

print(f"Graf dependensi tersimpan di {output_file}.png")
