# Oyun Türkçeleştirme Yamaları

Eski PC oyunları için hazırlanmış **resmî olmayan Türkçe yerelleştirme yamaları**.

Bu proje oyunların tamamını, orijinal çalıştırılabilir dosyalarını, müziklerini veya asset paketlerini dağıtmaz. Yama sistemi kullanıcının kendi oyun dosyalarını doğrular ve yalnızca desteklenen sürümlere yerelleştirme değişikliklerini uygular.

## Desteklenen oyunlar

| Oyun | Durum | İçerik |
|---|---|---|
| **SuperCow** | Destekleniyor | Türkçe metinler, ara sahne altyazıları, kupa metinleri, bazı görsel yazılar ve sınırlı motor içi metin değişiklikleri |
| **Jardinains 2!** | Destekleniyor | Türkçe arayüz/metinler, Türkçe karakter uyumluluğu ve Türkçeleştirilmiş yardım sayfası |
| **Feeding Frenzy** | Destekleniyor | Türkçe arayüz, bölüm ve bilgi metinleri, bitmap fontlarda Türkçe karakter desteği ve Türkçeleştirilmiş ana menü görselleri |
| **Feeding Frenzy 2** | Destekleniyor | Türkçe arayüz, hikâye ve bölüm girişleri, 100 eğlenceli bilgi, bitmap font uyarlamaları, Türkçeleştirilmiş arayüz görselleri ve açılış metni |

## Windows için kolay kullanım

**v0.4.0 ile birlikte Feeding Frenzy 2 desteği de grafik arayüzlü Windows yama yöneticisine eklendi.**

GitHub Releases bölümünden:

```text
Oyun-Turkcelestirme-Yamalari.exe
```

dosyasını indirip çalıştırmanız yeterlidir.

Python kurulumu gerekmez.

### Kullanım

1. Listeden oyunu seçin.
2. `Gözat...` ile oyunun kurulu olduğu klasörü seçin.
3. Uygulamanın oyun sürümünü kontrol etmesini bekleyin.
4. `Türkçe Yamayı Kur` düğmesine basın.
5. Yamayı kaldırmak isterseniz `Yamayı Kaldır` düğmesini kullanın.

Uygulama, değiştirdiği mevcut oyun dosyalarını kurulum sırasında otomatik olarak yedekler.

### Yama durumları

Arayüz oyun klasörünü otomatik olarak inceler ve aşağıdaki durumlardan birini gösterir:

- **Kuruluma hazır ✓** — Desteklenen orijinal oyun sürümü bulundu.
- **Yama kurulu ✓** — Türkçe yama zaten uygulanmış.
- **Kısmi yama ⚠** — Yama işlemi yarım kalmış veya dosyalar kısmen değiştirilmiş olabilir.
- **Uyumsuz ✕** — Seçilen klasör desteklenen oyun sürümüyle eşleşmiyor.

## Komut satırı kullanımı

Kaynak kod üzerinden çalıştırmak isteyen kullanıcılar için Python tabanlı patcher kullanılmaya devam edilebilir.

### Gereksinimler

- Python 3
- Oyunun bu yamanın desteklediği orijinal sürümü
- Oyun klasörüne yazma izni

### Uyumluluğu kontrol et

Bu komut oyun dosyalarını değiştirmez:

```powershell
python patcher.py verify supercow "C:\Oyunlar\SuperCow"
python patcher.py verify jardinains2 "C:\Oyunlar\Jardinains 2!"
python patcher.py verify feedingfrenzy1 "C:\Oyunlar\Feeding Frenzy"
python patcher.py verify feedingfrenzy2 "C:\Oyunlar\Feeding Frenzy 2"
```

### Türkçe yamayı kur

```powershell
python patcher.py install supercow "C:\Oyunlar\SuperCow"
python patcher.py install jardinains2 "C:\Oyunlar\Jardinains 2!"
python patcher.py install feedingfrenzy1 "C:\Oyunlar\Feeding Frenzy"
python patcher.py install feedingfrenzy2 "C:\Oyunlar\Feeding Frenzy 2"
```

### Yamayı kaldır

```powershell
python patcher.py restore supercow "C:\Oyunlar\SuperCow"
python patcher.py restore jardinains2 "C:\Oyunlar\Jardinains 2!"
python patcher.py restore feedingfrenzy1 "C:\Oyunlar\Feeding Frenzy"
python patcher.py restore feedingfrenzy2 "C:\Oyunlar\Feeding Frenzy 2"
```

Değiştirilen mevcut dosyalar oyun klasöründeki `.turkce_yama_backup` dizinine yedeklenir. Geri yükleme tamamlandığında yedek klasörü temizlenir.

## Oyunlara özel bilgiler

- [`games/supercow/README.md`](games/supercow/README.md)
- [`games/jardinains2/README.md`](games/jardinains2/README.md)
- [`games/feedingfrenzy1/README.md`](games/feedingfrenzy1/README.md)
- [`games/feedingfrenzy2/README.md`](games/feedingfrenzy2/README.md)

## Proje yapısı

```text
Oyun-Turkcelestirme-Yamalari/
├── games/
│   ├── supercow/
│   ├── jardinains2/
│   ├── feedingfrenzy1/
│   └── feedingfrenzy2/
├── tools/
├── saf_tool.py
├── gui.py
├── patcher.py
├── README.md
├── CHANGELOG.md
├── NOTICE.md
└── LICENSE-CODE.txt
```

Her oyun kendi `manifest.json`, açıklama dosyası ve delta yama verileriyle bağımsız şekilde tutulur. Feeding Frenzy gibi SAF tabanlı oyunlarda iç dosya deltaları yerelde uygulanır ve arşiv yeniden paketlenir; tam oyun arşivi depoda tutulmaz.

## Geliştirici için Windows EXE oluşturma

PyInstaller kurulu bir Windows ortamında:

```powershell
pyinstaller --noconfirm --clean --onefile --windowed --name "Oyun-Turkcelestirme-Yamalari" --add-data "games:games" gui.py
```

Oluşan çalıştırılabilir dosya:

```text
dist\Oyun-Turkcelestirme-Yamalari.exe
```

altında bulunur.

`build/`, `dist/`, `*.spec`, `__pycache__/` ve `*.pyc` dosyaları kaynak kod deposuna eklenmez.

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

`tools/build_delta.py`, orijinal ve Türkçeleştirilmiş iki dosya arasındaki delta verisini üretmek için kullanılabilir.

**Tam oyun klasörleri veya orijinal oyun dosyaları repoya eklenmemelidir.**
