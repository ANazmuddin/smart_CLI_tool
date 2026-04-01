import os
import typer
import subprocess
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# 1. Muat variabel environment dari file .env
load_dotenv()

# Inisialisasi aplikasi CLI
app = typer.Typer(help="Asisten Terminal Pintar berbasis AI")

@app.command()
def kerjakan(perintah: str):
    """
    Ubah teks natural menjadi perintah Bash dan jalankan.
    """
    # Cek apakah API Key sudah ada di .env
    if not os.getenv("GOOGLE_API_KEY"):
        typer.secho("❌ Error: GOOGLE_API_KEY tidak ditemukan. Pastikan file .env sudah diisi.", fg=typer.colors.RED)
        raise typer.Exit()

    typer.echo("🤖 Berpikir sejenak...")

    # 2. Inisialisasi LLM (Menggunakan model Gemini flash yang cepat)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    # 3. Membuat Prompt (Instruksi spesifik untuk AI)
    template = """
    Kamu adalah asisten terminal Linux KDE Plasma yang ahli.
    Tugasmu adalah mengubah permintaan user menjadi SATU baris perintah bash yang valid.
    Hanya kembalikan perintah bash-nya saja, tanpa penjelasan, tanpa format markdown (```bash).

    Permintaan user: {permintaan}
    """
    prompt = PromptTemplate.from_template(template)

    # 4. Membuat Chain (Menyambungkan Prompt dengan LLM)
    chain = prompt | llm

    # 5. Meminta AI memproses teks
    try:
        hasil_ai = chain.invoke({"permintaan": perintah}).content.strip()
    except Exception as e:
        typer.secho(f"❌ Terjadi kesalahan saat menghubungi AI: {e}", fg=typer.colors.RED)
        raise typer.Exit()

    # Membersihkan sisa markdown jika AI membandel membungkusnya dengan ```bash
    hasil_ai = hasil_ai.replace("```bash", "").replace("```", "").strip()

    # 6. Menampilkan perintah yang dihasilkan dengan warna kuning
    typer.secho(f"\n💻 Perintah yang dihasilkan: {hasil_ai}", fg=typer.colors.YELLOW)

    # 7. Fitur Keamanan: Meminta konfirmasi sebelum dieksekusi oleh sistem
    konfirmasi = typer.confirm("Apakah kamu ingin menjalankan perintah ini?")
    
    if konfirmasi:
        typer.secho("Menjalankan perintah...\n", fg=typer.colors.CYAN)
        # Menjalankan perintah bash di sistem operasi
        subprocess.run(hasil_ai, shell=True)
        typer.secho("\n✅ Eksekusi selesai!", fg=typer.colors.GREEN)
    else:
        typer.secho("❌ Eksekusi dibatalkan.", fg=typer.colors.RED)

if __name__ == "__main__":
    app()