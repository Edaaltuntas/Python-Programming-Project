from numpy import linspace, array, ones
import matplotlib.pyplot as plt
from random import uniform
from benchmark import *


def CozumHesapla(Func, karincaYol, test):
    # karıncanın gidebiliceği yol sayısını alıyoruz
    length = len(karincaYol)
    # karıncanın gideceği yolları tutacağımız xy dizisini oluşturuyoruz
    xy = []
    # karıncanın gidebiliceği yolları geziyoruz
    for i in range(length):
        # gelen test dizisinden x ve y değerleri çıkartılıyor
        xy.append(test[i][karincaYol[i]])
    # ilk x ve y değerleri kullanılarak seçilen fonksiyona göre çözüm hesaplanıyor
    return getattr(b, Func)(xy[0], xy[1])


def karincaOlustur(karincaSayisi):
    # karıncanın yolunu tutacağımız diziyi oluşturuyoruz
    karincaYol = []
    for _ in range(karincaSayisi):
        karincaYol.append(0)
    # karınca oluşturuluyor
    karinca = []
    # oluşturulan karıncanın içine yolu ekliyoruz
    karinca.append(karincaYol)
    karinca.append(1000)
    return karinca


def karincayiKontrolEt(koloni, deger):
    # kolonideki karıncaların çözüm değerini kontrol etmek için bir fonksiyon yazıyoruz bu fonksiyon aynı karıncaları bulmak için kullanıyoruz
    karincaListesi = []
    for i in range(len(koloni)):
        if koloni[i][1] == deger:
            karincaListesi.append(i)
    return karincaListesi


def yolSec(index, d, test):
    # rulet mantığı kullanılarak karıncanın gideceği rastgele yol seçiliyor
    l = []
    s = 0
    for i in range(d):
        s += test[index][i]

    for i in range(d):
        l.append(test[index][i]/s)
    r = round(uniform(0, 1), 3)
    s = 0
    p = 0
    for i in range(d):
        s += l[i]
        if (r <= s or i == d-1):
            p = i
            break
    return p


