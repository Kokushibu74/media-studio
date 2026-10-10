<div align="center">

# ✨ Media Metadata Studio

### Your Personal Media Metadata Workspace

**Inspect · Clean · Export · Manage**

A mobile-friendly, local-first media metadata tool built for Termux.

<p>
  <img src="https://img.shields.io/badge/Platform-Android-3DDC84?style=for-the-badge&logo=android&logoColor=white" alt="Android">
  <img src="https://img.shields.io/badge/Runtime-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Interface-Web%20UI-7C3AED?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Web UI">
  <img src="https://img.shields.io/badge/Network-Local%20Only-16A34A?style=for-the-badge" alt="Local only">
</p>

**A practical media workspace that runs on your phone.**

</div>

---

## 💎 Overview

Media Metadata Studio provides a browser-based interface for working with image and video metadata directly on your Android device.

Run it locally through Termux, open the interface in your mobile browser, and manage supported media files without needing a separate VPS.

> Designed for a phone-first workflow, with local processing and a simple web interface.

## 🚀 Features

<table>
<tr>
<td width="50%" valign="top">

### 🔍 Metadata Analysis
Inspect available metadata and review information extracted from supported media files.

</td>
<td width="50%" valign="top">

### 🧹 Metadata Cleaning
Remove supported metadata fields using the tools available in the application.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 📱 Mobile-Friendly Workflow
Use the web interface directly from your Android phone.

</td>
<td width="50%" valign="top">

### 📂 Local File Processing
Keep uploads and processed outputs in the project's local directories.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🎛️ Device Profiles
Use custom device profiles where supported. Profiles stored in sidecar JSON files do not alter the authenticity of camera-origin metadata.

</td>
<td width="50%" valign="top">

### 🧾 Processing History
Review processing history through the application's available history features.

</td>
</tr>
</table>

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Application | Python + Flask |
| Interface | HTML, CSS & JavaScript |
| Environment | Android + Termux |
| Metadata tools | ExifTool |
| Media tools | FFmpeg |
| Storage | Local project files and SQLite history |

## ⚡ Quick Start

### 01 — Install the requirements

Open Termux and run:

```bash
pkg update -y
pkg install python exiftool ffmpeg -y
```

### 02 — Open the project

```bash
cd ~/media-studio/media-studio
```

### 03 — Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

### 04 — Launch Media Metadata Studio

```bash
python app.py
```

### 05 — Open the dashboard

Open your Android browser and visit:

**http://127.0.0.1:5000**

Keep the Termux session running while you use the application.

## 📁 Project Structure

```text
media-studio/
├── app.py
├── requirements.txt
├── README.md
├── uploads/
├── output/
└── history.sqlite3
```

*Some files and directories may be created automatically when the application runs.*

## 🔐 Privacy & Security

- **Local binding:** The application is intended to run on `127.0.0.1`.
- **Local storage:** Uploaded files and generated outputs are stored in the project directories.
- **Storage management:** Delete files you no longer need to free up phone storage.
- **Metadata limitations:** Cleaning results depend on the file format and the installed tools.
- **AI detection:** Metadata indicators are clues, not reliable proof that media was or was not AI-generated.
- **Authenticity:** Changing metadata does not establish that a file was created by a particular camera or person.

## ⚠️ Important Notes

- Supports common image and video extensions; actual capabilities depend on the implementation and installed tools.
- Custom device profiles stored as sidecar JSON files are not the same as authentic camera-generated metadata.
- Keep the project and its dependencies updated.
- Do not upload confidential media unless you understand how the application handles and stores files.

## 🗺️ Roadmap

- [x] Local browser-based interface
- [x] Termux-oriented setup
- [x] Local upload and output workflow
- [ ] Improved metadata comparison interface
- [ ] More detailed processing reports
- [ ] Enhanced mobile dashboard

*Roadmap items are planned improvements, not claims that those features are already implemented.*

---

<div align="center">

### Made for a better mobile media workflow

**Media Metadata Studio**

<sub>Local-first · Mobile-friendly · Practical</sub>

</div>

---

## 💜 Support This Project

<div align="center">

### Enjoying Media Metadata Studio?

If this project is useful to you, consider supporting its development. Your support helps with maintenance, improvements, testing, and future features.

**Every contribution is appreciated. Thank you! ❤️**

<!-- Replace the placeholders below with your real donation links. -->

[![Donate](https://img.shields.io/badge/Support%20Development-Donate-7C3AED?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/YOUR_GITHUB_USERNAME)

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/YOUR_USERNAME)

</div>

> **Note:** Donation links are placeholders. Replace them with your own active support pages before publishing.

---
