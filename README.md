# Computational Pathology Course

🚀 **Welcome!** 

This repository contains the environment and tools for the MSc Computational Pathology course. 

Please follow these steps to prepare your laptop **before** the first session.

---

## 🛠️ Step 1: Install Git

* **Windows:** Download and install [Git for Windows](https://git-scm.com/download/win).
* **Mac:** Open Terminal and type `git --version`. Click **Install** if prompted.

## 📂 Step 2: Clone the Project

Open your Terminal (Mac) or Command Prompt (Windows) and run the following commands:

```bash
git clone https://github.com/coolpaul/msc_comp_path.git
cd msc_comp_path
```

## ⚙️ Step 3: Run the Auto-Setup

Run the script for your specific operating system to install **VS Code, Quarto, Zotero, QuPath**, and your **Python AI environment**.

### **For Windows Users**

Search for "Command Prompt" in your Start menu, **right-click it**, and select **Run as Administrator**. Then run:

```batch
setup_windows.bat
```

### **For Mac Users**

Run this command in your terminal:

```bash
./setup_mac.command
```
*(Note: You will be prompted for your Mac password. The cursor will stay still while you type—this is normal.)*

## 🧪 Step 4: Verify Your Installation

Once the scripts finish, **restart your terminal** and run these checks to ensure everything is ready:

### 1. Check Python & AI Libraries

```bash
conda activate msc_comp_path
python -c "import sys, ultralytics, openslide, cv2, plotnine, sklearn, pandas, scipy, numpy; print('✅ All set up on Python {sys.version.split()[0]}!')"
```

### 2. Check Reporting Tools (Quarto)

```bash
quarto check jupyter
```
*Look for green checkmarks next to "Pythons" and "Jupyter".*

## 🚀 Step 5: Launching the Course

To start working on course materials, navigate to this folder and run:

```bash
conda activate msc_comp_path
code .
```
*(The `code .` command opens the current project folder directly in VS Code).*

---

## 💡 Troubleshooting

* **Mac Security:** If macOS blocks QuPath or Zotero, go to **System Settings > Privacy & Security** and click **"Open Anyway"** at the bottom.
* **Conda Not Found:** If `conda` is not recognized, close and restart your terminal.
* **Browser Integration:** Install the [Zotero Browser Connector](https://www.zotero.org/download/connectors) to save papers from your web browser.
