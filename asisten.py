import os
import typer
import subprocess
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool

# Muat variabel environment
load_dotenv()
app = typer.Typer(help="Asisten Terminal Agentic Canggih")

# ==========================================
# 🛠️ KUMPULAN TOOLS UNTUK AI
# ==========================================

@tool
def cek_isi_folder(path: str = ".") -> str:
    """Melihat daftar file dan folder di direktori tertentu untuk mengetahui struktur file yang ada."""
    hasil = subprocess.run(f"ls -la {path}", shell=True, capture_output=True, text=True)
    return hasil.stdout

@tool
def baca_isi_file(nama_file: str) -> str:
    """Membaca isi teks dari sebuah file untuk memahami konteks atau mencari error."""
    hasil = subprocess.run(f"cat {nama_file}", shell=True, capture_output=True, text=True)
    return hasil.stdout

# Daftarkan tools ke dalam sebuah list
tools_ai = [cek_isi_folder, baca_isi_file]

# ==========================================
# 🤖 LOGIKA UTAMA AGENT
# ==========================================

@app.command()
def kerjakan(perintah: str):
    if not os.getenv("GOOGLE_API_KEY"):
        typer.secho("❌ Error: GOOGLE_API_KEY tidak ditemukan.", fg=typer.colors.RED)
        raise typer.Exit()

    typer.echo("🤖 Sedang menganalisis dan berpikir...")

    # 1. Inisialisasi LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    # 2. Membuat Prompt Khusus Agent
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Kamu adalah asisten terminal Linux yang sangat cerdas. 
        Kamu memiliki tools untuk mengecek folder dan membaca file. 
        GUNAKAN TOOLS TERSEBUT JIKA DIPERLUKAN untuk memahami konteks sebelum memberikan jawaban.
        
        ATURAN MUTLAK JAWABAN AKHIR:
        1. Jawaban akhir HARUS BERUPA SATU BARIS PERINTAH BASH saja.
        2. Jangan gunakan format markdown (```bash).
        3. Jangan berikan penjelasan apa pun di jawaban akhirmu.
        """),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    # 3. Merakit Agent dan Executor-nya
    agent = create_tool_calling_agent(llm, tools_ai, prompt)
    
    # verbose=True akan membuat AI mencetak proses "berpikir"-nya ke terminal!
    agent_executor = AgentExecutor(agent=agent, tools=tools_ai, verbose=True)

    try:
        # Menjalankan Agent
        respons = agent_executor.invoke({"input": perintah})
        hasil_ai = respons["output"].strip()
    except Exception as e:
        typer.secho(f"❌ Terjadi kesalahan: {e}", fg=typer.colors.RED)
        raise typer.Exit()

    # Membersihkan sisa markdown jika AI membandel
    hasil_ai = hasil_ai.replace("```bash", "").replace("```", "").strip()

    typer.secho(f"\n💻 Perintah akhir yang diusulkan: {hasil_ai}", fg=typer.colors.YELLOW)

    # 4. Fitur Keamanan Eksekusi
    konfirmasi = typer.confirm("Jalankan perintah ini?")
    if konfirmasi:
        typer.secho("Mengeksekusi...\n", fg=typer.colors.CYAN)
        subprocess.run(hasil_ai, shell=True)
        typer.secho("\n✅ Eksekusi selesai!", fg=typer.colors.GREEN)
    else:
        typer.secho("❌ Dibatalkan.", fg=typer.colors.RED)

if __name__ == "__main__":
    app()