# Benchmark fonksiyonlarının olduğu sınıfı oluşturuyoruz
b = Benchmark()
# fonksiyonların ayrı ayrı denenmesi için döngü oluşturuyoruz
for Func in ["ackley", "beale", "levi", "goldstein"]:
    # başlangıçtaki koloni ve karınca sayısı belirliyoruz
    koloniSayisi, karincaSayisi = 10, 2
    # belirlenen fonksiyon için minimum ve maksimum değerleri alıyoruz
    min_deger, max_deger = b.get_range(Func)
    # iterasyon limiti ve sayacını belirliyoruz
    iterasyon, iterasyonLimiti = 1, 300
    # minimum ve maksimum değer arasında yarım yarım alınabilecek kaç sayı olduğunu hesaplıyoruz
    d = int((max_deger - min_deger) / .5 + 1)

    test = array([linspace(min_deger, max_deger, d).tolist(
    ), linspace(min_deger, max_deger, d).tolist()])
    # başlangıç için 1lerden oluşan bir dizi oluşturuyoruz
    testFeremonTablosu = ones((karincaSayisi + 1, d))
    # koloniSayisi*karincaSayisi kadar karınca oluşturuyoruz
    testKolonisi = [karincaOlustur(karincaSayisi) for _ in range(koloniSayisi)]
    # kabul edilen çözümlerin olduğu bir boş dizi oluşturuyoruz
    kabulEdilenCozumler = []
    # kabul edilen x ve y değerlerinin olduğu bir boş dizi oluşturuyoruz
    kabulEdilenDegerler = []

    while iterasyon <= iterasyonLimiti:
        # karıncaların değerinin atılması için indis oluşturuyoruz
        index = 0
        # karınca sayısı ile indis sayısı eşit olana kadar döngü açıyoruz
        while index < karincaSayisi:
            # test kolonomizdeki karıncaları gezdiğimiz bir döngü açıyoruz
            for karinca in testKolonisi:
                # karınca CHANGE
                karinca[0][index] = yolSec(
                    index, d, testFeremonTablosu)
            # indis her karıncadan sonra bir arttırılıyor
            index += 1
        # test kolonisindeki karıncaları tekrar geziyor
        for karinca in testKolonisi:
            # karıncaların çözüm değerini belirlediğimiz fonksiyona göre hesaplıyoruz
            karinca[1] = CozumHesapla(Func, karinca[0], test)

        # başlangıç için en iyi karıncayı ilk kolonideki ilk karınca olarak atıyoruz
        enIyiKarinca = testKolonisi[0][1]
        # başlangıç için en kötü karıncayı ilk kolonideki ilk karınca olarak atıyoruz
        enKotuKarinca = testKolonisi[0][1]
        # en iyi ve kötü karıncaların tutulacağı dizileri oluşturuyoruz
        enIyiKarincalar, enKotuKarincalar = [], []

        # test kolonisi geziliyor
        for karinca in testKolonisi:
            # eğer karınca eski en iyi karıncadan daha iyiyse en iyi karıncayı değiştiriyoruz
            if karinca[1] <= enIyiKarinca:
                enIyiKarinca = karinca[1]
            # eğer karınca eski en kötü karıncadan dahada kötüyse en kötü karıncayı değiştiriyoruz
            if karinca[1] >= enKotuKarinca:
                enKotuKarinca = karinca[1]

        # bulunan en iyi karıncayı kabul edilen çözümlere ekliyoruz
        kabulEdilenCozumler.append(enIyiKarinca)

        # bulunan en iyi karıncanın çözümü ile aynı karıncalara bakılıyor
        enIyiKarincalar = karincayiKontrolEt(testKolonisi, enIyiKarinca)
        # bulunan en kötü karıncanın çözümü ile aynı karıncalara bakılıyor
        enKotuKarincalar = karincayiKontrolEt(testKolonisi, enKotuKarinca)

        # en iyi karıncanın x,y değeri alınarak en iyi yol değeri atanıyor
        enIyiYol = testKolonisi[enIyiKarincalar[0]][0]
        # elde edilen x,y değeri kabul edilen değerler dizisine ekleniyor
        kabulEdilenDegerler.append(enIyiYol)

        # eğer en iyi karınca sayısı koloni sayısına eşitse döngüyü kapat
        if len(enIyiKarincalar) == koloniSayisi:
            break
        # iterasyon bittiğinde sayaç arttırılıyor
        iterasyon += 1

    # matplotlib kütüphanesini kullanarak yeni bir grafik oluşturuyoruz ve fonksiyona uygun olarak isimlendiriyoruz
    fig = plt.figure("{} fonksiyonunun grafiği".format(Func))
    # oluşturulan grafiğin içine 2 satır ve bir sütundan oluşan indisi 1 olan bir plot oluşturuyoruz.
    ax1 = fig.add_subplot(211)
    # kabul edilen çözümler dizisini bu plota veriyoruz ve rengini kırmızı, şeklini çizgi ve çözümlerinde nokta halinde gösterilecek şekilde ayarlıyoruz
    ax1.plot(kabulEdilenCozumler, 'r.-')
    # bu plotun çözümlere ait olduğunu belirten bir yazı ekliyoruz
    ax1.legend(['Çözüm'])
    # önceden oluşturmuş olduğumuz grafiğin içine 2 satır ve bir sütundan oluşan indisi 2 olan bir plot daha oluşturuyoruz.
    ax2 = fig.add_subplot(212)
    # kabul edilen x değerini mavi çizgi halinde ve x değerinin nokta halinde gösterileceği bir plot çiziyoruz
    ax2.plot([x[0] for x in kabulEdilenDegerler], 'b.-')
    # kabul edilen y değerini yeşil çizgi halinde gösterileceği bir plot çiziyoruz
    ax2.plot([x[1] for x in kabulEdilenDegerler], 'g--')
    # bu plotun x ve y değerlerine ait olduğunu belirten bir yazı ekliyoruz
    ax2.legend(['x', 'y'])
    # oluşturulan grafiği fonksiyon ismine uygun olarak kayıt ediyoruz
    plt.savefig(f"ant-plot-{Func}.png")
    # oluşturulan grafiği ekrana çıkarıyoruz
    plt.show()
