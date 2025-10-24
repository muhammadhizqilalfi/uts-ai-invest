import json
import re

def load_knowledge_base(file_path="../knowledge_base/knowledge_base.json"):
    """Baca knowledge base dari file JSON"""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["rules"]

def check_rule(conditions, facts):
    """Memeriksa apakah semua kondisi dalam rule terpenuhi oleh working memory"""
    expr = " ".join(conditions)
    expr = expr.replace("AND", "and").replace("OR", "or")

    for key in facts.keys():
        expr = re.sub(rf'\b{key}\b', f'facts["{key}"]', expr)

    try:
        result = eval(expr)
        print(f"   Mengevaluasi: {expr} -> {result}")
    except Exception as e:
        print(f"   Gagal evaluasi: {expr}")
        print(f"   Error: {e}")
        result = False

    return result

def forward_chaining(user_data, file_path="../knowledge_base/knowledge_base.json"):
    """Proses utama forward chaining"""
    rules = load_knowledge_base(file_path)
    working_memory = user_data.copy()
    results = []

    print("\n=== PROSES FORWARD CHAINING ===")
    print(f"Working Memory Awal: {working_memory}\n")

    for rule_id, rule in rules.items():
        print(f" Mengevaluasi {rule_id}...")
        cocok = check_rule(rule["IF"], working_memory)

        if cocok:
            print(f" {rule_id} terpenuhi → {rule['THEN'].get('Rekomendasi')}\n")

            for k, v in rule["THEN"].items():
                if k not in working_memory:
                    print(f"   ➕ Menambahkan fakta baru: {k} = {v}")
                working_memory[k] = v

            results.append({
                "rule": rule_id,
                "rekomendasi": rule["THEN"].get("Rekomendasi", ""),
                "penjelasan": rule["THEN"].get("Penjelasan", ""),
                "alokasi": rule["THEN"].get("Alokasi", None),
                "cf": rule.get("CF", 1.0)
            })

        print("-" * 60)

    print("\n=== INFERENSI SELESAI ===")
    print(f"Working Memory Akhir: {working_memory}\n")

    # Urutkan hasil berdasarkan nilai CF (certainty factor)
    results.sort(key=lambda x: x["cf"], reverse=True)
    return results

def tampilkan_hasil_rekomendasi(results):
    """Menampilkan hanya rekomendasi utama dan 1–2 pendukung"""
    print("=== HASIL REKOMENDASI INVESTASI ===\n")

    if not results:
        print(" Tidak ditemukan rekomendasi yang sesuai dengan data Anda.\n")
        return

    # Ambil 1 hasil utama
    utama = results[0]

    print(" Berdasarkan profil dan tujuan Anda, sistem merekomendasikan:")
    print(f"  {utama['rekomendasi']}\n")
    if utama.get("alokasi"):
        print(" Rencana alokasi aset yang disarankan:")
        for aset, persen in utama["alokasi"].items():
            print(f"   • {aset}: {persen}")
    print(f"\n Penjelasan:\n{utama['penjelasan']}\n")

    # Ambil maksimal 2 hasil pendukung (CF > 0.7)
    pendukung = [r for r in results[1:] if r["cf"] >= 0.7][:2]
    if pendukung:
        print(" Catatan & Pertimbangan Tambahan:\n")
        for r in pendukung:
            print(f"• {r['rekomendasi']}")
            print(f"  {r['penjelasan']}\n")

def get_user_input_cli():
    """Input user langsung dari terminal"""
    print("=== SISTEM PAKAR REKOMENDASI ALOKASI ASET INVESTASI ===")

    while True:
        try:
            usia = int(input("Masukkan usia Anda (1–100): "))
            if 1 <= usia <= 100:
                break
            else:
                print("Usia harus antara 1 sampai 100.")
        except ValueError:
            print("Masukkan angka yang valid untuk usia.")

    print("\nPilih profil risiko:")
    print("1. Konservatif")
    print("2. Moderat")
    print("3. Aggresif")
    pilihan_profil = input("Masukkan pilihan (1/2/3 atau ketik langsung): ").strip().lower()
    if pilihan_profil in ["1", "konservatif"]:
        profil = "Konservatif"
    elif pilihan_profil in ["2", "moderat"]:
        profil = "Moderat"
    elif pilihan_profil in ["3", "agresif", "aggresif"]:
        profil = "Aggresif"
    else:
        print("Tidak dikenali, diset default: Moderat")
        profil = "Moderat"

    print("\nPilih tujuan finansial:")
    print("1. Jangka Pendek")
    print("2. Jangka Panjang")
    pilihan_tujuan = input("Masukkan pilihan (1/2 atau ketik langsung): ").strip().lower()
    if pilihan_tujuan in ["1", "jangka pendek"]:
        tujuan = "Jangka Pendek"
    elif pilihan_tujuan in ["2", "jangka panjang"]:
        tujuan = "Jangka Panjang"
    else:
        print("Tidak dikenali, diset default: Jangka Panjang")
        tujuan = "Jangka Panjang"

    print("\nPilih status investor:")
    print("1. Pemula")
    print("2. Bukan Pemula")
    pilihan_status = input("Masukkan pilihan (1/2 atau ketik langsung): ").strip().lower()
    if pilihan_status in ["1", "pemula"]:
        status = "Pemula"
    elif pilihan_status in ["2", "bukan pemula", "non-pemula"]:
        status = "Bukan Pemula"
    else:
        print("Tidak dikenali, diset default: Pemula")
        status = "Pemula"

    while True:
        try:
            income = int(input("\nMasukkan pendapatan yang dapat diinvestasikan (Rp): "))
            if income >= 0:
                break
            else:
                print("Pendapatan tidak boleh negatif.")
        except ValueError:
            print("Masukkan angka yang valid untuk pendapatan.")

    return {
        "usia": usia,
        "profil_risiko": profil,
        "tujuan_finansial": tujuan,
        "status_investor": status,
        "investable_income": income
    }

if __name__ == "__main__":
    user_data = get_user_input_cli()
    hasil = forward_chaining(user_data)
    print("\n" + "="*80 + "\n")
    tampilkan_hasil_rekomendasi(hasil)
