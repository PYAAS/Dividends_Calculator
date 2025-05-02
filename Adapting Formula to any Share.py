import yfinance as yf
from dateutil.relativedelta import relativedelta # Permite cálculo de diferença entre datas
import math 
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Set locale to Brazilian Portuguese
import matplotlib.pyplot as plt # Importa biblioteca para gráficos
from matplotlib.ticker import FuncFormatter

# Inicializa listas para armazenar os valores mensais
months = []
capital_history = []
share_amount_history = []
dividend_history = []
total_invested_history = []
dividend_amount_history = []

Capital = int(input("Digite o capital inicial para ser investido agora: "))  # Capital inicial
Aportes = int(input("Digite quanto deseja investir mensalmente: ")) # Aporte Mensal
Investment_Time = int(input("Digite o tempo de investimento em meses: "))  # Tempo de investimento em meses
Share = input("Digite o código da Ação ou Fundo que deseja calcular: ")  # Código da ação ou fundo
Share = Share.replace(" ", "")  # Remove espaços em branco
ticker = Share.upper() + ".SA"  # Converte para maiúsculo e add ".SA" para o formato Yahoo Finance
Share = yf.Ticker(ticker) # retorna os dados da ação selecionada
dividends = Share.dividends # retorna o histórico de dividendos da ação selecionada
current_price = Share.history(period="1d")["Close"].iloc[-1] # Trás o preço atual da ação selecionada
dividends = Share.dividends #Puxa informações referente aos dividendos da ação selecionada
latest_dividend = dividends.iloc[-1] if not dividends.empty else 0 # Pega o último dividendo pago

if not dividends.empty: # Verifica se existem dividendos
    dividend_dates = dividends.index.to_list() #Retorna as datas dos dividendos como uma lista
    dividend_dates = dividend_dates[-36:]  # Observa apenas os últimos 36 pagamentos

    # Calculate the difference in months between consecutive dividend dates
    month_differences = [ #calcula a diferença entre as datas dos dividendos pagos
        relativedelta(dividend_dates[i], dividend_dates[i - 1]).months +
        (relativedelta(dividend_dates[i], dividend_dates[i - 1]).years * 12)
        for i in range(1, len(dividend_dates))
    ]

    average_frequency = max(sum(month_differences) / len(month_differences), 1) # Determina a média de meses entre os dividendos pagos, garantindo que seja no mínimo 1 mês
    payments_per_year = round(12 / average_frequency, 0) # Calcula quantas vezes por ano os dividendos são pagos, arredondando para o inteiro mais próximo
    print()
    print(f"{ticker} pays dividends approximately {payments_per_year:.1f} times per year.") # Exibe a quantidade de dividendos pagos por ano
else:
    print(f"No dividend data available for {ticker}.") # Exibe mensagem caso não existam dividendos
print()
print(f"{ticker} - Current Price: {current_price:.2f} BRL") # Exibe o preço atual da ação
print(f"{ticker} - Latest Dividend: {latest_dividend:.2f} BRL") # Exibe o valor do último dividendo pago
print()

Share_Amount = 0
Dividend_Amount = 0
Total_Amount_Invested = 0
#Share_Amount = Capital // current_price # Calcula a quantidade de ações atuais
#Dividend_Amount = Share_Amount * latest_dividend # Calcula o valor total dos dividendos pagos
#Total_Amount_Invested = Share_Amount * current_price # Calcula o valor total investido

if payments_per_year > 0: # Verifica se o número de pagamentos por ano é maior que 0
    average_frequency = 12 / payments_per_year  # Retorna a frequência média de pagamento em meses
    dividend_per_payment = latest_dividend # / payments_per_year  # Retorna quanto é pago em cada dividendo
else: # Se não houver pagamentos por ano, retorna zero
    average_frequency = 0
    dividend_per_payment = 0

Total_Dividends_Received = 0 # Inicializa o valor total de dividendos recebidos como 0
Out_of_Pocket = 0 # Inicializa o valor total pago como 0

