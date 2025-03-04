# ipynb2md - Jupyter Notebook to Markdown Converter

**ipynb2md**, Jupyter Notebook (.ipynb) dosyalarını Markdown (.md) formatına dönüştüren bir Python aracıdır. Bu araç, özellikle Jupyter Notebook'larınızı belgelere veya blog gönderilerine dönüştürmek istediğinizde kullanışlıdır.

## :clipboard: İçindekiler

1. [Özellikler](https://github.com/thealper2/ipynb2md?tab=readme-ov-file#dart-%C3%B6zellikler)
2. [Kurulum](https://github.com/thealper2/ipynb2md?tab=readme-ov-file#hammer_and_wrench-kurulum)
3. [Kullanım](https://github.com/thealper2/ipynb2md?tab=readme-ov-file#joystick-kullan%C4%B1m)
4. [Katkıda Bulunma](https://github.com/thealper2/ipynb2md?tab=readme-ov-file#handshake-katk%C4%B1da-bulunma)
5. [Lisans](https://github.com/thealper2/ipynb2md?tab=readme-ov-file#scroll-lisans)

---

## :dart: Özellikler

- Jupyter Notebook hücrelerini Markdown formatına dönüştürür.
- Kod hücrelerini dil türüne göre otomatik algılar (Python, R, JavaScript, vb.).
- Notebook'taki görselleri çıkarır ve Markdown dosyasına ekler.
- Markdown hücrelerini ve HTML çıktılarını düzgün bir şekilde işler.

## :hammer_and_wrench: Kurulum

Projeyi yerel makinenize klonlayın:

```bash
git clone https://github.com/thealper2/ipynb2md.git
cd ipynb2md
```

Gerekli bağımlılıkları yüklemek için `pyproject.toml` dosyasını kullanın:

```bash
pip install .
```

## :joystick: Kullanım

### Komut Satırı Arayüzü (CLI)

Projeyi komut satırından çalıştırmak için `run.py` betiğini kullanabilirsiniz:

```bash
python run.py path/to/your_notebook.ipynb
```

Bu komut, belirtilen Jupyter Notebook dosyasını Markdown formatına dönüştürür ve aynı dizine kaydeder. Çıktı dosyasının adını belirtmek için `-o` veya `--output` seçeneğini kullanabilirsiniz:

```bash
python run.py path/to/your_notebook.ipynb -o output_file.md
```

### Python Modülü Olarak Kullanım

Projeyi bir Python modülü olarak da kullanabilirsiniz:

```python
from src.ipynb2md.notebook_converter import NotebookConverter

converter = NotebookConverter("path/to/your_notebook.ipynb")
converter.read_notebook()
success, output_path = converter.save("output_file.md")

if success:
    print(f"Markdown dosyası başarıyla kaydedildi: {output_path}")
else:
    print("Dönüştürme başarısız oldu.")
```

### Testler

Proje, `unittest` kütüphanesi kullanılarak test edilmiştir. Testleri çalıştırmak için aşağıdaki komutu kullanın:

```bash
python run_tests.py
```

Bu komut, `src/tests/` dizinindeki tüm test dosyalarını çalıştırır.

#### Test Dosyaları

- **test_notebook_cell.py**: `NotebookCell` sınıfının metodlarını test eder.
- **test_notebook_converter.py**: `NotebookConverter` sınıfının metodlarını test eder.

## :handshake: Katkıda Bulunma

Katkıda bulunmak isterseniz, lütfen aşağıdaki adımları izleyin:

1. Bu depoyu forklayın.
2. Yeni bir branch oluşturun (`git checkout -b feature/AmazingFeature`).
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`).
4. Branch'inizi pushlayın (`git push origin feature/AmazingFeature`).
5. Bir Pull Request açın.

## :scroll: Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına bakın.
