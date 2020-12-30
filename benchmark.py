from numpy import sqrt, exp, cos, pi, sin


# Benchmark isminde bir sınıf oluşturuyoruz
class Benchmark:

    def ackley(self, x, y):
        z = -20 * exp(-0.2*sqrt(0.5*(x**2 + y**2))) - \
            exp(0.5*(cos(2*pi*x) + cos(2*pi*y))) + exp(1) + 20
        return z

    def beale(self, x, y):
        z = (1.5 - x + x*y) ** 2 + (2.25 - x + x *
                                    y**2)**2 + (2.625 - x + x*y**3) ** 2
        return z

    def levi(self, x, y):
        z = (sin(3*pi*x)**2)+(x-1)**2*(1+(sin(3*pi*y)**2)) + \
            (y-1)**2*(1 + (sin(2*pi*y) ** 2))
        return z

    def goldstein(self, x, y):
        z = (1 + (x+y+1) ** 2 * (19-14*x+3*x**2-14*y+6*x*y+3*y**2)) * \
            (30+(2*x-3*y)**2*(18-32*x+12*x**2+48*y-36*x*y+27*y**2))
        return z

    # bu fonksiyonların min ve max değerlerini alabiliceğimiz bir fonksiyon yazıyoruz
    def get_range(self, f):
        ranges = {
            "ackley": [-5, 5],
            "beale": [-4.5, 4.5],
            "levi": [-10, 10],
            "goldstein": [-2, 2]
        }
        return ranges[f]
