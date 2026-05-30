
# 🇬🇧 English

## ✨ Features

- Scan all HTML files inside the `old/` directory
- Automatically add `{% load static %}` if missing
- Convert:

```html
src="img/logo.png"
```

into:

```html
src="{% static 'img/logo.png' %}"
```

- Supports:
  - `src`
  - `href`

- Skips:
  - External URLs
  - `mailto:` links
  - `tel:` links
  - Anchors (`#`)
  - Already templated paths

- Keeps internal HTML page links unchanged
- Creates output files inside `new/`
- Automatically renames files to:

```text
index.html → index_new.html
```

---

## 📁 Project Structure

```text
AddTemplateTag/
├── old/
├── new/
├── main.py
├── README.md
├── .gitignore
└── LICENSE
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/amirlwf/AddTemplateTag.git
```

Enter the project directory:

```bash
cd AddTemplateTag
```

---

## ▶️ Usage

Place your HTML files inside:

```text
old/
```

Run:

```bash
python main.py
```

Output files will be generated inside:

```text
new/
```

---

## 🧪 Example

### Input

```html
<img src="img/logo.png">
<link href="css/style.css" rel="stylesheet">
<a href="about.html">About</a>
<script src="js/app.js"></script>
```

### Output

```html
{% load static %}
<img src="{% static 'img/logo.png' %}">
<link href="{% static 'css/style.css' %}" rel="stylesheet">
<a href="about.html">About</a>
<script src="{% static 'js/app.js' %}"></script>
```

---

## 🛡️ Why This Tool?

When converting static HTML templates into Django templates, manually wrapping all asset paths with `{% static %}` is repetitive and error-prone.

This tool automates the entire process safely and quickly.

---

## 📌 Notes

- Designed specifically for Django template projects
- Internal page links like `about.html` are not modified
- Existing Django template tags remain untouched

---

## 🤝 Contributing

Pull requests and suggestions are welcome.

If you find a bug or have an idea for improvement, feel free to open an issue.

---

## 📄 License

This project is licensed under the MIT License.

<div align="center">

Made with ❤️ using Python


</div>