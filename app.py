# app.py — تشغيل:  python app.py
import json
from pathlib import Path
from datetime import datetime

from flask import (
    Flask, render_template, request, redirect, url_for, session, flash
)

BASE_DIR   = Path(file).parent
DATA_FILE  = BASE_DIR / "data" / "restaurant.json"
RES_FILE   = BASE_DIR / "data" / "reservations.jsonl"

app = Flask(name)
app.secret_key = "change-this-secret-key-later"   # غيّرها قبل النشر


# ---------- تحميل بيانات المطعم من JSON ----------
def load_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


# ---------- الترجمة الثابتة لواجهة الموقع ----------
UI = {
    "ar": {
        "home": "الرئيسية", "about": "عن المنتجع", "menu": "القائمة",
        "gallery": "المعرض", "hours": "أوقات العمل", "contact": "الموقع",
        "reserve": "احجز طاولة", "order_whatsapp": "اطلب عبر واتساب",
        "call": "اتصل بنا", "view_menu": "تصفح القائمة", "all": "الكل",
        "from": "من", "to": "إلى", "name": "الاسم", "phone": "رقم الهاتف",
        "date": "التاريخ", "time": "الوقت", "guests": "عدد الأشخاص",
        "notes": "ملاحظات (اختياري)", "submit": "إرسال الحجز",
        "success": "تم استلام طلبك بنجاح، سنتواصل معك قريباً.",
        "address": "العنوان", "hours_title": "أوقات العمل",
        "reserve_title": "احجز طاولتك", "menu_title": "قائمة الطعام",
        "gallery_title": "صور المنتجع", "contact_title": "زورونا",
        "reviews": "تقييم", "switch": "English",
        "rights": "جميع الحقوق محفوظة",
        "no_map": "خريطة الموقع ستظهر هنا عند إضافة رابط Google Maps.",
    },
    "en": {
        "home": "Home", "about": "About", "menu": "Menu",
        "gallery": "Gallery", "hours": "Hours", "contact": "Location",
        "reserve": "Reserve", "order_whatsapp": "Order on WhatsApp",
        "call": "Call us", "view_menu": "View Menu", "all": "All",
        "from": "From", "to": "To", "name": "Name", "phone": "Phone",
        "date": "Date", "time": "Time", "guests": "Guests",
        "notes": "Notes (optional)", "submit": "Send Reservation",
        "success": "Your request was received. We'll contact you soon.",
        "address": "Address", "hours_title": "Opening Hours",
        "reserve_title": "Reserve a Table", "menu_title": "Our Menu",
        "gallery_title": "Gallery", "contact_title": "Visit Us",
        "reviews": "rating", "switch": "العربية",
        "rights": "All rights reserved",
        "no_map": "Map will appear here once a Google Maps link is added.",
    },
}


def current_lang():
    return session.get("lang", "ar")


def pick(value):
    """يُرجع النص حسب اللغة الحالية (يدعم القواميس {ar,en} أو النصوص)."""
    if isinstance(value, dict):
        return value.get(current_lang()) or value.get("ar", "")
    return value


@app.context_processor
def inject_globals():
    lang = current_lang()
    return {
        "lang": lang,
        "dir": "rtl" if lang == "ar" else "ltr",
        "t": UI[lang],
        "pick": pick,
        "other_lang": "en" if lang == "ar" else "ar",
    }


# ---------- الصفحة الرئيسية ----------
@app.route("/")
def index():
    data = load_data()
    reserved = request.args.get("reserved") == "1"
    return render_template("index.html", data=data, reserved=reserved)


# ---------- تبديل اللغة ----------
@app.route("/lang/<code>")
def set_lang(code):
    if code in ("ar", "en"):
        session["lang"] = code
    return redirect(request.referrer or url_for("index"))


# ---------- حجز طاولة ----------
@app.route("/reserve", methods=["POST"])
def reserve():
    entry = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "name":   request.form.get("name", "").strip(),
        "phone":  request.form.get("phone", "").strip(),
        "date":   request.form.get("date", "").strip(),
        "time":   request.form.get("time", "").strip(),
      "guests": request.form.get("guests", "").strip(),
        "notes":  request.form.get("notes", "").strip(),
    }
    if entry["name"] and entry["phone"]:
        with open(RES_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return redirect(url_for("index", reserved=1))


if name == "main":
    app.run(debug=True, host="0.0.0.0", port=5000)
