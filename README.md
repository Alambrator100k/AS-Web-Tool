# AS Web Tool - أداة ويب متكاملة

أداة Python متكاملة للاختبار الأمني والويب، تعمل على Termux والأنظمة الأخرى.

## 📦 المميزات

- ✅ هجوم DDoS متعدد البروتوكولات
- ✅ هجوم UDP سريع
- ✅ سحب مواقع كاملة
- ✅ أخذ لقطات شاشة
- ✅ معلومات النظام
- ✅ واجهة ملونة
- ✅ ملف واحد متكامل

## 🚀 التثبيت على Termux

```bash
# تحديث الحزم
pkg update && pkg upgrade

# تثبيت Python
pkg install python git

# تنزيل الأداة
git clone https://github.com/Alambrator100k/AS-Web-Tool.git
cd AS-Web-Tool

# تثبيت المتطلبات
pip install -r requirements.txt

# التشغيل
python as_tool.py
