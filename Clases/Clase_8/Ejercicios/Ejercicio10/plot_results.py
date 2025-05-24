import matplotlib.pyplot as plt

def plot_results(data):
    """Genera una gráfica comparando los tiempos de los métodos de IPC."""
    plt.bar(data.keys(), data.values())
    plt.ylabel("Tiempo (segundos)")
    plt.title("Comparación de IPC en Python")
    plt.show()
