import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carregar dados do CSV consolidado
df = pd.read_csv("locust_results_template.csv")

# Garantir tipos numéricos
for col in ["wp_instances", "users", "rps_avg", "latency_median_ms", "latency_p95_ms"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Paletas de cores fixas (para manter padrão nos gráficos)
colors_instancias = ['#A7C7E7', '#FFE4B5', '#F4A6A6']  # azul, amarelo, rosa
colors_usuarios = ['#B4E0B4', '#A7C7E7', '#FFF1A6']    # verde, azul, amarelo

# =======================================================
# 1) Tempo de resposta (p95) vs número de usuários
# =======================================================
for scenario, d in df.groupby("scenario"):
    pivot = d.pivot_table(values="latency_p95_ms", index="users", columns="wp_instances")
    pivot = pivot[[1, 2, 3]]  # garantir ordem 1,2,3 instâncias
    pivot.plot(kind="bar", color=colors_instancias, width=0.75)
    plt.title(f"Tempo de resposta (p95) — {scenario}")
    plt.xlabel("Número de usuários")
    plt.ylabel("Tempo de resposta (ms)")
    plt.legend(title="Instâncias do WordPress")
    plt.xticks(rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(f"{scenario}_tempo_resposta_p95.png")
    plt.close()

# =======================================================
# 2) Requisições por segundo (RPS) vs número de instâncias
# =======================================================
for scenario, d in df.groupby("scenario"):
    pivot = d.pivot_table(values="rps_avg", index="wp_instances", columns="users")
    pivot = pivot[[10, 100, 1000]]  # garantir ordem
    pivot.plot(kind="bar", color=colors_usuarios, width=0.75)
    plt.title(f"Requisições por segundo — {scenario}")
    plt.xlabel("Número de instâncias do WordPress")
    plt.ylabel("Requisições por segundo (RPS)")
    plt.legend(title="Usuários simulados")
    plt.xticks(rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(f"{scenario}_rps_vs_instancias.png")
    plt.close()

print("Cenários encontrados:", df["scenario"].unique())

print("✅ Gráficos gerados no formato exigido (p95 e RPS).")
