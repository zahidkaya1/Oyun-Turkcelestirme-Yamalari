# Feeding Frenzy 2 Türkçe Yama

Bu klasör **Feeding Frenzy 2 v1.0** için hazırlanan resmî olmayan Türkçe yama verilerini içerir.

## Kapsam

- Ana menü, kullanıcı ekranları, seçenekler, duraklatma ve oyun sonu arayüzleri
- Bölüm girişleri, bölüm adları ve hikâye metinleri
- 100/100 eğlenceli bilgi metni
- Oyuncu rütbeleri, HUD ve oyun içi arayüz metinleri
- Türkçe karakterler için bitmap font uyarlamaları
- Harita ve çeşitli arayüz görsellerindeki İngilizce yazıların Türkçeleştirilmesi
- Bölüm giriş başlıklarında `Ş` karakterinden kaynaklanan XML kaçış sorununun düzeltilmesi
- İlk açılıştaki EXE içi `LOADING` metninin `BASLIYO` olarak değiştirilmesi

## Desteklenen sürüm

- Oyun sürümü: **1.0**
- Orijinal `FF2.saf` SHA-256:
  `177fb12081b9157e234b604c1b6fc25445133365a24eee28564047f204fd8983`
- Türkçe yama sonrası `FF2.saf` SHA-256:
  `91b79204b5ebcc5e39b97db54411c85c4befd182f67bb30a6da76964e73bbd43`
- Orijinal `FeedingFrenzyTwo.exe` SHA-256:
  `a942ecab8f992a3eb3a8bd51ddd25acafc08c82a62c40b007cfca05e840cf256`
- Türkçe yama sonrası `FeedingFrenzyTwo.exe` SHA-256:
  `d64005626a8d2bbd8a7c904243fd8710e278c7f2c239d91699482df9ea925ca5`

## Dağıtım yaklaşımı

Depoda tam oyun arşivi veya çalıştırılabilir dosya bulunmaz. `FF2.saf` içindeki değişiklikler dosya bazlı delta olarak uygulanır; `FeedingFrenzyTwo.exe` için de yalnızca `LOADING` → `BASLIYO` değişikliğini içeren delta tutulur. Kullanıcının desteklenen orijinal oyun dosyalarına sahip olması gerekir.

Yama yöneticisi kurulumdan önce sürümü hash ile doğrular ve değiştirdiği dosyaları `.turkce_yama_backup` klasörüne yedekler.
