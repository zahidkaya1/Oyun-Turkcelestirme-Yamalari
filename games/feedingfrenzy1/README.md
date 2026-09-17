# Feeding Frenzy Türkçe Yama

## Desteklenen sürüm

- Oyun: **Feeding Frenzy**
- Sürüm: **5.7.18.1**
- Doğrulanan ana arşiv: `FFArchive.saf`
- Orijinal SHA-256: `226df2f4d7bfae7be98d5e339a85996015b5b421589e543b8339862db1b5de81`

## Dahil edilen yerelleştirme değişiklikleri

- Ana menü ve seçenek ekranları Türkçeleştirilir.
- Rekor, duraklatma, oyun sonu ve diğer arayüz metinleri Türkçeleştirilir.
- Bölüm başlangıç/bitiş metinleri ve oyun içi bilgi metinleri Türkçeleştirilir.
- Eski bitmap font sistemi için `ı`, `ü`, `ş`, `ç`, `ğ` ve `ö` karakterleri uyarlanır.
- Ana menüdeki görsele işlenmiş İngilizce buton yazıları Türkçe karşılıklarla değiştirilir.
- Dar arayüz alanlarında taşmayı önlemek için kısa yerelleştirmeler kullanılır; Rekorlar ekranındaki ileri düğmesi `sonra >` olarak gösterilir.

## SAF yama yöntemi

Feeding Frenzy metin ve görsellerinin önemli bölümü `FFArchive.saf` içindedir. Bu nedenle yama yöneticisi:

1. Kullanıcının `FFArchive.saf` dosyasının desteklenen orijinal sürüm olduğunu doğrular.
2. Arşivi geçici bir klasöre açar ve SAF iç hashlerini doğrular.
3. Yalnızca Türkçeleştirilen iç dosyalara delta patch uygular.
4. Arşivi yeniden paketler; dosya hashlerini ve TOC hashini yeniden üretir.
5. Oluşturulan arşivin beklenen SHA-256 değerini doğruladıktan sonra orijinal dosyanın yerine yazar.

Kurulumdan önce orijinal `FFArchive.saf`, genel yama yöneticisinin `.turkce_yama_backup` klasörüne otomatik olarak yedeklenir. `restore` işlemi bu yedeği geri yükler.

## Dağıtım notu

Tam oyun, tam `FFArchive.saf` veya orijinal oyun assetleri bu depoda dağıtılmaz. Depoda yalnızca uyumlu bir orijinal kopya üzerinde uygulanmak üzere delta verileri ve yama kodu bulunur.
