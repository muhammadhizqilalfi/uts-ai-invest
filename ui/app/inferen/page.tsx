"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface FormState {
  usia: string;
  profil_risiko: string;
  tujuan_finansial: string;
  status_investor: string;
  investable_income: string;
}

interface ResultItem {
  rule: string;
  rekomendasi: string;
  alokasi?: Record<string, number>;
  penjelasan: string;
}

interface ResultType {
  results: ResultItem[];
}

export default function Inferen() {
  const [form, setForm] = useState<FormState>({
    usia: "21",
    profil_risiko: "",
    tujuan_finansial: "",
    status_investor: "",
    investable_income: "",
  });

  const [result, setResult] = useState<ResultType | null>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleIncomeChange = (delta: number) => {
    const newValue = Math.max(0, Number(form.investable_income) + delta);
    setForm({ ...form, investable_income: newValue.toString() });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/inferen", {
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
      if (!res.ok) throw new Error("Gagal fetch data");
      const data: ResultType = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setResult(null);
    }
  };

  // Animasi variants
  const leftVariant = {
    hidden: { x: "-100%", opacity: 0 },
    visible: {
      x: 0,
      opacity: 1,
      transition: { type: "spring" as const, stiffness: 60, damping: 15 },
    },
  };

  const rightVariant = {
    hidden: { x: "100%", opacity: 0 },
    visible: {
      x: 0,
      opacity: 1,
      transition: { type: "spring" as const, stiffness: 60, damping: 15, delay: 0.2 },
    },
  };

  return (
    <div className="flex flex-col lg:flex-row h-auto lg:h-screen bg-[#0a0f0d] text-white font-sans overflow-hidden">
      <AnimatePresence>
        {/* Form */}
        <motion.div
          key="form-section"
          variants={leftVariant}
          initial="hidden"
          animate="visible"
          exit="hidden"
          className="w-full lg:w-1/3 flex flex-col justify-between p-6 sm:p-8 relative border-b lg:border-b-0 lg:border-r border-gray-700/70"
        >
          <div>
            <h1 className="w-full text-center text-[48px] sm:text-[64px] lg:text-[80px] font-extrabold mb-4 sm:mb-6 text-transparent stroke-text">
              FinWise
            </h1>

            <p className="text-sm text-gray-400 mb-6 text-center lg:text-left">
              Masukkan Profil Anda
            </p>

            <form onSubmit={handleSubmit} className="flex flex-col gap-6 sm:gap-8">
              {/* Usia */}
              <div>
                <label className="block mb-7 text-sm text-gray-300">Usia Anda (Tahun)</label>
                <div className="relative w-full">
                  <input
                    type="range"
                    name="usia"
                    min="0"
                    max="100"
                    value={form.usia}
                    onChange={handleChange}
                    className="w-full accent-[#1b6b5c]"
                  />
                  <span
                    className="absolute text-[#1b6b5c] font-semibold"
                    style={{
                      left: `${(parseInt(form.usia) / 100) * 100}%`,
                      transform: "translateX(-50%) translateY(-100%)",
                    }}
                  >
                    {form.usia}
                  </span>
                </div>
              </div>

              {/* Profil Risiko */}
              <div>
                <label className="block mb-1 text-sm text-gray-300">Profil Risiko</label>
                <div className="flex flex-col gap-1">
                  {["Konservatif", "Moderat", "Agresif"].map((opt) => (
                    <label key={opt} className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="profil_risiko"
                        value={opt}
                        checked={form.profil_risiko === opt}
                        onChange={handleChange}
                        className="appearance-none w-4 h-4 border-2 border-gray-400 checked:bg-[#1b6b5c] checked:border-[#1b6b5c] rounded-sm focus:outline-none"
                      />
                      <span>{opt}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Tujuan */}
              <div>
                <label className="block mb-1 text-sm text-gray-300">Tujuan Investasi</label>
                <div className="flex flex-col gap-1">
                  {["Jangka Pendek", "Jangka Panjang"].map((opt) => (
                    <label key={opt} className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="tujuan_finansial"
                        value={opt}
                        checked={form.tujuan_finansial === opt}
                        onChange={handleChange}
                        className="appearance-none w-4 h-4 border-2 border-gray-400 checked:bg-[#1b6b5c] checked:border-[#1b6b5c] rounded-sm focus:outline-none"
                      />
                      <span>{opt}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Status */}
              <div>
                <label className="block mb-1 text-sm text-gray-300">Pengalaman Investasi</label>
                <div className="flex flex-col gap-1">
                  {["Pemula", "Bukan Pemula"].map((opt) => (
                    <label key={opt} className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="status_investor"
                        value={opt}
                        checked={form.status_investor === opt}
                        onChange={handleChange}
                        className="appearance-none w-4 h-4 border-2 border-gray-400 checked:bg-[#1b6b5c] checked:border-[#1b6b5c] rounded-sm focus:outline-none"
                      />
                      <span>{opt}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Pendapatan */}
              <div>
                <label className="block mb-5 text-sm text-gray-300">
                  Pendapatan yang Diinvestasikan (Rp)
                </label>
                <div className="flex items-center gap-4">
                  <button
                    type="button"
                    onClick={() => handleIncomeChange(-10000)}
                    className="bg-[#13584a] text-white rounded-xl w-8 h-8 flex justify-center items-center hover:bg-[#0d4036]"
                  >
                    -
                  </button>
                  <input
                    type="number"
                    name="investable_income"
                    value={form.investable_income}
                    onChange={handleChange}
                    className="bg-transparent text-[#13584a] rounded-2xl px-3 py-2 w-full text-center border-2 focus:outline-none"
                  />
                  <button
                    type="button"
                    onClick={() => handleIncomeChange(10000)}
                    className="bg-[#13584a] text-white rounded-xl w-8 h-8 flex justify-center items-center hover:bg-[#0d4036]"
                  >
                    +
                  </button>
                </div>
              </div>

              <button
                type="submit"
                className="bg-[#13584a] hover:bg-[#0d4036] transition text-white font-semibold rounded-2xl py-2 mt-2"
              >
                Submit
              </button>
            </form>
          </div>
        </motion.div>

        {/* Result */}
        <motion.div
          key="rekom-section"
          variants={rightVariant}
          initial="hidden"
          animate="visible"
          exit="hidden"
          className="w-full lg:w-2/3 px-6 sm:px-10 py-6 sm:py-8 overflow-y-auto"
        >
          <h2 className="text-2xl font-semibold mb-4">Rekomendasi</h2>
          {result?.results?.length ? (
            result.results.map((r) => (
              <div
                key={r.rule}
                className="mb-6 border-b border-gray-700 pb-4 last:border-none"
              >
                <p className="font-bold text-[#1b6b5c]">{r.rule}</p>
                <p className="mt-1">{r.rekomendasi}</p>

                {r.alokasi && (
                  <ul className="ml-5 list-disc mt-2 text-sm text-gray-300">
                    {Object.entries(r.alokasi).map(([aset, persen]) => (
                      <li key={aset}>
                        {aset}: {persen}%
                      </li>
                    ))}
                  </ul>
                )}
                <p className="text-sm mt-2 text-gray-400">{r.penjelasan}</p>
              </div>
            ))
          ) : (
            <p className="text-gray-500">
              Isi profil di kiri dan klik Submit untuk melihat rekomendasi.
            </p>
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
