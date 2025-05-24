import subprocess

resultados = {}

# Ejecutar benchmarks y capturar salida
for archivo in ["benchmark_pipe.py", "benchmark_queue.py", "benchmark_shared_list.py"]:
    resultado = subprocess.run(["python", archivo], capture_output=True, text=True)
    tiempo = float(resultado.stdout.split(":")[1].strip().split()[0])
    resultados[archivo.replace(".py", "")] = tiempo

# Imprimir resultados
for metodo, tiempo in resultados.items():
    print(f"{metodo}: {tiempo:.2f} segundos")

# Graficar resultados
import plot_results
plot_results.plot_results(resultados)
