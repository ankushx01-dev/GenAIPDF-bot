<a id="readme-top"></a>

<div align="center">

<img src="./assets/logo.png" alt="GenAI PDF Bot Logo" width="120" />

# GenAI PDF Bot

An intelligent Telegram bot for PDF utilities, automation, and document processing.

<a href="https://t.me/genaipdfbot">
  <img src="https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" />
</a>

<a href="https://github.com/ankushx01-dev/GenAIPDF-bot">
  <img src="https://img.shields.io/github/stars/ankushx01-dev/GenAIPDF-bot?style=for-the-badge" />
</a>

<a href="https://github.com/ankushx01-dev/GenAIPDF-bot/issues">
  <img src="https://img.shields.io/github/issues/ankushx01-dev/GenAIPDF-bot?style=for-the-badge" />
</a>

</div>

---

## Overview

GenAI PDF Bot is a Telegram-based automation system for handling common PDF operations directly inside chat.

The bot focuses on simplicity, speed, and lightweight document processing without requiring users to install desktop software.

Supported workflows include:

* Image to PDF conversion
* PDF merging
* PDF compression
* Watermark insertion
* Password protection

All operations are processed dynamically and delivered instantly through Telegram.

---

## System Design

Telegram User
→ Telegram Bot API
→ Python Processing Engine
→ PDF/Image Processing Modules
→ File Response Delivery

The architecture is intentionally lightweight and stateless.

---

## Core Features

### Image → PDF

* Convert multiple images into a single PDF
* Supports sequential image uploads
* Optimized RGB conversion

### Merge PDFs

* Combine multiple PDF files
* Maintains page ordering
* Fast in-memory processing

### Compress PDF

* Reduce PDF file size
* Powered by PyMuPDF
* Optimized for lightweight delivery

### Watermark PDF

* Dynamic text watermarking
* Adjustable transparency
* Page-wise overlay support

### Protect PDF

* Password encryption support
* Secure PDF locking
* Lightweight encryption workflow

---

## Tech Stack

<p align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Telegram_Bot_API-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" />
<img src="https://img.shields.io/badge/PyPDF2-FF6B6B?style=for-the-badge" />
<img src="https://img.shields.io/badge/Pillow-3670A0?style=for-the-badge" />
<img src="https://img.shields.io/badge/PyMuPDF-009688?style=for-the-badge" />
<img src="https://img.shields.io/badge/Render-000000?style=for-the-badge&logo=render" />

</p>

---

## Architecture

Telegram Client
↓
Telegram Bot API
↓
Python Bot Engine
↓
PDF Processing Layer
↓
Generated File Response

---

## Processing Workflow

### PDF Merge Flow

Upload PDFs
→ Temporary File Storage
→ Merge Engine
→ Output Generation
→ Auto Cleanup

### Image Conversion Flow

Upload Images
→ RGB Conversion
→ PDF Generation
→ Delivery to User

---

## Key Implementation Details

* Async Telegram bot handlers
* Stateless request processing
* Temporary file cleanup system
* Modular utility functions
* Environment-variable-based secret management
* Render deployment support

---

## Project Structure

```bash
GenAIPDF-bot/
│
├── GenAIPDF.py
├── requirements.txt
├── .env
├── .gitignore
└── assets/
    └── logo.png
```

---

## Getting Started

```bash
git clone https://github.com/ankushx01-dev/GenAIPDF-bot.git

cd GenAIPDF-bot

pip install -r requirements.txt

python GenAIPDF.py
```

---

## Environment Configuration

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

Sensitive values should never be committed publicly.

---

## Deployment

### Render Deployment

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
python GenAIPDF.py
```

Environment Variables:

```env
BOT_TOKEN=
```

---

## Performance Considerations

* Lightweight processing pipeline
* Automatic temporary file cleanup
* Minimal memory overhead
* Async Telegram event handling
* Optimized PDF processing flow

---

## Roadmap

* OCR support
* AI document summarization
* Cloud file storage
* Multi-language support
* Queue-based processing
* Usage analytics dashboard

---

## Contributing

Contributions are welcome.

If you want to improve features, optimize processing, or extend the bot with new PDF utilities, feel free to open a pull request.

The project structure is modular and designed for scalability.

---

## Author

Ankush Rana

Email
[rajputx000@gmail.com](mailto:rajputx000@gmail.com)

LinkedIn
https://www.linkedin.com/in/ankush-rana-x01

GitHub
https://github.com/ankushx01-dev

---

## Closing

GenAI PDF Bot simplifies document processing into a single Telegram conversation.

Fast workflows. Minimal friction. Direct utility.
