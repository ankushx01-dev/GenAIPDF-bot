import os
import subprocess
import traceback
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import fitz  # PyMuPDF for compression
from pptx import Presentation
from keep_alive import keep_alive
keep_alive()

# --- MENU ---
MAIN_MENU = [
    [InlineKeyboardButton("🖼 Image → PDF", callback_data="image_to_pdf")],
    [InlineKeyboardButton("📂 Merge PDFs", callback_data="merge_pdfs")],
    [InlineKeyboardButton("🗜 Compress PDF", callback_data="compress_pdf")],
    [InlineKeyboardButton("📊 PPT → PDF", callback_data="ppt_to_pdf")],
    [InlineKeyboardButton("💧 Watermark PDF", callback_data="watermark_pdf")],
    [InlineKeyboardButton("🔒 Protect PDF", callback_data="protect_pdf")],
]

# --- HELPER: cleanup ---
def cleanup(files):
    for f in files:
        try:
            os.remove(f)
        except:
            pass

# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup(MAIN_MENU)
    await update.message.reply_text(
        "👋 Welcome to GenAI PDF Bot!\n\nChoose a task below:",
        reply_markup=keyboard
    )

# --- MENU HANDLER ---
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    task = query.data
    context.user_data["task"] = task

    messages = {
        "image_to_pdf": "📸 Send me 1 or more images. Type /done when finished.",
        "merge_pdfs": "📂 Send me multiple PDFs. Type /done when finished.",
        "compress_pdf": "🗜 Send me a PDF to compress.",
        "ppt_to_pdf": "📊 Send me a PowerPoint (.pptx) file.",
        "watermark_pdf": "💧 Send me a PDF for watermarking.",
        "protect_pdf": "🔒 Send me a PDF to protect."
    }

    if task in ["image_to_pdf", "merge_pdfs"]:
        context.user_data["files"] = []
        if task == "image_to_pdf":
            context.user_data["images"] = []

    await query.edit_message_text(messages[task])

# --- FILE HANDLER ---
async def handle_files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        task = context.user_data.get("task")
        if not task:
            await update.message.reply_text("⚠️ Please choose a task first using /start")
            return

        # Check file size limit
        if update.message.document.file_size > 50 * 1024 * 1024:  # 50 MB
            await update.message.reply_text("⚠️ File too large. Maximum allowed: 50 MB.")
            return

        # Fetch file
        try:
            file = await update.message.document.get_file()
            file_path = f"{update.message.document.file_unique_id}_{update.message.document.file_name}"
            try:
                await file.download_to_drive(file_path)
            except Exception as e:
                await update.message.reply_text("❌ Failed to download the file. Please try again.")
                print("Download error:", e)
                return
        except Exception as e:
            await update.message.reply_text("❌ Error fetching the file.")
            print("File fetch error:", e)
            return

        # Process tasks
        if task == "image_to_pdf":
            await update.message.reply_text("❌ You uploaded a file. Please send only images in this mode.")
            cleanup([file_path])

        elif task == "merge_pdfs":
            context.user_data["files"].append(file_path)
            await update.message.reply_text(f"📂 Added PDF. Total: {len(context.user_data['files'])}\nType /done when ready.")

        elif task == "compress_pdf":
            await update.message.reply_text("⏳ Compressing PDF...")
            output = compress_pdf(file_path)
            await update.message.reply_document(document=open(output, "rb"))
            cleanup([file_path, output])
            await update.message.reply_text("✅ Done! Type /start to select another task.")

        elif task == "ppt_to_pdf":
            await update.message.reply_text("⏳ Converting PPT → PDF...")
            output = ppt_to_pdf(file_path)
            if output:
                await update.message.reply_document(document=open(output, "rb"))
                cleanup([file_path, output])
                await update.message.reply_text("✅ Done! Type /start to select another task.")
            else:
                await update.message.reply_text("❌ PPT → PDF conversion failed.")

        elif task == "watermark_pdf":
            context.user_data["file"] = file_path
            await update.message.reply_text("✍️ Type the watermark text.")

        elif task == "protect_pdf":
            context.user_data["file"] = file_path
            await update.message.reply_text("🔑 Type the password to set.")

    except Exception as e:
        await update.message.reply_text("❌ Error while processing file. Please try again.")
        print(traceback.format_exc())

# --- DONE COMMAND ---
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        task = context.user_data.get("task")

        if task == "image_to_pdf":
            images = context.user_data.get("images", [])
            if not images:
                await update.message.reply_text("⚠️ No images uploaded.")
                return
            await update.message.reply_text("⏳ Converting images → PDF...")
            output = images_to_pdf(images)
            await update.message.reply_document(document=open(output, "rb"))
            cleanup(images + [output])
            context.user_data["images"] = []
            await update.message.reply_text("✅ Done! Type /start to select another task.")

        elif task == "merge_pdfs":
            files = context.user_data.get("files", [])
            if not files:
                await update.message.reply_text("⚠️ No PDFs uploaded.")
                return
            await update.message.reply_text("⏳ Merging PDFs...")
            output = merge_pdfs(files)
            await update.message.reply_document(document=open(output, "rb"))
            cleanup(files + [output])
            context.user_data["files"] = []
            await update.message.reply_text("✅ Done! Type /start to select another task.")
    except Exception as e:
        await update.message.reply_text("❌ Error during merging or conversion.")
        print(traceback.format_exc())

