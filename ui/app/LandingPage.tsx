"use client";

import React, { useEffect, useRef } from "react";
import Link from "next/link";
import { motion } from "framer-motion";

export default function Home() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const mouse = useRef({ x: 0, y: 0 });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const waves = [
      { amp: 40, len: 0.015, speed: 0.015, color: "#00A884" },
      { amp: 20, len: 0.02, speed: 0.02, color: "#007F67" },
    ];

    const resize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener("resize", resize);

    const onMove = (e: MouseEvent) => {
      mouse.current.x = e.clientX / width - 0.5;
      mouse.current.y = e.clientY / height - 0.5;
    };
    window.addEventListener("mousemove", onMove);

    let time = 0;
    function animate() {
      if (!ctx) return; // guard against null context
      ctx.clearRect(0, 0, width, height);
      ctx.lineWidth = 2;

      waves.forEach((w, i) => {
        ctx.beginPath();
        for (let x = 0; x < width; x++) {
          const y =
            height * 0.7 +
            Math.sin(x * w.len + time * w.speed) * w.amp +
            mouse.current.y * 50 * (i + 1);
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        const gradient = ctx.createLinearGradient(0, 0, width, 0);
        gradient.addColorStop(0, ${w.color}80);
        gradient.addColorStop(0.5, ${w.color});
        gradient.addColorStop(1, ${w.color}80);
        ctx.strokeStyle = gradient;
        ctx.shadowBlur = 10;
        ctx.shadowColor = w.color;
        ctx.stroke();
      });

      time += 0.03;
      requestAnimationFrame(animate);
    }

    animate();

    return () => {
      window.removeEventListener("resize", resize);
      window.removeEventListener("mousemove", onMove);
    };
  }, []);

  return (
    <main className="relative flex flex-col items-center justify-center min-h-screen text-center overflow-hidden bg-[#0a0f0d]">
      {/* 🌊 Wave Canvas Background */}
      <canvas
        ref={canvasRef}
        className="absolute inset-0 pointer-events-none"
      />

      {/* Main */}
      <motion.div
        className="z-10 flex flex-col items-center px-6"
        initial={{ opacity: 0, y: 100 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{
          duration: 1.2,
          ease: [0.16, 1, 0.3, 1],
        }}
      >
        <h1 className="text-[48px] sm:text-[64px] md:text-[80px] font-extrabold mb-4 sm:mb-6 text-transparent stroke-text leading-tight drop-shadow-[0_0_10px_rgba(0,168,132,0.4)]">
          FinWise
        </h1>

        <p className="text-[#9ab3af] italic text-sm sm:text-base md:text-lg mb-10 leading-relaxed max-w-md sm:max-w-lg">
          Optimalkan keputusan finansial Anda dengan{" "}
          <br className="hidden sm:block" />
          sistem pakar berbasis AI yang memahami{" "}
          <br className="hidden sm:block" />
          kebutuhan investasi Anda
        </p>

        <Link
          href="/inferen"
          className="relative px-8 sm:px-10 py-3 border border-[#00A884] text-[#00A884] rounded-full
          overflow-hidden transition-all duration-300 group hover:bg-[#00A884]/10 text-sm sm:text-base"
        >
          <span className="relative z-10 font-semibold tracking-wide group-hover:tracking-widest transition-all duration-300">
            Mulai
          </span>

          {/* Pulse */}
          <motion.span
            className="absolute inset-0 rounded-full bg-[#00A884]/20 blur-xl"
            animate={{
              opacity: [0.2, 0.4, 0.2],
              scale: [1, 1.1, 1],
            }}
            transition={{ repeat: Infinity, duration: 3, ease: "easeInOut" }}
          />
        </Link>
      </motion.div>

      <motion.div
        className="absolute bottom-0 left-0 right-0"
        initial={{ y: "100%" }}
        animate={{ y: 0 }}
        transition={{
          duration: 1.5,
          ease: [0.16, 1, 0.3, 1],
          delay: 0.3,
        }}
      >
        <div className="relative">
          {/* Garis bawah */}
          <div className="absolute bottom-0 w-full h-16 sm:h-20 bg-[#00A884]" />
          <div
            className="relative h-20 sm:h-24 bg-[#0a0f0d]"
            style={{
              borderBottomLeftRadius: "50%",
              borderBottomRightRadius: "50%",
            }}
          />
        </div>
      </motion.div>
    </main>
  );
}