## 🔒 Ejercicio 10: Sincronización con RLock

# ✅ Objetivo:
Crear una clase CuentaBancaria con métodos depositar y retirar.

Ambos métodos deben estar protegidos con multiprocessing.RLock.

Permitir que los métodos se llamen recursivamente (por ejemplo, transferir() que llama a ambos).

Simular accesos concurrentes desde varios procesos.

# ▶️ Cómo ejecutar:

python3 cuenta_bancaria_rlock.py

Verás depósitos, retiros y transferencias internas protegidas con RLock, que permite reentrar en el mismo hilo/proceso sin deadlocks