# --- TEXT HANDLER ---
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        task = context.user_data.get("task")
        if task == "watermark_pdf":
            text = update.message.text
            pdf_file = context.user_data["file"]
            await update.message.reply_text("⏳ Adding watermark...")
            output = add_watermark(pdf_file, text)
            await update.message.reply_document(document=open(output, "rb"))
            cleanup([pdf_file, output])
            await update.message.reply_text("✅ Done! Type /start to select another task.")

        elif task == "protect_pdf":
            password = update.message.text
            pdf_file = context.user_data["file"]
            await update.message.reply_text("⏳ Protecting PDF...")
            output = protect_pdf(pdf_file, password)
            await update.message.reply_document(document=open(output, "rb"))
            cleanup([pdf_file, output])
            await update.message.reply_text("✅ Done! Type /start to select another task.")
    except Exception as e:
        await update.message.reply_text("❌ Error while applying text operation.")
        print(traceback.format_exc())

# --- PDF FUNCTIONS ---
def images_to_pdf(image_files):
    pdf_path = "output_images.pdf"
    images = [Image.open(img).convert("RGB") for img in image_files]
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    return pdf_path

def merge_pdfs(files):
    merger = PdfMerger()
    for pdf in files:
        merger.append(pdf)
    output = "merged.pdf"
    merger.write(output)
    merger.close()
    return output

def compress_pdf(file_path):
    doc = fitz.open(file_path)
    output = "compressed.pdf"
    doc.save(output, deflate=True, garbage=4, clean=True)
    return output

def ppt_to_pdf(file_path):
    """
    Windows-friendly PPT → PDF conversion using LibreOffice.
    """
    output_dir = os.path.dirname(file_path)

    if os.name == "nt":
        # Default Windows LibreOffice path
        libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
        if not os.path.exists(libreoffice_path):
            print("LibreOffice not found at:", libreoffice_path)
            return None
    else:
        # Linux / macOS
        libreoffice_path = "libreoffice"

    try:
        subprocess.run(
            [libreoffice_path, "--headless", "--convert-to", "pdf", file_path, "--outdir", output_dir],
            check=True
        )
        output_file = os.path.splitext(file_path)[0] + ".pdf"
        if os.path.exists(output_file):
            return output_file
        else:
            print("PDF conversion failed, output file not found.")
            return None
    except Exception as e:
        print("LibreOffice conversion failed:", e)
        return None

def add_watermark(pdf_file, text):
    watermark_pdf = "watermarked.pdf"
    c = canvas.Canvas("temp_watermark.pdf", pagesize=letter)
    c.setFont("Helvetica", 40)
    c.setFillAlpha(0.3)
    c.drawCentredString(300, 400, text)
    c.save()

    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    watermark = PdfReader("temp_watermark.pdf").pages[0]

    for page in reader.pages:
        page.merge_page(watermark)
        writer.add_page(page)

    with open(watermark_pdf, "wb") as f:
        writer.write(f)
    return watermark_pdf

def protect_pdf(pdf_file, password):
    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(password)
    output = "protected.pdf"
    with open(output, "wb") as f:
        writer.write(f)
    return output

# --- IMAGE HANDLER ---
async def handle_images(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task = context.user_data.get("task")

    if task != "image_to_pdf":
        await update.message.reply_text("⚠️ Please choose '🖼 Image → PDF' first from /start.")
        return

    if update.message.document:
        await update.message.reply_text("❌ You uploaded a PDF/file. Please send only images in this mode.")
        return

    try:
        photo = update.message.photo[-1]
        file = await photo.get_file()
        file_path = f"{photo.file_unique_id}.jpg"
        try:
            await file.download_to_drive(file_path)
        except Exception as e:
            await update.message.reply_text("❌ Failed to download the image. Please try again.")
            print("Download error:", e)
            return

        if "images" not in context.user_data:
            context.user_data["images"] = []
        context.user_data["images"].append(file_path)

        await update.message.reply_text(
            f"🖼 Added image ({len(context.user_data['images'])}). Type /done when finished."
        )
    except Exception as e:
        await update.message.reply_text("❌ Error while processing image.")
        print("Image error:", e)

# --- RUN BOT ---
def main():
    app = Application.builder().token("8182673135:AAE-G5eOnDDrM_etqNsofhEuXD6xEBMO2Qg").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(CallbackQueryHandler(menu_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_files))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_images))

    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
