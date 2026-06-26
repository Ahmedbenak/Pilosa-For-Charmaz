#!/usr/bin/env python3
"""Pipeline Etape 1 — Segmentation du corpus (Lecture)."""
import os, sys, re
from datetime import datetime
sys.path.insert(0, os.path.dirname(__file__))
from gerer_tracabilite import *
from gerer_tracabilite import _ecrire_checkpoint

ENTRETIENS_DIR = Path(__file__).parent.parent / "entretiens"
EXCLUDE_FILES = {"README.md"}

def compter_lignes_et_mots(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    return text.count("\n") + 1, len(text.split())

def has_dialogue_markers(text):
    """Check if text has explicit [Speaker] or Speaker: patterns."""
    for line in text.split("\n")[:50]:
        if re.match(r'^\[([^\]]+)\][:\s]?', line):
            return True
        if re.match(r'^(?:Enqu[e\u00ea]t[\u00e9\u00e8]r?i?c?e?|Moi|Enqueteur)\s*:', line, re.IGNORECASE):
            return True
    return False

def segmenter_fichier(path):
    """Segment by dialogue turns (bracketed or named) or by paragraph."""
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")

    # Check if file has dialogue markers
    has_markers = has_dialogue_markers(text)

    if not has_markers:
        # Fallback: paragraph-level segmentation (every content line)
        segments = []
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped:
                segments.append({
                    "texte": stripped,
                    "locuteur": "participant",
                    "debut": i + 1,
                    "fin": i + 1,
                })
        return segments

    # Dialogue-based segmentation
    segments = []
    current_lines = []
    current_locutor = None
    start_line = 1

    for i, line in enumerate(lines):
        m = re.match(r'^\[([^\]]+)\][:\s]?(.*)', line)
        locutor = None
        line_rest = line
        if m:
            locutor = m.group(1).strip()
            line_rest = m.group(2)
        else:
            m2 = re.match(r'^(Enqu[e\u00ea]t[\u00e9\u00e8]r?i?c?e?|Moi|Enqueteur)\s*:\s*(.*)', line, re.IGNORECASE)
            if m2:
                locutor = m2.group(1).strip()
                line_rest = m2.group(2)

        if locutor:
            if current_locutor is not None and locutor != current_locutor:
                if current_lines:
                    t = "\n".join(current_lines).strip()
                    if t:
                        segments.append({"texte": t, "locuteur": current_locutor, "debut": start_line, "fin": i})
                current_lines = [line_rest.strip()] if line_rest.strip() else []
                current_locutor = locutor
                start_line = i + 1
            else:
                current_locutor = locutor
                if line_rest.strip():
                    current_lines.append(line_rest.strip())
        else:
            stripped = line.strip()
            if stripped:
                current_lines.append(stripped)

    if current_lines:
        t = "\n".join(current_lines).strip()
        if t:
            segments.append({"texte": t, "locuteur": current_locutor or "narrateur", "debut": start_line, "fin": len(lines)})

    return segments

# --- Main ---
checkpoint = lire_checkpoint()
if checkpoint["statut"] == "termine":
    print("Pipeline deja terminee.")
    sys.exit(0)

files = sorted([f for f in ENTRETIENS_DIR.iterdir()
                if f.suffix.lower() in (".md", ".txt", ".docx") and f.name not in EXCLUDE_FILES])
print(f"Fichiers trouves : {len(files)}")

seen_hashes = {}
all_segments = []
entretiens_data = []
ent_global_id = 1
seg_global_id = 1

for f in files:
    content = f.read_text(encoding="utf-8", errors="replace")
    ch = hash(content)
    if ch in seen_hashes:
        print(f"  [SKIP] {f.name} (duplicate de {seen_hashes[ch]})")
        continue
    seen_hashes[ch] = f.name

    lines_nb, words_nb = compter_lignes_et_mots(f)
    ent_id = f"ENT_{ent_global_id:04d}"
    segments = segmenter_fichier(f)

    # Also filter segments: skip very short meaningless ones (< 5 chars) in non-dialogue files
    if not has_dialogue_markers(content):
        segments = [s for s in segments if len(s["texte"]) > 10]

    print(f"  {ent_id} {f.name}: {len(segments)} segments, {lines_nb}l, {words_nb}mots")

    entretiens_data.append({
        "id_entretien": ent_id,
        "fichier_source": f.name,
        "format": f.suffix.lower().lstrip("."),
        "date_entretien": "2026",
        "duree_approx": str(words_nb) + " mots",
        "nb_segments": str(len(segments)),
        "notes_non_identifiantes": "",
    })

    for seg in segments:
        all_segments.append([f"SEG_{seg_global_id:04d}", ent_id, seg["texte"],
                             "", seg["locuteur"], str(seg["debut"]), str(seg["debut"])])
        seg_global_id += 1
    ent_global_id += 1

print(f"\nTotal entretiens uniques: {len(entretiens_data)}, Total segments: {len(all_segments)}")

# Write to Excel
source_rows = [[e["id_entretien"], e["fichier_source"], e["format"], e["date_entretien"],
                e["duree_approx"], e["nb_segments"], e["notes_non_identifiantes"]] for e in entretiens_data]
ecrire_lignes_atomique("00_Corpus_Source", source_rows)
print(f"  00_Corpus_Source: {len(source_rows)} lignes")

# Write segments in batches (Excel may have limits)
BATCH = 500
written = 0
for i in range(0, len(all_segments), BATCH):
    batch = all_segments[i:i+BATCH]
    written += ecrire_lignes_atomique("01_Segments", batch)
print(f"  01_Segments: {written} lignes ecrites")

# Update checkpoint
checkpoint = lire_checkpoint()
checkpoint["premier_lancement"] = checkpoint.get("premier_lancement") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
checkpoint["dernier_lancement"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
checkpoint["dernier_heartbeat"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
checkpoint["corpus"]["total_entretiens"] = len(entretiens_data)
checkpoint["corpus"]["entretiens"] = [
    {"id_entretien": e["id_entretien"], "fichier": e["fichier_source"],
     "statut": "termine", "etape_en_cours": "segmentation",
     "dernier_segment_valide": f"SEG_{(i+1)*500 if (i+1)*500 < len(all_segments) else len(all_segments):04d}"}
    for i, e in enumerate(entretiens_data)
]
# Set correct last segment per entretien
for ent in checkpoint["corpus"]["entretiens"]:
    last = None
    for s in all_segments:
        if s[1] == ent["id_entretien"]:
            last = s[0]
    ent["dernier_segment_valide"] = last

checkpoint["etapes"]["segmentation"]["statut"] = "en_cours"
checkpoint["etapes"]["segmentation"]["dernier_id_valide"] = f"SEG_{len(all_segments):04d}" if all_segments else None
checkpoint["etapes"]["segmentation"]["nb_valides"] = len(all_segments)
checkpoint["statut"] = "en_cours"
_ecrire_checkpoint(checkpoint)
regenerer_etat_avancement()
print("\nEtape 1 - Segmentation terminee.")
