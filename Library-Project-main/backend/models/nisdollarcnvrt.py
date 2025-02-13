import requests


def get_exchange_rate():
    # Replace 'YOUR_API_KEY' with the actual API key
    url = f'https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/ILS'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        usd_rate = data['conversion_rates']['USD']
        return usd_rate
    else:
        print("Error fetching data.")
        return None


def convert_nis_to_usd(nis_amount):
    exchange_rate = get_exchange_rate()
    if exchange_rate:
        return nis_amount * exchange_rate
    else:
        return None


# Example usage
nis_amount = 100  # You can change this value
usd_amount = convert_nis_to_usd(nis_amount)
if usd_amount:
    print(f"{nis_amount} NIS is equal to {usd_amount:.2f} USD")
