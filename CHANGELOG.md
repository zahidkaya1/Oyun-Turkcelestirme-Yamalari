# Changelog

## 0.2.0
- Windows için grafik arayüzlü yama yöneticisi eklendi.
- SuperCow ve Jardinains 2! tek uygulama üzerinden seçilebilir hale getirildi.
- Oyun klasörü grafik arayüz üzerinden seçilebilir hale getirildi.
- Yama durumu otomatik algılanarak `Kuruluma hazır`, `Yama kurulu`, `Kısmi yama` ve `Uyumsuz` durumları gösterilmeye başlandı.
- Uyumluluk kontrolü, yama kurulumu ve geri yükleme işlemleri GUI üzerinden kullanılabilir hale getirildi.
- Yama durumuna göre kurulum ve kaldırma düğmeleri otomatik olarak etkinleştirilip devre dışı bırakılıyor.
- Son seçilen oyun ve oyun klasörü hatırlanıyor.
- Seçilen oyun klasörünü Dosya Gezgini'nde açma özelliği eklendi.
- İşlem günlüğü ve kullanıcı onay pencereleri eklendi.
- GUI işlem/tarama sonrasında `Gözat...` düğmesinin devre dışı kalmasına neden olan durum yönetimi hatası giderildi.
- PyInstaller ile tek dosyalık, konsolsuz Windows `.exe` üretim desteği eklendi.
- Windows `.exe` üzerinden SuperCow ve Jardinains 2! için kurulum, gerçek oyun çalışması ve geri yükleme akışları test edildi.

## 0.1.1
- `verify` komutu eklendi; kurulumdan önce dosyalara dokunmadan sürüm uyumluluğu kontrol edilebilir.
- Oyun kimlikleri `games/` dizinindeki manifestlerden dinamik olarak okunacak şekilde patcher geliştirildi.
- Geri yükleme sonrasında eski yedek klasörünün kalması nedeniyle oluşabilecek bayat yedek riski giderildi.
- Yama tarafından oluşturulan boş dizinlerin geri yükleme sonrasında temizlenmesi sağlandı.
- README kurulum ve test akışı daha açık olacak şekilde güncellendi.

## 0.1.0
- İlk delta-patch altyapısı oluşturuldu.
- SuperCow ve Jardinains 2! manifestleri eklendi.
- Orijinal oyun paketlerinin repoya eklenmesini gerektirmeyen kurulum/geri alma akışı eklendi.
