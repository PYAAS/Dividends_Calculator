import yfinance as yf
from dateutil.relativedelta import relativedelta # Permite cálculo de diferença entre datas
import math 

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

Share_Amount = Capital // current_price # Calcula a quantidade de ações atuais
Dividend_Amount = Share_Amount * latest_dividend # Calcula o valor total dos dividendos pagos
Total_Amount_Invested = Share_Amount * current_price # Calcula o valor total investido

if payments_per_year > 0: # Verifica se o número de pagamentos por ano é maior que 0
    average_frequency = 12 / payments_per_year  # Retorna a frequência média de pagamento em meses
    dividend_per_payment = latest_dividend / payments_per_year  # Retorna quanto é pago em cada dividendo
else: # Se não houver pagamentos por ano, retorna zero
    average_frequency = 0
    dividend_per_payment = 0

Total_Dividends_Received = 0 # Inicializa o valor total de dividendos recebidos como 0
Out_of_Pocket = 0 # Inicializa o valor total pago como 0

for Month in range(1, Investment_Time + 1):  # Gera um loop pelo tempo definido pelo usuário
    Dividend_Amount = 0 # Inicializa o valor do dividendo como 0 a cada mês
    Capital += Aportes  # Adiciona Aporte Mensal ao Capital todo mês
    additional_shares = 0 # Inicia a variável de ações adicionais como 0 a cada mês

    if average_frequency > 0 and Month % average_frequency == 0:  # Verifica se é um mês que paga dividendos
        Dividend_Amount = Share_Amount * dividend_per_payment  # Verifica a quantidade de dividendos pagos
        Capital += Dividend_Amount  # Adiciona os dividendos ao Capital
        Total_Dividends_Received += Dividend_Amount # Adiciona os dividendos recebidos ao total de dividendos recebidos

    while Capital >= current_price:  # Realiza a compra de ações enquanto o capital for maior que o preço atual
        additional_shares = Capital // current_price  # Calcula quantas ações podem ser compradas
        Capital -= round(additional_shares * current_price, 2)  # Subtrai o valor das ações compradas do Capital
        Share_Amount += additional_shares  # Adiciona as ações compradas à quantidade total de ações

    Total_Amount_Invested = Share_Amount * current_price # Calcula o valor total investido
    Out_of_Pocket = Total_Amount_Invested - Total_Dividends_Received # Calcula o valor total pago, subtraindo os dividendos recebidos do valor total investido
    
    # Retorna os valores de cada mês
    print(f"Month {Month}: Remaining Capital = {Capital:.2f}, Total Shares = {math.floor(Share_Amount):.0f}, Total Dividend = {Dividend_Amount:.2f}, Total_Amount_Invested = {Total_Amount_Invested:.2f}")
    print()
print(f"From a total of {Total_Amount_Invested:.2f} BRL invested, {Out_of_Pocket:.2f} came out of pocket and {Total_Dividends_Received:.2f} BRL were reinvested from dividends.")