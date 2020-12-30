import numpy as np
import matplotlib.pyplot as plt
import random
from numpy import exp, log
from benchmark import *
from random import random

b = Benchmark()  # Benchmark fonksiyonlarının olduğu sınıfı oluşturuyoruz

dds, ids = 50, 50  # dış ve iç iterasyon sayısını belirtiyoruz

# başlangıç için kullanılacak rastgele x,y değerini belirliyoruz
rastgeleDeger = [0.5, -0.5]

# başlangıç ve bitiş sıcaklık değerlerini belirliyoruz
baslangicSicakligi, bitisSicakligi = -1.0/log(0.7), -1.0/log(0.001)

azalmaDegeri = (bitisSicakligi/baslangicSicakligi)**(1.0 /
                                                     (dds-1))  # fraktal azalım değerini hesaplıyoruz

# fonksiyonların ayrı ayrı denenmesi için döngü oluşturuyoruz
for Func in ["ackley", "beale", "levi", "goldstein"]:
    # başlangıç için seçilen rastgele x ve y değerini, değer değişkenimize atıyoruz
    deger = rastgeleDeger
    # benchmark sınıfındaki seçilen fonksiyonu çağırıyor ve x, y değerleri ile başlangıç çözümünü alıyoruz
    x = getattr(b, Func)(deger[0], deger[1])
    # sıcaklık değişkenini başlangıç sıcaklığına eşitliyoruz
    sicaklik = baslangicSicakligi
    # kabul edilen çözümlerin olduğu bir boş dizi oluşturuyoruz
    kabulEdilenCozumler = []
    # kabul edilen x ve y değerlerinin olduğu bir boş dizi oluşturuyoruz
    kabulEdilenDegerler = []
    # dış iterasyonu başlatıyoruz
    for i in range(dds):
        # iç iterasyonu başlatıyoruz
        for j in range(ids):
            # belirlenen fonksiyon için minimum ve maksimum değerleri alıyoruz
            min_deger, max_deger = b.get_range(Func)
            # kabul edilen bir önceki değeri baz alıp rassal bir şekilde yeni değer oluşturuyoruz ve bu değeri fonksiyonun minimum ve maksimum değerine uygun olarak min-max işlemi uyguluyoruz
            adayDeger = [max(
                min(deger[0] + random() - 0.5, max_deger), min_deger), max(
                min(deger[1] + random() - 0.5, max_deger), min_deger)]
            # elde edilen bu değeri benchmark sınıfıdaki seçilen fonksiyona az önce oluşturmuş olduğumuz x ve y değerlerini vererek yeni bir çözüm üretiyoruz.
            y = getattr(b, Func)(adayDeger[0], adayDeger[1])
            # elde edilen çözümü bir önceki çözüm ile karşılaştırıyoruz, eğer yeni elde edilen çözüm bir öncekinden daha iyiyse kabul edilen çözümü ve değerleri düzenliyoruz.
            if x > y:
                x = y
                deger = adayDeger
            # eğer değilse exp((f(x)-f(y))/t) formülü ile p değerini hesaplıyor ve rastgele bir değerden büyük olup olmadığına bakıyoruz. eğer büyük ise kabul edilen çözümü ve değerleri düzenliyoruz.
            elif (exp((x-y) / sicaklik) > random()):
                x = y
                deger = adayDeger
        # iterasyonun kabul edilen x ve y değerlerini kabul edilen değerler dizimize atıyoruz
        kabulEdilenDegerler.append(deger)
        # iterasyonun kabul edilen çözüm değerini kabul edilen çözümler dizimize atıyoruz
        kabulEdilenCozumler.append(x)
        # her dış iterasyonumuzda sıcaklık değerini hesapladığımız fraktal değer ile çarparak sıcaklığı her iterasyonda eşit bir azalım olacak şekilde düşürüyoruz.
        sicaklik = sicaklik * azalmaDegeri

    # bütün iterasyonlar bittiğinde bulunan en iyi x ve y değerlerini yazdırıyoruz
    print("{} fonksiyonu için en iyi x ve y değerleri: {}".format(Func, deger))
    # bütün iterasyonlar bittiğinde bulunan en iyi çözüm değerini yazdırıyoruz
    print("{} fonksiyonu en iyi çözüm: {}".format(Func, x))

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
    ax2.plot([xy[0] for xy in kabulEdilenDegerler], 'b.-')
    # kabul edilen y değerini yeşil çizgi halinde gösterileceği bir plot çiziyoruz
    ax2.plot([xy[1] for xy in kabulEdilenDegerler], 'g--')
    # bu plotun x ve y değerlerine ait olduğunu belirten bir yazı ekliyoruz
    ax2.legend(['x', 'y'])
    # oluşturulan grafiği fonksiyon ismine uygun olarak kayıt ediyoruz
    plt.savefig('sa-plot-{}.png'.format(Func))
    # oluşturulan grafiği ekrana çıkarıyoruz
    plt.show()
