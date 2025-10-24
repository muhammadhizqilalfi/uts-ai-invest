"use client";

import { useState } from "react";

export default function Home() {
  const [form, setForm] = useState({
    usia: "",
    profil_risiko: "",
    tujuan_finansial: "",
    status_investor: "",
    investable_income: "",
  });

  const [result, setResult] = useState<any>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const res = await fetch("http://localhost:8000/interference", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        usia: Number(form.usia),
        profil_risiko: form.profil_risiko,
        tujuan_finansial: form.tujuan_finansial,
        status_investor: form.status_investor,
        investable_income: Number(form.investable_income),
      }),
    });

    const data = await res.json();
    setResult(data);
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 border rounded-lg shadow">
      <h1 className="text-2xl font-bold mb-4">Sistem Pakar Alokasi Aset Investasi</h1>
      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          name="usia"
          placeholder="Usia"
          type="number"
          value={form.usia}
          onChange={handleChange}
          className="border p-2 w-full rounded"
        />
        <select
          name="profil_risiko"
          value={form.profil_risiko}
          onChange={handleChange}
          className="border p-2 w-full rounded"
        >
          <option value="">Pilih Profil Risiko</option>
          <option value="Konservatif">Konservatif</option>
          <option value="Moderat">Moderat</option>
          <option value="Aggresif">Aggresif</option>
        </select>

        <select
          name="tujuan_finansial"
          value={form.tujuan_finansial}
          onChange={handleChange}
          className="border p-2 w-full rounded"
        >
          <option value="">Pilih Tujuan Finansial</option>
          <option value="Jangka Pendek">Jangka Pendek</option>
          <option value="Jangka Panjang">Jangka Panjang</option>
        </select>

        <select
          name="status_investor"
          value={form.status_investor}
          onChange={handleChange}
          className="border p-2 w-full rounded"
        >
          <option value="">Pilih Status Investor</option>
          <option value="Pemula">Pemula</option>
          <option value="Bukan Pemula">Bukan Pemula</option>
        </select>

        <input
          name="investable_income"
          placeholder="Pendapatan dapat diinvestasikan"
          type="number"
          value={form.investable_income}
          onChange={handleChange}
          className="border p-2 w-full rounded"
        />

        <button type="submit" className="bg-blue-600 text-white p-2 rounded w-full">
          Jalankan Inferensi
        </button>
      </form>

      {result && (
        <div className="mt-6 p-4 border rounded bg-gray-50">
          <h2 className="font-semibold text-lg">Hasil Rekomendasi:</h2>
          {result.results.map((r: any) => (
            <div key={r.rule} className="mt-3">
              <p className="font-bold">{r.rule}: {r.rekomendasi}</p>
              {r.alokasi && (
                <ul className="ml-4 list-disc">
                  {Object.entries(r.alokasi).map(([aset, persen]) => (
                    <li key={aset}>{aset}: {persen}</li>
                  ))}
                </ul>
              )}
              <p className="text-sm mt-1">{r.penjelasan}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