for Month in range(1, Investment_Time + 1):  # Gera um loop pelo tempo definido pelo usuário
    Capital += Aportes  # Adiciona Aporte Mensal ao Capital todo mês
    additional_shares = 0  # Inicia a variável de ações adicionais como 0 a cada mês

    while Capital >= current_price:  # Realiza a compra de ações enquanto o capital for maior que o preço atual
        additional_shares = Capital // current_price  # Calcula quantas ações podem ser compradas
        Capital -= round(additional_shares * current_price, 2)  # Subtrai o valor das ações compradas do Capital
        Share_Amount += additional_shares  # Adiciona as ações compradas à quantidade total de ações

    if average_frequency > 0 and (Month % round(average_frequency)) == 0:  # Verifica se é um mês que paga dividendos
        Dividend_Amount = Share_Amount * dividend_per_payment  # Verifica a quantidade de dividendos pagos
        Capital += Dividend_Amount  # Adiciona os dividendos ao Capital
        Total_Dividends_Received += Dividend_Amount  # Adiciona os dividendos recebidos ao total de dividendos recebidos

        while Capital >= current_price:  # Realiza a compra de ações enquanto o capital for maior que o preço atual
            additional_shares = Capital // current_price  # Calcula quantas ações podem ser compradas
            Capital -= round(additional_shares * current_price, 2)  # Subtrai o valor das ações compradas do Capital
            Share_Amount += additional_shares  # Adiciona as ações compradas à quantidade total de ações
    else:
        Dividend_Amount = 0  # Zera os dividendos em meses que não há pagamento de dividendos

    Total_Amount_Invested = Share_Amount * current_price  # Calcula o valor total investido
    Out_of_Pocket = Total_Amount_Invested - Total_Dividends_Received  # Calcula o valor total pago, subtraindo os dividendos recebidos do valor total investido

    # Armazena os valores mensais nas listas
    months.append(Month)
    capital_history.append(Capital)
    share_amount_history.append(Share_Amount)
    dividend_history.append(Total_Dividends_Received)
    total_invested_history.append(Total_Amount_Invested)
    dividend_amount_history.append(Dividend_Amount) 


    # Retorna os valores de cada mês
    print(f"Month {Month}: Remaining Capital = {locale.currency(Capital, grouping=True)}, "
        f"Total Shares = {math.floor(Share_Amount):.0f}, "
        f"Total Dividend = {locale.currency(Dividend_Amount, grouping=True)}, "
        f"Total_Amount_Invested = {locale.currency(Total_Amount_Invested, grouping=True)}")
    print()

# Cria o gráfico ao final do loop
fig, ax = plt.subplots(figsize=(12, 6))  # Define o tamanho do gráfico

# Adiciona as linhas ao gráfico
ax.plot(months, total_invested_history, label="Total Investido (BRL)", marker='o')
ax.plot(months, dividend_history, label="Dividendos Recebidos (BRL)", marker='o')
ax.plot(months, share_amount_history, label="Quantidade de Ações", marker='o')

# Configurações do gráfico
ax.set_title(f"Evolução dos Investimentos - {ticker}", fontsize=16)
ax.set_xlabel("Meses", fontsize=12)
ax.set_ylabel("Valores (BRL)", fontsize=12)
ax.legend()
ax.grid(True)
# Formata os valores do eixo Y para exibir números completos
ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))

# Cria um gráfico separado para Dividend_Amount
fig2, ax2 = plt.subplots(figsize=(12, 6))  # Define o tamanho do gráfico separado

# Adiciona a linha ao gráfico separado
ax2.plot(months, dividend_amount_history, label="Dividendos Mensais (BRL)", marker='o', linestyle='--', color='green')

# Configurações do gráfico separado
ax2.set_title(f"Evolução dos Dividendos Mensais - {ticker}", fontsize=16)
ax2.set_xlabel("Meses", fontsize=12)
ax2.set_ylabel("Dividendos Mensais (BRL)", fontsize=12)
ax2.legend()
ax2.grid(True)
# Formata os valores do eixo Y para exibir números completos
ax2.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))

plt.show()  # Exibe o gráfico

# CORRIGIR: Calculo do valor investido vs Valor de dividendos está errado
# print(f"From a total of {Total_Amount_Invested:.2f} BRL invested, {Out_of_Pocket:.2f} came out of pocket and {Total_Dividends_Received:.2f} BRL were reinvested from dividends.")

# possíveis melhorias:
# front para o usuário
# melhorar o tratamento de erros
# adicionar mais informações sobre a ação, como dividend yield, P/L, etc.
# permitir valores decimais no Capital e Aportes
# adicionar opção de reinvestir dividendos ou não
# validar ação com try catch

