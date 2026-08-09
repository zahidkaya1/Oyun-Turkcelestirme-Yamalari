# Oyun Türkçeleştirme Yamaları

Eski PC oyunları için hazırlanmış **resmî olmayan Türkçe yerelleştirme yamaları**.

Bu depo oyunların tamamını, orijinal çalıştırılabilir dosyalarını, müziklerini veya asset paketlerini dağıtmaz. Yama sistemi kullanıcının kendi oyun dosyalarını SHA-256 ile doğrular ve yalnızca desteklenen sürümlere yerelleştirme değişikliklerini uygular.

## Desteklenen oyunlar

| Oyun | Durum | İçerik |
|---|---|---|
| **SuperCow** | İlk sürüm hazır | Türkçe metinler, ara sahne altyazıları, kupa metinleri, bazı görsel yazılar ve sınırlı motor içi metin değişiklikleri |
| **Jardinains 2!** | İlk sürüm hazır | Türkçe arayüz/metinler, Türkçe karakter uyumluluğu ve Türkçeleştirilmiş yardım sayfası |

## Gereksinimler

- Oyunun bu yamanın desteklediği **orijinal sürümü**
- Python 3
- Windows üzerinde oyunun kendi kurulum klasörüne yazma izni

## Önce uyumluluğu kontrol et

Bu komut **hiçbir oyun dosyasını değiştirmez**:

```powershell
python patcher.py verify supercow "C:\Oyunlar\SuperCow"
python patcher.py verify jardinains2 "C:\Oyunlar\Jardinains 2!"
```

Kontrol başarılıysa kurulum yapılabilir.

## Türkçe yamayı kur

```powershell
python patcher.py install supercow "C:\Oyunlar\SuperCow"
python patcher.py install jardinains2 "C:\Oyunlar\Jardinains 2!"
```

Değiştirilecek mevcut dosyalar oyun klasöründeki `.turkce_yama_backup` dizinine yedeklenir.

## Yamayı kaldır

```powershell
python patcher.py restore supercow "C:\Oyunlar\SuperCow"
python patcher.py restore jardinains2 "C:\Oyunlar\Jardinains 2!"
```

Geri yükleme tamamlandığında yedek klasörü temizlenir; böylece daha sonraki bir kurulumda yeni ve doğru yedek alınır.

## Oyunlara özel bilgiler

- [`games/supercow/README.md`](games/supercow/README.md)
- [`games/jardinains2/README.md`](games/jardinains2/README.md)

## Telif ve dağıtım yaklaşımı

Bu proje, orijinal oyun paketlerini yeniden dağıtmak yerine **delta patch** yaklaşımı kullanır. Kullanıcının uyumlu bir orijinal oyun kopyasına sahip olması gerekir.

Oyun adları, markalar, program kodları, görseller, sesler ve diğer orijinal içerikler ilgili hak sahiplerine aittir. Bu depo resmî bir yayın değildir ve ilgili geliştirici/yayıncılar tarafından desteklendiğini veya onaylandığını iddia etmez.

Kod için lisans bilgisi [`LICENSE-CODE.txt`](LICENSE-CODE.txt) dosyasındadır. Bu lisansın üçüncü taraf oyun içeriğine, çeviri içeriğine veya delta verilerine otomatik olarak hak verdiği varsayılmamalıdır. Ayrıntılar için [`NOTICE.md`](NOTICE.md) dosyasına bakın.

## Yeni oyun ekleme

Her oyun şu yapıyla eklenir:

```text
games/
└── oyun-id/
    ├── README.md
    ├── manifest.json
    └── patches/
```

`tools/build_delta.py`, orijinal ve Türkçeleştirilmiş iki dosya arasındaki delta verisini üretmek için kullanılabilir. Tam oyun klasörleri veya orijinal oyun dosyaları repoya eklenmemelidir.
