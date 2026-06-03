# Supernova_project
Crab nebula

# 📦 Supernova Project – Setup Handleiding (Beginner Friendly)

Deze handleiding helpt je stap voor stap om het project werkend te krijgen, ook als je nog nooit met Git of Python hebt gewerkt.

---

# 🌐 1. Repository downloaden (GitHub)

Klik op deze link om de repository te klonen:

👉 **REPO URL:**

```
https://github.com/kickbaltus/Supernova_project.git
```

Open een terminal (PowerShell of VS Code terminal) en voer uit:

```bash
git clone https://github.com/kickbaltus/Supernova_project.git
cd Supernova_project
```

---

# 🐍 2. Controleren of Python is geïnstalleerd

Voer dit uit in de terminal:

```bash
python --version
```

### ✔ Goed voorbeeld:

```
Python 3.10+ / 3.11+ / 3.14
```

### ❌ Als het niet werkt:

* Installeer Python via: https://www.python.org/downloads/
* Zorg dat je tijdens installatie **“Add Python to PATH” aanvinkt**

---

# 📁 3. Virtual Environment aanmaken

Maak een eigen omgeving (belangrijk voor dependencies):

```bash
python -m venv .venv
```

---

# ⚡ 4. Environment activeren

## Windows (PowerShell)

```powershell
.\.venv\Scripts\Activate.ps1
```

## Windows (als dat niet werkt)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Probeer daarna opnieuw activeren.

---

## ✔ Als het werkt zie je dit:

```
(.venv) PS C:\...
```

---

# 📦 5. Installeren van benodigde packages

Installeer alle libraries:

```bash
pip install -r requirements.txt
```

---

# 🚀 6. Werken in het project (dagelijkse workflow)

## 📥 Eerst altijd updates ophalen:

```bash
git pull
```

## ✏️ Code aanpassen

Werk in de Python bestanden in de map `Python/`.

## 📤 Wijzigingen opslaan naar GitHub:

```bash
git add .
git commit -m "Beschrijf wat je hebt gedaan"
git push
```

---

# 🧪 7. Nieuwe packages installeren

Als je extra libraries nodig hebt:

```bash
pip install <package>
```

Daarna altijd:

```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

---

# ⚠️ 8. Belangrijke regels

* ❌ NOOIT `.venv` uploaden (staat al goed ingesteld via `.gitignore`)
* ✔ Altijd eerst `git pull` vóór je begint
* ✔ Gebruik altijd dezelfde repository
* ✔ Werk in je eigen `.venv` (iedereen heeft zijn eigen)

---

# 🧠 9. Hoe samenwerken werkt (simpel uitgelegd)

Iedereen:

* gebruikt dezelfde GitHub code
* heeft zijn eigen Python omgeving (.venv)
* werkt lokaal op zijn eigen laptop
* deelt code via GitHub (push/pull)

👉 Git zorgt ervoor dat jullie code samenkomt zonder elkaar te overschrijven.

---

# 🔁 10. Samenvatting (belangrijkste workflow)

```bash
git pull
# werken aan code
git add .
git commit -m "update"
git push
```

---

# 💡 Tip

Als je ergens vastloopt:

* vraag eerst ChatGPT
* of check Python versie + venv activatie

Dit zijn de 2 meest voorkomende problemen.

---

Einde setup 🎉
