
# 🇮🇷 فارسی

## ✨ امکانات

- بررسی تمام فایل‌های HTML داخل پوشه `old/`
- اضافه کردن خودکار:

```django
{% load static %}
```

در صورت نبودن

- تبدیل خودکار:

```html
src="img/logo.png"
```

به:

```html
src="{% static 'img/logo.png' %}"
```

- پشتیبانی از:
  - `src`
  - `href`

- نادیده گرفتن:
  - لینک‌های خارجی
  - `mailto:`
  - `tel:`
  - لینک‌های `#`
  - مسیرهایی که قبلاً template شده‌اند

- حفظ لینک‌های داخلی HTML
- ساخت خروجی داخل پوشه `new/`
- تغییر خودکار نام فایل‌ها:

```text
index.html → index_new.html
```

---

## 📁 ساختار پروژه

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

## 🚀 نصب

ابتدا پروژه را Clone کنید:

```bash
git clone https://github.com/YOUR_USERNAME/AddTemplateTag.git
```

وارد پوشه پروژه شوید:

```bash
cd AddTemplateTag
```

---

## ▶️ نحوه استفاده

فایل‌های HTML را داخل پوشه زیر قرار دهید:

```text
old/
```

سپس اجرا کنید:

```bash
python main.py
```

فایل‌های خروجی داخل پوشه زیر ساخته می‌شوند:

```text
new/
```

---

## 🧪 مثال

### ورودی

```html
<img src="img/logo.png">
<link href="css/style.css" rel="stylesheet">
<a href="about.html">About</a>
<script src="js/app.js"></script>
```

### خروجی

```html
{% load static %}
<img src="{% static 'img/logo.png' %}">
<link href="{% static 'css/style.css' %}" rel="stylesheet">
<a href="about.html">About</a>
<script src="{% static 'js/app.js' %}"></script>
```

---

## 🛡️ چرا این ابزار؟

وقتی قالب‌های HTML را به Django Template تبدیل می‌کنید، تبدیل دستی تمام مسیرها به `{% static %}` کاری زمان‌بر و پراشتباه است.

این ابزار کل فرایند را به صورت خودکار، سریع و امن انجام می‌دهد.

---

## 📌 نکات

- مخصوص پروژه‌های Django Template طراحی شده
- لینک‌های داخلی مانند `about.html` تغییر نمی‌کنند
- Template Tagهای موجود دست‌نخورده باقی می‌مانند

---

## 🤝 مشارکت

اگر ایده یا پیشنهادی دارید، خوشحال می‌شوم Pull Request یا Issue ثبت کنید.

---

## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است.

---

<div align="center">

ساخته شده با ❤️ و پایتون

</div>