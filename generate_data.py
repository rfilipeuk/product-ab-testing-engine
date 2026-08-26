import numpy as np
import pandas as pd

np.random.seed(42)

# Simulação: 50.000 usuários expostos ao teste no fluxo de paywall
n_users = 50000
user_ids = [f"USR_{i:06d}" for i in range(1, n_users + 1)]

# Alocação 50/50 (Controle: Preço Padrão $29.99/mês vs Tratamento: Novo Pacote com Trial $19.99/mês)
variants = np.random.choice(['control', 'treatment'], size=n_users, p=[0.50, 0.50])
devices = np.random.choice(['iOS', 'Android', 'Web'], size=n_users, p=[0.45, 0.35, 0.20])
countries = np.random.choice(['US', 'UK', 'DE', 'FR', 'BR'], size=n_users, p=[0.40, 0.20, 0.15, 0.15, 0.10])

df_users = pd.DataFrame({
    'user_id': user_ids,
    'variant': variants,
    'device': devices,
    'country': countries,
    'signup_date': pd.date_range(start='2026-07-01', periods=n_users, freq='T')
})

# Efeito Real (Ground Truth):
# Controle: Baseline Conversion = 5.0%, Ticket Médio = $29.99
# Tratamento: Conversion = 6.2% (+24% uplift relativo), Ticket Médio = $24.50 (mix de planos)
def simulate_outcome(row):
    is_treatment = (row['variant'] == 'treatment')
    
    # Probabilidade de conversão
    base_prob = 0.050
    prob = 0.062 if is_treatment else base_prob
    
    converted = np.random.binomial(1, prob)
    
    # Receita gerada
    if converted == 1:
        if is_treatment:
            revenue = np.random.choice([19.99, 29.99, 49.99], p=[0.70, 0.20, 0.10])
        else:
            revenue = np.random.choice([29.99, 49.99], p=[0.85, 0.15])
    else:
        revenue = 0.0
        
    return pd.Series([converted, revenue], index=['converted', 'revenue'])

df_users[['converted', 'revenue']] = df_users.apply(simulate_outcome, axis=1)

# Salvar o dataset na pasta data/
df_users.to_csv('data/ab_test_monetization_raw.csv', index=False)
print(f"Dataset gerado com sucesso em data/ab_test_monetization_raw.csv com {len(df_users)} registros.")
