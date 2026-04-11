
```
# msc_comp_path: Computational Pathology Course

🚀 **Welcome!** This repository contains the environment and tools for the MSc Computational Pathology course. Please follow these steps to prepare your laptop **before** the first session.

## 🛠️ Step 1: Install Git
- **Windows:** Download and install [Git for Windows](https://git-scm.com/download/win).
- **Mac:** Open Terminal and type `git --version`. Click **Install** if prompted.

## 📂 Step 2: Clone the Project
Open your Terminal and run:
```bash
git clone [https://github.com/coolpaul/msc_comp_path.git](https://github.com/coolpaul/msc_comp_path.git)
cd msc_comp_path
```

## ⚙️ Step 3: Run the Auto-Setup

Run the script for your OS to install  **VS Code, Quarto, Zotero, QuPath** , and your  **AI environment** .

* **Windows:** (Run as Admin) `setup_windows.bat`
* **Mac:** `chmod +x setup_mac.command && ./setup_mac.command`

## 🧪 Step 4: Verify the Installation

**Bash**

```
conda activate msc_comp_path
python -c "import ultralytics, cv2, plotnine, sklearn, pandas, scipy, numpy; print('✅ All Systems Go!')"
quarto check jupyter
```
