# Changelog

## 0.3.0
- Feeding Frenzy 2 v1.0 için Türkçe yama desteği eklendi.
- Ana menü, kullanıcı ekranları, seçenekler, duraklatma/oyun sonu ekranları ve HUD Türkçeleştirildi.
- Bölüm girişleri, bölüm adları ve hikâye metinleri Türkçeleştirildi; bölüm başlıklarının kaybolmasına yol açan XML `Ş`/`&` kaçış sorunu giderildi.
- 100/100 eğlenceli bilgi Türkçeleştirildi.
- Bitmap font atlaslarına Türkçe karakter uyarlamaları eklendi.
- Harita ve çeşitli arayüz görsellerindeki İngilizce yazılar Türkçeleştirildi/temizlendi.
- `FF2.saf` için 103 iç dosyayı delta olarak uygulayan SAF manifesti eklendi; tam oyun arşivi dağıtılmıyor.
- SAF kurulum performansı iyileştirildi: SHA-256 ile doğrulanmış kaynak arşivlerde değişmeyen iç dosyaların mevcut Sprout hashleri yeniden kullanılıyor; hedef arşiv yine bilinen SHA-256 ile birebir doğrulanıyor.
- `FeedingFrenzyTwo.exe` içindeki `LOADING` metni aynı uzunlukta `BASLIYO` metnine yalnızca delta patch ile dönüştürülüyor; tam EXE dağıtılmıyor.
- Feeding Frenzy 2 grafik arayüzde dinamik oyun listesine dahil edildi.
- Uygulama sürümü v0.3.0 olarak güncellendi.

- Feeding Frenzy 5.7.18.1 için Türkçe yama desteği eklendi.
- Feeding Frenzy ana menüsü, arayüz metinleri, bölüm başlangıç/bitiş metinleri ve bilgi metinleri Türkçeleştirildi.
- Eski bitmap font atlaslarına Türkçe karakter uyarlamaları eklendi.
- FFAS/SAF arşivlerini iç hash ve TOC hash doğrulamasıyla açıp yeniden paketleyen destek eklendi.
- SAF içindeki dosyalara delta patch uygulayan yeni `saf_internal` yama türü eklendi; tam `FFArchive.saf` depoda tutulmuyor.
- Feeding Frenzy desteği grafik arayüzde dinamik oyun listesine dahil edildi.
- Uygulama sürümü v0.3.0 olarak güncellendi.

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
