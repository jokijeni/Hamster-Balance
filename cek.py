import requests

with open('data.txt', 'r') as file:
    bearer_tokens = [line.strip() for line in file.readlines()]

url_balance = "https://api.hamsterkombatgame.io/interlude/sync"

url_account_info = "https://api.hamsterkombatgame.io/auth/account-info"

total_tokens_all_accounts = 0  
total_unclaimed_tokens_all_accounts = 0 
total_next_unlocked_all_accounts = 0  

for token in bearer_tokens:
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response_balance = requests.post(url_balance, headers=headers, json={})

    if response_balance.status_code == 200:
        data_balance = response_balance.json()
        token_balance = data_balance.get('interludeUser', {}).get('tokenBalance', {})
        
        total_tokens = token_balance.get('total', 0) / 1e9  
        unclaimed_tokens = token_balance.get('unclaimed', 0) / 1e9  
        next_unlocked = token_balance.get('nextUnlocked', 0) / 1e9  

        response_account_info = requests.post(url_account_info, headers=headers, json={})
        
        if response_account_info.status_code == 200:
            data_account_info = response_account_info.json()
            account_info = data_account_info.get('accountInfo', {})
            account_id = account_info.get('id')
            account_name = account_info.get('name')

            print(f"Account ID: {account_id}  | Account Name: {account_name}  | Total Tokens: {total_tokens:.9f}  | Unclaimed Tokens: {unclaimed_tokens:.9f}  | Next Unlocked: {next_unlocked:.9f}")

            total_tokens_all_accounts += total_tokens
            total_unclaimed_tokens_all_accounts += unclaimed_tokens
            total_next_unlocked_all_accounts += next_unlocked  
        else:
            print(f"Error fetching account info: {response_account_info.status_code}, Message: {response_account_info.text}")
    else:
        print(f"Error fetching token balance: {response_balance.status_code}, Message: {response_balance.text}")

print(f"\nTotal Tokens from All Accounts: {total_tokens_all_accounts:.9f}")
print(f"Total Unclaimed Tokens from All Accounts: {total_unclaimed_tokens_all_accounts:.9f}")
print(f"Total Next Unlocked from All Accounts: {total_next_unlocked_all_accounts:.9f}")
